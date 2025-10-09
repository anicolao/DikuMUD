# DikuMUD Questing System Design

## Overview

This document describes the design of a questing system for DikuMUD that allows players to receive, track, and complete quests from NPCs. The design leverages the existing affect system to track active quests while maintaining the historical character of the DikuMUD codebase.

## Design Philosophy

The questing system is built upon the existing DikuMUD affect system, which already provides:
- Time-limited effects on characters
- Storage for numeric values (modifier, location)
- Bitvector for status flags
- Automatic expiration and cleanup

This approach requires **minimal code changes** and reuses proven, well-tested infrastructure.

## Core Mechanism: Quest Affects

### Quest as an Affect

A quest is represented as a special `affected_type` structure applied to a character:

```c
struct affected_type {
    sbyte type;           // Quest skill number (new: QUEST_* constants)
    sh_int duration;      // Time remaining in MUD hours
    sbyte modifier;       // Object vnum to deliver (item quest)
    byte location;        // Target mob vnum (quest giver/receiver)
    long bitvector;       // Quest status flags (AFF_QUEST)
    struct affected_type *next;
};
```

### Quest Type Constants

New skill/spell type constants are added to `spells.h`:

```c
/* Quest types (after SKILL_RESCUE = 52) */
#define QUEST_DELIVERY       61  /* Deliver an object to an NPC */
#define QUEST_RETRIEVAL      62  /* Retrieve an object from the world */
#define QUEST_KILL           63  /* Kill a specific mob */
#define QUEST_EXPLORE        64  /* Visit a specific room */
#define QUEST_COLLECT        65  /* Collect N items of a type */
```

### Quest Status Bitvector

A new bitvector flag in `structs.h`:

```c
/* Add to affected_by bitvector definitions */
#define AFF_QUEST            16777216  /* Character is on a quest */
```

## Quest Assignment Process

### 1. NPC Special Procedure

Quest-giving NPCs have a special procedure that handles conversation:

```c
int quest_giver(struct char_data *ch, int cmd, char *arg)
{
    struct char_data *questor;
    struct affected_type af;
    struct quest_data *quest;
    int i;
    
    /* Only respond to 'ask <npc> quest' or 'quest' command */
    if (cmd != CMD_ASK && cmd != CMD_QUEST)
        return FALSE;
    
    /* Find the player character */
    questor = /* player who spoke */;
    
    /* Check if player already has a quest */
    if (affected_by_spell(questor, QUEST_DELIVERY)) {
        do_say(ch, "You already have a quest to complete!", 0);
        return TRUE;
    }
    
    /* Find quest for this NPC from quest_index */
    quest = NULL;
    for (i = 0; i < top_of_quest_table; i++) {
        if (quest_index[i].giver_vnum == ch->nr) {
            quest = &quest_index[i];
            break;
        }
    }
    
    if (!quest) {
        do_say(ch, "I have no tasks for you at this time.", 0);
        return TRUE;
    }
    
    /* Assign quest affect from template */
    af.type = quest->quest_type;
    af.duration = quest->duration;
    af.modifier = quest->item_vnum;
    af.location = quest->target_vnum;
    af.bitvector = AFF_QUEST | quest->quest_flags;
    
    affect_to_char(questor, &af);
    
    /* Send quest text to player */
    act(quest->quest_text, FALSE, ch, 0, questor, TO_VICT);
    return TRUE;
}
```

### 2. Quest Data Storage

Quest templates are loaded from the database file into a global quest index:

```c
/* In structs.h or db.h */
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

/* Global quest index (loaded from lib/tinyworld.qst) */
extern struct quest_data *quest_index;
extern int top_of_quest_table;
```

Quest-giving NPCs reference quests by their quest number (qnum) from the quest_index.

## Quest Types Implementation

### Type 1: Delivery Quest

**Assignment**: Player receives object to deliver
- `af.type = QUEST_DELIVERY`
- `af.modifier = object_vnum` (what to deliver)
- `af.location = target_mob_vnum` (who to deliver to)

