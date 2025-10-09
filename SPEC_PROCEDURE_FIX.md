# MOB Special Procedure Validation and Fix

## Problem Statement

The DikuMUD server was logging numerous errors at startup:
```
Non-Existing MOB[4212] SPEC procedure (mobact.c)
Non-Existing MOB[4202] SPEC procedure (mobact.c)
Non-Existing MOB[4214] SPEC procedure (mobact.c)
...
```

Additionally, there was a format string bug causing:
```
Unknown option - 112n argument string.
```

## Root Cause

### Issue 1: MOB Special Procedures
Mobiles had the `ACT_SPEC` flag (bit 0, value 1) set in their `action_flags`, indicating they should have a special procedure assigned. However, no special procedure was actually assigned in `dm-dist-alfa/spec_assign.c`.

When the game tried to call these non-existent procedures in `mobact.c`, it logged errors and removed the flag.

**Affected Mobiles:**
- atmosphere_factory: 4102, 4103, 4104, 4105, 4107, 4112-4119
- atmosphere_lower: 4202, 4212, 4214, 4215  
- southern_approach: 3402, 3403, 3412, 3414-3416

### Issue 2: Format String Bug
In `dm-dist-alfa/comm.c`, line 143 had:
```c
sprintf(buf, "Unknown option -% in argument string.", *(argv[pos] + 1));
```

The format specifier was missing the `c`, causing it to print the ASCII value instead of the character.

### Issue 3: Missing -p Option
The server accepted `-p` for port specification in practice (as shown in the problem statement), but it wasn't handled in the argument parser, causing "Unknown option" warnings.

## Solution

### 1. Enhanced Validation (`tools/validate_world.py`)

Added validation to detect mobiles with `ACT_SPEC` flag but no assigned procedure:

```python
# Track assigned spec procedures from spec_assign.c
self.assigned_spec_procedures = {
    1, 3005, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027,
    3060, 3061, 3062, 3066, 3067, 3143
}

# Check for ACT_SPEC flag (bit 0, value 1) without assigned procedure
action_flags = mob.get('action_flags', 0)
if action_flags & 1:  # ACT_SPEC flag is set
    self.mobs_with_spec_flag[vnum] = zone_name
```

The validation now checks:
- Mobiles with ACT_SPEC flag but no assigned procedure → ERROR
- Mobiles with assigned procedure but no ACT_SPEC flag → WARNING

### 2. Fixed YAML Files

Removed the `ACT_SPEC` flag from 23 mobiles that don't have assigned special procedures:
- Changed `action_flags: 23` to `action_flags: 22` (removed bit 0)

Added the `ACT_SPEC` flag to 9 mobiles that have assigned procedures but were missing the flag:
- Changed `action_flags: 2` to `action_flags: 3` (added bit 0)

### 3. Fixed Format String Bug (`dm-dist-alfa/comm.c`)

Changed line 143:
```c
sprintf(buf, "Unknown option -%c in argument string.", *(argv[pos] + 1));
```

### 4. Added -p Option Support

Added explicit handling for `-p` port option:
```c
case 'p':
    if (*(argv[pos] + 2))
        port = atoi(argv[pos] + 2);
    else if (++pos < argc)
        port = atoi(argv[pos]);
    else
    {
        slog("Port number expected after option -p.");
        exit(0);
    }
break;
```

Updated usage message to reflect the new option.

## Results

### Before:
```
$ ./dmserver -p 5174
Unknown option - 112n argument string.
...
Non-Existing MOB[4212] SPEC procedure (mobact.c)
Non-Existing MOB[4202] SPEC procedure (mobact.c)
[22 more similar errors]
```

### After:
```
$ ./dmserver -p 5174
Running game on port 5174.
Using lib as data directory.
...
Boot db -- DONE.
Entering game loop.
[No errors]
```

### Validation Results:
```
$ python3 tools/validate_world.py dm-dist-alfa/lib/zones_yaml/*.yaml
Validating 12 zone files...
Found 402 rooms, 231 mobiles, 423 objects
Found 12 zones

✓ Validation passed! No errors or warnings found.
```

## Benefits

1. **Clean Server Startup**: No more runtime errors about missing special procedures
2. **Build-Time Validation**: Issues are caught during validation before server startup
3. **Better Error Messages**: Format string bug fixed for clearer error reporting
4. **User-Friendly**: `-p` option now works as expected
5. **Maintainable**: Validator tracks which mobiles should have special procedures

## Future Maintenance

When adding new special procedures:
1. Implement the procedure in `dm-dist-alfa/spec_procs.c`
2. Assign it in `dm-dist-alfa/spec_assign.c`
3. Update `tools/validate_world.py` to add the vnum to `assigned_spec_procedures`
4. Set the `ACT_SPEC` flag (bit 0) in the mobile's `action_flags` in the YAML file
5. Run validation before building

## Files Modified

- `dm-dist-alfa/comm.c` - Fixed format string, added -p option
- `tools/validate_world.py` - Added special procedure validation
- `dm-dist-alfa/lib/zones_yaml/atmosphere_factory.yaml` - Fixed 13 mobiles
- `dm-dist-alfa/lib/zones_yaml/atmosphere_lower.yaml` - Fixed 4 mobiles
- `dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml` - Fixed 9 mobiles
- `dm-dist-alfa/lib/zones_yaml/southern_approach.yaml` - Fixed 6 mobiles
