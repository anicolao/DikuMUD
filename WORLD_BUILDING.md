# DikuMUD World Building Guide

This document explains the new YAML-based world building system for DikuMUD.

## Overview

The DikuMUD world data has been converted from the legacy text format to YAML for easier editing and maintenance. The build system automatically converts YAML files to the format expected by the game server.

## Why YAML?

The original DikuMUD format had several issues:
1. **Multiple EOF markers**: When concatenating zone files with `cat`, each file's `$~` marker was preserved, causing parsing errors
2. **Manual text terminators**: The `~` character had to be carefully placed, easy to forget
3. **Difficult to validate**: Text format made it hard to catch errors before runtime
4. **Error-prone editing**: Easy to accidentally corrupt the format

YAML provides:
- **Structured format**: Clear field boundaries
- **Native multiline strings**: No manual terminators needed
- **Validation**: Can check for errors before building
- **Better diffs**: Git diffs are more readable
- **Comments**: Can document zones inline

## Directory Structure

```
dm-dist-alfa/
├── lib/
│   ├── zones_yaml/        # YAML source files (edit these)
│   │   ├── limbo.yaml
│   │   ├── lesser_helium.yaml
│   │   └── ...
│   ├── zones/             # Legacy format (preserved for reference)
│   │   ├── limbo.wld
│   │   ├── limbo.mob
│   │   └── ...
│   ├── tinyworld.wld      # Built from YAML (do not edit)
│   ├── tinyworld.mob      # Built from YAML (do not edit)
│   ├── tinyworld.obj      # Built from YAML (do not edit)
│   └── tinyworld.zon      # Built from YAML (do not edit)
└── ...

tools/
├── world_builder.py       # Converts YAML to/from DikuMUD format
├── validate_world.py      # Validates YAML world data
└── build_world.sh         # Helper script for building
```

## Workflow

### Editing World Data

1. **Edit YAML files** in `dm-dist-alfa/lib/zones_yaml/`
   ```bash
   cd dm-dist-alfa/lib/zones_yaml
   nano limbo.yaml
   ```

2. **Validate your changes** (optional but recommended)
   ```bash
   cd /path/to/DikuMUD
   python3 tools/validate_world.py dm-dist-alfa/lib/zones_yaml/*.yaml
   ```

3. **Build the world files**
   ```bash
   cd dm-dist-alfa
   make worldfiles
   ```

4. **Test the server**
   ```bash
   cd dm-dist-alfa
   ./dmserver -p 5174
   ```

### Creating a New Zone

1. **Copy an existing zone as a template**
   ```bash
   cp dm-dist-alfa/lib/zones_yaml/limbo.yaml dm-dist-alfa/lib/zones_yaml/myzone.yaml
   ```

2. **Edit the zone file** and update:
   - Zone number and name
   - Room vnums (must be unique across all zones)
   - Mobile vnums (must be unique across all zones)
   - Object vnums (must be unique across all zones)

3. **Add to build order** in `dm-dist-alfa/makefile`:
   ```makefile
   ZONE_ORDER = limbo ... myzone system
   ```

4. **Build and test** as above

### Converting Legacy Format to YAML

If you have old `.wld`, `.mob`, `.obj`, `.zon` files:

```bash
python3 tools/world_builder.py convert <zone_name> <input_dir> <output.yaml>
```

Example:
```bash
python3 tools/world_builder.py convert midgaard lib/zones lib/zones_yaml/midgaard.yaml
```

### Converting YAML Back to Legacy Format

To build individual files:

```bash
python3 tools/world_builder.py build <type> <output> <yaml_files...>
```

Where `<type>` is one of: `wld`, `mob`, `obj`, `zon`, `shp`

Example:
```bash
python3 tools/world_builder.py build wld /tmp/test.wld lib/zones_yaml/limbo.yaml
```

## YAML Format Reference

See [DIKUMUD_YAML_SCHEMA.md](DIKUMUD_YAML_SCHEMA.md) for complete format specification.

### Quick Example

