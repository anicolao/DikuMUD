# Quest Completion Tracking

## Overview

The quest completion tracking system ensures that players can only receive rewards for completing a quest once. After receiving the reward, if a player completes the quest objective again, they receive a special acknowledgment message but no additional rewards.

## Implementation

### Data Storage

Quest completion is tracked using a 128-bit bitfield stored in the player data:

- `quests_completed_low` (64 bits): Tracks quest numbers 0-63 (bits 0-63)
- `quests_completed_high` (64 bits): Tracks quest numbers 64-127 (bits 64-127)

These fields are part of:
1. `struct char_player_data` - Runtime character data
2. `struct char_file_u` - Persistent player file data

### Quest Number Mapping

Quest numbers (e.g., 3001, 4002) are mapped to bit positions using modulo 128:
```
bit_position = quest_number % 128
```

This mapping allows tracking up to 128 unique quest completions per player.

### Key Functions

#### `set_quest_completed(struct char_data *ch, int quest_num)`
Marks a quest as completed (player has received reward).
- Called automatically by `grant_quest_reward()`
- Sets the appropriate bit in the completion bitfield
- Only affects PC characters (NPCs are ignored)

#### `is_quest_completed(struct char_data *ch, int quest_num)`
Checks if a quest has been completed and rewarded.
- Returns 1 if quest has been completed, 0 otherwise
- Used by quest_giver before offering quests
- Used before granting rewards to prevent duplicates

#### `grant_quest_reward(struct char_data *ch, struct quest_data *quest)`
Grants quest rewards to the player.
- Awards experience, gold, and items
- Calls `set_quest_completed()` to mark the quest as done
- Only called once per quest per player

### Quest Flow

#### Normal Quest Flow
1. Player asks NPC for quest
2. System checks `is_quest_completed()` - if true, NPC says: "You have already completed this task and received your reward."
3. If not completed, quest is assigned
4. Player completes objective
5. Player returns to NPC
6. `grant_quest_reward()` gives rewards
7. `set_quest_completed()` marks quest as done

#### Second Completion Attempt
1. Player completes quest objective again
2. Player talks to NPC
3. System detects quest is marked complete in objectives
4. System checks `is_quest_completed()` - returns true
5. NPC says: "I see you've already received the reward. Thank you for performing my task again!"
6. No rewards are given
7. Quest affect is removed

#### Quest Acceptance After Completion
1. Player who previously completed quest asks NPC for quest
2. System checks `is_quest_completed()` before offering
3. NPC says: "You have already completed this task and received your reward. I have no other tasks for you at this time."
4. Quest is not assigned

### Data Persistence

Quest completion data persists across logins:

**Saving (char_to_store in db.c):**
```c
st->quests_completed_low = ch->player.quests_completed_low;
st->quests_completed_high = ch->player.quests_completed_high;
```

**Loading (store_to_char in db.c):**
```c
ch->player.quests_completed_low = st->quests_completed_low;
ch->player.quests_completed_high = st->quests_completed_high;
```

### Quest Types Supported

All quest types respect completion tracking:
- **QUEST_DELIVERY** (type 61): Deliver item to NPC
- **QUEST_RETRIEVAL** (type 62): Retrieve item and return
- **QUEST_KILL** (type 63): Kill specific mob
- **QUEST_EXPLORE** (type 64): Visit specific location

## Benefits

1. **Prevents Reward Farming**: Players can't repeatedly complete the same quest for unlimited rewards
2. **Maintains Game Balance**: XP, gold, and items are limited per quest
3. **Provides Closure**: Clear feedback when quest has been completed
4. **Encourages Exploration**: Players must find new quests for advancement
5. **Persistent Tracking**: Completion status survives logout/login

## Testing

Integration tests validate:
- Single quest completion and reward granting
- Repeated quest attempts are blocked
- Appropriate messages for completed quests
- Data persistence across sessions
- No regression in existing quest functionality

Test files:
- `test_quest_repeat_completion.yaml`
- `test_quest_double_completion_message.yaml`
- `test_quest_persistence.yaml`

## Limitations and Considerations

1. **Quest Number Range**: Quest numbers should be kept below 10000 to avoid bit position conflicts
2. **Maximum Quests**: System supports up to 128 unique quest completions per player
3. **Bit Position Collision**: Quest numbers that differ by 128 will map to the same bit (e.g., 3001 and 3129)
4. **No Time-Based Reset**: Once completed, quests remain marked forever (no daily/weekly resets)

## Future Enhancements

Potential improvements:
1. Add time-based quest reset functionality
2. Implement quest completion counter (how many times completed)
3. Add quest achievement tracking (speed runs, no-death completions)
4. Support for repeatable quests with reduced rewards
5. Quest completion history/log for players

## Modified Files

### Core Implementation
- `dm-dist-alfa/structs.h`: Added quest completion bitfields to data structures
- `dm-dist-alfa/quest.h`: Added function prototypes
- `dm-dist-alfa/quest.c`: Implemented helper functions and updated reward granting
- `dm-dist-alfa/db.c`: Updated save/load functions
- `dm-dist-alfa/spec_procs.c`: Updated quest_giver to check completion status

### Tests
- `tests/integration/quests/test_quest_repeat_completion.yaml`
- `tests/integration/quests/test_quest_double_completion_message.yaml`
- `tests/integration/quests/test_quest_persistence.yaml`

## Example Usage

A player completes Sola's White Ape quest:

```
> ask sola quest
Sola speaks: "White apes have been threatening our people..."
[Quest assigned]

> [Player gets white ape tooth]

> give tooth sola
Sola's eyes light up with relief and gratitude...
You gain 500 experience!
You receive Tars Tarkas's Practice Sword!
[Quest marked as completed]

> ask sola quest
Sola says, 'You have already completed this task and received your reward.'
[Quest not offered again]
```

## Backward Compatibility

The implementation is backward compatible:
- Existing player files work (new fields initialize to 0)
- All existing quests continue to function
- No changes to quest data files required
- Clear_char() automatically initializes fields to 0 for new players
