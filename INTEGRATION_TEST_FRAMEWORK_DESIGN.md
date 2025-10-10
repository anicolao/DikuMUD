# Integration Testing Framework Design for DikuMUD

## Executive Summary

This document outlines the design of an integration testing framework for validating user bug reports in DikuMUD. The framework will enable developers to create automated tests that simulate player actions, verify game state, and validate bug fixes without manual gameplay testing.

## Problem Statement

Currently, bug reports are logged via the `bug` command in the format:
```
**Winifred[3003]: nobles waiter doesn't list
**Winifred[3020]: armory list
**Winifred[3011]: weapns list
**Winifred[3011]: weapons
**Kheldar[3010]: general store shouldn't be a grocer
**Kheldar[3005]: lamp in temple of the jeddak has no light left
```

Developers need a way to:
1. Create automated tests that reproduce the bug
2. Verify the bug exists before the fix
3. Validate that the fix resolves the issue
4. Ensure the fix doesn't break over time (regression testing)

## Design Goals

### Primary Goals
1. **Easy to write**: Developers should be able to create a test from a bug report in minutes
2. **Readable**: Test scripts should be understandable by non-programmers
3. **Maintainable**: Tests should survive codebase changes and be easy to update
4. **Automated**: Tests should run without human intervention
5. **Fast**: Test suite should complete quickly to enable rapid development

### Secondary Goals
1. **Comprehensive**: Support testing all player actions (movement, buying, combat, etc.)
2. **Flexible**: Support both positive tests (feature works) and negative tests (bug exists)
3. **Informative**: Provide clear error messages when tests fail
4. **Composable**: Allow tests to build on common sequences

## Architecture Overview

The framework consists of three main components:

### 1. Test Runner (Python)
- Starts and manages the DikuMUD server
- Connects as a virtual player via telnet
- Executes test scripts
- Validates expected outcomes
- Reports test results

### 2. Test Scripts (YAML format)
- Declarative test definitions
- Specify player actions and expected outcomes
- Human-readable and easy to edit
- Support for comments and documentation

### 3. Test Harness (Shell wrapper)
- Discovers and executes tests
- Manages server lifecycle
- Aggregates results
- Integrates with CI/CD

## Component Details

### 1. Test Runner: `tools/integration_test_runner.py`

**Responsibilities:**
- Server lifecycle management (start, stop, cleanup)
- Network communication via telnet
- Command execution and response parsing
- State validation
- Test orchestration

**Key Features:**
- Automatic server startup on random port
- Timeout handling for hung commands
- Pattern matching for expected outputs
- Support for multi-step test scenarios
- Cleanup of test artifacts

**API Design:**
```python
class IntegrationTestRunner:
    def __init__(self, server_path, lib_path, timeout=30)
    def start_server(self, port=None)
    def stop_server(self)
    def create_character(self, name, password, char_class)
    def execute_command(self, command, timeout=5)
    def expect_output(self, pattern, timeout=5)
    def move_to_room(self, room_vnum)
    def verify_room(self, room_vnum)
    def verify_inventory(self, item_pattern)
    def verify_shop_list(self, items)
    def run_test(self, test_file)
```

### 2. Test Script Format: YAML

**Structure:**
```yaml
# Test metadata
test:
  id: bug_3003_nobles_waiter_list
  description: "Verify nobles waiter shop allows listing drinks"
  bug_report: "**Winifred[3003]: nobles waiter doesn't list"
  author: Developer Name
  created: 2025-10-10
  
# Test configuration
setup:
  character:
    name: TestChar
    class: warrior
    level: 1
  starting_room: 3001  # Temple of the Jeddak
  gold: 1000  # Starting gold for purchases
  
# Test steps
steps:
  - action: move
    description: "Walk to room 3003"
    path: [north, east, south]
    expected_room: 3003
    
  - action: look
    description: "Verify waiter is present"
    expected:
      - pattern: "waiter"
        message: "Waiter should be visible in room"
    
  - action: command
    description: "List items for sale"
    command: "list"
    expected:
      - pattern: "flask of wine"
        message: "Wine should be available"
      - pattern: "whiskey"
        message: "Whiskey should be available"
    fail_on:
      - pattern: "don't seem interested"
        message: "Shop should allow listing items"
      
  - action: command
    description: "Buy a drink to verify shop works"
    command: "buy wine"
    expected:
      - pattern: "You buy"
        message: "Should be able to purchase wine"
    
  - action: inventory
    description: "Verify wine is in inventory"
    expected:
      - pattern: "flask of wine"
        message: "Wine should be in inventory after purchase"

# Expected outcome
result:
  should_pass: true  # Test passes if bug is fixed
  description: "Player should be able to list and buy items from nobles waiter"
```