```yaml
zone:
  number: 30
  name: "My Zone"
  top_room: 3099
  lifespan: 10
  reset_mode: 2

rooms:
  - vnum: 3001
    name: "A Test Room"
    description: |
      This is a multi-line description.
      It can span multiple lines without needing ~
    zone: 30
    room_flags: 0
    sector_type: 0
    exits:
      - direction: 0  # north
        description: "You see another room."
        keywords: ""
        door_flag: 0
        key_vnum: -1
        to_room: 3002
    extra_descriptions: []

mobiles:
  - vnum: 3060
    namelist: "guard city"
    short_desc: "a city guard"
    long_desc: "A guard stands here."
    detailed_desc: "This is a detailed description."
    action_flags: 0
    affection_flags: 0
    alignment: 1000
    type: simple
    simple:
      level: 10
      thac0: 10
      ac: 5
      hp_dice: "5d8+50"
      damage_dice: "2d4+2"
      gold: 100
      experience: 1000
      position: 8
      default_position: 8
      sex: 1

objects:
  - vnum: 3001
    namelist: "sword"
    short_desc: "a sword"
    long_desc: "A sword lies here."
    action_desc: ""
    type_flag: 5
    extra_flags: 0
    wear_flags: 8193
    value0: 0
    value1: 2
    value2: 5
    value3: 3
    weight: 5
    cost: 100
    rent: 10
    extra_descriptions: []
    affects: []

resets:
  - command: M
    if_flag: 0
    arg1: 3060  # mob vnum
    arg2: 1     # max in zone
    arg3: 3001  # room vnum
    comment: "Load city guard"
```

## Validation

The validator checks for:
- **Syntax errors**: Invalid YAML format
- **Unique vnums**: No duplicate room/mob/object numbers
- **Cross-references**: All referenced entities exist
- **Format correctness**: Dice notation, required fields, etc.
- **Zone boundaries**: Rooms belong to correct zones

Run the validator:
```bash
python3 tools/validate_world.py dm-dist-alfa/lib/zones_yaml/*.yaml
```

## Build System

The makefile automatically:
1. Loads all YAML zone files
2. Validates basic format
3. Sorts records by vnum
4. Converts to DikuMUD format
5. Adds proper EOF markers
6. Writes `tinyworld.*` files

Build commands:
```bash
make worldfiles      # Build only world data files
make all             # Build world files and executables
make clean           # Remove built files
```

## Troubleshooting

### "Room X does not exist in database"

This error occurred with the old concatenation system when multiple `$~` EOF markers were present. The new YAML system ensures exactly one EOF marker per file.

### Validation errors

If the validator reports errors:
1. Check the error messages for the zone name and vnum
2. Edit the corresponding YAML file
3. Run validator again
4. Rebuild with `make worldfiles`

### Server won't start after changes

1. Check for syntax errors in YAML:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('dm-dist-alfa/lib/zones_yaml/yourzone.yaml'))"
   ```

2. Validate the world:
   ```bash
   python3 tools/validate_world.py dm-dist-alfa/lib/zones_yaml/*.yaml
   ```

3. Check server output for specific errors:
   ```bash
   ./dmserver -p 5174
   ```

### Reverting to legacy format

The original `.wld`, `.mob`, `.obj`, `.zon` files are preserved in `lib/zones/`. To use them:

1. Edit the makefile to use `cat` instead of `world_builder.py`
2. Make sure to remove duplicate `$~` markers from concatenated files

## Benefits of YAML System

1. **No EOF marker issues**: Automatic handling of file terminators
2. **Easier validation**: Catch errors before runtime
3. **Better editing**: Structure is clearer
4. **Version control**: More readable diffs
5. **Safer**: Less chance of corrupting format
6. **Documented**: Inline comments possible
7. **Maintainable**: Easier to understand and modify

## See Also

- [DIKUMUD_FILE_FORMATS.md](DIKUMUD_FILE_FORMATS.md) - Original format specification
- [DIKUMUD_YAML_SCHEMA.md](DIKUMUD_YAML_SCHEMA.md) - YAML schema details
- [GAMMA_DESIGN.md](GAMMA_DESIGN.md) - Overall system design
