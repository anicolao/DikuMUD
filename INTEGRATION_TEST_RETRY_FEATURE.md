# Integration Test Retry Feature

## Overview

The integration test framework now supports incremental retries. When tests fail, their outputs are moved to a `integration_test_failures/` directory. Running `make all` again will only rerun the previously failed tests, not all tests.

## How It Works

### Normal Test Run (All Pass)
```bash
$ cd dm-dist-alfa
$ make test

# All tests run
Running test: ../tests/integration/test_a.yaml
Running test: ../tests/integration/test_b.yaml
Running test: ../tests/integration/test_c.yaml

==========================================
Integration Test Results Summary
==========================================
Total:  3
Passed: 3
Failed: 0

✅ All tests passed!
```

Outputs remain in `integration_test_outputs/`:
- `integration_test_outputs/test_a.out` (PASSED)
- `integration_test_outputs/test_b.out` (PASSED)
- `integration_test_outputs/test_c.out` (PASSED)

### Test Run With Failures
```bash
$ cd dm-dist-alfa
$ make test

# All tests run
Running test: ../tests/integration/test_a.yaml
Running test: ../tests/integration/test_b.yaml
Running test: ../tests/integration/test_c.yaml

==========================================
Integration Test Results Summary
==========================================
Total:  3
Passed: 2
Failed: 1

❌ 1 test(s) failed

Failed tests:
  - integration_test_outputs/test_b.out

Moving failed test outputs to integration_test_failures/...
  Moved: integration_test_outputs/test_b.out -> integration_test_failures/test_b.out

Run 'make all' again to retry only the failed tests.
```

After this run:
- `integration_test_outputs/test_a.out` (PASSED)
- `integration_test_outputs/test_c.out` (PASSED)
- `integration_test_failures/test_b.out` (FAILED) ← moved here

### Retry Failed Tests
```bash
$ make all

# Only failed test runs
Running test: ../tests/integration/test_b.yaml

==========================================
Integration Test Results Summary
==========================================
Total:  3
Passed: 3
Failed: 0

✅ All tests passed!
```

**Key Point:** Only `test_b.yaml` ran because its output file was missing from `integration_test_outputs/`. Make's dependency tracking automatically handled this.

## Benefits

1. **Save Time**: Don't rerun tests that already passed
2. **Focus on Failures**: Quickly iterate on fixing broken tests
3. **Preserve Context**: Failed outputs are kept in `integration_test_failures/` for inspection
4. **Simple Workflow**: Just run `make all` repeatedly until all tests pass

## Directory Structure

```
dm-dist-alfa/
├── integration_test_outputs/     # Passed tests (not in git)
│   ├── test_a.out
│   ├── test_c.out
│   ├── shops/
│   │   └── test_shop.out
│   └── quests/
│       └── test_quest.out
│
└── integration_test_failures/    # Failed tests (not in git)
    ├── test_b.out
    ├── shops/
    ├── items/
    └── quests/
```

Both directories are in `.gitignore`.

## Cleaning Up

```bash
# Remove all test outputs and start fresh
$ make clean
```

This removes:
- All compiled objects and executables
- World files
- `integration_test_outputs/`
- `integration_test_failures/`

## Example Workflow

```bash
# 1. Run all tests
$ make all

# If failures occur:
# 2. Inspect failed test outputs
$ cat integration_test_failures/test_something.out

# 3. Fix the issue (update code or test)
$ vim ../tests/integration/test_something.yaml

# 4. Retry only failed tests
$ make all

# Repeat steps 2-4 until all tests pass
```

## Implementation Details

- **Script**: `dm-dist-alfa/process_test_results.py` handles result processing
- **Makefile Target**: `integration_tests` calls the script after running tests
- **Make Dependencies**: Pattern rule `integration_test_outputs/%.out` depends on YAML files
- **Automatic Rerun**: Missing output files trigger test execution via Make's dependency system

## Notes

- Failed test outputs are moved AFTER the summary is displayed
- The failures directory preserves the same subdirectory structure (shops/, items/, quests/)
- Only files marked with "FAILED" on the last line are moved
- If all tests pass, no failures directory is created
