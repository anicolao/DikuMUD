# Quest System Expansion - Phase 2 Quest Design

## Overview

This document outlines the design for 15-20 new quests to be added across all major zones in the Barsoom world as part of Milestone 2 from WHATS_NEXT.md.

## Current Status

**Phase 1: COMPLETE ✅**
- All quest types (DELIVERY, RETRIEVAL, KILL, EXPLORE, COLLECT) are fully functional
- KILL quests integrated with fight.c
- EXPLORE quests integrated with act.movement.c
- Quest completion detection working for all types
- 6 existing quests:
  - Quest 4001: Sola's White Ape Tooth (RETRIEVAL) - Thark Territory
  - Quest 4201: Biological Specimen (RETRIEVAL) - Atmosphere Factory
  - Quest 4202: Vad Varo's Research Notes (DELIVERY) - Atmosphere Factory
  - Quest 4203: Radium Mutant Kill (KILL) - Atmosphere Factory
  - Quest 4204: Archive Chamber Exploration (EXPLORE) - Atmosphere Factory
  - Quest 4205: Ras Thavas's Data Crystal (RETRIEVAL) - Atmosphere Factory

**Phase 2: COMPLETE ✅**
- 15 new quests added across 7 major zones
- Total of 21 quests across 8 zones
- Each zone has at least 1-3 quests
- Quest difficulty matches zone level ranges
- See MILESTONE_2_PHASE2_COMPLETE.md for full details

## Quest Design Principles

1. **Level Appropriate**: Match quest difficulty to zone level range
2. **Thematic**: Quests should fit Barsoom lore and zone theme
3. **Varied Types**: Use all quest types (DELIVERY, RETRIEVAL, KILL, EXPLORE, COLLECT)
4. **Clear Objectives**: Players should understand what to do
5. **Rewarding**: Experience, gold, and items appropriate to level
6. **Lore Integration**: Reference Barsoom characters and events

## Zone Quest Plans

### Lesser Helium (Vnum 3000-3099, Levels 1-10)

**Zone Theme**: Starting city, noble houses, temple, market
**Target Players**: New characters (levels 1-10)
**Existing NPCs**: Nobles, temple priests, guards, merchants

**Planned Quests:**

1. **"Guard's Training"** (KILL)
   - **Quest Giver**: City Guard Captain (need to identify/create)
   - **Objective**: Kill 1 sewer rat or similar low-level creature
   - **Location**: Lesser Helium sewers
   - **Rewards**: 200 exp, 50 gold, basic weapon
   - **Level**: 1-5
   - **Quest Text**: "Welcome, recruit! To prove you're ready to serve Helium, venture into the sewers and deal with one of the vermin. Return when you've succeeded."

2. **"Market Survey"** (EXPLORE)
   - **Quest Giver**: Market Administrator (need to identify/create)
   - **Objective**: Visit the central marketplace
   - **Location**: Lesser Helium market area
   - **Rewards**: 250 exp, 100 gold, food/drink items
   - **Level**: 1-8
   - **Quest Text**: "I need someone to check on the market stalls. Simply make your way to the central marketplace and report back."

3. **"Temple Offerings"** (DELIVERY)
   - **Quest Giver**: Temple Acolyte (need to identify/create)
   - **Objective**: Deliver sacred offering to temple priest
   - **Location**: Lesser Helium temple
   - **Rewards**: 300 exp, 75 gold, healing item
   - **Level**: 3-10
   - **Quest Text**: "Please take this offering to the high priest at the temple altar. He awaits the daily blessing."

### Greater Helium (Vnum 3200-3299, Levels 10-18)

**Zone Theme**: Capital city, palace, arena, John Carter's domain
**Target Players**: Mid-level characters (levels 10-18)
**Existing NPCs**: John Carter, Dejah Thoris, palace guards, arena fighters

**Planned Quests:**

1. **"John Carter's Challenge"** (KILL)
   - **Quest Giver**: John Carter (need to identify/create if not exists)
   - **Objective**: Defeat an arena champion or worthy opponent
   - **Location**: Greater Helium arena
   - **Rewards**: 1500 exp, 500 gold, quality weapon
   - **Level**: 12-18
   - **Quest Text**: "You look capable, warrior. The arena awaits those with courage. Face the champion and prove your mettle."

2. **"Dejah Thoris's Research"** (RETRIEVAL)
   - **Quest Giver**: Dejah Thoris (need to identify/create if not exists)
   - **Objective**: Retrieve ancient artifact from ruins
   - **Location**: Connected ruins or wilderness area
   - **Rewards**: 1800 exp, 600 gold, technological device
   - **Level**: 14-18
   - **Quest Text**: "I require an ancient technological artifact for my research. Retrieve it from the old ruins and I shall reward you well."