**Completion**: When player gives the object to the target NPC
- NPC special procedure checks if player has active QUEST_DELIVERY
- Verifies object matches `af.modifier`
- Verifies NPC matches `af.location`
- Removes quest affect
- Grants rewards

### Type 2: Retrieval Quest

**Assignment**: Player must find and retrieve an object
- `af.type = QUEST_RETRIEVAL`
- `af.modifier = object_vnum` (what to retrieve)
- `af.location = quest_giver_vnum` (who gave the quest)

**Completion**: When player returns with object
- Quest giver checks player inventory for object
- Verifies player has QUEST_RETRIEVAL active
- Takes the object
- Removes quest affect
- Grants rewards

### Type 3: Kill Quest

**Assignment**: Player must kill a specific mob
- `af.type = QUEST_KILL`
- `af.modifier = target_mob_vnum` (mob to kill)
- `af.location = quest_giver_vnum`

**Completion**: Modified in `fight.c` death handling
- When mob dies, check if any players in room have QUEST_KILL
- Check if dead mob's vnum matches quest target
- Automatically mark quest as complete (store in bitvector)
- Player returns to quest giver who verifies completion

### Type 4: Exploration Quest

**Assignment**: Player must visit a specific location
- `af.type = QUEST_EXPLORE`
- `af.modifier = target_room_vnum`
- `af.location = quest_giver_vnum`

**Completion**: Modified in `act.movement.c`
- When player enters room, check for QUEST_EXPLORE
- If room vnum matches target, mark as complete
- Player returns to quest giver

### Type 5: Collection Quest

**Assignment**: Player must collect N items of a type
- `af.type = QUEST_COLLECT`
- `af.modifier = object_vnum` (type of item)
- Uses extended quest_data for count tracking

**Completion**: Quest giver counts matching items in inventory
- Verifies count meets requirement
- Takes all required items
- Grants rewards

## Time Tracking

### Duration System

Quests use the existing affect duration system:
- Duration is measured in MUD hours (75 real seconds each)
- `af.duration = 48` gives 1 real hour (48 * 75 = 3600 seconds)
- `af.duration = 96` gives 2 real hours
- System automatically decrements duration via `affect_update()` in `spells.c`

### Quest Expiration

When duration reaches 0:
- `affect_update()` automatically removes the quest affect
- Player can optionally be notified via a check in `affect_update()`:
  ```c
  if (af->type >= QUEST_DELIVERY && af->type <= QUEST_COLLECT) {
      if (af->duration == 1) {
          send_to_char("Your quest is about to expire!\n\r", i);
      }
  }
  ```

## Player Quest Information

### Score Command Enhancement

Modify `do_score()` in `act.informative.c` to display active quests:

```c
void do_score(struct char_data *ch, char *argument, int cmd)
{
    /* ... existing score display ... */
    
    /* Display active quests */
    struct affected_type *af;
    bool has_quest = FALSE;
    
    for (af = ch->affected; af; af = af->next) {
        if (af->type >= QUEST_DELIVERY && af->type <= QUEST_COLLECT) {
            if (!has_quest) {
                send_to_char("\n\rActive Quests:\n\r", ch);
                has_quest = TRUE;
            }
            display_quest_info(ch, af);
        }
    }
}
```

### Quest Information Display

```c
void display_quest_info(struct char_data *ch, struct affected_type *af)
{
    char buf[MAX_STRING_LENGTH];
    int hours = af->duration;
    
    sprintf(buf, "Quest: ");
    
    switch(af->type) {
        case QUEST_DELIVERY:
            sprintf(buf + strlen(buf), "Deliver %s to %s",
                get_obj_name(af->modifier),
                get_mob_name(af->location));
            break;
        case QUEST_RETRIEVAL:
            sprintf(buf + strlen(buf), "Retrieve %s",
                get_obj_name(af->modifier));
            break;
        case QUEST_KILL:
            sprintf(buf + strlen(buf), "Defeat %s",
                get_mob_name(af->modifier));
            break;
        case QUEST_EXPLORE:
            sprintf(buf + strlen(buf), "Explore %s",
                get_room_name(af->modifier));
            break;
        case QUEST_COLLECT:
            sprintf(buf + strlen(buf), "Collect items");
            break;
    }
    
    sprintf(buf + strlen(buf), " (Time remaining: %d hours)\n\r", hours);
    send_to_char(buf, ch);
}
```

