# Thor's Hammer Test Implementation

## Problem Statement
The `test_experience_gain` integration test was flaky because the character didn't always kill the creature in time to see the experience gain message within the test timeout window.

## Solution
Created an impossibly powerful test weapon "Thor's Hammer" that guarantees one-hit kills, eliminating timing variability and making the test 100% reliable.

## Implementation Details

### 1. Test Weapon Specification
**File:** `tests/integration/test_data/hammer_object.yml`

Thor's Hammer specifications:
- **Damage:** 1d4+200 (minimum 201, maximum 204 damage per hit)
- **Hit modifiers:** +50 to hitroll and +50 to damroll
- **Weight:** 8 (same as standard weapons, wieldable)
- **Object vnum:** 12001 (in test-only range)

### 2. Test Framework Enhancement
**File:** `tools/integration_test_runner.py`

Added support for `test_extensions` in test YAML files:
- New `set_test_extensions()` method in `ServerManager` class
- New `_apply_test_extensions()` method that:
  - Copies zone YAML files to test_lib
  - Merges extension objects into specified zones
  - Adds reset commands to load objects into rooms
  - Rebuilds world files with test objects included
- Extensions are applied only during test setup
- Test objects never contaminate production data

### 3. Test Update
**File:** `tests/integration/test_experience_gain.yaml`

Changes:
- Added `test_extensions` to setup section
- Changed from loading a weapon via god command to picking up Thor's Hammer from the room
- Reduced combat steps from 2 to 1 (instant kill)
- Reduced delay from 6s to 3s total

### 4. File Organization
**Directory:** `tests/integration/test_data/`

Created dedicated directory for test data files:
- Uses `.yml` extension (not `.yaml`) to prevent test runner from treating them as tests
- Contains README.md documenting usage and security
- Ensures clean separation between tests and test data

## Test Results

### Reliability Testing
- **Before:** Test could fail intermittently due to combat timing
- **After:** 100% success rate over 80+ consecutive runs
- **Average runtime:** ~2 seconds per test

### Full Test Suite
- All 79 integration tests pass
- No regressions introduced
- Thor's Hammer never appears in production builds

## Security Verification

1. **Production isolation:** Thor's Hammer (vnum 12001) does not appear in:
   - `dm-dist-alfa/lib/tinyworld.obj`
   - `dm-dist-alfa/lib/zones_yaml/` directory
   - Any production world files

2. **Test-only usage:** The weapon only exists in:
   - Test extension file: `tests/integration/test_data/hammer_object.yml`
   - Temporary test_lib directory (deleted after each test)

3. **Build verification:**
   ```bash
   grep "12001" dm-dist-alfa/lib/tinyworld.obj  # Returns nothing
   grep -r "thor" dm-dist-alfa/lib/             # No Thor references
   ```

## Usage Example

To use test extensions in other tests:

```yaml
setup:
  character:
    name: TestChar
    level: 10
  start_room: 1200
  test_extensions:
    - zone_file: zone_1200.yaml
      extension_file: test_data/hammer_object.yml
```

The test runner will automatically:
1. Create an isolated test environment
2. Merge the extension objects
3. Rebuild world files
4. Run the test
5. Clean up

## Benefits

1. **Reliability:** Eliminates flaky test failures
2. **Speed:** Faster test execution (fewer combat rounds)
3. **Maintainability:** Easy to add more test objects using the same pattern
4. **Safety:** Test objects isolated from production
5. **Clarity:** Tests are more focused and deterministic

## Running the Reliability Test

To verify the fix with 100 consecutive runs:

```bash
cd tests
./test_reliability_100.sh
```

Or manually:
```bash
cd dm-dist-alfa
for i in {1..100}; do 
  python3 ../tools/integration_test_runner.py ./dmserver \
    ../tests/integration/test_experience_gain.yaml
done
```

## Future Enhancements

The test_extensions framework can be used for:
- Testing with overpowered armor for defensive tests
- Testing with heavy/light objects for weight tests
- Testing with special-effect items for spell/ability tests
- Creating temporary quest objects for quest testing

All without polluting the production game world.