3. **"Palace Security"** (EXPLORE)
   - **Quest Giver**: Palace Guard Commander (need to identify/create)
   - **Objective**: Patrol palace perimeter, visit key security points
   - **Location**: Greater Helium palace grounds
   - **Rewards**: 1200 exp, 400 gold, armor piece
   - **Level**: 10-15
   - **Quest Text**: "We need someone to check the palace security. Visit the guard posts and report back on their readiness."

### Gathol (Vnum 3300-3399, Levels 12-20)

**Zone Theme**: Jetan (Martian chess), Gahan of Gathol's city
**Target Players**: Mid to high-level characters (levels 12-20)
**Existing NPCs**: Gahan, Jetan players, city officials

**Planned Quests:**

1. **"Jetan Tournament"** (KILL or SPECIAL)
   - **Quest Giver**: Jetan Master (need to identify/create)
   - **Objective**: Defeat opponent in combat (simulating Jetan)
   - **Location**: Gathol game halls
   - **Rewards**: 2000 exp, 800 gold, strategic item
   - **Level**: 15-20
   - **Quest Text**: "The Jetan tournament requires champions. Face an opponent and show your tactical prowess."

2. **"Gahan's Trust"** (DELIVERY)
   - **Quest Giver**: Gahan of Gathol (need to identify/create if not exists)
   - **Objective**: Deliver diplomatic message to ally city
   - **Location**: Gathol to another city
   - **Rewards**: 1800 exp, 700 gold, diplomatic gift
   - **Level**: 12-18
   - **Quest Text**: "I trust you to deliver this sealed message to our allies. Guard it with your life."

### Ptarth (Vnum 3500-3599, Levels 15-23)

**Zone Theme**: Thuvia's city, diplomacy, culture
**Target Players**: High-level characters (levels 15-23)
**Existing NPCs**: Thuvia, city officials, guards

**Planned Quests:**

1. **"Thuvia's Request"** (RETRIEVAL or KILL)
   - **Quest Giver**: Thuvia (need to identify/create if not exists)
   - **Objective**: Retrieve item or defeat banth threat
   - **Location**: Ptarth territory
   - **Rewards**: 2500 exp, 1000 gold, rare item
   - **Level**: 18-23
   - **Quest Text**: "I need your assistance with a matter of importance. Banths threaten our borders - deal with them."

2. **"Diplomatic Mission"** (DELIVERY)
   - **Quest Giver**: Ptarth Ambassador (need to identify/create)
   - **Objective**: Deliver treaty to allied city
   - **Location**: Ptarth to ally city
   - **Rewards**: 2200 exp, 900 gold, diplomatic reward
   - **Level**: 15-20
   - **Quest Text**: "Carry this treaty to our allies. The future of Ptarth depends on this alliance."

### Kaol (Vnum 3600-3699, Levels 18-26)

**Zone Theme**: Military city, Kulan Tith's domain
**Target Players**: High-level characters (levels 18-26)
**Existing NPCs**: Kulan Tith, military commanders, warriors

**Planned Quests:**

1. **"Kulan Tith's Honor"** (KILL)
   - **Quest Giver**: Kulan Tith (need to identify/create if not exists)
   - **Objective**: Defeat dishonorable enemy or threat
   - **Location**: Kaol territory or borders
   - **Rewards**: 3000 exp, 1500 gold, masterwork weapon
   - **Level**: 20-26
   - **Quest Text**: "A dishonorable foe threatens Kaol. Defeat them and restore our honor."

2. **"Military Training"** (EXPLORE or KILL)
   - **Quest Giver**: Training Commander (need to identify/create)
   - **Objective**: Complete training course or defeat training opponents
   - **Location**: Kaol military grounds
   - **Rewards**: 2800 exp, 1200 gold, military equipment
   - **Level**: 18-24
   - **Quest Text**: "Prove your combat skills. Complete the training course and show you're worthy of Kaol's finest."

### Thark Territory (Vnum 4000-4099, Levels 10-18)

**Zone Theme**: Green Martian territory, Tars Tarkas's people
**Target Players**: Mid-level characters (levels 10-18)
**Existing NPCs**: Tars Tarkas, Sola, Thark warriors
**Existing Quest**: Sola's White Ape Tooth quest (4001)

**Planned Quests:**