### Optional: Quest Command

A new `do_quest` command in `act.informative.c`:

```c
void do_quest(struct char_data *ch, char *argument, int cmd)
{
    struct affected_type *af;
    bool found = FALSE;
    
    for (af = ch->affected; af; af = af->next) {
        if (af->type >= QUEST_DELIVERY && af->type <= QUEST_COLLECT) {
            found = TRUE;
            display_quest_detail(ch, af);
        }
    }
    
    if (!found) {
        send_to_char("You are not currently on any quests.\n\r", ch);
        send_to_char("Ask NPCs about quests to begin your adventure!\n\r", ch);
    }
}
```

## Quest Completion System

### Completion Detection

Each quest type has its own completion trigger:

1. **Delivery/Retrieval**: When player interacts with quest NPC
2. **Kill**: When target mob dies (checked in death handler)
3. **Exploration**: When player enters target room
4. **Collection**: When player has required items and talks to quest giver

### Reward System

```c
void grant_quest_reward(struct char_data *ch, struct quest_data *quest)
{
    char buf[MAX_STRING_LENGTH];
    
    /* Experience reward */
    if (quest->reward_exp > 0) {
        gain_exp(ch, quest->reward_exp);
        sprintf(buf, "You gain %d experience!\n\r", quest->reward_exp);
        send_to_char(buf, ch);
    }
    
    /* Gold reward */
    if (quest->reward_gold > 0) {
        GET_GOLD(ch) += quest->reward_gold;
        sprintf(buf, "You receive %d gold coins!\n\r", quest->reward_gold);
        send_to_char(buf, ch);
    }
    
    /* Item reward */
    if (quest->reward_item > 0) {
        struct obj_data *obj = read_object(quest->reward_item, VIRTUAL);
        if (obj) {
            obj_to_char(obj, ch);
            sprintf(buf, "You receive %s!\n\r", 
                obj->short_description);
            send_to_char(buf, ch);
        }
    }
    
    /* Remove quest affect */
    affect_from_char(ch, quest->quest_type);
}
```

## Group Quest Support

### Shared Quest Mechanism

For group quests, all group members receive the same quest affect:

```c
void assign_group_quest(struct char_data *leader, struct affected_type *af)
{
    struct follow_type *f;
    
    /* Assign to leader */
    affect_to_char(leader, af);
    
    /* Assign to all followers in same room */
    for (f = leader->followers; f; f = f->next) {
        if (f->follower->in_room == leader->in_room) {
            affect_to_char(f->follower, af);
        }
    }
}
```

### Group Completion

Group quests can be configured to:
1. **Individual completion**: Each member completes independently
2. **Shared completion**: When one member completes, all complete
3. **Collective completion**: All members must participate

This is handled by checking the bitvector flags and group membership during completion.

## Quest Visibility Options

### Hidden Quest Details

Some quests should be harder by hiding information:

```c
/* Quest visibility flags - stored in upper bits of bitvector */
#define QUEST_SHOW_TARGET    (1 << 24)  /* Show target NPC name */
#define QUEST_SHOW_ITEM      (1 << 25)  /* Show item name */
#define QUEST_SHOW_LOCATION  (1 << 26)  /* Show room/location */

void display_quest_info(struct char_data *ch, struct affected_type *af)
{
    /* If QUEST_SHOW_ITEM is not set, display vague description */
    if (!(af->bitvector & QUEST_SHOW_ITEM)) {
        sprintf(buf, "Deliver something to someone");
    } else {
        sprintf(buf, "Deliver %s to %s",
            get_obj_name(af->modifier),
            get_mob_name(af->location));
    }
}
```

