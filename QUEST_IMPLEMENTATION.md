# Quest System Implementation Summary

## Overview

This document describes the implementation of the DikuMUD questing system and the first quest: Sola's quest for Tars Tarkas's Practice Sword.

## Architecture

The quest system leverages DikuMUD's existing affect system to track active quests with minimal code changes:

### Core Components

1. **Quest Constants** (`spells.h`)
   - `QUEST_DELIVERY` (61): Deliver an object to an NPC
   - `QUEST_RETRIEVAL` (62): Retrieve an object from the world
   - `QUEST_KILL` (63): Kill a specific mob
   - `QUEST_EXPLORE` (64): Visit a specific room
   - `QUEST_COLLECT` (65): Collect N items of a type

2. **Quest Bitvector** (`structs.h`)
   - `AFF_QUEST` (16777216): Character is on a quest
   - `QUEST_SHOW_TARGET`, `QUEST_SHOW_ITEM`, `QUEST_SHOW_LOCATION`: Visibility flags

3. **Quest Data Structure** (`structs.h`)
   ```c
   struct quest_data {
       int qnum;             /* Quest number (virtual) */
       int giver_vnum;       /* Mob that gives quest */
       int quest_type;       /* QUEST_* constant */
       int duration;         /* Time limit in MUD hours */
       int target_vnum;      /* Target mob/room vnum */
       int item_vnum;        /* Item to deliver/retrieve */
       int quest_flags;      /* Visibility flags */
       int reward_exp;       /* Experience reward */
       int reward_gold;      /* Gold reward */
       int reward_item;      /* Item vnum reward */
       char *quest_text;     /* Assignment message */
       char *complete_text;  /* Completion message */
       char *fail_text;      /* Failure message */
   };
   ```

4. **Quest Management** (`quest.c`, `quest.h`)
   - `boot_quests()`: Loads quests from `lib/tinyworld.qst` at startup
   - `find_quest_by_giver()`: Finds quest data by NPC vnum
   - `has_quest_type()`: Checks if character has active quest
   - `grant_quest_reward()`: Awards quest rewards to player

5. **Quest Display** (`act.informative.c`)
   - Modified `do_score()` to display active quests
   - Shows quest type and time remaining

6. **World Builder Integration** (`tools/world_builder.py`)
   - Added quest file building from YAML
   - `_build_quest()` method generates DikuMUD format quest records
   - Quests defined in zone YAML files under `quests:` section

## Quest File Format

Quests are defined in `lib/tinyworld.qst` in DikuMUD format:

```
#<quest_number>
<giver_vnum> <quest_type> <duration>
<target_vnum> <item_vnum> <quest_flags>
<reward_exp> <reward_gold> <reward_item_vnum>
<quest_text>~
<complete_text>~
<fail_text>~
S
```

## Sola's Quest

### Quest Details

- **Quest Number**: 4001
- **Quest Giver**: Sola (vnum 4051) in Thark Territory
- **Type**: QUEST_RETRIEVAL (simplified conversation-based)
- **Duration**: 96 MUD hours (~2 real hours)
- **Reward**: 
  - 500 experience points
  - Tars Tarkas's Practice Sword (vnum 4090)

### Quest Flow

1. Player finds Sola in Thark Territory (zone 40)
2. Player asks Sola about "quest", "help", "sword", or "task"
3. Sola gives quest and encourages player to prove themselves
4. Player adventures and gains experience
5. Player returns to Sola and speaks with her again
6. Sola recognizes player's growth and rewards them with the practice sword

### Implementation

**Special Procedure** (`spec_procs.c`):
- `sola_quest_giver()`: Handles quest assignment and completion
- Responds to specific keywords in conversation
- Checks for active quest and completes it on second visit
- Awards rewards automatically upon completion

**Quest Assignment** (`spec_assign.c`):
```c
mob_index[real_mobile(4051)].func = sola_quest_giver;
```

## Tars Tarkas's Practice Sword

### Object Details

- **Vnum**: 4090
- **Type**: ITEM_WEAPON (slash)
- **Damage**: 1d8+1
- **Weight**: 8 lbs
- **Value**: 500 gold
- **Rent**: 150 gold/day
- **Flags**: MAGIC (can hit magical creatures)
- **Wear**: WIELD

### Lore

A well-worn training blade from Tars Tarkas's early days. The weapon bears the marks of four-handed grips from the great Thark chieftain's youth. It's enchanted with minor magic to strike creatures immune to normal weapons.

## Usage

### For Players

To get the quest:
```
go to Thark Territory
find Sola
ask Sola quest
```

To complete the quest:
```
adventure and gain experience
return to Sola
talk to Sola
```

Check quest status:
```
score
```

### For World Builders

Define quests in zone YAML files:

```yaml
quests:
- qnum: 4001
  giver: 4051
  type: 62
  duration: 96
  target: 4051
  item: 0
  flags: 16777216
  reward_exp: 500
  reward_gold: 0
  reward_item: 4090
  quest_text: "Quest assignment text goes here..."
  complete_text: "Quest completion text goes here..."
  fail_text: "Quest failure text goes here..."
```

Build with:
```bash
make worldfiles
```

## Future Enhancements

### Planned Features

1. **Kill Quest Integration**: Modify `fight.c` to detect quest mob deaths
2. **Exploration Quest Integration**: Modify `act.movement.c` to detect room visits
3. **Quest Command**: Add `do_quest()` command for detailed quest information
4. **Quest Chains**: Link quests together for storylines
5. **Group Quests**: Support for party-wide quests
6. **Quest Expiration Warnings**: Alert players when quests are about to expire
7. **Quest History**: Track completed quests for reputation system

### Extension Points

- Add more quest types by defining new QUEST_* constants
- Create quest-giver special procedures for other NPCs
- Design quest chains by setting prerequisites
- Implement hidden quest details with visibility flags
- Add multiple simultaneous quest support

## Design Philosophy

The quest system follows DikuMUD principles:

1. **Minimal Changes**: Uses existing affect system
2. **Historical Style**: 1990s C coding conventions
3. **Automatic Cleanup**: Quest expiration via affect system
4. **Simple but Extensible**: Easy to add new quest types
5. **Lore Integration**: Quests tie to Barsoom world lore

## Testing

Build and test:
```bash
cd dm-dist-alfa
make clean
make all
./dmserver
```

Then connect with telnet and test the quest flow.

## Credits

Designed according to QUESTING_DESIGN.md specification.
Implements first quest from barsoom/DESIRABLE_ARTIFACTS.md.