1. **"Tars Tarkas's Challenge"** (KILL)
   - **Quest Giver**: Tars Tarkas (need to identify/create if not exists, vnum ~4050)
   - **Objective**: Defeat a powerful creature proving combat prowess
   - **Location**: Thark hunting grounds
   - **Rewards**: 1600 exp, 600 gold, Thark weapon
   - **Level**: 14-18
   - **Quest Text**: "You have proven yourself to Sola. Now prove yourself to me. Hunt the great calot and bring proof of your kill."

### Zodanga (Vnum 3700-3799, Levels 18-26)

**Zone Theme**: Enemy city, hostile territory, Than Kosis's domain
**Target Players**: High-level characters (levels 18-26)
**Existing NPCs**: Enemy soldiers, Than Kosis, spies

**Planned Quests:**

1. **"Sabotage Mission"** (KILL or RETRIEVAL)
   - **Quest Giver**: Helium Spy (need to create in safe zone)
   - **Objective**: Sabotage enemy operations or steal plans
   - **Location**: Zodanga territory (dangerous)
   - **Rewards**: 3200 exp, 1600 gold, spy equipment
   - **Level**: 20-26
   - **Quest Text**: "Helium needs brave souls to disrupt Zodanga's war preparations. Are you willing to risk everything?"

2. **"Intelligence Gathering"** (EXPLORE)
   - **Quest Giver**: Intelligence Officer (need to create in safe zone)
   - **Objective**: Scout Zodanga defenses, visit key locations
   - **Location**: Zodanga territory (dangerous)
   - **Rewards**: 2900 exp, 1400 gold, information reward
   - **Level**: 18-24
   - **Quest Text**: "We need maps of Zodanga's defenses. Infiltrate their territory and report on key positions."

## Implementation Checklist

### Prerequisites for Each Quest

1. **NPC Identification**:
   - [ ] Identify existing NPCs in each zone that can be quest givers
   - [ ] Create new NPCs where needed
   - [ ] Set appropriate vnum ranges for new NPCs

2. **Item Creation**:
   - [ ] Quest items (items to deliver/retrieve)
   - [ ] Reward items (weapons, armor, special items)
   - [ ] Ensure vnums don't conflict with existing items

3. **Target Specification**:
   - [ ] For KILL quests: identify or create target mobs
   - [ ] For EXPLORE quests: identify target room vnums
   - [ ] For DELIVERY/RETRIEVAL: identify target NPCs/rooms

4. **Quest Data**:
   - [ ] Assign quest vnums (follow zone numbering)
   - [ ] Write quest_text (assignment message)
   - [ ] Write complete_text (completion message)
   - [ ] Write fail_text (failure message)
   - [ ] Set duration (MUD hours before expiration)
   - [ ] Set quest_flags (visibility settings)
   - [ ] Balance rewards (exp, gold, items) for level range

### Implementation Steps

1. **Zone Survey** (Week 2-3):
   - Review each zone's YAML file
   - Document existing NPCs and their vnums
   - Document existing items and their vnums
   - Identify suitable locations for quest objectives

2. **Quest Creation** (Week 3-4):
   - Create quest YAML entries for each zone
   - Create new NPCs where needed
   - Create quest items and rewards
   - Write compelling quest text with Barsoom flavor

3. **Testing** (Week 4-5):
   - Test each quest individually
   - Verify quest assignment works
   - Verify quest completion works
   - Verify rewards are granted correctly
   - Test quest expiration
   - Create integration tests for new quests

4. **Documentation** (Week 5):
   - Update QUEST_IMPLEMENTATION.md
   - Document new quests in zone guides
   - Create quest walkthrough guide for players

## Quest Vnum Allocation

Follow zone numbering convention:
- Lesser Helium (3000s): Quests 3001-3003
- Greater Helium (3200s): Quests 3201-3203
- Gathol (3300s): Quests 3301-3302
- Ptarth (3500s): Quests 3501-3502
- Kaol (3600s): Quests 3601-3602
- Thark Territory (4000s): Quest 4001 exists, add 4002
- Zodanga (3700s): Quests 3701-3702

## Success Metrics

- [ ] Total of 15-20 quests across all zones
- [ ] Each major zone has at least 1 quest
- [ ] All 5 quest types represented (DELIVERY, RETRIEVAL, KILL, EXPLORE, COLLECT)
- [ ] Quest difficulty matches zone level ranges
- [ ] All quests have integration tests
- [ ] Build succeeds with no errors
- [ ] All tests pass

## Notes

- COLLECT quest type not yet implemented - may need additional code
- Some zones may need minor additions (NPCs, items) to support quests
- Quest chains (prerequisites) can be added in future milestone
- Multiple simultaneous quests requires additional work
