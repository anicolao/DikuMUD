# Barsoom Class Balance Guide

## Purpose

This document provides comprehensive statistical reference data for all four character classes in the Barsoom MUD. Use these charts when designing creatures and encounters to ensure proper balance between challenge and character capabilities. The guide is themed for Edgar Rice Burroughs' Mars setting but maintains the underlying DikuMUD mechanics.

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
| Scientist | 3-8 | 5.5 | 3-8 |
| Noble | 5-10 | 7.5 | 5-10 |
| Assassin | 7-13 | 10 | 7-13 |
| Warrior | 10-15 | 12.5 | 10-15 |

**Note**: Constitution bonus/penalty is added to each roll (see [Constitution Modifier](#constitution-modifier))

### Expected Total Hit Points by Level

These values assume average dice rolls plus a Constitution of 14 (+0 HP modifier). For characters with different Constitution scores, adjust by the CON modifier multiplied by level.

| Level | Scientist | Noble | Assassin | Warrior |
|-------|-----------|-------|----------|---------|
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

| Level | Scientist | Noble | Assassin | Warrior |
|-------|-----------|-------|----------|---------|
| 1-3 | 3-4 | 4-5 | 4-5 | 5-7 |
| 4-6 | 4-6 | 5-7 | 6-8 | 8-11 |
| 7-9 | 5-7 | 6-9 | 7-10 | 10-14 |
| 10-13 | 6-9 | 8-11 | 9-13 | 12-17 |
| 14-17 | 7-11 | 9-13 | 11-16 | 14-20 |
| 18-20 | 8-13 | 10-15 | 13-19 | 16-24 |

**Notes:**
- Scientists typically use light weapons and radium pistols (limited to ranged/light weapons)
- Nobles can use any weapon but favor ornate long swords and pistols
- Assassins excel with short swords and throwing knives (backstab specialists)
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

### Backstab Damage (Assassins Only)

When an assassin successfully backstabs, damage is multiplied:

| Level | Backstab Multiplier |
|-------|---------------------|
| 1-4 | x2 |
| 5-8 | x3 |
| 9-13 | x4 |
| 14+ | x5 |

**Backstab Damage Formula**: `(Base Damage + Modifiers) × Multiplier`

**Example**: Level 10 assassin with short sword (1d6) and 16 STR:
- Normal hit: 1d6 + 1 (STR) = 2-7 damage (avg 4.5)
- Backstab: (1d6 + 1) × 4 = 8-28 damage (avg 18)

---

## Combat Statistics (THAC0)

THAC0 (To Hit Armor Class 0) determines hit chance. **Lower THAC0 is better**.

### THAC0 by Class and Level

| Level | Scientist | Noble | Assassin | Warrior |
|-------|-----------|-------|----------|---------|
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

### Scientist

**Strengths:**
- Advanced technology and inventions
- Healing and surgical abilities
- Ranged weapons (radium pistols, rifles)
- Problem-solving and knowledge

**Weaknesses:**
- Lowest hit points
- Worst THAC0 progression
- Limited armor options (light harness only)
- Limited weapon selection (light weapons, pistols)
- Vulnerable in melee combat

**Combat Role:**
- Ranged damage with technology
- Support/healing
- Utility and problem-solving
- Avoid close combat

**Creature Balancing:**
- Should be 1-2 levels higher than party to threaten Scientists
- Fast melee creatures are particularly dangerous
- Consider low HP when designing encounter damage
- Scientists excel against technology-vulnerable enemies

### Noble

**Strengths:**
- Leadership and inspiration abilities
- Social skills and diplomacy
- Moderate combat capability
- Good hit points
- Can wear quality armor and use all weapons

**Weaknesses:**
- Not specialized in any single combat role
- Moderate damage output
- Abilities depend on allies and followers

**Combat Role:**
- Party leader and coordinator
- Secondary combatant
- Morale booster
- Diplomat and negotiator

**Creature Balancing:**
- More durable than Scientists but less than Warriors
- Extended fights can favor Nobles due to leadership bonuses
- Consider medium HP when designing encounters
- Social encounters can bypass combat entirely

### Assassin

**Strengths:**
- Backstab ability (massive burst damage)
- Skills: hide, sneak, pick locks, poison, disguise
- Good hit points (third best)
- High damage with backstab
- Access to most weapons

**Weaknesses:**
- Moderate THAC0
- Limited to light armor (affects AC)
- Backstab requires surprise/positioning
- Vulnerable in sustained melee

**Combat Role:**
- Burst damage dealer (backstab)
- Stealth and infiltration
- Ambusher and scout
- Trap detection

**Creature Balancing:**
- High-AC creatures reduce backstab effectiveness
- Alert enemies that can't be surprised counter Assassins
- Consider backstab multiplier when designing creature HP
- Assassins excel against single targets, struggle with groups

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

**Creature Balancing:**
- Should require Warriors to engage in melee
- High-damage creatures test Warrior durability
- Ranged and technical threats are Warrior weaknesses
- Consider high HP when designing encounters
- Extended fights favor Warriors due to durability

---

## Using This Guide for Creature Design

### Balancing Single Creature Encounters

**Design Philosophy**: Encounters should allow players to fight 2-3 battles in a row as a solo character, or 3-5 battles in a party of 2, without requiring rest. This means individual encounters should consume roughly 25-35% of the party's resources.

**For Standard Encounter (1 creature vs 1 PC, same level):**

| Creature vs | HP Range | AC Range | Damage/Round | THAC0 |
|-------------|----------|----------|--------------|-------|
| Scientist | 15-25 | 60-80 | 3-5 | 20-18 |
| Noble | 20-35 | 50-70 | 4-7 | 20-18 |
| Assassin | 25-40 | 50-70 | 5-8 | 20-18 |
| Warrior | 30-50 | 40-60 | 6-10 | 20-18 |

**Resource Consumption Guidelines:**
- **Standard encounter**: Should consume 20-30% of character HP and resources
- **Challenging encounter (+1-2 levels)**: Should consume 35-45% of resources
- **Difficult encounter (+3-4 levels)**: Should consume 50-65% of resources (save for boss/special)
- **Boss encounter (+5+ levels)**: May consume 80%+ resources (end of dungeon/quest)

### Group Encounter Guidelines

**Design for Sustainability**: A party should be able to complete a dungeon with 3-5 encounters before needing to rest.

**Party of 2 (typical pairing, level 5):**
- Combined HP: ~50-100 (varies by class combination)
- Combined damage/round: ~12-20
- Best AC: ~50-60
- Party THAC0: 16-19

**Equivalent Creature Force Options for 2-Person Party:**
- One standard creature: 25-35 HP, AC 50-60, 4-6 damage/round
- Two weak creatures: 15-20 HP each, AC 60-70, 3-4 damage/round each
- Three very weak creatures: 10-12 HP each, AC 70-80, 2-3 damage/round each

**Party of 4 (1 of each class, level 5):**
- Combined HP: ~150-180
- Combined damage/round: ~25-40
- Tank AC: ~40-60
- Party THAC0: 16-20

**Equivalent Creature Force Options for 4-Person Party:**
- One moderate creature: 40-60 HP, AC 40-50, 8-12 damage/round
- Two standard creatures: 25-35 HP each, AC 50-60, 5-7 damage/round each
- Four weak creatures: 15-20 HP each, AC 60-70, 3-5 damage/round each

### Special Considerations

1. **Technology Resistance**: Reduces Scientist effectiveness, increase for technology-heavy parties
2. **Regeneration**: Effectively multiplies creature HP, requires burst damage
3. **Multiple Attacks**: Increases effective damage, dangerous to low-AC characters (e.g., green martians' four arms)
4. **Special Abilities**: Worth 1-2 levels of power (paralysis, poison, blood drain)
5. **Immunities**: Worth 1-3 levels depending on party composition

### Level Ranges and Appropriate Challenges

| Character Level | Recommended Creature Level | Notes |
|----------------|----------------------------|-------|
| 1-3 | 1-4 | Learning Barsoom, avoid instant death |
| 4-7 | 3-8 | Players learning tactics |
| 8-12 | 6-14 | Competent adventurers |
| 13-17 | 10-19 | Experienced heroes |
| 18-20 | 15-20+ | Epic challenges (white apes, jeddaks) |

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

Standard XP awards are based on creature level:

| Creature Level | Base XP | XP Range |
|----------------|---------|----------|
| 1-3 | 100-500 | Easy encounters (calots, wild thoats) |
| 4-6 | 500-2000 | Moderate encounters (banths, green martian scouts) |
| 7-10 | 2000-8000 | Challenging encounters (plant men, white apes) |
| 11-15 | 8000-32000 | Hard encounters (great white apes, jeds) |
| 16-20 | 32000-100000 | Epic encounters (jeddaks, ancient horrors) |

Modify based on:
- Special abilities: +10-50%
- Technology resistance: +20-40%
- Regeneration: +30-60%
- Multiple attacks: +20-40% per extra attack (e.g., green martians' four arms)

---

## Practical Examples

### Example 1: Designing a Level 5 Green Martian Warrior (Standard Encounter)

**Target**: Standard challenge for a level 5 party (consumable as part of wilderness exploration)

**Party Stats (Level 5 average):**
- Scientist: 32 HP, AC 70, 5 damage/round, THAC0 19
- Noble: 40 HP, AC 60, 7 damage/round, THAC0 18
- Assassin: 48 HP, AC 60, 8 damage/round, THAC0 19
- Warrior: 60 HP, AC 50, 11 damage/round, THAC0 16

**Green Martian Scout Design:**
- **Hit Points**: 30 (roughly half of weakest party member)
- **Armor Class**: 60 (leather harness, easier to hit)
- **Damage**: 1d6+1 (spear + moderate strength), average 4.5/round
- **THAC0**: 18 (standard for level 5 creature)
- **Special**: Four-armed (can wield multiple weapons), excellent marksman

**Combat Analysis:**
- Warrior can kill green martian in ~3 rounds (30 HP / 11 damage = 3 rounds)
- Party can kill in 1-2 rounds if focused (30 HP / 31 combined damage)
- Green martian can damage Scientist for ~14 HP over 3 rounds (3 × 4.5)
- Party takes minimal casualties, can fight 3-4 more green martians before rest

**Verdict**: Balanced for wilderness area with 3-4 green martian encounters, party continues after each fight

### Example 2: Designing a Level 10 Great White Ape (Boss Encounter)

**Target**: Epic boss for level 10 party at end of ancient ruins (should consume most resources)

**Party Stats (Level 10 average):**
- Scientist: 61 HP, AC 40, 8 damage/round, THAC0 18
- Noble: 79 HP, AC 30, 10 damage/round, THAC0 16
- Assassin: 98 HP, AC 40, 12 damage/round (24 with backstab), THAC0 16
- Warrior: 123 HP, AC 20, 15 damage/round, THAC0 11

**Great White Ape Alpha Design (Revised):**
- **Hit Points**: 180 (roughly half of party total HP)
- **Armor Class**: 10 (thick hide and muscle)
- **Damage**: 2d8+4 (massive claws + bite), average 13/round
- **THAC0**: 12 (dangerous but not overwhelming)
- **Special**: Crushing embrace 6d6 (average 21 damage, grapple attack, once per combat if it grabs someone)

**Combat Analysis:**
- Ape deals ~13 damage/round, threatens Scientist but not instant kill
- Crushing embrace is significant threat (21 damage) but not party wipe
- Party deals ~45 damage/round combined
- Ape survives ~4 rounds (180 HP / 45 damage)
- Party takes ~52-73 HP damage during fight (mix of melee and grapple)
- Scientist and Noble will need healing after
- Party can continue to explore but needs short rest

**Verdict**: Epic boss that's challenging and memorable but doesn't require perfect execution

### Example 3: Balancing for Solo Player

**Scenario**: Level 8 Warrior exploring solo (most common solo class)

**Warrior Stats:**
- HP: 98
- AC: 40 (metal harness + some technology)
- Damage: 12 (long sword + strength)
- THAC0: 13
- Special: Good armor, high HP, no healing

**Creature Options:**

**Option A - Wild Calot (Standard encounter):**
- HP: 20 (Warrior kills in 2 rounds)
- AC: 70 (fast but easy to hit)
- Damage: 3 (bite)
- THAC0: 18
- **Analysis**: Warrior takes ~4-6 damage, can fight 5-6 in a row before rest
- **Result**: Good for wilderness encounters

**Option B - Banth (Moderate encounter):**
- HP: 35 (Warrior kills in 3 rounds)
- AC: 60 (tough hide)
- Damage: 5 (claws and teeth)
- THAC0: 17
- **Analysis**: Warrior takes ~12-15 damage, can fight 3-4 in a row before rest
- **Result**: Good for wilderness predator encounters

**Option C - Plant Man (Challenging encounter):**
- HP: 60 (Warrior kills in 5 rounds)
- AC: 50 (thick vegetable hide)
- Damage: 8 (tentacles + blood drain)
- THAC0: 16
- **Analysis**: Warrior takes ~35-40 damage, can fight 1-2 before needing rest
- **Result**: Good for mini-boss or dangerous area

**Solo Scientist Option - Reanimated Corpse:**
- HP: 25 (easy to kill with technology)
- AC: 80 (slow, easy to hit)
- Damage: 4 (claws)
- THAC0: 18
- Special: Immune to certain effects (failed surgical experiment)
- **Analysis**: Scientist can kill with ranged weapons in 1-2 rounds, takes minimal damage
- **Result**: Solo player can handle 3-4 corpses before needing rest

---

## Conclusion

This guide provides the statistical foundation for balancing creatures against player characters on Barsoom. Remember:

1. **Scientists** are glass cannons - fragile but technologically powerful
2. **Nobles** are versatile leaders - moderate combat with social power
3. **Assassins** are burst damage - high single-target damage from stealth
4. **Warriors** are sustained damage tanks - reliable frontline combatants

### Encounter Design Philosophy

**Key Principle**: Design encounters that allow for multiple consecutive battles without rest.

- **Solo players** should handle 2-3 standard encounters in a row
- **Parties of 2** should handle 3-5 standard encounters in a row
- **Parties of 4** should clear an entire dungeon wing (5-8 encounters) before rest

**Resource Management:**
- Standard encounters consume 20-30% of party resources
- Challenging encounters consume 35-45% of resources
- Boss encounters consume 60-80% of resources (placed at end of dungeon sections)

**Dungeon Flow:**
- 3-4 standard encounters → 1 challenging encounter → short rest
- 2-3 challenging encounters → 1 boss encounter → long rest
- Vary monster types and tactics to keep gameplay interesting

When designing encounters:
- Consider party composition and sustainability
- Mix encounter difficulty within areas (ruins, wilderness, cities)
- Provide rest opportunities between major sections
- Test encounters with expected character stats
- Remember that player tactics and technology can significantly affect outcomes
- Avoid "single encounter = forced rest" design unless it's a major boss
- Use Barsoom-appropriate creatures for each area (calots in cities, banths in wilderness, etc.)

For questions or updates to this guide, consult the game masters or review the source code in:
- `dm-dist-alfa/limits.c` (HP advancement)
- `dm-dist-alfa/fight.c` (combat mechanics)
- `dm-dist-alfa/constants.c` (THAC0, modifiers, tables)
- `barsoom/CLASSES.md` (class descriptions)
- `barsoom/summaries/CREATURES.md` (creature reference)
