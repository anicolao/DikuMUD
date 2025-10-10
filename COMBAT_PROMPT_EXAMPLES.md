# Combat Prompt Examples

This document provides visual examples of how the combat prompt appears in different scenarios.

## Prompt Format

The combat status is displayed as `[name:status] [name:status]` at the end of the prompt, after the exits.

### Normal Prompt (No Combat)
```
100H 50F 82V 100C Exits:NESW>
```

### Combat Prompt Examples

#### Perfect Health vs Hurt Mob
```
100H 50F 82V 100C Exits:NESW [Warrior:perfect] [goblin:hurt]>
```

#### Taking Damage - Just a Scratch
```
93H 45F 75V 100C Exits:N [Warrior:just a scratch] [goblin:hurt]>
```

#### Getting Hurt
```
70H 30F 60V 100C Exits:N [Warrior:hurt] [goblin:pretty hurt]>
```

#### Pretty Hurt vs Nearly Dead Mob
```
45H 20F 50V 100C Exits:NE [Warrior:pretty hurt] [troll:awful]>
```

#### Critical Condition
```
8H 10F 30V 100C Exits:S [Warrior:awful] [dragon:just a scratch]>
```

#### Stunned
```
-2H 5F 20V 100C Exits:None [Warrior:stunned] [orc:hurt]>
```

#### Mostly Dead (Mortally Wounded)
```
-8H 0F 10V 100C Exits:None [Warrior:mostly dead] [giant:perfect]>
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

### Scenario 1: Two-Person Group, Alice Tanking

**Alice (fighting, being hit by troll):**
```
70H 30F 60V 50C Exits:NESW [Alice:hurt] [troll:pretty hurt]>
```

**Bob (in group, assisting but not being targeted):**
```
100H 50F 82V 100C Exits:NESW [Alice:hurt] [troll:pretty hurt]>
```

Both players see Alice's status because the troll is attacking Alice. Bob can assist but knows Alice is the one taking damage.

### Scenario 2: Three-Person Group, Bob Tanking

**Alice (group leader, assisting):**
```
100H 50F 82V 100C Exits:NESW [Bob:perfect] [goblin:hurt]>
```

**Bob (follower, tanking - being hit by goblin):**
```
100H 45F 75V 75C Exits:NE [Bob:perfect] [goblin:hurt]>
```

**Carol (follower, assisting):**
```
98H 48F 80V 120C Exits:NESW [Bob:perfect] [goblin:hurt]>
```

All three see Bob's combat status because the goblin is attacking Bob. Alice and Carol can assist safely while Bob takes the hits.

### Scenario 3: Solo Combat (Not in Group)

**Player (fighting alone):**
```
70H 30F 60V 50C Exits:N [Warrior:hurt] [orc:pretty hurt]>
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
