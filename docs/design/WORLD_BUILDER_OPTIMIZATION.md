# World Builder Optimization

## Summary

The world builder has been optimized to significantly reduce build times by reading YAML zone files only once instead of multiple times.

## Problem

Previously, the build process invoked the world builder 7 times:
1. Once for validation (`validate_world.py`)
2. Six times for building each file type (wld, mob, obj, zon, shp, qst)

Each invocation read all 19 YAML zone files, resulting in:
- **7 complete passes** through all YAML files
- **~15 seconds** total build time
- Redundant file I/O and parsing

## Solution

Added a new `build-all` command to `world_builder.py` that:
1. Reads all YAML files once
2. Validates them (integrated validation)
3. Generates all 6 output files in a single pass

The makefile now uses this optimized approach by default.

## Performance Improvement

- **Before**: ~15 seconds (7 passes)
- **After**: ~5.7 seconds (1 pass)
- **Improvement**: 63% faster (2.7x speedup)

## Technical Details

### New Command

```bash
python3 tools/world_builder.py build-all <output_dir> <yaml_file1> [yaml_file2 ...]
```

This command:
- Validates all YAML files first (fails early if there are errors)
- Loads all YAML data into memory once
- Generates all file types (wld, mob, obj, zon, shp, qst) sequentially
- Maintains identical output to the individual build commands

### Makefile Changes

The makefile now:
1. Uses a marker file (`lib/.worldfiles_built`) to track build status
2. Rebuilds all files when any YAML file or tool changes
3. Supports incremental builds (no rebuild if nothing changed)
4. Maintains backward compatibility with individual file targets

### Backward Compatibility

The old individual build commands still work:
```bash
python3 tools/world_builder.py build wld output.wld zones/*.yaml
python3 tools/world_builder.py build mob output.mob zones/*.yaml
# etc.
```

The standalone validation also still works:
```bash
make validate-world
```

## Build Targets

### Main Targets

- `make worldfiles` - Build all world files (uses optimized build-all)
- `make all` - Build everything (server + world files)
- `make clean` - Remove all build artifacts

### Development Targets

- `make validate-world` - Run validation only
- `make build-worldfiles` - Force rebuild of world files

## Files Modified

1. **tools/world_builder.py**
   - Added `build_all_files()` method to `WorldBuilder` class
   - Integrated `WorldValidator` for validation
   - Added `build-all` command to main entry point

2. **dm-dist-alfa/makefile**
   - Changed from 6 individual build rules to single build-all invocation
   - Added marker file for dependency tracking
   - Updated clean target

3. **dm-dist-alfa/.gitignore**
   - Added `lib/.worldfiles_built` marker file
   - Added `lib/tinyworld.qst` (was missing)

## Verification

All generated files are byte-identical to the previous build method:
- ✓ tinyworld.wld
- ✓ tinyworld.mob
- ✓ tinyworld.obj
- ✓ tinyworld.zon
- ✓ tinyworld.shp
- ✓ tinyworld.qst

## Important: Zone Ordering

The `ZONE_ORDER` variable in the makefile **must** list zones in ascending order by room number range. This is because the DikuMUD server assigns rooms to zones sequentially based on the zone's `top` value in the `.zon` file.

**How zone assignment works:**
1. Zones are processed in the order they appear in `tinyworld.zon`
2. Each room is assigned to the first zone where `room_vnum <= zone.top`
3. If zones are out of order, rooms will be assigned to the wrong zones

The world builder:
- Automatically calculates each zone's `top` value from its maximum room vnum
- Preserves the input order of zones (does not sort by zone number)
- Ensures zones appear in `tinyworld.zon` in the same order as `ZONE_ORDER`

**Example:**
```
ZONE_ORDER = limbo system zone_1200 lesser_helium southern_approach ...
```
This ensures rooms 0-2 go to limbo, 1200-1202 go to zone_1200, 3001-3055 go to lesser_helium, etc.

## Future Improvements

Possible further optimizations:
- Cache parsed YAML in a binary format for even faster loading
- Parallelize file generation for each type
- Add progress indicators for large world builds
