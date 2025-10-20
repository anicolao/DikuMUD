# FLUX_CAPACITY Design Document

## Overview

FLUX_CAPACITY (referred to as "mana" in the code but displayed as "flux" to players) represents the energy charge available to power technological devices and abilities in the Barsoom MUD. This document describes how flux costs are calculated, regeneration mechanics, factors affecting regeneration rate, and flux capacity at various character levels.

## Flux Capacity by Level

### Maximum Flux Capacity

All player characters (PCs) have a **fixed maximum flux capacity of 100 points**, regardless of level or class. This is defined in the `mana_limit()` function in `limits.c`:

```c
int mana_limit(struct char_data *ch)
{
    int max;
    
    if (!IS_NPC(ch))
        max = (100); /* Fixed at 100 for all PCs */
    else 
        max = 100;
    
    return(max);
}
```

**Key Point**: Unlike hit points, which scale with level, flux capacity remains constant at 100 for all player characters. This creates a resource management dynamic where higher-level spellcasters must carefully balance using more powerful (and expensive) abilities.

### NPCs (Non-Player Characters)

NPCs also have a flux capacity of 100 by default, though individual NPCs may have different values assigned in their mob definitions.

## Spell Cost Calculation

### Base Cost Formula

Spell costs are calculated using the `USE_MANA` macro defined in `spell_parser.c`:

```c
#define USE_MANA(ch, sn) \
    MAX(spell_info[sn].min_usesmana, 100/(2+GET_LEVEL(ch)-SPELL_LEVEL(ch,sn)))
```

This formula ensures that:
1. The cost never falls below the spell's minimum flux requirement
2. The cost decreases as the character's level exceeds the minimum level required for the spell

### Formula Breakdown

**Parameters**:
- `spell_info[sn].min_usesmana`: The minimum flux cost for spell number `sn`
- `GET_LEVEL(ch)`: The character's current level
- `SPELL_LEVEL(ch, sn)`: The minimum level required to cast the spell (varies by class)

**Calculation**:
```
Dynamic Cost = 100 / (2 + Character_Level - Min_Spell_Level)
Actual Cost = MAX(Min_Cost, Dynamic Cost)
```

### Examples

#### Example 1: Low-level spell at minimum level
- **Spell**: Personal Shield (Armor) - min cost: 5
- **Character**: Level 5 Scientist (min level for this spell: 5)
- **Calculation**: 
  - Dynamic: 100 / (2 + 5 - 5) = 100 / 2 = 50
  - Actual: MAX(5, 50) = **50 flux**

#### Example 2: Same spell at higher level
- **Spell**: Personal Shield (Armor) - min cost: 5
- **Character**: Level 10 Scientist (min level: 5)
- **Calculation**:
  - Dynamic: 100 / (2 + 10 - 5) = 100 / 7 = 14.2
  - Actual: MAX(5, 14) = **14 flux**

#### Example 3: High-cost spell at minimum level
- **Spell**: Clone Vat - min cost: 40
- **Character**: Level 15 Scientist (min level: 15)
- **Calculation**:
  - Dynamic: 100 / (2 + 15 - 15) = 100 / 2 = 50
  - Actual: MAX(40, 50) = **50 flux**

#### Example 4: High-level spell well above minimum
- **Spell**: Clone Vat - min cost: 40
- **Character**: Level 20 Scientist (min level: 15)
- **Calculation**:
  - Dynamic: 100 / (2 + 20 - 15) = 100 / 7 = 14.2
  - Actual: MAX(40, 14) = **40 flux** (minimum enforced)

### Spell Cost Table

Common spell minimum costs defined in the codebase:

| Spell Name | Min Cost | Notes |
|------------|----------|-------|
| Personal Shield (Armor) | 5 | Basic defensive technology |
| First Aid Injector | 15 | Basic healing |
| Critical Trauma Kit | 20 | Advanced healing |
| Strength Amplifier | 20 | Buff technology |
| Toxin Injector | 10 | Debuff |
| Clone Vat | 40 | Very expensive |
| Matter Transmitter | 35 | Teleportation |
| Vitality Drain | 35 | High-damage attack |
| Regeneration Chamber (Heal) | 50 | Most expensive healing |
| Sanctuary Field | 75 | Very expensive protection |
| Weapon Enhancer | 100 | Extremely expensive enhancement |

### Failed Spell Attempts

When a spell activation fails (due to failed skill check), the character still expends flux, but only **half the normal cost**:

```c
if (number(1,101) > ch->skills[spl].learned) {
    send_to_char("The device malfunctions!\n\r", ch);
    GET_MANA(ch) -= (USE_MANA(ch, spl)>>1); // Right shift by 1 = divide by 2
    return;
}
```

## Flux Regeneration

### Base Regeneration Rate

