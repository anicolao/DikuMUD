# DikuMUD YAML Schema Design

This document defines the YAML schema for representing DikuMUD world data in a more maintainable format.

## Design Goals

1. **Eliminate manual text terminators**: YAML handles string boundaries
2. **Prevent EOF marker issues**: YAML doesn't require explicit EOF markers
3. **Enable validation**: Structured data easier to validate
4. **Improve readability**: YAML is more human-friendly than the original format
5. **Support comments**: YAML native comment support
6. **Type safety**: Explicit types prevent common errors

## Zone File Schema

A zone file contains all data for one zone: rooms, mobiles, objects, zone metadata, and shops.

```yaml
---
# Zone metadata
zone:
  number: 0
  name: "LIMBO"
  top_room: 3
  lifespan: 1
  reset_mode: 0  # 0=never, 1=when empty, 2=always

# Room definitions
rooms:
  - vnum: 0
    name: "The Void"
    description: |
      You step out into ......
      You don't think that you are not floating in nothing.
    zone: 0
    room_flags: 8
    sector_type: 1
    exits:
      - direction: 4  # up
        description: "void"
        keywords: ""
        door_flag: 0
        key_vnum: -1
        to_room: 3001
    extra_descriptions: []

  - vnum: 1
    name: "The Void"
    description: "You don't think that you are not floating in nothing."
    zone: 0
    room_flags: 8
    sector_type: 1
    exits: []
    extra_descriptions: []

# Mobile definitions
mobiles:
  - vnum: 1
    namelist: "puff banth ancient"
    short_desc: "Puff"
    long_desc: "Puff, an ancient white banth, rests here contemplating mysteries."
    detailed_desc: |
      This legendary banth is unlike any other on Mars. Its ten legs end in
      massive paws, and its white fur shimmers with an otherworldly quality.
      Ancient beyond measure, it seems to perceive realities beyond normal
      understanding. Its leonine face holds wisdom and power in equal measure.
    action_flags: 1
    affection_flags: 0
    alignment: 1000
    type: simple
    simple:
      level: 26
      thac0: 1
      ac: -1
      hp_dice: "5d10+550"
      damage_dice: "4d6+3"
      gold: 10000
      experience: 155000
      position: 8
      default_position: 8
      sex: 2

# Object definitions
objects:
  - vnum: 1
    namelist: "parchment rules"
    short_desc: "a parchment of rules"
    long_desc: "A formal parchment document has been placed here."
    action_desc: |
      Rules text here...
    type_flag: 16  # NOTE
    extra_flags: 0
    wear_flags: 16385  # TAKE | HOLD
    value0: 0
    value1: 0
    value2: 0
    value3: 0
    weight: 1
    cost: 10
    rent: 2
    extra_descriptions: []
    affects: []

# Zone reset commands
resets:
  - command: M
    if_flag: 0
    arg1: 1      # mob vnum
    arg2: 1      # max existing
    arg3: 2      # room vnum
    comment: "Load Puff in Limbo"

# Shop definitions (optional)
shops: []
```

## Field Descriptions

### Zone Section

- **number**: Integer zone ID
- **name**: String zone name
- **top_room**: Highest room vnum in zone
- **lifespan**: Minutes before reset
- **reset_mode**: 0, 1, or 2

### Rooms Section

Each room has:
- **vnum**: Integer virtual number (required, unique)
- **name**: String room name (required)
- **description**: String or multi-line description (required)
- **zone**: Integer zone number (required)
- **room_flags**: Integer bitvector (required)
- **sector_type**: Integer 0-7 (required)
- **exits**: List of exit objects (optional)
  - **direction**: Integer 0-5 (0=N, 1=E, 2=S, 3=W, 4=Up, 5=Down)
  - **description**: String exit description
  - **keywords**: String door keywords
  - **door_flag**: Integer 0-2
  - **key_vnum**: Integer key object vnum or -1
  - **to_room**: Integer destination room vnum or -1
- **extra_descriptions**: List of extra description objects (optional)
  - **keywords**: String space-separated keywords
  - **description**: String description text

### Mobiles Section

Each mobile has:
- **vnum**: Integer virtual number (required, unique)
- **namelist**: String space-separated aliases (required)
- **short_desc**: String short description (required)
- **long_desc**: String long description (required)
- **detailed_desc**: String or multi-line detailed description (required)
- **action_flags**: Integer bitvector (required)
- **affection_flags**: Integer bitvector (required)
- **alignment**: Integer -1000 to 1000 (required)
- **type**: String "simple" or "detailed" (required)
- **simple**: Object (if type is simple)
  - **level**: Integer level
  - **thac0**: Integer THAC0
  - **ac**: Integer AC
  - **hp_dice**: String dice notation (XdY+Z)
  - **damage_dice**: String dice notation (XdY+Z)
  - **gold**: Integer gold amount
  - **experience**: Integer XP value
  - **position**: Integer position code
  - **default_position**: Integer default position
  - **sex**: Integer sex code (0, 1, 2)

### Objects Section

Each object has:
- **vnum**: Integer virtual number (required, unique)
- **namelist**: String space-separated aliases (required)
- **short_desc**: String short description (required)
- **long_desc**: String long description (required)
- **action_desc**: String action description (required)
- **type_flag**: Integer type code (required)
- **extra_flags**: Integer bitvector (required)
- **wear_flags**: Integer bitvector (required)
- **value0**: Integer value field 0 (required)
- **value1**: Integer value field 1 (required)
- **value2**: Integer value field 2 (required)
- **value3**: Integer value field 3 (required)
- **weight**: Integer weight (required)
- **cost**: Integer cost (required)
- **rent**: Integer rent cost (required)
- **extra_descriptions**: List of extra description objects (optional)
  - **keywords**: String space-separated keywords
  - **description**: String description text
