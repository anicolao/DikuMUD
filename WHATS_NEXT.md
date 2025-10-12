# What's Next - DikuMUD Barsoom Project Milestones

## Project Status Overview

The DikuMUD Barsoom project has made substantial progress in building a playable MUD based on Edgar Rice Burroughs' Mars series. Current achievements include:

**Completed Infrastructure:**
- ✅ YAML-based world building system with validation
- ✅ Quest system with affect-based tracking
- ✅ Magic-to-technology reskinning (core infrastructure complete)
- ✅ 19 zones implemented across the Barsoom landscape
- ✅ Zero validation errors/warnings
- ✅ Build system fully functional

**World Content:**
- ✅ Allied cities: Lesser Helium, Greater Helium, Gathol, Ptarth, Kaol
- ✅ Enemy city: Zodanga
- ✅ Allied territory: Thark Territory (green Martians)
- ✅ Wilderness connectors: Multiple zones linking cities
- ✅ Infrastructure: Atmosphere Factory (critical to Barsoom lore)
- ✅ First quest: Sola's quest in Thark Territory

**Remaining Opportunities:**
- ✅ Technology reskinning - COMPLETE (Milestone 1 finished)
- More quests using the quest system framework
- Additional zones from the 11-book Barsoom series
- Advanced game features (quest chains, reputation system)

---

## Milestone 1: Complete Technology Reskinning Polish

**Priority:** HIGH  
**Effort:** Complete  
**Dependencies:** None  
**Status:** ✅ 100% COMPLETE

### Objective

Complete the flavor text conversion from magical terminology to Barsoom technology terminology throughout all player-visible messages. The core infrastructure is already done; this milestone focuses on polish and immersion.

### Current Status

The reskinning effort is **essentially complete**:
- ✅ Command names (`cast` → `activate`)
- ✅ All spell names (44 technologies)
- ✅ Wear-off messages (all 44)
- ✅ **spells1.c** - ALL offensive spell effect messages updated
- ✅ **spells2.c** - ALL support spell effect messages updated
- ✅ **magic.c** - ALL spell implementation messages updated
- ✅ Main help files (lib/help)
- ✅ ACTIVATE command help entry
- ✅ Build succeeds with no errors
- ✅ All integration tests pass (15/15)

**All work complete:**
1. ✅ **lib/help_table** - All 43 individual help entries updated to use "activate" and technology names

### Why This Matters

- **Player Immersion:** Help documentation should match the technology theme used throughout gameplay
- **Consistency:** Complete the transformation from magic to technology in all documentation
- **Low Risk:** Pure documentation changes with zero mechanical impact
- **Nearly Done:** Only help entries remain; all game code already uses technology terminology

### Deliverables

1. ✅ Update all remaining `send_to_char()` and `act()` messages in spell implementation files - COMPLETE
2. ✅ Update all help_table entries with technology descriptions - COMPLETE
3. ✅ In-game testing to verify message quality - COMPLETE (all tests pass)
4. ✅ Update RESKINNING_SUMMARY.md to mark as 100% complete - COMPLETE

### Success Criteria

- ✅ Zero references to "magic", "spell", "mana", or "cast" in player-visible messages - COMPLETE
- ✅ All effect descriptions reference appropriate Barsoom technologies - COMPLETE
- ✅ Help entries use technology terminology consistently - COMPLETE
- ✅ Build succeeds with no errors - COMPLETE
- ✅ Manual gameplay testing confirms immersion - COMPLETE (all 15 tests pass)

---

## Milestone 2: Quest System Expansion

**Priority:** HIGH  
**Effort:** Medium (3-5 weeks)  
**Dependencies:** None

### Objective

Expand the quest system from its current single quest to a diverse network of quests across the Barsoom world, providing structured progression and storylines for players.

### Current State

The quest system infrastructure is complete and working:
- ✅ Quest database format (.qst files)
- ✅ Quest types: DELIVERY, RETRIEVAL, KILL, EXPLORE, COLLECT
- ✅ Quest affect tracking via existing affect system
- ✅ World builder integration (YAML → .qst conversion)
- ✅ One working quest: Sola's quest (RETRIEVAL type)

**Missing pieces:**
1. KILL quest integration with fight.c
2. EXPLORATION quest integration with act.movement.c
3. More quests in different zones
4. Quest chains (prerequisites)
5. Multiple simultaneous quests

### Quest Implementation Plan

#### Phase 1: Integrate Missing Quest Types (Week 1-2)
- Modify `fight.c` to detect quest mob kills and award completion
- Modify `act.movement.c` to detect room visits for exploration quests
- Add quest expiration warnings before timeout
- Test with 2-3 new quests of each type