Flux regenerates over time based on the character's age, class, position, and condition. The regeneration occurs every MUD hour (75 real seconds).

The base regeneration is calculated in the `mana_gain()` function in `limits.c`:

```c
int mana_gain(struct char_data *ch)
{
    int gain;
    
    if(IS_NPC(ch)) {
        gain = GET_LEVEL(ch);  // NPCs regenerate flux = their level per MUD hour
    } else {
        gain = graf(age(ch).year, 2,4,6,8,6,5,8);
        // Returns flux gain based on age brackets
    }
    // ... additional modifiers applied below
    return (gain);
}
```

### Age-Based Regeneration

The `graf()` function determines base regeneration based on character age using the parameters: `graf(age, 2, 4, 6, 8, 6, 5, 8)`:

| Age Range | Base Flux Gain per MUD Hour |
|-----------|---------------------------|
| < 15 years | 2 |
| 15-29 years | 4-6 (linear interpolation from 4 at age 15 to 6 at age 29) |
| 30-44 years | 6-8 (linear interpolation from 6 at age 30 to 8 at age 44) |
| 45-59 years | 8-6 (linear decline from 8 at age 45 to 6 at age 59) |
| 60-79 years | 6-5 (linear decline from 6 at age 60 to 5 at age 79) |
| ≥ 80 years | 8 |

**Note**: Most player characters fall in the 15-29 age range at character creation. At age 15 they gain 4 flux/hour base, increasing linearly to 6 flux/hour at age 29. A 20-year-old character (common starting age) would gain approximately 4.7 flux per MUD hour base.

### Class Modifiers

**Magic Users (Scientists) and Clerics (Nobles)** regenerate flux **twice as fast** as other classes:

```c
if ((GET_CLASS(ch) == CLASS_MAGIC_USER) || (GET_CLASS(ch) == CLASS_CLERIC))
    gain += gain;  // Doubles the base gain
```

**Effective regeneration by class** (assuming age 20, base gain of 4):
- **Scientist/Noble**: 8 flux per MUD hour (before position modifiers)
- **Warrior/Assassin**: 4 flux per MUD hour (before position modifiers)

### Position Modifiers

Character position significantly affects flux regeneration:

```c
switch (GET_POS(ch)) {
    case POSITION_SLEEPING:
        gain += gain;          // +100% (double the current gain)
        break;
    case POSITION_RESTING:
        gain += (gain>>1);     // +50% (add half the current gain)
        break;
    case POSITION_SITTING:
        gain += (gain>>2);     // +25% (add quarter of current gain)
        break;
}
```

**Position multipliers**:
- **Sleeping**: 2x base regeneration
- **Resting**: 1.5x base regeneration
- **Sitting**: 1.25x base regeneration
- **Standing/Fighting**: 1x base regeneration

### Condition Penalties

#### Poison

Being poisoned reduces flux regeneration to **25%** (divides by 4):

```c
if (IS_AFFECTED(ch,AFF_POISON))
    gain >>= 2;  // Right shift by 2 = divide by 4
```

#### Hunger and Thirst

Being hungry or thirsty also reduces flux regeneration to **25%**:

```c
if((GET_COND(ch,FULL)==0)||(GET_COND(ch,THIRST)==0))
    gain >>= 2;  // Divide by 4
```

**Important**: These penalties stack multiplicatively. If both poisoned AND hungry/thirsty, regeneration is reduced to approximately 6.25% of base.

## Comprehensive Regeneration Examples

### Example 1: Optimal Conditions (Scientist)
- **Character**: Level 10 Scientist, Age 20
- **Position**: Sleeping
- **Condition**: Well-fed, hydrated, not poisoned

**Calculation**:
1. Base gain (age 20): 4 flux/hour
2. Class bonus (Scientist): 4 + 4 = 8 flux/hour
3. Sleeping bonus: 8 + 8 = 16 flux/hour
4. **Total: 16 flux per MUD hour**

**Time to full regeneration** (from 0 to 100): ~6.25 MUD hours (~7.8 real minutes)

### Example 2: Active Combat (Warrior)
- **Character**: Level 10 Warrior, Age 20
- **Position**: Fighting
- **Condition**: Well-fed, hydrated, not poisoned

**Calculation**:
1. Base gain (age 20): 4 flux/hour
2. Class bonus (Warrior): None (stays at 4)
3. Position bonus: None (fighting)
4. **Total: 4 flux per MUD hour**

**Time to full regeneration**: ~25 MUD hours (~31.25 real minutes)

### Example 3: Resting Noble
- **Character**: Level 10 Noble, Age 20
- **Position**: Resting
- **Condition**: Well-fed, hydrated, not poisoned

**Calculation**:
1. Base gain (age 20): 4 flux/hour
2. Class bonus (Noble): 4 + 4 = 8 flux/hour
3. Resting bonus: 8 + (8/2) = 12 flux/hour
4. **Total: 12 flux per MUD hour**