## Implementation Files

### New Files

1. **quest.h** - Quest constants, structures, and function prototypes
2. **quest.c** - Quest management functions
3. **act.quest.c** - Quest command implementations

### Modified Files

1. **structs.h** - Add AFF_QUEST, quest_data structure
2. **spells.h** - Add QUEST_* constants
3. **handler.c** - Quest-specific affect handling
4. **act.informative.c** - Add quest display to score/quest commands
5. **interpreter.c** - Register quest command
6. **spec_procs.c** - Add quest-giver special procedures
7. **fight.c** - Check for kill quest completion on mob death
8. **act.movement.c** - Check for exploration quest on room entry
9. **spells.c** - Quest expiration warnings in affect_update()

## Database Integration

### Quest File Format (.qst)

Quest files follow the same format conventions as other DikuMUD data files (.mob, .obj, .wld, .zon).

#### Record Structure

```
#<quest_number>
<quest_giver_vnum> <quest_type> <duration>
<target_vnum> <item_vnum> <quest_flags>
<reward_exp> <reward_gold> <reward_item_vnum>
<quest_text>~
<complete_text>~
<fail_text>~
S
```

#### Field Definitions

- **quest_number**: Unique quest identifier (virtual number)
- **quest_giver_vnum**: Mobile vnum that assigns this quest
- **quest_type**: Quest type constant (61-65: DELIVERY, RETRIEVAL, KILL, EXPLORE, COLLECT)
- **duration**: Time limit in MUD hours (48 = 1 real hour)
- **target_vnum**: Mob/room vnum for quest target (or 0 if not applicable)
- **item_vnum**: Object vnum for quest item (or 0 if not applicable)
- **quest_flags**: Bitvector for visibility options (QUEST_SHOW_TARGET, QUEST_SHOW_ITEM, etc.)
- **reward_exp**: Experience points awarded on completion
- **reward_gold**: Gold coins awarded on completion
- **reward_item_vnum**: Object vnum to create as reward (or 0 for no item)
- **quest_text**: Text shown when quest is assigned (~ terminated)
- **complete_text**: Text shown when quest is completed (~ terminated)
- **fail_text**: Text shown when quest expires (~ terminated)
- **S**: Record terminator

#### File Terminator

Like all DikuMUD data files, quest files end with:
```
#99999
$~
```

#### Example Quest File

```
#1
3001 61 48
3002 3010 100663296
100 50 3020
Please bring me some fresh bread from the baker.~
Thank you for the bread! Here is your reward.~
You have failed to bring me the bread in time.~
S
#2
3050 62 96
0 3075 0
200 100 0
I seek an ancient amulet. Find it and return to me.~
You have found the amulet! Your reward is well-earned.~
You took too long. The amulet is lost to us now.~
S
#3
3100 63 72
3200 0 16777216
500 250 3105
A dangerous bandit leader threatens our city. Defeat him!~
The bandit leader is dead! You have our gratitude.~
The bandit leader still lives. You have failed us.~
S
#99999
$~
```

### Quest Organization by Zone

Quests are organized by zone - each quest is defined in the same zone file as the quest-giving NPC. This keeps related content together and makes zone maintenance easier.

**Key Principle**: A quest belongs in the zone where its quest-giver NPC is defined, even if the quest references mobs, objects, or rooms in other zones.

**Example**:
- Greater Helium (zone 39) has NPC 3940 (a merchant)
- Quest 3901 is defined in `greater_helium.yaml` because mob 3940 gives it
- Quest 3901 might require delivering item 3010 (from zone 30) to mob 3050 (also zone 30)
- The quest still belongs in zone 39's file because that's where the quest giver is

### YAML Quest Format

For easier maintenance, quests are defined in YAML within zone files and converted to .qst format by the world builder.