**Test Script Variations:**

**Simple Movement Test:**
```yaml
test:
  id: verify_room_connection
  description: "Verify rooms are properly connected"
  
setup:
  starting_room: 3001
  
steps:
  - action: move
    direction: north
    expected_room: 3054
  - action: move
    direction: south
    expected_room: 3001
```

**Shop Validation Test:**
```yaml
test:
  id: bug_3010_general_store_type
  description: "Verify general store sells general goods, not groceries"
  bug_report: "**Kheldar[3010]: general store shouldn't be a grocer"
  
setup:
  starting_room: 3001
  gold: 100
  
steps:
  - action: move
    path: [north, east]
    expected_room: 3010
    
  - action: command
    command: "list"
    expected:
      - pattern: "lantern|pack|rope"
        message: "Should sell general goods"
    fail_on:
      - pattern: "bread|fruit|provisions"
        message: "Should not sell food items"
```

**Item State Test:**
```yaml
test:
  id: bug_3005_lamp_no_light
  description: "Verify temple lamp has light charges"
  bug_report: "**Kheldar[3005]: lamp in temple of the jeddak has no light left"
  
setup:
  starting_room: 3001  # Temple
  
steps:
  - action: look
    description: "Check for lamp in room"
    expected:
      - pattern: "lamp"
        message: "Lamp should be present"
  
  - action: command
    command: "examine lamp"
    expected:
      - pattern: "lit|glowing|hours"
        message: "Lamp should have light remaining"
    fail_on:
      - pattern: "dark|empty|no light"
        message: "Lamp should not be empty"
```

### 3. Test Harness: `dm-dist-alfa/run_integration_tests.sh`

**Responsibilities:**
- Test discovery
- Batch test execution
- Result aggregation
- CI/CD integration

**Features:**
```bash
#!/bin/bash
# Run integration tests

# Usage:
#   ./run_integration_tests.sh              # Run all tests
#   ./run_integration_tests.sh bug_3003*    # Run specific test(s)
#   ./run_integration_tests.sh --verbose    # Detailed output

# Environment:
#   TEST_DIR=tests/integration             # Test directory
#   SERVER_PATH=./dmserver                 # Server binary
#   LIB_PATH=./lib                         # Game data
#   TIMEOUT=60                             # Per-test timeout
```

**Output Format:**
```
=== DikuMUD Integration Test Suite ===

Running test: bug_3003_nobles_waiter_list
  ✓ Server started on port 54321
  ✓ Character created: TestChar
  ✓ Moved to room 3003
  ✓ Waiter visible in room
  ✓ Shop listing works
  ✓ Purchase successful
  ✓ Item in inventory
  ✓ Test passed (6.2s)

Running test: bug_3010_general_store_type
  ✓ Server started on port 54322
  ✓ Character created: TestChar
  ✓ Moved to room 3010
  ✓ General goods available
  ✗ FAILED: Found food items in general store
  ✗ Test failed (3.1s)

=== Test Results ===
Tests run: 2
Passed: 1
Failed: 1
Time: 9.3s

Failed tests:
  - bug_3010_general_store_type: Found food items in general store
```

## Test Directory Structure

```
tests/
├── integration/                  # Integration test scripts
│   ├── shops/                   # Shop-related tests
│   │   ├── bug_3003_nobles_waiter_list.yaml
│   │   ├── bug_3010_general_store_type.yaml
│   │   └── bug_3020_armory_list.yaml
│   ├── items/                   # Item-related tests
│   │   └── bug_3005_lamp_no_light.yaml
│   ├── movement/                # Movement tests
│   │   └── room_connections.yaml
│   └── common/                  # Reusable test fragments
│       ├── setup_noble.yaml
│       └── movement_helpers.yaml
├── fixtures/                    # Test data
│   ├── test_characters.yaml
│   └── test_scenarios.yaml
└── README.md                    # Test documentation
```

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- [ ] Implement basic IntegrationTestRunner class
- [ ] Server lifecycle management
- [ ] Telnet communication
- [ ] Basic command execution
- [ ] Simple YAML test parsing

