# DikuMUD Data File Format Specification

This document provides a comprehensive specification of the DikuMUD data file formats based on the original documentation and syntax checker analysis.

## Overview

DikuMUD uses four main data file types to define the game world:
- **World files (.wld)**: Define rooms/locations
- **Mobile files (.mob)**: Define NPCs/monsters
- **Object files (.obj)**: Define items
- **Zone files (.zon)**: Define zone metadata and reset commands

Each file type follows a record-oriented text format with specific delimiters.

## General Format Rules

### Common Elements

1. **Virtual Numbers**: Records are identified by virtual numbers starting with `#`
   ```
   #<virtual_number>
   ```
   - Must be unique within file type
   - Must be in ascending order
   - Used for cross-referencing between files

2. **Text Fields**: Terminated by tilde (`~`) on its own line or at end
   ```
   Text content here~
   ```
   or
   ```
   Multi-line text
   content here
   ~
   ```

3. **Record Terminator**: Each record ends with `S` on its own line
   ```
   S
   ```

4. **File Terminator**: Each file ends with special EOF marker
   ```
   #<any_number>
   $~
   ```
   - The number after # is ignored
   - `$~` must appear on a single line
   - This marks the absolute end of the file

### Critical Format Rules

1. All records MUST be sorted by virtual number in ascending order
2. Text fields may be empty but the `~` terminator is REQUIRED
3. Numeric fields use space separation
4. The `S` terminator is required for each complete record
5. The `$~` EOF marker should appear ONLY ONCE at the very end of each complete file
6. When multiple zone files are concatenated, all but the last `$~` must be removed

## World File Format (.wld)

Defines rooms (locations) in the game world.

### Record Structure

```
#<virtual_number>
<name>~
<description>
~
<zone_nr> <room_flags> <sector_type>
[Direction Blocks]*
[Extra Description Blocks]*
S
```

### Field Definitions

#### Virtual Number
- Unique room identifier
- Used in exits, zone resets, and code references

#### Name
- Short title displayed in room header and exits
- Single line, terminated with `~`

#### Description
- Long description shown when player looks
- Multi-line, terminated with `~` on its own line

#### Zone Number
- Integer identifying which zone this room belongs to
- Used for reset and mobile movement

#### Room Flags
- Bitvector of room properties:
  - `1` - DARK: Requires light to see
  - `2` - DEATH: Player dies on entry
  - `4` - NO_MOB: Mobiles can't enter
  - `8` - INDOORS: Indoor location
  - `16` - LAWFUL
  - `32` - NEUTRAL
  - `64` - CHAOTIC
  - `128` - NO_MAGIC
  - `256` - TUNNEL
  - `512` - PRIVATE: Teleport restrictions

#### Sector Type
- Terrain type affecting movement cost:
  - `0` - INSIDE
  - `1` - CITY
  - `2` - FIELD
  - `3` - FOREST
  - `4` - HILLS
  - `5` - MOUNTAIN
  - `6` - WATER_SWIM
  - `7` - WATER_NOSWIM

### Direction Blocks (Optional)

Format:
```
D<direction>
<exit_description>
~
<keywords>~
<door_flag> <key_vnum> <to_room>
```

Fields:
- **direction**: 0=North, 1=East, 2=South, 3=West, 4=Up, 5=Down
- **exit_description**: Text shown when looking in direction
- **keywords**: Words for door commands (e.g., "door", "gate")
- **door_flag**: 0=no door, 1=can be locked/picked, 2=locked only
- **key_vnum**: Virtual number of key object (-1 for no key)
- **to_room**: Virtual number of destination room (-1 for nowhere)

### Extra Description Blocks (Optional)

Format:
```
E
<keywords>~
<description>
~
```

Fields:
- **keywords**: Space-separated words triggering this description
- **description**: Text shown when examining keywords

### Example

```
#3001
The Temple Of Midgaard~
You are in the southern end of the temple hall in the Temple of Midgaard.
The temple has been constructed from giant marble blocks, eternal in
appearance, and most of the walls are covered by ancient wall paintings.
~
30 0 0
D0
Through the temple hall you see the big statue.
~
~
0 -1 3002
D3
~
~
0 -1 3021
E
paintings wall~
The paintings depict ancient battles and ceremonies.
~
S
```

## Mobile File Format (.mob)

Defines NPCs and monsters.

### Record Structure

```
#<virtual_number>
<namelist>~
<short_description>~
<long_description>
~
<detailed_description>
~
<action_flags> <affection_flags> <alignment> <type_flag>

[If type_flag == 'S' (Simple)]
<level> <thac0> <ac> <hit_points> <damage>
<gold> <experience>
<position> <default_position> <sex>

[If type_flag != 'S' (Detailed)]
<str> <int> <wis> <dex> <con>
<hit_low> <hit_high> <armor> <mana> <move> <gold> <exp>
<position> <default> <sex> <class> <level> <age> <weight> <height>
<cond0> <cond1> <cond2>
<save0> <save1> <save2> <save3> <save4>
```