#### YAML Schema Addition

Add to each zone's YAML file (e.g., `lib/zones_yaml/greater_helium.yaml`):

```yaml
zone:
  number: 39
  name: "Greater Helium"
  # ... existing zone fields ...

# ... existing rooms, mobiles, objects, resets ...

quests:
  - qnum: 3901
    giver: 3940
    type: 61  # DELIVERY
    duration: 48
    target: 3941
    item: 3510
    flags: 100663296  # SHOW_TARGET | SHOW_ITEM
    reward_exp: 100
    reward_gold: 50
    reward_item: 3520
    quest_text: "Please deliver this message scroll to the officer."
    complete_text: "Excellent! Here is your reward."
    fail_text: "You took too long to deliver the message."
    
  - qnum: 3902
    giver: 3942
    type: 62  # RETRIEVAL
    duration: 96
    target: 0
    item: 3530
    flags: 16777216  # SHOW_ITEM only
    reward_exp: 200
    reward_gold: 100
    reward_item: 0
    quest_text: "Retrieve the stolen artifact and bring it back to me."
    complete_text: "You found it! The artifact is safe once more."
    fail_text: "The artifact remains lost."
```

#### Quest YAML Field Definitions

- **qnum**: Quest virtual number (unique across all zones)
- **giver**: Mobile vnum that gives this quest (must exist in database)
- **type**: Quest type (61=DELIVERY, 62=RETRIEVAL, 63=KILL, 64=EXPLORE, 65=COLLECT)
- **duration**: Time limit in MUD hours
- **target**: Target mobile/room vnum (0 if not used)
- **item**: Required item vnum (0 if not used)
- **flags**: Quest visibility flags (bitfield)
- **reward_exp**: Experience reward
- **reward_gold**: Gold reward
- **reward_item**: Item vnum reward (0 for none)
- **quest_text**: Assignment message (multiline string)
- **complete_text**: Completion message
- **fail_text**: Failure/expiration message

### Cross-Zone Validation

Quest validation must verify references across zones:

#### Validation Rules

1. **Quest Giver Exists**: The `giver` mobile vnum must exist in the world
2. **Target Exists**: The `target` mob/room vnum must exist (if non-zero)
3. **Item Exists**: The `item` object vnum must exist (if non-zero)
4. **Reward Item Exists**: The `reward_item` object vnum must exist (if non-zero)
5. **Zone Dependencies**: Track which zones a quest depends on

#### Validation Example

For a quest in Greater Helium (zone 39):
```yaml
qnum: 3901
giver: 3940     # Must exist in zone 39 (where quest is defined)
target: 3050    # May exist in different zone (Lesser Helium, zone 30)
item: 3010      # May exist in different zone
```

**Validation checks**:
- Quest 3901 belongs in Greater Helium (where mob 3940 is defined)
- Mob 3940 must exist
- Mob 3050 must exist (may be in a different zone)
- Object 3010 must exist (may be in a different zone)
- Note dependency: Greater Helium quests require Lesser Helium data

#### Dependency Tracking

The world builder tracks zone dependencies for quests:

```
Zone 39 (Greater Helium) quests depend on:
  - Zone 30 (Lesser Helium) for mob 3050
  - Zone 30 (Lesser Helium) for object 3010
  
If Lesser Helium is disabled, Greater Helium quests will fail validation.
```

**Implementation**:

```python
def analyze_quest_dependencies(quests: List[Quest], 
                               mob_zones: Dict[int, int],
                               obj_zones: Dict[int, int],
                               room_zones: Dict[int, int]) -> Dict[int, Set[int]]:
    """Map each zone to the zones its quests depend on."""
    dependencies = {}
    
    for quest in quests:
        # Quest belongs to zone of its giver
        giver_zone = mob_zones.get(quest.giver, None)
        if not giver_zone:
            continue
            
        if giver_zone not in dependencies:
            dependencies[giver_zone] = set()
        
        # Check target dependency
        if quest.target != 0:
            if quest.type in [61, 62, 63]:  # MOB target
                target_zone = mob_zones.get(quest.target)
                if target_zone and target_zone != giver_zone:
                    dependencies[giver_zone].add(target_zone)
            elif quest.type == 64:  # ROOM target
                target_zone = room_zones.get(quest.target)
                if target_zone and target_zone != giver_zone:
                    dependencies[giver_zone].add(target_zone)
        
        # Check item dependency
        if quest.item != 0:
            item_zone = obj_zones.get(quest.item)
            if item_zone and item_zone != giver_zone:
                dependencies[giver_zone].add(item_zone)
        
        # Check reward item dependency
        if quest.reward_item != 0:
            reward_zone = obj_zones.get(quest.reward_item)
            if reward_zone and reward_zone != giver_zone:
                dependencies[giver_zone].add(reward_zone)
    
    return dependencies
```

This ensures all quest-related entities are available when zones are loaded.

### World Builder Integration

Update `tools/world_builder.py` to handle quest conversion.

#### Quest Loading from YAML

```python
@dataclass
class Quest:
    """Represents a quest."""
    qnum: int
    giver: int
    type: int
    duration: int
    target: int
    item: int
    flags: int
    reward_exp: int
    reward_gold: int
    reward_item: int
    quest_text: str
    complete_text: str
    fail_text: str
```

#### Quest File Generation

The world builder collects quests from all zone YAML files and concatenates them into a single `tinyworld.qst` file:

```python
def write_quest_file(quests: List[Quest], output_path: str):
    """Write quests to DikuMUD .qst format."""
    with open(output_path, 'w') as f:
        # Sort all quests by qnum across all zones
        for quest in sorted(quests, key=lambda q: q.qnum):
            f.write(f"#{quest.qnum}\n")
            f.write(f"{quest.giver} {quest.type} {quest.duration}\n")
            f.write(f"{quest.target} {quest.item} {quest.flags}\n")
            f.write(f"{quest.reward_exp} {quest.reward_gold} {quest.reward_item}\n")
            f.write(f"{quest.quest_text}~\n")
            f.write(f"{quest.complete_text}~\n")
            f.write(f"{quest.fail_text}~\n")
            f.write("S\n")
        
        # Single EOF marker at end of concatenated file
        f.write("#99999\n")
        f.write("$~\n")
```

**Note**: Like other database files, quests from all zones are concatenated into a single `lib/tinyworld.qst` file with quest records sorted by qnum and only one `$~` EOF marker at the very end.

#### Quest Validation

```python
def validate_quests(quests: List[Quest], 
                   all_mobs: Dict[int, Mobile],
                   all_objs: Dict[int, Object],
                   all_rooms: Dict[int, Room]) -> List[str]:
    """Validate quest references."""
    errors = []
    
    for quest in quests:
        # Validate giver exists
        if quest.giver not in all_mobs:
            errors.append(f"Quest {quest.qnum}: giver mob {quest.giver} not found")
        
        # Validate target exists (if specified)
        if quest.target != 0:
            if quest.type in [61, 62, 63]:  # DELIVERY, RETRIEVAL, KILL
                if quest.target not in all_mobs:
                    errors.append(f"Quest {quest.qnum}: target mob {quest.target} not found")
            elif quest.type == 64:  # EXPLORE
                if quest.target not in all_rooms:
                    errors.append(f"Quest {quest.qnum}: target room {quest.target} not found")
        
        # Validate item exists (if specified)
        if quest.item != 0 and quest.item not in all_objs:
            errors.append(f"Quest {quest.qnum}: item {quest.item} not found")
        
        # Validate reward item exists (if specified)
        if quest.reward_item != 0 and quest.reward_item not in all_objs:
            errors.append(f"Quest {quest.qnum}: reward item {quest.reward_item} not found")
    
    return errors
```

### Loading Quests in Game

Add to `db.c`:

```c
#define QUEST_FILE "lib/tinyworld.qst"

struct quest_data {
    int qnum;
    int giver_vnum;
    int quest_type;
    int duration;
    int target_vnum;
    int item_vnum;
    int quest_flags;
    int reward_exp;
    int reward_gold;
    int reward_item;
    char *quest_text;
    char *complete_text;
    char *fail_text;
};

struct quest_data *quest_index;
int top_of_quest_table = 0;

void boot_quests(void)
{
    FILE *fl;
    int nr = -1, last = 0;
    char buf[256];
    
    if (!(fl = fopen(QUEST_FILE, "r"))) {
        slog("No quest file found - quests disabled");
        return;
    }
    
    /* Count quests */
    while (fgets(buf, 256, fl)) {
        if (*buf == '#')
            nr++;
    }
    
    rewind(fl);
    
    if (nr >= 0) {
        CREATE(quest_index, struct quest_data, nr);
        
        for (nr = 0; nr < top_of_quest_table; nr++) {
            /* Parse quest record */
            fscanf(fl, " #%d\n", &quest_index[nr].qnum);
            fscanf(fl, " %d %d %d\n", 
                   &quest_index[nr].giver_vnum,
                   &quest_index[nr].quest_type,
                   &quest_index[nr].duration);
            fscanf(fl, " %d %d %d\n",
                   &quest_index[nr].target_vnum,
                   &quest_index[nr].item_vnum,
                   &quest_index[nr].quest_flags);
            fscanf(fl, " %d %d %d\n",
                   &quest_index[nr].reward_exp,
                   &quest_index[nr].reward_gold,
                   &quest_index[nr].reward_item);
            
            quest_index[nr].quest_text = fread_string(fl);
            quest_index[nr].complete_text = fread_string(fl);
            quest_index[nr].fail_text = fread_string(fl);
            
            /* Read S terminator */
            fgets(buf, 256, fl);
        }
        
        top_of_quest_table = nr;
    }
    
    fclose(fl);
    sprintf(buf, "   %d quests loaded", top_of_quest_table);
    slog(buf);
}
```

### Makefile Integration

Update the makefile to build quest files:

```makefile
# Quest file building
lib/tinyworld.qst: $(ZONE_YAML_FILES)
	$(PYTHON) $(WORLD_BUILDER) --output-dir lib --build-quests
```

## Advantages of This Design

### 1. Minimal Code Changes
- Leverages existing affect system (proven and tested)
- Reuses existing duration/expiration mechanisms
- No new database tables or complex state management

### 2. Automatic Cleanup
- Expired quests automatically removed by `affect_update()`
- No memory leaks or stale quest data
- Server restart-safe (affects saved with player)

### 3. Natural Integration
- Quests visible in score (like other affects)
- Duration tracking works identically to spell durations
- Quest status persists through logout/login

### 4. Extensible
- Easy to add new quest types (just new QUEST_* constants)
- Quest-giver NPCs use familiar special procedure system
- Can layer complexity gradually

### 5. Historical Consistency
- Follows DikuMUD design patterns
- Uses 1990s C coding style
- Minimal dependencies on external systems

## Alternative Considered: Separate Quest System

The problem statement suggested using the affect system, which I agree with because:

**Alternative approach** (NOT recommended):
- Separate `quest_data` structure linked to `char_data`
- Manual time tracking and cleanup
- Additional save/load code for player files
- More complex state management

**Why affect system is better**:
- Already has time tracking (`duration`)
- Already has storage for key values (`modifier`, `location`)
- Already saves/loads with player data
- Already has automatic expiration
- No new infrastructure needed

## Example Quest Flows

### Example 1: Simple Delivery

1. Player talks to baker (mob 3001)
2. Baker assigns QUEST_DELIVERY affect:
   - duration: 48 (1 hour)
   - modifier: 3010 (bread)
   - location: 3002 (noble)
   - bitvector: AFF_QUEST | QUEST_SHOW_TARGET | QUEST_SHOW_ITEM