### Phase 2: Test Actions (Week 2)
- [ ] Movement actions
- [ ] Look/examine actions
- [ ] Shop interactions (list, buy, sell)
- [ ] Inventory checks
- [ ] Pattern matching for validation

### Phase 3: Advanced Features (Week 3)
- [ ] Multi-step scenarios
- [ ] Test fixtures and setup
- [ ] Cleanup and teardown
- [ ] Parallel test execution
- [ ] Result reporting

### Phase 4: Test Coverage (Week 4)
- [ ] Create tests for all bug reports in bugs file
- [ ] Shop validation tests
- [ ] Movement/navigation tests
- [ ] Combat tests (future)
- [ ] Quest tests (future)

## Test Runner Implementation Details

### Server Management

```python
class ServerManager:
    """Manages DikuMUD server lifecycle"""
    
    def start(self, port=None):
        """Start server on specified or random port"""
        if port is None:
            port = self._find_free_port()
        
        self.process = subprocess.Popen(
            ['./dmserver', '-p', str(port)],
            cwd=self.server_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to be ready
        self._wait_for_startup(timeout=10)
        return port
    
    def stop(self):
        """Stop server gracefully"""
        self.process.terminate()
        self.process.wait(timeout=5)
    
    def cleanup(self):
        """Clean up test artifacts"""
        # Remove test player files
        # Clear log files
        # Reset database state
```

### Telnet Client

```python
class GameClient:
    """Handles telnet communication with server"""
    
    def connect(self, host, port, timeout=10):
        """Connect to game server"""
        self.tn = telnetlib.Telnet(host, port, timeout)
        self._wait_for_prompt()
    
    def send_command(self, command):
        """Send command and return response"""
        self.tn.write(command.encode('ascii') + b'\n')
        return self._read_until_prompt()
    
    def expect_output(self, pattern, timeout=5):
        """Wait for expected output pattern"""
        output = self._read_until_prompt(timeout)
        if re.search(pattern, output):
            return True
        return False
```

### Test Executor

```python
class TestExecutor:
    """Executes test steps and validates results"""
    
    def execute_step(self, step):
        """Execute a single test step"""
        action = step['action']
        
        if action == 'move':
            return self._execute_move(step)
        elif action == 'command':
            return self._execute_command(step)
        elif action == 'look':
            return self._execute_look(step)
        elif action == 'inventory':
            return self._execute_inventory(step)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _execute_move(self, step):
        """Execute movement action"""
        # Handle single direction or path
        # Verify expected room reached
        # Return success/failure with details
    
    def validate_expectations(self, output, expected):
        """Validate output matches expectations"""
        results = []
        for expectation in expected:
            pattern = expectation['pattern']
            message = expectation['message']
            
            if re.search(pattern, output):
                results.append({
                    'passed': True,
                    'message': message
                })
            else:
                results.append({
                    'passed': False,
                    'message': f"FAILED: {message}",
                    'expected': pattern,
                    'actual': output[:100]
                })
        return results
```

## Integration with Existing Tools

### Validation Tools
The framework complements existing validation tools:

- **validate_shops.py**: Static validation of shop configuration
- **Integration tests**: Dynamic validation of shop behavior
- **validate_world.py**: Static world file validation
- **Integration tests**: Dynamic gameplay validation

### Continuous Integration

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build server
        run: cd dm-dist-alfa && make dmserver
      - name: Run integration tests
        run: cd dm-dist-alfa && ./run_integration_tests.sh
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: dm-dist-alfa/test-results/
```

## Example Test Cases

### Test Case 1: Nobles Waiter Shop
**Bug Report:** `**Winifred[3003]: nobles waiter doesn't list`