**Time to full regeneration**: ~8.3 MUD hours (~10.4 real minutes)

### Example 4: Poisoned Scientist
- **Character**: Level 10 Scientist, Age 20
- **Position**: Resting
- **Condition**: Poisoned, well-fed, hydrated

**Calculation**:
1. Base gain (age 20): 4 flux/hour
2. Class bonus (Scientist): 4 + 4 = 8 flux/hour
3. Resting bonus: 8 + (8/2) = 12 flux/hour
4. Poison penalty: 12 / 4 = 3 flux/hour
5. **Total: 3 flux per MUD hour**

**Time to full regeneration**: ~33.3 MUD hours (~41.6 real minutes)

### Example 5: Hungry and Thirsty Assassin
- **Character**: Level 10 Assassin, Age 20
- **Position**: Sitting
- **Condition**: Hungry and thirsty (not poisoned)

**Calculation**:
1. Base gain (age 20): 4 flux/hour
2. Class bonus (Assassin): None (stays at 4)
3. Sitting bonus: 4 + (4/4) = 5 flux/hour
4. Hunger/Thirst penalty: 5 / 4 = 1.25 flux/hour (rounded down to 1)
5. **Total: 1 flux per MUD hour**

**Time to full regeneration**: ~100 MUD hours (~125 real minutes or ~2 hours)

**Note**: Characters should maintain food and water supplies to ensure adequate flux regeneration.

## Time Conversions

Understanding MUD time is crucial for flux management:

- **1 MUD hour** = 75 real seconds (1.25 real minutes)
- **1 MUD day** = 24 MUD hours = 1800 real seconds (30 real minutes)
- **Flux regeneration** occurs once per MUD hour (every 75 real seconds)

## Strategic Implications

### For Spellcasters (Scientists and Nobles)

1. **Flux Management**: With only 100 flux total, casting expensive spells (40-100 flux) can deplete reserves quickly
2. **Recovery Time**: Even with optimal regeneration (16 flux/hour while sleeping), full recovery takes ~6.25 MUD hours (~7.8 real minutes)
3. **Combat Efficiency**: In combat (no position bonus), regeneration is slow (8 flux/hour for Scientists/Nobles)
4. **Rest Between Encounters**: Plan to rest after major spell expenditures

### For Non-Spellcasters (Warriors and Assassins)

1. **Limited Flux**: Cannot normally cast spells until level 21 (deity level)
2. **Slow Regeneration**: Only 4 flux/hour base when standing (for age 20)
3. **Magic Item Dependency**: Must rely on scrolls, wands, potions for magical effects
4. **No Flux Management**: Generally not a concern for class mechanics

### For All Characters

1. **Maintain Supplies**: Keep food and water to avoid regeneration penalties
2. **Cure Poison Quickly**: Poison severely impacts flux recovery
3. **Position Matters**: Rest or sleep when recovering flux
4. **Plan Spell Usage**: Expensive spells should be reserved for critical moments

## Code References

All flux/mana mechanics are implemented in the following files:

- **`dm-dist-alfa/limits.c`**: Contains `mana_gain()` and `mana_limit()` functions
- **`dm-dist-alfa/spell_parser.c`**: Contains spell cost calculation (`USE_MANA` macro) and spell definitions
- **`dm-dist-alfa/structs.h`**: Defines character point structure including mana field
- **`dm-dist-alfa/utils.h`**: Defines `GET_MANA()` and `GET_MAX_MANA()` macros
- **`dm-dist-alfa/act.informative.c`**: Displays flux in score command

## Design Philosophy

The flux system is designed to:

1. **Create Resource Management**: Fixed 100 capacity forces careful spell selection
2. **Reward Planning**: Resting and position management optimize recovery
3. **Differentiate Classes**: Scientists/Nobles recover faster, encouraging their spellcasting role
4. **Encourage Exploration**: Players must manage flux across multiple encounters
5. **Add Tactical Depth**: Choosing when to cast expensive vs. cheap spells matters
6. **Promote Party Play**: Non-spellcasters complement spellcasters' limitations

The constant flux capacity (not scaling with level) is a deliberate design choice that keeps resource management relevant throughout character progression. Higher-level spellcasters get access to more powerful spells but must still carefully manage the same 100-point pool.

## Future Considerations

Potential enhancements to the flux system might include:

1. **Equipment Bonuses**: Items that increase maximum flux capacity
2. **Flux Potions**: Consumables that restore flux immediately
3. **Flux Wells**: Special locations with enhanced regeneration
4. **Class Variations**: Different flux capacities for different classes
5. **Flux Draining**: Enemy abilities that drain flux
6. **Flux Shields**: Defensive abilities that use flux to absorb damage

However, any changes should preserve the core resource management gameplay that defines the current system.
