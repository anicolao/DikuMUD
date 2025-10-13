# Integration Tests for DikuMUD

This directory contains integration tests for validating DikuMUD functionality through automated gameplay simulation.

## Overview

Integration tests automate the process of:
1. Starting a DikuMUD server
2. Connecting as a virtual player
3. Executing commands (movement, shopping, combat, etc.)
4. Validating expected outcomes
5. Reporting results

## Quick Start

### Running All Tests

```bash
cd dm-dist-alfa
make integration_tests
```

Or use the legacy `test` target:

```bash
cd dm-dist-alfa
make test
```

### Running Specific Tests

```bash
# Run a specific test
cd dm-dist-alfa
make integration_test_outputs/shops/bug_3003_nobles_waiter_list.out

# Run all shop tests (using make's pattern matching)
make integration_test_outputs/shops/bug_3003_nobles_waiter_list.out \
     integration_test_outputs/shops/bug_3010_general_store_type.out \
     integration_test_outputs/shops/bug_3011_weapons_list.out \
     integration_test_outputs/shops/bug_3020_armory_list.out
```

### Viewing Test Results

Test output files are stored in `integration_test_outputs/`:

```bash
cd dm-dist-alfa
cat integration_test_outputs/shops/bug_3003_nobles_waiter_list.out
```

### Creating Your First Test

1. Create a new YAML file in the appropriate subdirectory
2. Define test metadata and setup
3. Add test steps
4. Run the test to verify it works

**Example test:**
```yaml
test:
  id: my_first_test
  description: "Test basic movement"
  
setup:
  starting_room: 3001
  
steps:
  - action: move
    direction: north
    expected_room: 3054
    
  - action: look
    expected:
      - pattern: "altar"
        message: "Should see altar in temple"
```

## Test Organization

### Directory Structure

```
integration/
├── shops/          # Shop functionality tests
├── items/          # Item behavior tests
├── movement/       # Navigation tests
├── combat/         # Combat system tests (future)
├── quests/         # Quest system tests (future)
└── common/         # Reusable test components
```

### Test Naming Convention

Format: `bug_ROOM_description.yaml` or `feature_name.yaml`

Examples:
- `bug_3003_nobles_waiter_list.yaml` - Bug fix validation
- `feature_fountain_fill.yaml` - Feature test
- `shops_basic_purchase.yaml` - Functional test

## Test Structure

### Minimal Test

```yaml
test:
  id: unique_test_id
  description: "Brief description"
  
steps:
  - action: command
    command: "look"
    expected:
      - pattern: "room description"
```

### Complete Test

```yaml
test:
  id: comprehensive_shop_test
  description: "Test shop listing and purchasing"
  bug_report: "**Player[room]: bug description"
  author: Your Name
  created: 2025-10-10
  tags: [shop, commerce, bug_fix]
  
setup:
  character:
    name: TestChar
    class: warrior
    level: 5
  starting_room: 3001
  gold: 1000
  inventory:
    - waterskin
  
steps:
  - action: move
    description: "Navigate to shop"
    path: [north, east]
    expected_room: 3010
    
  - action: command
    description: "List shop items"
    command: "list"
    expected:
      - pattern: "lantern"
        message: "Lantern should be for sale"
    fail_on:
      - pattern: "don't seem interested"
        message: "Shop should respond to list command"
    
  - action: command
    description: "Purchase item"
    command: "buy lantern"
    expected:
      - pattern: "You buy"
    
  - action: inventory
    expected:
      - pattern: "lantern"
        message: "Lantern should be in inventory"
        
cleanup:
  remove_character: true
  
result:
  should_pass: true
  description: "Shop should allow listing and purchasing"
```

## Available Actions

### Movement Actions

**Single Direction:**
```yaml
- action: move
  direction: north
  expected_room: 3054
```

**Path (multiple rooms):**
```yaml
- action: move
  path: [north, east, south]
  expected_room: 3010
```

**With Description:**
```yaml
- action: move
  description: "Walk to market square"
  path: [north, north, west]
  expected_room: 3014
```

### Look/Examine Actions

**Basic Look:**
```yaml
- action: look
  expected:
    - pattern: "temple"
```

**Look at Object:**
```yaml
- action: look
  target: "fountain"
  expected:
    - pattern: "water"
```

### Command Actions

**Simple Command:**
```yaml
- action: command
  command: "inventory"
  expected:
    - pattern: "carrying"
```

**Command with Validation:**
```yaml
- action: command
  command: "list"
  expected:
    - pattern: "wine.*\\d+ gold"
      message: "Wine should be listed with price"
  fail_on:
    - pattern: "nothing to sell"
      message: "Shop should have items"
```

### Shop Actions

**List Items:**
```yaml
- action: shop_list
  expected_items:
    - name: "flask of wine"
      min_price: 5
      max_price: 50
```

**Purchase:**
```yaml
- action: buy
  item: "wine"
  expected:
    - pattern: "You buy"
```

### Inventory Checks

**Simple Check:**
```yaml
- action: inventory
  expected:
    - pattern: "sword"
```

**Detailed Check:**
```yaml
- action: inventory
  expected:
    - pattern: "leather waterskin"
      message: "Should have waterskin"
  should_not_contain:
    - pattern: "broken"
      message: "Should not have broken items"
```