**Test validates:**
1. Can navigate to room 3003
2. Waiter NPC is present
3. `list` command works
4. Can see available drinks
5. Can purchase items

### Test Case 2: General Store Type
**Bug Report:** `**Kheldar[3010]: general store shouldn't be a grocer`

**Test validates:**
1. Can navigate to room 3010
2. Shop sells general goods (lanterns, packs)
3. Shop does NOT sell food items

### Test Case 3: Temple Lamp
**Bug Report:** `**Kheldar[3005]: lamp in temple of the jeddak has no light left`

**Test validates:**
1. Lamp exists in temple (room 3001)
2. Lamp has light charges remaining
3. Lamp can be used for illumination

## Benefits

### For Developers
- **Rapid validation**: Test fixes without manual gameplay
- **Regression prevention**: Ensure bugs stay fixed
- **Documentation**: Tests serve as examples of correct behavior
- **Confidence**: Deploy knowing features work

### For Testers
- **Reproducible tests**: Same test runs identically each time
- **Clear reporting**: Know exactly what passed/failed
- **Time savings**: Automated tests run faster than manual testing

### For Project
- **Quality assurance**: Catch bugs before deployment
- **Maintainability**: Tests document expected behavior
- **Collaboration**: Easy for anyone to contribute tests
- **CI/CD**: Automated validation on every commit

## Limitations and Considerations

### Current Limitations
1. **Combat testing**: Complex interactions may be hard to test
2. **Timing issues**: Server response times may vary
3. **State management**: Tests must handle varying game state
4. **Test isolation**: Tests should not interfere with each other

### Future Enhancements
1. **Visual debugging**: Show what the player would see
2. **Record/playback**: Record manual sessions as tests
3. **Fuzzing**: Automatic test generation
4. **Performance testing**: Load testing with multiple clients
5. **Coverage analysis**: Track which code paths are tested

## Alternative Approaches Considered

### Approach 1: Shell Script + Expect
**Pros:** Simple, uses existing tools
**Cons:** Hard to maintain, limited validation capabilities

### Approach 2: Custom C Test Harness
**Pros:** Native integration, fast
**Cons:** Complex to implement, high maintenance

### Approach 3: JavaScript + Node.js
**Pros:** Good async support, active ecosystem
**Cons:** Additional dependency, team less familiar

**Selected Approach:** Python + YAML
- Python is already used (validate_shops.py, world_builder.py)
- YAML is readable and maintainable
- Good balance of simplicity and power
- Easy to extend and enhance

## Success Metrics

The framework will be considered successful if:

1. **Easy adoption**: New tests can be written in <15 minutes
2. **Fast execution**: Test suite completes in <5 minutes
3. **Reliable**: <1% flaky test rate
4. **Comprehensive**: Covers all reported bugs
5. **Maintainable**: Tests survive codebase changes

## Documentation Requirements

1. **README.md**: Getting started guide
2. **TUTORIAL.md**: Step-by-step test creation
3. **API.md**: TestRunner API reference
4. **EXAMPLES.md**: Common test patterns
5. **TROUBLESHOOTING.md**: Common issues and solutions

## Conclusion

This integration testing framework will significantly improve the development workflow for DikuMUD by:

1. **Automating validation** of bug fixes
2. **Preventing regressions** through continuous testing
3. **Documenting expected behavior** in executable form
4. **Enabling rapid development** with confidence

The framework is designed to be simple, maintainable, and extensible, with a focus on making it easy for developers to write and maintain tests.

## Next Steps

1. **Review this design** with stakeholders
2. **Get approval** to proceed with implementation
3. **Create initial prototype** of core components
4. **Implement Phase 1** (Core Infrastructure)
5. **Create example tests** for bug reports
6. **Iterate based on feedback**

## Questions for Review

1. Is the YAML format sufficiently expressive for test cases?
2. Should we support other test formats (JSON, custom DSL)?
3. What priority should be given to parallel test execution?
4. Should we integrate with existing test frameworks (pytest)?
5. What level of test isolation is required?
6. Should tests clean up after themselves or leave artifacts for debugging?

---

**Document Status:** Draft for Review  
**Author:** GitHub Copilot  
**Date:** 2025-10-10  
**Version:** 1.0
