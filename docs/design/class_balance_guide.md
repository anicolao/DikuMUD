# DikuMUD Class Balance Guide

## Purpose

This document provides comprehensive statistical reference data for all four character classes in DikuMUD. Use these charts when designing monsters and encounters to ensure proper balance between challenge and character capabilities.

## Table of Contents

1. [Hit Points by Level](#hit-points-by-level)
2. [Armor Class Expectations](#armor-class-expectations)
3. [Weapon Damage by Level](#weapon-damage-by-level)
4. [Combat Statistics (THAC0)](#combat-statistics-thac0)
5. [Attribute Modifiers](#attribute-modifiers)
6. [Class-Specific Considerations](#class-specific-considerations)

---

## Hit Points by Level

Hit points are gained at each level based on class and Constitution modifier. The formulas are:

### HP Gain per Level (excluding CON bonus)

| Class | HP Dice Roll | Average HP/Level | HP Range/Level |
|-------|--------------|------------------|----------------|
| Magic User | 3-8 | 5.5 | 3-8 |
| Cleric | 5-10 | 7.5 | 5-10 |
| Thief | 7-13 | 10 | 7-13 |
| Warrior | 10-15 | 12.5 | 10-15 |

**Note**: Constitution bonus/penalty is added to each roll (see [Constitution Modifier](#constitution-modifier))

### Expected Total Hit Points by Level

These values assume average dice rolls plus a Constitution of 14 (+0 HP modifier). For characters with different Constitution scores, adjust by the CON modifier multiplied by level.

| Level | Magic User | Cleric | Thief | Warrior |
|-------|------------|--------|-------|---------|
| 1 | 8 | 8 | 8 | 8 |
| 2 | 14 | 16 | 18 | 21 |
| 3 | 20 | 24 | 28 | 34 |
| 4 | 26 | 32 | 38 | 47 |
| 5 | 32 | 40 | 48 | 60 |
| 6 | 37 | 47 | 58 | 72 |
| 7 | 43 | 55 | 68 | 85 |
| 8 | 49 | 63 | 78 | 98 |
| 9 | 55 | 71 | 88 | 111 |
| 10 | 61 | 79 | 98 | 123 |
| 11 | 66 | 86 | 108 | 136 |
| 12 | 72 | 94 | 118 | 149 |
| 13 | 78 | 102 | 128 | 162 |
| 14 | 84 | 110 | 138 | 174 |
| 15 | 90 | 118 | 148 | 187 |
| 16 | 95 | 125 | 158 | 200 |
| 17 | 101 | 133 | 168 | 212 |
| 18 | 107 | 141 | 178 | 225 |
| 19 | 113 | 149 | 188 | 238 |
| 20 | 119 | 157 | 198 | 251 |

**Important Notes:**
- Level 1 starts with 8 HP base for all classes
- Each subsequent level adds: base roll + CON modifier
- Age also provides a small HP modifier (2-17 HP bonus depending on age)
- Maximum HP = base HP + age modifier

### Constitution Modifier

Constitution affects hit points gained per level:

| CON Score | HP Modifier | Resurrection Chance |
|-----------|-------------|---------------------|
| 3 | -4 | 20% |
| 4 | -2 | 25% |
| 5-6 | -1 | 30-45% |
| 7-14 | 0 | 50-85% |
| 15 | +1 | 90% |
| 16 | +2 | 95% |
| 17 | +2 | 97% |
| 18 | +3 | 99% |
| 19-20 | +3 | 99% |
| 21-23 | +4-5 | 99% |
| 24-25 | +6-7 | 100% |

---

## Armor Class Expectations

Armor Class (AC) in DikuMUD uses the traditional D&D system where **lower is better**. Base AC without armor is 100 (displayed as 10). The theoretical range is -100 to 100 (displayed as -10 to 10).

### AC Calculation

```
Displayed AC = Internal AC / 10
Internal AC = 100 - (armor bonuses) + (magic bonuses) - (dexterity bonus)
```

### Expected AC by Level

These values represent what a character should have with appropriate equipment for their level:

| Level | Expected AC | Equipment Type | AC Display |
|-------|-------------|----------------|------------|
| 1-3 | 80-90 | Leather, minimal protection | 8-9 |
| 4-6 | 60-70 | Mixed leather/chain, some magic | 6-7 |
| 7-9 | 40-50 | Chain mail, +1 magic items | 4-5 |
| 10-13 | 20-30 | Plate mail, several magic items | 2-3 |
| 14-17 | 0-10 | Full plate, many magic items | 0-1 |
| 18-20 | -10-0 | Exceptional plate, powerful magic | -1-0 |

**Best Achievable AC**: Approximately -100 (display: -10) with exceptional armor, shield, and magic items

### Dexterity AC Bonus

Dexterity provides an AC bonus when the character is awake and actively defending:

| DEX Score | AC Modifier |
|-----------|-------------|
| 3 | +4 (worse) |
| 4 | +3 |
| 5 | +2 |
| 6 | +1 |
| 7-14 | 0 |
| 15 | -1 (better) |
| 16 | -2 |
| 17 | -3 |
| 18 | -4 |
| 19+ | -4 to -5 |

---

## Weapon Damage by Level

### Base Damage Calculation

Weapon damage formula:
```
Damage = Weapon Dice + Strength Modifier + Damage Roll Bonus + Magic Bonuses
```

### Typical Weapon Damage Dice

| Weapon Type | Dice | Average | Range |
|-------------|------|---------|-------|
| Unarmed/Fist | 1d2 | 1.5 | 0-2 |
| Dagger | 1d4 | 2.5 | 1-4 |
| Short Sword | 1d6 | 3.5 | 1-6 |
| Long Sword | 1d8 | 4.5 | 1-8 |
| Bastard Sword | 1d10 | 5.5 | 1-10 |
| Two-Handed Sword | 2d6 | 7 | 2-12 |
| Club/Mace | 1d6 | 3.5 | 1-6 |
| Morning Star | 2d4 | 5 | 2-8 |
| Flail | 2d5 | 6 | 2-10 |
| War Hammer | 2d4 | 5 | 2-8 |
| Staff | 1d6 | 3.5 | 1-6 |
| Spear | 1d8 | 4.5 | 1-8 |

### Expected Damage Output by Level

Average damage per hit including typical Strength (16, +1 damage) and equipment bonuses:

| Level | Magic User | Cleric | Thief | Warrior |
|-------|------------|--------|-------|---------|
| 1-3 | 3-4 | 4-5 | 4-5 | 5-7 |
| 4-6 | 4-6 | 5-7 | 6-8 | 8-11 |
| 7-9 | 5-7 | 6-9 | 7-10 | 10-14 |
| 10-13 | 6-9 | 8-11 | 9-13 | 12-17 |
| 14-17 | 7-11 | 9-13 | 11-16 | 14-20 |
| 18-20 | 8-13 | 10-15 | 13-19 | 16-24 |

**Notes:**
- Magic Users typically use daggers or staves (limited weapon selection)
- Clerics cannot use edged weapons (limited to blunt weapons)
- Thieves have access to most weapons but excel with daggers (backstab)
- Warriors have access to all weapons and highest damage potential

### Strength Damage Modifier

| STR Score | Damage Modifier |
|-----------|-----------------|
| 3 | -4 |
| 4-5 | -2 to -1 |
| 6-7 | -1 to 0 |
| 8-15 | 0 |
| 16 | +1 |
| 17 | +1 |
| 18 | +2 |
| 18/01-50 | +3 |
| 18/51-90 | +3-4 |
| 18/91-00 | +5-6 |
| 19-25 | +7-14 |

### Backstab Damage (Thieves Only)

When a thief successfully backstabs, damage is multiplied:

| Level | Backstab Multiplier |
|-------|---------------------|
| 1-4 | x2 |
| 5-8 | x3 |
| 9-13 | x4 |
| 14+ | x5 |

**Backstab Damage Formula**: `(Base Damage + Modifiers) × Multiplier`

**Example**: Level 10 thief with short sword (1d6) and 16 STR:
- Normal hit: 1d6 + 1 (STR) = 2-7 damage (avg 4.5)
- Backstab: (1d6 + 1) × 4 = 8-28 damage (avg 18)

---

## Combat Statistics (THAC0)

THAC0 (To Hit Armor Class 0) determines hit chance. **Lower THAC0 is better**.

### THAC0 by Class and Level

| Level | Magic User | Cleric | Thief | Warrior |
|-------|------------|--------|-------|---------|
| 1-3 | 20 | 20 | 20/20/19 | 20/19/18 |
| 4-6 | 19 | 18 | 19/18/18 | 17/16/15 |
| 7-9 | 19 | 18 | 17/17/16 | 14/13/12 |
| 10-12 | 18 | 16 | 16/15/15 | 11/10/9 |
| 13-15 | 18 | 16 | 14/13/13 | 8/7/6 |
| 16-18 | 17 | 14 | 12/12/11 | 5/4/3 |
| 19-21 | 17 | 14 | 11/10/10 | 2/1/1 |
| 22-24 | 16 | 12 | 9/9/8 | 1/1/1 |

**To Hit Calculation:**
```
Hit if: 1d20 + Bonuses ≥ THAC0 - Target AC
```

### Hit Roll Modifiers

**Strength To-Hit Bonus:**

| STR Score | To-Hit Modifier |
|-----------|-----------------|
| 3 | -5 |
| 4-5 | -3 to -2 |
| 6-7 | -1 to 0 |
| 8-16 | 0 |
| 17 | +1 |
| 18 | +1 |
| 18/51-00 | +2-3 |
| 19-25 | +3-7 |

**Additional Modifiers:**
- Magic weapons: +1 to +5 to hit
- Character's hitroll bonus: typically 0-5 from equipment/spells
- Natural 1 always misses
- Natural 20 always hits

---

## Class-Specific Considerations

### Magic User

**Strengths:**
- Powerful offensive spells at higher levels
- Area effect damage (fireballs, lightning bolts)
- Utility spells (invisibility, teleport, fly)

**Weaknesses:**
- Lowest hit points
- Worst THAC0 progression
- Limited armor options (no armor or very light)
- Limited weapon selection (daggers, staves, darts)
- Vulnerable in melee combat

**Combat Role:**
- Ranged spell damage dealer
- Crowd control
- Support/utility
- Avoid melee at all costs

**Monster Balancing:**
- Should be 1-2 levels higher than party to threaten Magic Users
- Flying/ranged monsters are particularly dangerous
- Magic-resistant creatures are natural counters
- Consider low HP when designing encounter damage

### Cleric

**Strengths:**
- Healing spells (critical for party survival)
- Good defensive spells (armor, sanctuary, bless)
- Moderate hit points
- Decent THAC0
- Can wear heavy armor

**Weaknesses:**
- Limited to blunt weapons (no swords/daggers)
- Fewer offensive spells than Magic Users
- Moderate damage output

**Combat Role:**
- Support healer
- Secondary tank
- Crowd control (hold person)
- Undead specialist (turn undead)

**Monster Balancing:**
- More durable than Magic Users but less than Warriors
- Undead should be challenging for Clerics to make "turn undead" valuable
- Extended fights favor Clerics due to healing
- Consider medium HP when designing encounters

### Thief

**Strengths:**
- Backstab ability (massive burst damage)
- Skills: hide, sneak, pick locks, steal, detect traps
- Good hit points (third best)
- Good damage with backstab
- Access to most weapons

**Weaknesses:**
- Moderate THAC0
- Limited to leather armor (affects AC)
- Backstab requires surprise/positioning
- Vulnerable in sustained melee

**Combat Role:**
- Burst damage dealer (backstab)
- Utility (locks, traps, scouting)
- Flanker/ambusher
- Scout/detector

**Monster Balancing:**
- High-AC monsters reduce backstab effectiveness
- Alert enemies that can't be surprised counter Thieves
- Consider backstab multiplier when designing monster HP
- Thieves excel against single targets, struggle with groups

### Warrior

**Strengths:**
- Highest hit points
- Best THAC0 progression
- Can use all weapons and armor
- Highest sustained damage
- Most durable in combat

**Weaknesses:**
- No magical abilities
- No healing
- Limited utility
- Vulnerable to magic
- No ranged options (beyond throwing)

**Combat Role:**
- Primary tank
- Sustained damage dealer
- Frontline combatant
- Absorb damage for party

**Monster Balancing:**
- Should require Warriors to engage in melee
- High-damage monsters test Warrior durability
- Magic attacks are Warrior weakness
- Consider high HP when designing encounters
- Extended fights favor Warriors due to durability

---

## Using This Guide for Monster Design

### Balancing Single Monster Encounters

**For Equal Level Encounter (1 monster vs 1 PC):**

| Monster vs | HP Range | AC Range | Damage/Round | THAC0 |
|------------|----------|----------|--------------|-------|
| Magic User | 30-60 | 50-70 | 6-10 | 18-16 |
| Cleric | 40-80 | 40-60 | 8-12 | 18-16 |
| Thief | 50-100 | 40-60 | 10-15 | 18-16 |
| Warrior | 60-120 | 30-50 | 12-18 | 18-16 |

**For Challenging Encounter (+2 levels):**
- Increase HP by 50%
- Improve AC by 10-20
- Increase damage by 30-50%
- Improve THAC0 by 2

**For Deadly Encounter (+5 levels):**
- Double HP
- Improve AC by 20-30
- Double damage
- Improve THAC0 by 5

### Group Encounter Guidelines

**Party of 4 (1 of each class, level 5):**
- Combined HP: ~150
- Combined damage/round: ~25-40
- Tank AC: ~40-60
- Party THAC0: 16-20

**Equivalent Monster Force Options:**
- One tough monster: 150 HP, AC 20, 30 damage/round
- Three moderate monsters: 50 HP each, AC 40, 10 damage/round each
- Six weak monsters: 25 HP each, AC 60, 5 damage/round each

### Special Considerations

1. **Magic Resistance**: Reduces Magic User effectiveness, increase for caster-heavy parties
2. **Regeneration**: Effectively multiplies monster HP, requires burst damage
3. **Multiple Attacks**: Increases effective damage, dangerous to low-AC characters
4. **Special Abilities**: Worth 1-2 levels of power (paralysis, poison, drain)
5. **Immunities**: Worth 1-3 levels depending on party composition

### Level Ranges and Appropriate Challenges

| Character Level | Recommended Monster Level | Notes |
|----------------|---------------------------|-------|
| 1-3 | 1-4 | Learning phase, avoid instant death |
| 4-7 | 3-8 | Players learning tactics |
| 8-12 | 6-14 | Competent adventurers |
| 13-17 | 10-19 | Experienced heroes |
| 18-20 | 15-20+ | Epic challenges |

---

## Appendix: Quick Reference Tables

### Damage by Position

When victim is not standing:

| Position | Damage Multiplier |
|----------|-------------------|
| Standing/Fighting | x1.0 |
| Sitting | x1.33 |
| Resting | x1.66 |
| Sleeping | x2.0 |
| Stunned | x2.33 |
| Incapacitated | x2.66 |
| Mortally wounded | x3.0 |

### Sanctuary Spell

When affected by Sanctuary spell:
- **Maximum damage taken**: 18 per hit (regardless of actual damage)
- **Important**: Sanctuary effectively makes characters invulnerable to high-damage single attacks

### Experience Point Guidelines

Standard XP awards are based on monster level:

| Monster Level | Base XP | XP Range |
|--------------|---------|----------|
| 1-3 | 100-500 | Easy encounters |
| 4-6 | 500-2000 | Moderate encounters |
| 7-10 | 2000-8000 | Challenging encounters |
| 11-15 | 8000-32000 | Hard encounters |
| 16-20 | 32000-100000 | Epic encounters |

Modify based on:
- Special abilities: +10-50%
- Magic resistance: +20-40%
- Regeneration: +30-60%
- Multiple attacks: +20-40% per extra attack

---

## Conclusion

This guide provides the statistical foundation for balancing monsters against player characters. Remember:

1. **Magic Users** are glass cannons - fragile but powerful
2. **Clerics** are support tanks - durable healers
3. **Thieves** are burst damage - high single-target damage
4. **Warriors** are sustained damage tanks - reliable frontline

When designing encounters:
- Consider party composition
- Mix monster types for varied challenges
- Test encounters with expected character stats
- Adjust based on actual play experience
- Remember that player tactics and equipment can significantly affect outcomes

For questions or updates to this guide, consult the game masters or review the source code in:
- `dm-dist-alfa/limits.c` (HP advancement)
- `dm-dist-alfa/fight.c` (combat mechanics)
- `dm-dist-alfa/constants.c` (THAC0, modifiers, tables)
