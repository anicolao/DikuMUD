# Combat Status in Prompt Implementation

## Overview

This document describes the implementation of combat status display in the player prompt. When any member of a player's group is in combat, all group members see the health status of the front-line combatant and their opponent.

## Problem Statement

When combat is in progress between any character in a player's group and a mob, add `[PLAYER:<hits>]` and `[MOB:<hits>]` to all participating group member's prompt.

## Health Status Scale

The implementation uses the following health status scale based on HP percentage:

- **mostly dead** - Character at 0HP or below and dying (POSITION_DEAD, POSITION_MORTALLYW, POSITION_INCAP, or HP < 0%)
- **stunned** - Character is stunned (POSITION_STUNNED)
- **awful** - HP < 10%
- **pretty hurt** - HP < 50%
- **hurt** - HP < 85%
- **just a scratch** - HP < 95%
- **perfect** - HP >= 95%

## Implementation Details

### Files Modified

- **`dm-dist-alfa/comm.c`** - Modified `make_prompt()` function and added `get_health_status()` helper

### Key Functions

#### `get_health_status(struct char_data *ch)`

Helper function that calculates and returns the health status string for a character based on their current HP, maximum HP, and position.

```c
const char* get_health_status(struct char_data *ch)
```

**Returns:** A string describing the character's health status (e.g., "perfect", "hurt", "awful", etc.)

#### `make_prompt(struct descriptor_data *d, char *prompt_buf, int buf_size)`

Modified to check if the player or any group member is in combat. If so, displays combat status at the end of the prompt, after the exits.

**Behavior:**
1. If player is in a group (AFF_GROUP flag set):
   - Find the group leader (ch->master or ch itself)
   - Iterate through the global combat_list
   - Check if any fighter in combat_list is the group leader or a group follower
   - If found, extract the player fighter and their opponent
   - Display combat status for all group members

2. If player is not in a group but is fighting:
   - Display combat status showing the player and their opponent

**Prompt Format:**
- Without combat: `%dH %dF %dV %dC Exits:%s> `
- With combat: `%dH %dF %dV %dC Exits:%s [name:status] [name:status]> `

The names shown are:
- For players: their character name (via GET_NAME)
- For NPCs/mobs: their short description

Example prompts:
```
100H 50F 82V 100C Exits:NESW>
100H 50F 82V 100C Exits:NESW [Warrior:perfect] [goblin:hurt]>
45H 30F 60V 100C Exits:N [Warrior:pretty hurt] [troll:just a scratch]>
```

## Technical Design Choices

### Group Detection

The implementation checks for group membership using the `AFF_GROUP` flag. This flag is set on characters who are actively part of a group via the `group` command.

### Combat List Traversal

The code uses the global `combat_list` linked list (defined in `fight.c`) which contains all characters currently in combat. Each character in this list has a `next_fighting` pointer to the next combatant.

### Group Member Matching

For each character in combat:
1. Check if they are the group leader (with AFF_GROUP flag)
2. Check if they are a follower of the group leader (iterate through leader->followers)
3. Verify each follower has the AFF_GROUP flag set

### Safety Checks

- Null pointer checks for character data
- Check for valid opponent (ch->specials.fighting)
- Check MAX_HIT > 0 before calculating percentage
- Use snprintf with buffer size limits to prevent overflow

## Testing

### Manual Testing Steps

1. **Build the server:**
   ```bash
   cd dm-dist-alfa
   make dmserver
   ```

2. **Start the server:**
   ```bash
   ./dmserver
   ```

3. **Connect with two clients** (using telnet or MUD client)

4. **Create/login with two characters**

5. **Form a group:**
   - Character A: `group B` (where B is the other character's name)
   - Character B: `follow A`
   - Character A: `group B` (to add B to the group)

6. **Verify group status:**
   - Both characters: `group` (should show group members)

7. **Initiate combat:**
   - Character A: `kill <mob>` (attack a mob)
   - Observe both A and B's prompts showing `[PLAYER:...] [MOB:...]`

8. **Test health status changes:**
   - As combat progresses, watch the status strings change
   - Test with different damage levels to see various status messages

9. **Test non-grouped combat:**
   - Have Character B leave the group
   - Character B: `kill <mob>`
   - Verify B sees combat status but A does not

### Expected Behavior

- ✓ When any group member enters combat, all group members see combat status
- ✓ Combat status updates with each prompt (typically every command)
- ✓ Health status reflects accurate HP percentage
- ✓ Non-grouped players in combat see their own combat status
- ✓ Players not in combat and not in a group with combat see no combat status

## Code Style Notes

This implementation follows the DikuMUD historical coding style:
- 1990s C conventions
- Tab-based indentation
- K&R-style bracing
- Minimal comments (as per original codebase style)
- Use of global variables (combat_list)
- Buffer safety using snprintf (modern addition for security)

## Future Enhancements

Potential improvements that could be made:

1. **Multiple combatants** - Show status for all group members in combat, not just the first
2. **Color coding** - Add ANSI color codes for different health levels (if terminal supports it)
3. **Position indicators** - Show who is tanking vs assisting
4. **Damage per round** - Track and display damage dealt/received
5. **Combat timer** - Show how long combat has been active

## Compatibility

This implementation:
- Does not modify any data structures
- Does not change network protocol
- Does not affect saved player data
- Is backward compatible with existing worlds
- Works with existing group and combat mechanics

## References

- Original prompt code: `comm.c` lines 253-293
- Combat system: `fight.c`
- Group system: `act.other.c` (do_group function)
- Health display reference: `act.informative.c` (look_at_char function)
