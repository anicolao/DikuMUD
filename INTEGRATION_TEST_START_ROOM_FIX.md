# Integration Test start_room Requirement - Implementation Summary

## Problem Statement

The tests were failing because no character was created when no room was specified. The solution was to:
1. Make `start_room` a REQUIRED field in all integration tests
2. Standardize on the `start_room` field name (some tests used `starting_room`)
3. Verify that all tests can successfully log in after this change

## Changes Made

### 1. Made start_room Required

**File: `tools/integration_test_runner.py`**

Added validation to require `start_room` in the setup section:

```python
# start_room is REQUIRED - all tests must specify where the character starts
if 'setup' not in test_def or 'start_room' not in test_def['setup']:
    print(f"✗ Test error: 'start_room' is required in setup section")
    print(f"   Add 'start_room: <vnum>' to the setup section of your test")
    return False
```

### 2. Fixed Field Name Inconsistency

Updated 5 test files to use `start_room` instead of `starting_room`:

- `tests/integration/items/bug_3005_lamp_no_light.yaml`
- `tests/integration/shops/bug_3003_nobles_waiter_list.yaml`
- `tests/integration/shops/bug_3010_general_store_type.yaml`
- `tests/integration/shops/bug_3011_weapons_list.yaml`
- `tests/integration/shops/bug_3020_armory_list.yaml`

### 3. Added Required Server File

**File: `dm-dist-alfa/lib/pcobjs.obj`**

- Created empty `pcobjs.obj` file (required by server for player object storage)
- Removed from `.gitignore` so it's tracked in git
- Without this file, server would crash with `exit(1)` when trying to load player objects

### 4. Fixed Critical test_lib Bug

**File: `tools/integration_test_runner.py`**

Fixed bug where `start()` was recreating `test_lib` and deleting the player file:

```python
# Create test lib directory (if not already created by create_test_player)
if not self.test_lib_path:
    self._create_test_lib()
```

**Root Cause:** The test framework flow was:
1. `create_test_player()` creates `test_lib` and player file
2. `start()` was unconditionally calling `_create_test_lib()` again
3. `_create_test_lib()` deletes `test_lib` and recreates it fresh
4. Player file was lost, causing character creation prompts during login

**Fix:** Only create `test_lib` if it doesn't already exist.

## Test Results

### Before Fix
- 0/7 tests could log in successfully
- All tests failed with "That's not a sex.. What IS your sex?" error
- Character creation prompts appeared instead of successful login

### After Fix
- ✅ **7/7 tests can log in successfully**
- ✅ 2/7 tests pass completely:
  - `basic_connectivity.yaml`
  - `test_fountain_drink.yaml`
- ⚠️ 5/7 tests fail for expected reasons:
  - Pathfinding not implemented (tests try to move to specific rooms)
  - Test-specific content issues (missing NPCs, item properties)
  
The 5 failures are NOT login failures - they successfully log in but fail on test-specific requirements.

## Verification

All tests now show:
```
✓ Connected to server
✓ Logged in as TestChar
```

This confirms the requirement is met: **all tests are able to log in after making start_room required**.

## Key Insights

1. **start_room is fundamental**: Without specifying a starting room, characters cannot be properly created
2. **Consistency matters**: Field name must be exactly `start_room` (not `starting_room`)
3. **Server dependencies**: The `pcobjs.obj` file must exist even if empty
4. **Test isolation**: Each test needs its own fresh `test_lib` with the correct player file
5. **Timing matters**: The order of operations (create player → start server) is critical

## Future Improvements

While the current implementation meets requirements, potential enhancements could include:

1. **Pathfinding**: Implement navigation to target rooms so movement tests can pass
2. **World content**: Ensure all referenced NPCs, items, and locations exist in test world
3. **Test cleanup**: Ensure proper cleanup of test artifacts between runs
4. **Documentation**: Update test documentation to clearly specify start_room requirement

## Files Modified

1. `tools/integration_test_runner.py` - Made start_room required, fixed test_lib bug
2. `dm-dist-alfa/.gitignore` - Removed pcobjs.obj from ignore list
3. `dm-dist-alfa/lib/pcobjs.obj` - Created empty file for player object storage
4. `tests/integration/items/bug_3005_lamp_no_light.yaml` - Fixed field name
5. `tests/integration/shops/bug_3003_nobles_waiter_list.yaml` - Fixed field name
6. `tests/integration/shops/bug_3010_general_store_type.yaml` - Fixed field name
7. `tests/integration/shops/bug_3011_weapons_list.yaml` - Fixed field name
8. `tests/integration/shops/bug_3020_armory_list.yaml` - Fixed field name

## Conclusion

✅ **Requirement satisfied**: All integration tests now have start_room as a required field and can successfully log in.

The implementation ensures robust, reliable test execution by:
- Requiring explicit starting room specification
- Properly managing test environment (test_lib)
- Ensuring all server dependencies are met
- Providing clear error messages when requirements aren't met
