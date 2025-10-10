# Integration Testing Framework - Quick Start Guide

## What Is This?

An automated testing framework for DikuMUD that simulates player actions to verify bug fixes and features work correctly.

## Status

**Currently:** Design phase complete  
**Next:** Implementation phase

## Why Do We Need This?

When players report bugs like:
```
**Winifred[3003]: nobles waiter doesn't list
**Kheldar[3010]: general store shouldn't be a grocer
```

We need to:
1. Reproduce the bug
2. Fix it
3. Verify the fix works
4. Ensure it stays fixed

Manual testing is slow and error-prone. Automated tests solve this.

## How It Works

### 1. Write a Test (YAML file)

```yaml
test:
  id: bug_3003_nobles_waiter_list
  description: "Verify nobles waiter shop works"
  
setup:
  starting_room: 3001
  gold: 1000
  
steps:
  - action: move
    target_room: 3003
    
  - action: command
    command: "list"
    expected:
      - pattern: "wine|whiskey"
        message: "Should show drinks"
```

### 2. Run the Test

```bash
cd dm-dist-alfa
./run_integration_tests.sh shops/bug_3003_nobles_waiter_list.yaml
```

### 3. Get Results

```
✓ Server started
✓ Character created
✓ Moved to room 3003
✓ Shop listing works
✓ Test passed
```

## What Can Tests Do?

- **Move**: Navigate between rooms
- **Look**: Examine rooms and objects
- **Command**: Execute any game command
- **Shop**: List items, buy/sell
- **Inventory**: Check what player is carrying
- **Validate**: Verify expected outputs

## Example Tests Created

We've created example tests for bug reports:

1. **bug_3003_nobles_waiter_list.yaml** - Nobles waiter shop
2. **bug_3020_armory_list.yaml** - Armory listing
3. **bug_3011_weapons_list.yaml** - Weapons shop
4. **bug_3010_general_store_type.yaml** - General store type
5. **bug_3005_lamp_no_light.yaml** - Temple lamp light

Find them in: `tests/integration/`

## Test File Structure

### Minimal Test
```yaml
test:
  id: my_test
  description: "What this tests"
  
steps:
  - action: command
    command: "look"
    expected:
      - pattern: "temple"
```

### Complete Test
```yaml
test:
  id: comprehensive_test
  description: "Full test with setup"
  bug_report: "**Player[room]: bug description"
  
setup:
  starting_room: 3001
  gold: 1000
  character:
    name: TestChar
    class: warrior
    
steps:
  - action: move
    path: [north, east]
    expected_room: 3010
    
  - action: command
    command: "list"
    expected:
      - pattern: "\\d+ gold"
        message: "Should show prices"
    fail_on:
      - pattern: "not interested"
        message: "Shop should respond"
```

## Benefits

### For Developers
- Test fixes without manual gameplay
- Catch regressions automatically
- Document expected behavior

### For Testers
- Reproducible tests
- Faster validation
- Clear pass/fail results

### For Project
- Quality assurance
- Continuous integration
- Confidence in changes

## Architecture

```
┌─────────────────────────────────────────┐
│  Test Script (YAML)                     │
│  - What to test                         │
│  - Steps to execute                     │
│  - Expected results                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Test Runner (Python)                   │
│  - Parse YAML                           │
│  - Start server                         │
│  - Connect via telnet                   │
│  - Execute commands                     │
│  - Validate results                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  DikuMUD Server                         │
│  - Process commands                     │
│  - Return responses                     │
└─────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Core (Week 1)
- Server lifecycle management
- Telnet communication
- Basic command execution
- YAML parsing

### Phase 2: Actions (Week 2)
- Movement actions
- Look/examine
- Shop interactions
- Inventory checks

### Phase 3: Advanced (Week 3)
- Multi-step scenarios
- Fixtures and setup
- Parallel execution
- Result reporting

### Phase 4: Coverage (Week 4)
- Tests for all bug reports
- Shop validation
- Navigation tests
- Combat/quest tests

## Current Files

### Documentation
- `INTEGRATION_TEST_FRAMEWORK_DESIGN.md` - Full specification
- `INTEGRATION_TEST_QUICKSTART.md` - This file
- `tests/integration/README.md` - Test writing guide

### Example Tests
- `tests/integration/shops/` - Shop tests
- `tests/integration/items/` - Item tests

### Stubs (Design Only)
- `dm-dist-alfa/run_integration_tests.sh` - Test harness
- `tools/integration_test_runner.py` - Python runner

## Next Steps

1. **Review this design** with team
2. **Get approval** to implement
3. **Phase 1 implementation**
4. **Test with bug reports**
5. **Iterate and improve**

## FAQ

**Q: Why YAML instead of code?**  
A: YAML is readable by non-programmers, easy to maintain, and declarative.

**Q: Why not use existing test frameworks?**  
A: DikuMUD needs custom telnet communication and game-specific actions.

**Q: Can tests run in CI/CD?**  
A: Yes! Tests can run automatically on every commit.

**Q: How long do tests take?**  
A: Target: <5 minutes for full suite, <10 seconds per test.

**Q: What about combat testing?**  
A: Planned for Phase 4 after core framework is stable.

**Q: Can I write tests now?**  
A: Yes! Write YAML tests. They'll run once framework is implemented.

## Getting Help

- Read: `INTEGRATION_TEST_FRAMEWORK_DESIGN.md` for details
- Read: `tests/integration/README.md` for test writing
- Ask: Project Discord for questions

## Contributing

Want to help implement this?

1. Pick a component from the design
2. Implement it following the spec
3. Write tests for your implementation
4. Submit PR with documentation

Key components needing implementation:
- Server management (start/stop)
- Telnet client (send/receive)
- YAML parser (load tests)
- Test actions (move, command, etc.)
- Result validation (pattern matching)

## Summary

This framework will make DikuMUD development:
- **Faster**: Automated testing beats manual
- **Safer**: Catch bugs before deployment
- **Better documented**: Tests show how things work
- **More confident**: Know features work correctly

The design is complete. Implementation can begin.

---

**Questions?** See full design document or ask in Discord.  
**Ready to implement?** Start with Phase 1 components.  
**Want to contribute?** Write tests or implement framework.
