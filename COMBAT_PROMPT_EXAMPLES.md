# Combat Prompt Examples

This document provides visual examples of how the combat prompt appears in different scenarios.

## Prompt Format

The combat status is displayed as `[PLAYER:<status>] [MOB:<status>]` before the normal prompt information.

### Normal Prompt (No Combat)
```
100H 50F 82V 100C Exits:NESW>
```

### Combat Prompt Examples

#### Perfect Health vs Hurt Mob
```
[PLAYER:perfect] [MOB:hurt] 100H 50F 82V 100C Exits:NESW>
```

#### Taking Damage - Just a Scratch
```
[PLAYER:just a scratch] [MOB:hurt] 93H 45F 75V 100C Exits:N>
```

#### Getting Hurt
```
[PLAYER:hurt] [MOB:pretty hurt] 70H 30F 60V 100C Exits:N>
```

#### Pretty Hurt vs Nearly Dead Mob
```
[PLAYER:pretty hurt] [MOB:awful] 45H 20F 50V 100C Exits:NE>
```

#### Critical Condition
```
[PLAYER:awful] [MOB:just a scratch] 8H 10F 30V 100C Exits:S>
```

#### Stunned
```
[PLAYER:stunned] [MOB:hurt] -2H 5F 20V 100C Exits:None>
```

#### Mostly Dead (Mortally Wounded)
```
[PLAYER:mostly dead] [MOB:perfect] -8H 0F 10V 100C Exits:None>
```

## Health Status Thresholds

| Status | HP Range | Notes |
|--------|----------|-------|
| **perfect** | 95-100% | Excellent condition |
| **just a scratch** | 85-94% | Minor injuries |
| **hurt** | 50-84% | Significant damage |
| **pretty hurt** | 10-49% | Badly wounded |
| **awful** | 1-9% | Near death |
| **stunned** | ≤0 HP, POSITION_STUNNED | Unconscious but alive |
| **mostly dead** | ≤0 HP, dying positions | Mortally wounded or incapacitated |

## Group Combat Scenarios

### Scenario 1: Two-Person Group, One Fighting

**Player A (fighting):**
```
[PLAYER:hurt] [MOB:pretty hurt] 70H 30F 60V 50C Exits:NESW>
```

**Player B (in group, not fighting):**
```
[PLAYER:hurt] [MOB:pretty hurt] 100H 50F 82V 100C Exits:NESW>
```

Both players see the same combat status showing Player A's health and their opponent's health.

### Scenario 2: Three-Person Group, One Fighting

**Player A (group leader, not fighting):**
```
[PLAYER:perfect] [MOB:hurt] 100H 50F 82V 100C Exits:NESW>
```

**Player B (follower, fighting):**
```
[PLAYER:perfect] [MOB:hurt] 100H 45F 75V 75C Exits:NE>
```

**Player C (follower, not fighting):**
```
[PLAYER:perfect] [MOB:hurt] 98H 48F 80V 120C Exits:NESW>
```

All three see Player B's combat status (the first group member found fighting).

### Scenario 3: Solo Combat (Not in Group)

**Player (fighting alone):**
```
[PLAYER:hurt] [MOB:pretty hurt] 70H 30F 60V 50C Exits:N>
```

When not in a group, the player only sees their own combat status.

## Position-Based Status Messages

The system also considers character position when determining status:

- **POSITION_DEAD**: Shows "dead"
- **POSITION_MORTALLYW**: Shows "mostly dead"
- **POSITION_INCAP**: Shows "mostly dead"
- **POSITION_STUNNED**: Shows "stunned"

These override the HP percentage calculation, ensuring accurate status display even when HP drops below zero.

## Implementation Notes

- Combat status appears immediately when combat starts
- Updates with every prompt (typically after each command)
- Shows status for the first group member found fighting
- Automatically disappears when combat ends
- Works for both player groups and solo combat
- Safe buffer handling prevents overflow

## Testing Checklist

When testing this feature, verify:

- [ ] Solo combat shows combat status
- [ ] Group leader in combat shows status to all members
- [ ] Group follower in combat shows status to all members
- [ ] Multiple group members - shows first fighter's status
- [ ] Status updates as HP changes during combat
- [ ] Status disappears when combat ends
- [ ] Status shows correct thresholds (perfect, hurt, awful, etc.)
- [ ] Stunned and dying positions display correctly
- [ ] Non-grouped players don't see other's combat status
- [ ] Combat status appears before normal prompt info

## Related Files

- **Implementation**: `dm-dist-alfa/comm.c`
- **Documentation**: `COMBAT_PROMPT_IMPLEMENTATION.md`
- **Test Script**: `test_combat_prompt.sh`
