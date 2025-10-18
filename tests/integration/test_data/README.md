# Test Data Directory

This directory contains data files used by integration tests but are NOT tests themselves.

## Files

### hammer_object.yml

Thor's Hammer - An impossibly powerful test weapon (1d4+200 damage, +50 tohit/damage modifiers).

**Purpose:** Used by `test_experience_gain.yaml` to ensure reliable, non-flaky test results. The weapon guarantees that the test character can kill the test mobile in a single hit, eliminating timing variability.

**Important:** This file uses `.yml` extension (not `.yaml`) to prevent the test runner from attempting to execute it as a test.

**Security:** This weapon should NEVER appear in production. The test framework dynamically merges this object into the test zone during test setup only.

## Usage

Test files reference these data files using the `test_extensions` setup parameter:

```yaml
setup:
  test_extensions:
    - zone_file: zone_1200.yaml
      extension_file: test_data/hammer_object.yml
```

The test runner will:
1. Create a test_lib directory (copy of production lib)
2. Merge the extension objects into the specified zone file
3. Rebuild the world files with the test objects included
4. Run the test with the modified world
5. Clean up afterwards

This ensures test objects never contaminate production data.