3. Player checks score: "Quest: Deliver bread to noble (Time: 48 hours)"
4. Player gets bread from baker's shop
5. Player gives bread to noble
6. Noble's special procedure detects quest completion
7. Noble grants reward: 100 exp, 50 gold
8. Quest affect removed

### Example 2: Hidden Retrieval

1. Player talks to mysterious merchant (mob 3050)
2. Merchant assigns QUEST_RETRIEVAL affect:
   - duration: 96 (2 hours)
   - modifier: 3075 (ancient amulet)
   - location: 3050 (merchant)
   - bitvector: AFF_QUEST (no visibility flags)

3. Player checks score: "Quest: Retrieve something (Time: 96 hours)"
4. Player must explore and discover what to find
5. Player finds ancient amulet in dungeon
6. Player returns to merchant with amulet
7. Merchant verifies and grants reward
8. Quest affect removed

### Example 3: Group Kill Quest

1. Party leader talks to guard captain (mob 3100)
2. Captain assigns QUEST_KILL to entire group:
   - duration: 72
   - modifier: 3200 (bandit leader)
   - location: 3100 (captain)
   - bitvector: AFF_QUEST | GROUP_QUEST

3. All party members see: "Quest: Defeat bandit leader (Time: 72 hours)"
4. Party hunts down and kills bandit leader
5. Death handler marks all party members' quests as complete
6. Party returns to captain
7. Captain grants reward to each member
8. Quest affects removed from all

## Implementation Priority

### Phase 1: Core System (Minimum Viable)
1. Add QUEST_* constants to spells.h
2. Add AFF_QUEST to structs.h
3. Implement basic quest affect handling in handler.c
4. Add quest display to do_score()
5. Create one quest-giver NPC with QUEST_DELIVERY

### Phase 2: Quest Commands
1. Implement do_quest() command
2. Add quest information helpers
3. Add quest completion detection

### Phase 3: Multiple Quest Types
1. Implement QUEST_RETRIEVAL
2. Implement QUEST_KILL (with fight.c integration)
3. Implement QUEST_EXPLORE (with movement integration)

### Phase 4: Advanced Features
1. Quest templates and database file
2. Group quest support
3. Hidden quest details
4. Quest expiration warnings
5. Multiple simultaneous quests

### Phase 5: World Integration
1. Create quest-giving NPCs for each major zone
2. Design quest chains and storylines
3. Balance quest rewards
4. Add unique quest reward items

## Testing Strategy

### Unit Tests
1. Quest affect creation and removal
2. Duration countdown and expiration
3. Quest completion detection
4. Reward calculation and granting

### Integration Tests
1. Player receives quest from NPC
2. Quest displays correctly in score
3. Quest completes when conditions met
4. Quest expires after time limit
5. Quest persists through logout/login

### Gameplay Tests
1. Complete each quest type successfully
2. Let quest expire and verify cleanup
3. Test with group quest mechanics
4. Test with hidden quest information
5. Test multiple simultaneous quests

## Future Enhancements

### Dynamic Quest Generation
- Randomly generate quest parameters
- Scale difficulty to player level
- Vary rewards based on difficulty

### Quest Chains
- Completion of one quest unlocks next
- Story progression through quest series
- Epic quest lines for max-level players

### Reputation System
- Track quest completions per NPC
- Unlock special quests with high reputation
- Better prices from quest-giving merchants

### Quest Journal
- Dedicated quest log separate from score
- Quest history and completion statistics
- Hints and clues for active quests

## Conclusion

This quest system design provides a robust, extensible foundation for questing in DikuMUD while maintaining the historical character and simplicity of the original codebase. By leveraging the existing affect system, we achieve maximum functionality with minimal code changes, ensuring reliability and maintainability.

The affect-based approach is elegant: quests are temporary effects on characters, just like spells. They have duration, they modify character state, and they automatically clean up when expired. This is the DikuMUD way.