- **affects**: List of affect objects (optional, max 2)
  - **location**: Integer apply location code
  - **modifier**: Integer modifier value

### Resets Section

Each reset command has:
- **command**: String command type (M, O, G, E, P, D, R)
- **if_flag**: Integer 0 or 1
- **arg1**: Integer first argument
- **arg2**: Integer second argument
- **arg3**: Integer third argument (optional, depends on command)
- **arg4**: Integer fourth argument (optional, depends on command)
- **comment**: String comment (optional)

### Shops Section

Each shop has:
- **vnum**: Integer shop number
- **keeper**: Integer mobile vnum
- **buy_types**: List of integers (item types shop buys)
- **buy_markup**: Float buy price multiplier
- **sell_markup**: Float sell price multiplier
- **hours**: List of integers [open_hour1, close_hour1, open_hour2, close_hour2]
- **rooms**: List of integers (room vnums where shop operates)
- **messages**: Object with shop messages
  - **no_such_item1**: String
  - **no_such_item2**: String
  - **no_buy_item**: String
  - **cant_afford**: String
  - **buy_success**: String
  - **sell_success**: String

## Validation Rules

1. **Uniqueness**: All vnums must be unique within their type (rooms, mobs, objects)
2. **Ordering**: Vnums should be in ascending order for efficiency (warning if not)
3. **Cross-references**: All referenced vnums must exist
4. **Range validation**: Numeric fields within valid ranges
5. **String validation**: Required strings not empty
6. **Dice notation**: hp_dice and damage_dice match pattern `\d+d\d+[+-]\d+`
7. **Zone consistency**: Room zone numbers match zone definition
8. **Door reciprocity**: Exits with doors should exist in both rooms (warning if not)

## Conversion Strategy

### YAML to DikuMUD Format

1. Load YAML file
2. Validate against schema
3. Sort records by vnum
4. Write records in DikuMUD format
5. Add single `$~` EOF marker at end

### DikuMUD to YAML Format

1. Parse DikuMUD format
2. Extract all records
3. Group by type
4. Convert to YAML structure
5. Write YAML file

## Benefits

1. **No EOF marker issues**: YAML handles file boundaries
2. **Better error messages**: YAML parsers give line numbers
3. **Native multiline strings**: No manual `~` terminators
4. **Comments preserved**: Can document zones inline
5. **Type checking**: Validators can check types
6. **Easier editing**: Standard text editors with YAML support
7. **Diff-friendly**: Git diffs are more readable
8. **Extensible**: Easy to add new fields without breaking format

## Migration Path

1. Create converter tool (DikuMUD → YAML)
2. Convert all existing zones to YAML
3. Create validator tool
4. Create builder tool (YAML → DikuMUD)
5. Update makefile to use builder
6. Test thoroughly
7. Document new workflow

## Example Full Zone File

```yaml
---
zone:
  number: 30
  name: "The Temple Zone"
  top_room: 3099
  lifespan: 10
  reset_mode: 2

rooms:
  - vnum: 3001
    name: "The Temple Of Midgaard"
    description: |
      You are in the southern end of the temple hall in the Temple of Midgaard.
      The temple has been constructed from giant marble blocks, eternal in
      appearance, and most of the walls are covered by ancient wall paintings.
    zone: 30
    room_flags: 0
    sector_type: 0
    exits:
      - direction: 0
        description: "Through the temple hall you see the big statue."
        keywords: ""
        door_flag: 0
        key_vnum: -1
        to_room: 3002
      - direction: 3
        description: ""
        keywords: ""
        door_flag: 0
        key_vnum: -1
        to_room: 3021
    extra_descriptions:
      - keywords: "paintings wall"
        description: "The paintings depict ancient battles and ceremonies."

mobiles:
  - vnum: 3060
    namelist: "guard cityguard"
    short_desc: "the cityguard"
    long_desc: "A cityguard stands here, watching the street."
    detailed_desc: |
      The cityguard is a tough-looking warrior, wearing chain mail and carrying
      a longsword and shield. He looks alert and ready for trouble.
    action_flags: 2
    affection_flags: 0
    alignment: 1000
    type: simple
    simple:
      level: 15
      thac0: 8
      ac: 5
      hp_dice: "8d8+200"
      damage_dice: "4d4+2"
      gold: 500
      experience: 18000
      position: 8
      default_position: 8
      sex: 1

objects:
  - vnum: 3001
    namelist: "key gold golden"
    short_desc: "a golden key"
    long_desc: "A golden key lies here."
    action_desc: ""
    type_flag: 18
    extra_flags: 64
    wear_flags: 1
    value0: 0
    value1: 0
    value2: 0
    value3: 0
    weight: 1
    cost: 100
    rent: 10
    extra_descriptions: []
    affects: []

resets:
  - command: M
    if_flag: 0
    arg1: 3060
    arg2: 1
    arg3: 3001
    comment: "Load the cityguard"
  - command: G
    if_flag: 1
    arg1: 3001
    arg2: 1
    comment: "Give him the key"
  - command: E
    if_flag: 1
    arg1: 3010
    arg2: 1
    arg3: 5
    comment: "Equip him with armor"

shops: []
```