### Field Definitions

#### Namelist
- Space-separated aliases for the mobile
- Used in targeting commands

#### Short Description
- Name used in action messages (e.g., "The guard leaves south")
- No newline before `~`

#### Long Description
- Text shown when mobile is in default position
- Multi-line, terminated with `~`

#### Detailed Description
- Shown when player looks at mobile
- Multi-line, terminated with `~`

#### Action Flags (Bitvector)
- `1` - SPEC: Has special procedure
- `2` - SENTINEL: Doesn't move
- `4` - SCAVENGER: Picks up items
- `8` - ISNPC: Reserved
- `16` - NICE_THIEF: Won't attack caught thieves
- `32` - AGGRESSIVE: Attacks on sight
- `64` - STAY_ZONE: Won't leave zone
- `128` - WIMPY: Flees when low HP

#### Affection Flags (Bitvector)
- `2` - INVISIBLE
- `8` - DETECT_INVISIBLE
- `128` - SANCTUARY: Half damage
- `524288` - SNEAK: Silent movement
- `1048576` - HIDE
- `4194304` - CHARM

#### Alignment
- Range: -1000 to +1000
- +350 to +1000: Good
- -349 to +349: Neutral
- -1000 to -350: Evil

#### Type Flag
- `'S'` - Simple mobile (recommended)
- Anything else - Detailed mobile (complex)

#### Simple Mobile Fields

- **level**: Mobile level (1-50+)
- **thac0**: To Hit Armor Class 0 (lower is better)
- **ac**: Armor Class (lower is better, can be negative)
- **hit_points**: Format `XdY+Z` (e.g., `5d8+100`)
- **damage**: Format `XdY+Z` (bare hand damage)
- **gold**: Gold carried
- **experience**: XP awarded when killed
- **position**: Starting position (4=sleeping, 5=resting, 6=sitting, 8=standing)
- **default_position**: Position returned to after combat
- **sex**: 0=neutral, 1=male, 2=female

### Example

```
#3060
guard cityguard~
the cityguard~
A cityguard stands here, watching the street.
~
The cityguard is a tough-looking warrior, wearing chain mail and carrying
a longsword and shield. He looks alert and ready for trouble.
~
2 0 1000 S
15 8 5 8d8+200 4d4+2
500 18000
8 8 1
```

## Object File Format (.obj)

Defines items in the game.

### Record Structure

```
#<virtual_number>
<namelist>~
<short_description>~
<long_description>~
<action_description>~
<type_flag> <extra_flags> <wear_flags>
<value0> <value1> <value2> <value3>
<weight> <cost> <rent_cost>
[Extra Description Blocks]*
[Affect Blocks]*
```

### Field Definitions

#### Type Flag
- `1` - LIGHT
- `5` - WEAPON
- `8` - TREASURE
- `9` - ARMOR
- `12` - OTHER
- `13` - TRASH
- `15` - CONTAINER
- `16` - NOTE
- `17` - DRINKCON
- `18` - KEY
- `19` - FOOD
- `20` - MONEY
- `21` - PEN
- `22` - BOAT

#### Extra Flags (Bitvector)
- `1` - GLOW
- `2` - HUM
- `32` - INVISIBLE
- `64` - MAGIC
- `128` - NODROP
- `256` - BLESS
- `512` - ANTI_GOOD
- `1024` - ANTI_EVIL
- `2048` - ANTI_NEUTRAL

#### Wear Flags (Bitvector)
- `1` - TAKE
- `2` - WEAR_FINGER
- `4` - WEAR_NECK
- `8` - WEAR_BODY
- `16` - WEAR_HEAD
- `32` - WEAR_LEGS
- `64` - WEAR_FEET
- `128` - WEAR_HANDS
- `256` - WEAR_ARMS
- `512` - WEAR_SHIELD
- `1024` - WEAR_ABOUT
- `2048` - WEAR_WAIST
- `4096` - WEAR_WRIST
- `8192` - WIELD
- `16384` - HOLD

#### Values
Meaning depends on type_flag. See values.doc for details.

For WEAPON (type 5):
- value0: Unused
- value1: Number of damage dice
- value2: Size of damage dice
- value3: Weapon type

For ARMOR (type 9):
- value0: AC apply
- value1-3: Unused

For CONTAINER (type 15):
- value0: Max weight capacity
- value1: Container flags (1=closeable, 2=pickproof, 4=closed, 8=locked)
- value2: Key vnum (-1 for no key)
- value3: Internal use

#### Weight, Cost, Rent
- **weight**: Weight in pounds
- **cost**: Value if sold to shop
- **rent_cost**: Daily storage cost

### Extra Description Blocks (Optional)

Same format as room extra descriptions:
```
E
<keywords>~
<description>~
```

### Affect Blocks (Optional, max 2)

Format:
```
A
<location> <modifier>
```