### Wait Actions

**Wait for Time:**
```yaml
- action: wait
  seconds: 5
  description: "Wait for regeneration"
```

**Wait for Output:**
```yaml
- action: wait_for
  pattern: "You feel better"
  timeout: 10
```

## Pattern Matching

Tests use regular expressions for pattern matching:

### Simple String Match
```yaml
pattern: "You buy a flask of wine"
```

### Case-Insensitive Match
```yaml
pattern: "(?i)wine"  # Matches "wine", "Wine", "WINE"
```

### Partial Match
```yaml
pattern: ".*wine.*"  # Matches any line containing "wine"
```

### Number Extraction
```yaml
pattern: "(\\d+) gold coins"  # Captures the number
```

### Multiple Alternatives
```yaml
pattern: "(sword|blade|weapon)"  # Matches any of these
```

## Common Test Patterns

### Pattern 1: Basic Shop Test

```yaml
test:
  id: shop_basic_test
  description: "Verify shop allows listing and purchasing"
  
setup:
  starting_room: 3009
  gold: 500
  
steps:
  - action: command
    command: "list"
    expected:
      - pattern: "\\d+ gold"
        message: "Should show items with prices"
  
  - action: command
    command: "buy bread"
    expected:
      - pattern: "You buy"
  
  - action: inventory
    expected:
      - pattern: "bread"
```

### Pattern 2: Movement and Interaction

```yaml
test:
  id: navigation_test
  description: "Navigate to location and interact"
  
setup:
  starting_room: 3001
  
steps:
  - action: move
    description: "Walk to destination"
    path: [north, east, south]
    expected_room: 3010
    
  - action: look
    expected:
      - pattern: "shop"
    
  - action: command
    command: "say hello"
    expected:
      - pattern: "You say"
```

### Pattern 3: Item State Verification

```yaml
test:
  id: item_state_test
  description: "Verify item has correct state"
  
setup:
  starting_room: 3001
  
steps:
  - action: look
    target: "lamp"
    expected:
      - pattern: "(lit|glowing)"
        message: "Lamp should be lit"
    fail_on:
      - pattern: "(dark|empty)"
        message: "Lamp should not be empty"
```

### Pattern 4: Gold and Economy

```yaml
test:
  id: economy_test
  description: "Test purchasing with gold"
  
setup:
  starting_room: 3009
  gold: 100
  
steps:
  - action: command
    command: "buy bread"
    expected:
      - pattern: "You buy.*bread"
    
  - action: command
    command: "score"
    expected:
      - pattern: "gold"
        message: "Should show remaining gold"
```

## Debugging Tests

### View Test Output

Test output is saved to files in `integration_test_outputs/`. View them to debug:
```bash
cat integration_test_outputs/shops/bug_3003_nobles_waiter_list.out
```

### Manual Testing

For manual testing, you can run the Python test runner directly with options:
```bash
cd dm-dist-alfa
python3 ../tools/integration_test_runner.py ./dmserver ../tests/integration/shops/bug_3003_nobles_waiter_list.yaml
```

### Advanced Debugging

The test runner Python script (`../tools/integration_test_runner.py`) supports various debugging options. Check its source for details on available command-line flags.

## Troubleshooting

### Test Times Out

**Problem:** Test doesn't complete within timeout
**Solutions:**
- Increase timeout in test setup
- Check if server is responding
- Verify room numbers are correct
- Check for blocking prompts

### Pattern Doesn't Match

**Problem:** Expected pattern not found in output
**Solutions:**
- Run with --verbose to see actual output
- Use --save-transcript to review full session
- Check for typos in pattern
- Verify regex syntax

### Server Fails to Start

**Problem:** Integration test can't start server
**Solutions:**
- Verify dmserver is built: `make dmserver`
- Check for port conflicts
- Verify lib/ directory exists
- Check server logs

### Test Flakiness

**Problem:** Test passes sometimes, fails others
**Solutions:**
- Add wait actions for asynchronous operations
- Increase timeouts
- Check for race conditions
- Verify test isolation

## Best Practices

1. **Keep tests focused**: One bug or feature per test
2. **Use descriptive names**: Make purpose clear
3. **Add comments**: Explain non-obvious steps
4. **Test isolation**: Don't depend on other tests
5. **Clean up**: Remove test characters/items
6. **Be specific**: Use precise patterns
7. **Document expectations**: Explain what should happen

## Contributing

When adding new tests:

1. Place in appropriate subdirectory
2. Follow naming conventions
3. Include bug report reference if applicable
4. Add descriptive comments
5. Test your test (ensure it runs)
6. Update this README if adding new patterns

## Future Enhancements

Planned features:
- [ ] Combat action support
- [ ] Quest progression testing
- [ ] Multi-player scenarios
- [ ] Performance benchmarks
- [ ] Visual test reports
- [ ] Record/playback mode

## Support

For questions or issues:
- Check [INTEGRATION_TEST_FRAMEWORK_DESIGN.md](../../docs/testing/INTEGRATION_TEST_FRAMEWORK_DESIGN.md)
- Review example tests in each subdirectory
- Ask in project Discord: https://discord.gg/MeNQzXNCfb

---

**Last Updated:** 2025-10-10  
**Framework Version:** 1.0 (Design Phase)
