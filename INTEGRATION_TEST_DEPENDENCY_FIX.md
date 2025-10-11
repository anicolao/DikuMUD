# Integration Test Dependency Fix

## Problem

Integration tests were always running all tests, even when only a single test YAML file changed. This made iterative test development slow and inefficient.

## Root Cause

The integration test pattern rule in `dm-dist-alfa/makefile` (line 68) depended on the phony target `worldfiles`:

```makefile
integration_test_outputs/%.out: ../tests/integration/%.yaml dmserver worldfiles ../tools/create_test_player | integration_test_outputs
```

Since `worldfiles` is a phony target (`.PHONY`), Make treats it as always out-of-date. This caused all integration tests to rerun every time, regardless of what actually changed.

## Solution

Changed the dependency from the phony `worldfiles` target to the actual world files:

```makefile
integration_test_outputs/%.out: ../tests/integration/%.yaml dmserver lib/tinyworld.wld lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.zon lib/tinyworld.shp lib/tinyworld.qst ../tools/create_test_player | integration_test_outputs
```

This allows Make to properly track file timestamps and only rerun tests when necessary.

## Behavior After Fix

Tests now only run when:
1. **The test YAML file changes** - only that specific test reruns
2. **dmserver binary changes** - all tests rerun (correct, as the server code changed)
3. **create_test_player binary changes** - all tests rerun (correct, as the test infrastructure changed)
4. **Any tinyworld.* file changes** - all tests rerun (correct, as the game world changed)

## Testing

Verified the fix works correctly by:
- Running tests twice with no changes → tests don't rerun ✓
- Touching one test YAML → only that test reruns ✓
- Touching dmserver → all tests rerun ✓
- Touching create_test_player → all tests rerun ✓
- Touching tinyworld.mob → all tests rerun ✓

## Impact

- **Development speed**: Faster iteration when working on individual tests
- **CI/CD efficiency**: Only necessary tests run, reducing build times
- **Correctness**: Tests still run when dependencies change
- **Build system**: More accurate dependency tracking

## Additional Fix: validate-commands Dependency

Initially, there was a separate issue where `interpreter.o` depended on the phony target `validate-commands`, causing dmserver to rebuild on every make invocation. This masked the benefits of the worldfiles dependency fix.

This was fixed using the same marker file approach:

1. Created `.validate-commands-passed` marker file
2. Made the phony `validate-commands` target depend on the marker file
3. The marker file depends on `interpreter.c` and `validate_commands.py`
4. Changed `interpreter.o` to depend on `.validate-commands-passed` instead of `validate-commands`
5. Added marker file to clean target and .gitignore

This ensures validation only runs when `interpreter.c` or the validation script changes, not on every build.

## Files Changed

- `dm-dist-alfa/makefile` - One line changed (line 68)

## Commit

```
Fix integration test dependencies to use actual world files instead of phony target
```