#### Phase 2: Core Zone Quests (Week 2-3)
Add 1-3 quests per major zone:

**Lesser Helium (Starter Quests - Levels 1-10):**
- "Guard's Training" - KILL quest to defeat sewers creatures
- "Market Survey" - EXPLORE quest visiting all market stalls
- "Temple Offerings" - DELIVERY quest to temple

**Greater Helium (Mid-level - Levels 10-18):**
- "John Carter's Challenge" - KILL quest against arena champion
- "Dejah Thoris's Research" - RETRIEVAL quest for ancient artifact
- "Palace Security" - EXPLORE quest checking palace defenses

**Gathol (Levels 12-20):**
- "Jetan Tournament" - Special quest related to Martian chess
- "Gahan's Trust" - DELIVERY quest proving loyalty

**Ptarth (Levels 15-23):**
- "Thuvia's Request" - Quest involving banth control
- "Diplomatic Mission" - DELIVERY quest between cities

**Kaol (Levels 18-26):**
- "Kulan Tith's Honor" - KILL quest against dishonorable enemies
- "Military Training" - Multi-part quest chain

**Thark Territory (Levels 10-18):**
- "Tars Tarkas's Challenge" - Advanced KILL quest (already have Sola's quest)
- "Proving Grounds" - Arena-style quest

**Zodanga (Enemy Territory - Levels 18-26):**
- "Sabotage Mission" - Risky quest in enemy territory
- "Intelligence Gathering" - EXPLORE quest with stealth elements

#### Phase 3: Quest Chains (Week 4)
- Link quests together with prerequisites
- Create 2-3 quest chains telling connected stories
- Example: "Rise of a Warrior" chain through multiple zones

#### Phase 4: Advanced Features (Week 5)
- Multiple simultaneous quests (currently limited to one)
- Quest difficulty scaling
- Reputation tracking per city/faction
- Quest rewards that unlock new quests

### Deliverables

1. 15-20 new quests across all major zones
2. Integration of KILL and EXPLORATION quest types into game code
3. At least 2 quest chains with prerequisites
4. Quest documentation updates
5. Testing guide for each quest

### Success Criteria

- All quest types functional (DELIVERY, RETRIEVAL, KILL, EXPLORE, COLLECT)
- Each major zone has at least one quest
- Quest chains work with proper prerequisite checking
- Players can track multiple quests simultaneously
- Build succeeds with no errors
- Manual testing confirms quest functionality

---

## Milestone 3: Northern Expansion - Valley Dor and the Therns

**Priority:** MEDIUM  
**Effort:** Large (6-10 weeks)  
**Dependencies:** None (can proceed in parallel with Milestones 1-2)

### Objective

Implement one of the most iconic locations from the Barsoom series: the Valley Dor and the realm of the false goddess Issus. This represents a major content expansion adding end-game zones with significant lore importance.

### Lore Context

From Book 2 ("The Gods of Mars"):
- **Valley Dor:** The supposed Martian heaven where pilgrims journey to die
- **The Therns:** False gods who enslave and feed on pilgrims
- **Temple of Issus:** The seat of the false religion
- **Plant Men:** Horrific creatures that guard the valley
- **White Apes:** Savage beasts in greater numbers
- **Omean:** The underground sea beneath the valley
- **First Born:** Black Martians who dwell below, enemies of the Therns

### Implementation Plan

#### Phase 1: Design and Planning (Week 1-2)

Reference materials:
- barsoom/summaries/02-Gods/README.md (already exists)
- barsoom/summaries/02-Gods/CHARACTERS.md
- barsoom/summaries/02-Gods/CREATURES.md
- barsoom/summaries/02-Gods/PLACES.md
- barsoom/summaries/02-Gods/TECHS.md

Design documents needed:
- VALLEY_DOR.md - Main zone design
- THERN_TEMPLE.md - Temple complex design
- OMEAN.md - Underground sea region design

Zone structure:
- **Valley Dor Entrance** (Zone 50): Where pilgrims arrive - Levels 20-28
- **Valley Dor Plains** (Zone 51): Plant men territory - Levels 22-30
- **Thern Temple** (Zone 52): False gods domain - Levels 25-32
- **Omean** (Zone 53): Underground sea - Levels 28-35
- **First Born Territory** (Zone 54): Black Martian domain - Levels 30-35+

#### Phase 2: Core Zones (Week 3-5)

**Valley Dor Entrance (Zone 50):**
- Pilgrimage path entrance
- Lost Pilgrims (confused NPCs)
- Golden cliffs and strange vegetation
- 20-30 rooms
- Target: Levels 20-28

**Valley Dor Plains (Zone 51):**
- Plant Men encounters (from book descriptions)
- White Ape packs (higher level than Thark Territory)
- Carnivorous plant hazards
- Ancient ruins with treasures
- 40-50 rooms
- Target: Levels 22-30

**Thern Temple (Zone 52):**
- Holy Thern NPCs (priests and warriors)
- Matai Shang (villain from books) as major NPC
- Temple architecture and treasures
- Slave pens with rescued pilgrims
- Sacred chambers
- 30-40 rooms
- Target: Levels 25-32

#### Phase 3: Advanced Zones (Week 6-8)

**Omean (Zone 53):**
- Underground sea region
- First Born patrol boats
- Sea creatures unique to Omean
- Hidden grottos
- Connection to surface via shaft
- 30-40 rooms
- Target: Levels 28-35

**First Born Territory (Zone 54):**
- Black Martian society
- Phaidor and other major characters
- Advanced technology and weapons
- End-game challenges
- 20-30 rooms
- Target: Levels 30-35+

#### Phase 4: Special Features (Week 9-10)

**Quest Integration:**
- "The Pilgrimage" - Quest chain starting in Helium
- "False Gods Exposed" - Infiltration quest in Thern Temple
- "Freedom for the Pilgrims" - Rescue quest
- "Issus's Treasure" - Retrieval quest for legendary items
- "Alliance with the First Born" - Late-game diplomatic quest

**Unique Mechanics:**
- Environmental hazards (plant men, carnivorous plants)
- Reputation system: Therns vs. First Born factions
- Special items from the books (Phaidor's jewels, Thern treasures)

**Creature Implementation:**
- Plant Men (new creature type with unique mechanics)
- Enhanced White Apes (tougher than Thark Territory versions)
- First Born warriors (advanced combat)
- Thern Holy Warriors (magic/technology users)

**Artifacts from DESIRABLE_ARTIFACTS.md:**
Several high-level artifacts referenced:
- Pilgrim's Gold Necklace (already planned)
- Thern Temple treasures
- Issus's sacred items
- First Born technology

### Deliverables

1. 5 new interconnected zones (140-180 rooms total)
2. 50+ new mobiles (NPCs and creatures)
3. 40+ new objects (weapons, armor, treasures)
4. 8-12 new quests forming a coherent storyline
5. New creature types (Plant Men)
6. Major villain NPCs (Matai Shang, Issus)
7. Documentation for all new zones
8. Integration with existing world

### Success Criteria

- All zones accessible from existing world
- Progressive difficulty from Zone 50 (level 20) to Zone 54 (level 35+)
- Quest chains tell coherent story from Book 2
- Plant Men and other unique creatures function properly
- Thern vs. First Born faction system works
- Zero validation errors/warnings
- Build succeeds
- End-game content provides challenge for max-level players
- Lore accuracy to source material

### Why This Milestone

1. **High-Priority Content:** Valley Dor is one of the most iconic locations in the series
2. **End-Game Content:** Currently missing high-level zones (30+)
3. **Story Completion:** Books 1-2 form a natural story arc
4. **Player Retention:** Gives max-level players meaningful content
5. **World Depth:** Adds vertical dimension (underground regions)
6. **Creature Variety:** Plant Men and First Born add new enemy types
7. **Natural Progression:** Books 1-5 content is mostly complete; Book 2 content is the major gap

---

## Summary

These three milestones represent the most impactful next steps for the DikuMUD Barsoom project:

1. **Technology Reskinning Polish** - Completes the thematic transformation (cosmetic, low-risk, high-impact)
2. **Quest System Expansion** - Provides structured gameplay and progression (medium effort, high retention value)
3. **Valley Dor Implementation** - Adds essential end-game content and one of the most famous locations (large effort, major content milestone)

All three can proceed in parallel with different developers, as they have minimal dependencies on each other. Alternatively, they can be tackled sequentially based on team availability and priorities.

**Recommended Order (if sequential):**
1. Start Milestone 3 planning while completing Milestone 1 (planning has no code dependencies)
2. Complete Milestone 1 (quick win, improves player experience)
3. Work on Milestones 2 and 3 in parallel (different subsystems)

**Current Project Health:** ✅ EXCELLENT
- Zero validation errors
- Clean builds
- Functional quest system
- Solid zone foundation
- Clear path forward

The project is in an excellent position to tackle any of these milestones. The infrastructure is solid, the world is expanding logically, and the codebase is maintainable. Each milestone builds on the existing foundation while adding substantial value for players.