Locations:
- `1` - STR
- `2` - DEX
- `3` - INT
- `4` - WIS
- `5` - CON
- `13` - HIT (max HP)
- `17` - AC (armor class)
- `18` - HITROLL
- `19` - DAMROLL
- `20-24` - SAVING_THROWS

### Example

```
#3001
sword long~
a long sword~
A long sword has been left here.~
~
5 0 8193
0 2 5 3
8 0 0
A
18 1
A
19 2
```

## Zone File Format (.zon)

Defines zone metadata and reset behavior.

### Record Structure

```
#<zone_number>
<zone_name>~
<top_room> <lifespan> <reset_mode>
[Reset Commands]*
S
```

### Field Definitions

#### Zone Number
- Zone identifier
- Should match zone_nr in rooms

#### Zone Name
- Descriptive name for the zone

#### Top Room
- Highest room virtual number in this zone
- Rooms belong to zone X if: zone[X-1].top < room_vnum <= zone[X].top

#### Lifespan
- Minutes before zone resets (when conditions met)

#### Reset Mode
- `0` - Never reset
- `1` - Reset when empty (no players)
- `2` - Reset always

### Reset Commands

Each command has format:
```
<cmd_type> <if_flag> <arg1> <arg2> [<arg3>] [<arg4>]
```

#### Common Field: if_flag
- `0` - Execute unconditionally
- `1` - Execute only if previous command succeeded

#### Command Types

**M - Load Mobile**
```
M <if_flag> <mob_vnum> <max_existing> <room_vnum>
```
- Loads mobile into room if fewer than max_existing already exist

**O - Load Object to Room**
```
O <if_flag> <obj_vnum> <max_existing> <room_vnum>
```
- Places object in room if fewer than max_existing exist

**G - Give Object to Mobile**
```
G <if_flag> <obj_vnum> <max_existing>
```
- Gives object to last loaded mobile

**E - Equip Object on Mobile**
```
E <if_flag> <obj_vnum> <max_existing> <position>
```
- Equips object on last loaded mobile
- Position: 0=light, 1-2=finger, 3-4=neck, 5=body, 6=head, 7=legs, 8=feet, 9=hands, 10=arms, 11=shield, 12=about, 13=waist, 14-15=wrist, 16=wield, 17=hold

**P - Put Object in Object**
```
P <if_flag> <obj_vnum1> <max_existing> <obj_vnum2>
```
- Puts obj1 inside obj2

**D - Set Door State**
```
D <if_flag> <room_vnum> <direction> <state>
```
- Direction: 0=N, 1=E, 2=S, 3=W, 4=Up, 5=Down
- State: 0=open, 1=closed, 2=locked

**R - Remove Object from Room**
```
R <if_flag> <room_vnum> <obj_vnum>
```
- Removes object from room

**Comments**
```
* Comment text
```
- Lines starting with `*` are comments and ignored

### Example

```
#30
The Temple Zone~
3099 10 2
* Load the high priest
M 0 3060 1 3001
* Give him a key
G 1 3001 1
* Equip him with armor
E 1 3010 1 5
* Load altar object
O 0 3020 1 3001
* Close and lock the door
D 0 3001 0 2
S
```

## File Concatenation Rules

When building complete world files from multiple zone files:

1. **Remove intermediate EOF markers**: All `$~` markers except the final one must be removed
2. **Preserve record terminators**: All `S` terminators must remain
3. **Maintain sort order**: Records must remain in ascending virtual number order
4. **Add final EOF marker**: Ensure exactly one `$~` at the end of the complete file

Example of incorrect concatenation:
```
#100
Room data
S
$~
#200
Room data
S
$~
```

Correct concatenation:
```
#100
Room data
S
#200
Room data
S
$~
```

## Validation Requirements

A proper validator should check:

1. **Virtual number ordering**: All records in ascending order
2. **Unique virtual numbers**: No duplicates within file type
3. **Proper terminators**: All text fields end with `~`, records end with `S`
4. **Single EOF marker**: Exactly one `$~` at end of file
5. **Cross-references**: All referenced vnums exist:
   - Room exits point to valid rooms
   - Zone commands reference valid mobs/objects/rooms
   - Key vnums reference valid objects
6. **Numeric ranges**: Values within valid ranges
7. **Format correctness**: Dice notation (XdY+Z), bitvectors, etc.
8. **Required fields**: All mandatory fields present
9. **Zone boundaries**: Rooms belong to declared zones
10. **Door consistency**: Doors exist in both connected rooms

## Common Errors

1. **Multiple EOF markers**: Occurs when concatenating zone files naively
2. **Missing text terminators**: Forgetting `~` on text fields
3. **Missing record terminators**: Forgetting `S` at end of record
4. **Out of order records**: Virtual numbers not ascending
5. **Missing references**: Referencing non-existent rooms/objects/mobiles
6. **Invalid dice notation**: Malformed XdY+Z strings
7. **Zone overlap**: Rooms assigned to wrong zones
8. **One-way doors**: Door defined in only one room
