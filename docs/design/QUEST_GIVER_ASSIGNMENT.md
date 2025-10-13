# Quest Giver Automatic Assignment System

## Overview

The quest system now automatically assigns the `quest_giver` special procedure to all quest-giving NPCs at boot time. This eliminates the need to manually add code in `spec_assign.c` for each new quest.

## How It Works

### Boot Sequence

1. **Load Quest Data** (`boot_quests()` in `quest.c`)
   - Reads `lib/tinyworld.qst` file
   - Parses all quest definitions
   - Builds `quest_index[]` array with quest data
   - Reports: `"X quests loaded"`

2. **Assign Quest Givers** (`assign_quest_givers()` in `quest.c`)
   - Iterates through all loaded quests
   - For each quest, finds the mob with the giver vnum
   - Assigns the `quest_giver` special procedure to that mob
   - Reports: `"X quest givers assigned"`

### Implementation Details

**File: `quest.c`**
```c
void assign_quest_givers(void)
{
    extern struct index_data *mob_index;
    extern int real_mobile(int virtual);
    extern int quest_giver(struct char_data *ch, int cmd, char *arg);
    
    for (i = 0; i < top_of_quest_table; i++) {
        real_mob = real_mobile(quest_index[i].giver_vnum);
        if (real_mob >= 0) {
            mob_index[real_mob].func = quest_giver;
            assigned++;
        }
    }
}
```

**File: `db.c`** (boot sequence)
```c
slog("Loading quests.");
boot_quests();
slog("Assigning quest givers.");
assign_quest_givers();
```

## Adding New Quests

To add new quests, you now only need to add quest data to YAML zone files. No code changes required!

### Step-by-Step

1. **Edit zone YAML file** (e.g., `lib/zones_yaml/my_zone.yaml`)
   ```yaml
   quests:
   - qnum: 5001
     giver: 5010  # Mob vnum of quest giver
     type: 62     # Quest type constant
     duration: 96
     target: 5010
     item: 5050
     flags: 50331648
     reward_exp: 1000
     reward_gold: 500
     reward_item: 5051
     quest_text: "Quest giver speaks..."
     complete_text: "Thank you for completing..."
     fail_text: "You failed to complete..."
   ```

2. **Rebuild world files**
   ```bash
   cd dm-dist-alfa
   make worldfiles
   ```

3. **Restart server**
   - The quest giver mob (5010) will automatically have the `quest_giver` special procedure assigned
   - No changes to `spec_assign.c` needed!

## Benefits

### Before This Change

Every new quest required:
1. Adding quest data to YAML file
2. **Adding hardcoded line in `spec_assign.c`:**
   ```c
   mob_index[real_mobile(5010)].func = quest_giver;
   ```
3. Recompiling the server

### After This Change

New quests require only:
1. Adding quest data to YAML file
2. Rebuilding world files (no recompilation needed unless code changes)

**Pure data-driven quest creation!**

## Backward Compatibility

- Existing quests continue to work without any changes
- The old hardcoded assignments in `spec_assign.c` have been removed
- All quest assignments are now automatic

## Testing

Run the automated test:
```bash
./test_quest_assignment.sh
```

This test verifies:
- Quest file is properly generated
- All quest givers are automatically assigned
- No hardcoded assignments remain in `spec_assign.c`
- Quest count matches assigned giver count

## Implementation Files

### Modified Files

- **`dm-dist-alfa/quest.h`** - Added `assign_quest_givers()` declaration
- **`dm-dist-alfa/quest.c`** - Implemented `assign_quest_givers()` function
- **`dm-dist-alfa/db.c`** - Added call to `assign_quest_givers()` after `boot_quests()`
- **`dm-dist-alfa/spec_assign.c`** - Removed all hardcoded `quest_giver` assignments

### New Files

- **`test_quest_assignment.sh`** - Automated test for quest assignment system

## Technical Notes

### Error Handling

If a quest references a non-existent mob vnum, the system logs a warning:
```
Warning: Quest 5001 references non-existent mob 5010
```

The server will still boot, but that particular quest will not be available until the mob is added.

### Quest Giver Procedure

The `quest_giver` special procedure (in `spec_procs.c`) is a generic handler that:
1. Uses `find_quest_by_giver()` to look up quest data by mob vnum
2. Responds to player commands like "ask <npc> quest"
3. Assigns quests to players
4. All quest-specific behavior is data-driven

### Multiple Quests per Mob

Currently, each mob can give one quest. The system assigns `quest_giver` to a mob if it appears as a giver in any quest. If multiple quests share the same giver vnum, `find_quest_by_giver()` returns the first matching quest.

## Future Enhancements

Potential improvements:
- Support for multiple quests per NPC
- Quest prerequisites and chains
- Dynamic quest generation
- Quest state persistence across server restarts

## See Also

- `QUESTING_DESIGN.md` - Overall quest system design
- `QUEST_IMPLEMENTATION.md` - Quest system implementation details
- `DIKUMUD_YAML_SCHEMA.md` - YAML file format specification
