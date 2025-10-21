# Deep Discovery Design Process

## Overview

This document defines a systematic process for enriching DikuMUD zones to reward players who thoroughly explore and interact with every aspect of the game world. The goal is to transform zones with sparse, disconnected flavor text and purposeless objects into coherent, rewarding experiences for "completionist" players who want to discover every secret and use every item.

## The Problem

Many zones currently have:
- **Flavor text without depth**: Descriptions mention objects (compartments, ropes, etc.) that can't be examined or used
- **Purposeless objects**: Items that exist but serve no function in gameplay or quests
- **Disconnected elements**: Room descriptions, objects, and NPCs that don't form a coherent narrative
- **Hidden connections**: Relationships between items that aren't well-clued (e.g., "What is this iron key for?")

This creates a frustrating experience for thorough players and wastes world-building potential.

## The Solution: Deep Discovery

**Deep Discovery** is a zone design methodology that ensures every mentioned element has meaning and every object has purpose. Players who "open every chest" are rewarded with:
- Rich, interconnected storylines
- Puzzles that can be solved through careful observation
- Objects that serve clear purposes (combat, quests, or puzzle-solving)
- Extra descriptions that provide clues and enhance immersion

## The Deep Discovery Process

### Phase 1: Zone Analysis and Storyline Development

**Objective**: Read the zone comprehensively and create a coherent narrative framework that reuses existing content.

#### Steps:

1. **Complete Zone Walkthrough**
   - Visit every room in the zone
   - Read all room descriptions carefully
   - Identify all mentioned objects, features, and NPCs
   - Note all existing extra descriptions
   - List all objects present in the zone (both equipment and flavor items)
   - Map out spatial relationships and zone flow

2. **Identify Existing Elements**
   Create an inventory:
   - **NPCs**: Who is present? What are their roles?
   - **Objects**: What items exist? What are they described as?
   - **Flavor text**: What environmental details are mentioned?
   - **Themes**: What mood or setting does the zone convey?
   - **Quests**: What quests already exist? What items/NPCs do they use?

3. **Develop Core Storyline**
   Write a coherent narrative that:
   - Explains why the zone exists (history, purpose)
   - Defines the main conflict or situation
   - Identifies the zone's primary inhabitants and their relationships
   - Creates natural objectives for players (what would they want to do here?)
   - Incorporates existing NPCs, objects, and flavor text wherever possible

4. **Define Deep Discovery Objectives**
   
   For **casual players** (just passing through):
   - What is the obvious content? (main paths, visible NPCs, basic combat/loot)
   
   For **deep discovery players** (thorough explorers):
   - What secrets can be discovered through careful examination?
   - What puzzles can be solved?
   - What hidden quests or objectives exist?
   - What rare or unique rewards await?

5. **Map Element Connections**
   
   Create a connection map showing:
   - Which flavor text references which objects
   - Which objects are needed for which puzzles/quests
   - Which NPCs relate to which storylines
   - How different areas of the zone interconnect thematically

#### Example: The Sewers (Zone 31)

**Current State Analysis:**
- Flavor text mentions: compartments, spider webs, rope, iron key, dried meat, vermin
- Objects exist: rope (from spiders), iron key, dried meat, various vermin
- Existing quest: Retrieve dried meat for calot feeding (Quest 3003)
- Problem: Rope has no purpose, key's purpose unclear, compartments can't be examined

**Proposed Storyline:**
*The ancient sewers beneath Lesser Helium were once a marvel of engineering, designed by the early Martian builders with hidden maintenance passages and storage compartments. Over centuries, the system fell into disrepair. Now, giant carrion birds nest in the upper tunnels, bringing scraps of meat from their hunts. Banths occasionally venture into the deeper passages, leaving kills behind. Ulsio vermin have made the sewers their home. Most significantly, a maintenance compartment contains an ancient valve wheel that requires a rope to operate - when activated, it drains a flooded chamber, revealing a cache of ancient tools and a hidden passage to deeper sewers.*

**Deep Discovery Objectives:**
- **Casual players**: Kill vermin, retrieve dried meat for quest, basic exploration
- **Deep discovery players**: 
  - Find the iron key in a carrion bird nest
  - Collect rope from spider webs
  - Discover keyword for examining maintenance compartments
  - Use iron key to unlock sealed compartment
  - Use rope with valve wheel to drain flooded chamber
  - Find ancient tool cache and hidden passage
  - Discover deeper sewer levels with rare encounters

### Phase 2: Extra Description Enhancement

**Objective**: Add keyword-based extra descriptions to make every mentioned element examinable and provide clear clues for object use.

#### Design Principles:

1. **Every Noun Gets Keywords**
   - If room description mentions "compartments", add extra description for "compartment", "compartments"
   - If description mentions "valve", add keywords "valve", "wheel", "mechanism"
   - Multiple related keywords should point to the same extra description

2. **Extra Descriptions Should:**
   - Provide sensory details (what does it look like, feel like, smell like?)
   - Offer clues about function or purpose
   - Hint at interaction possibilities without being explicit
   - Maintain the zone's tone and atmosphere
   - Build on the established storyline

3. **Clue Hierarchy** (from subtle to obvious):
   - **Environmental**: General description mentions the element
   - **Examination**: Extra description provides details and hints
   - **Interaction**: Object description or NPC dialogue suggests use
   - **Direct**: Quest text or signs explicitly state purpose

4. **Writing Style**:
   - Use vivid, specific language
   - Avoid anachronistic terms
   - Match the tone of existing descriptions
   - Keep descriptions concise (3-5 sentences typically)
   - Include actionable details

#### Example Extra Descriptions:

**Room: Main Sewer Tunnel**
*Current description mentions: "water channels run along both sides"*

Add extra description:
```yaml
extra_descriptions:
  - keywords: "channel channels water"
    description: |
      The water channels are carved into the stone floor, about a foot deep and 
      running the length of the tunnel. Most are now dry, but fetid pools remain in 
      the lower sections. The channels show remarkable craftsmanship - smooth, even 
      surfaces that must have taken years to complete. Along the eastern channel, 
      you notice what appears to be a maintenance hatch built into the wall.
```

**Room: Spider Den**
*Current description mentions: "massive webs stretch across the chamber"*

Add extra description:
```yaml
extra_descriptions:
  - keywords: "web webs silk"
    description: |
      The spider webs are thick and sticky, stretching from floor to ceiling in 
      elaborate patterns. The silk is remarkably strong - you could probably gather 
      some usable rope from these webs if you had a blade to cut it with. Among 
      the webbing, you notice the wrapped remains of previous victims, including 
      what looks like a small metal object glinting in the dim light.
```

**Room: Maintenance Chamber**
*Adding new examination target based on storyline*

Room description updated to mention: "...ancient machinery lines one wall, long since fallen silent."

Add extra description:
```yaml
extra_descriptions:
  - keywords: "machinery machine valve wheel mechanism"
    description: |
      The machinery is an ancient water control system, covered in rust and grime 
      but still structurally intact. At its center is a large valve wheel mounted 
      on a horizontal axis. The wheel is seized in place - it would need significant 
      force to turn it. You notice a hook above the wheel and markings on the floor 
      suggesting this mechanism was designed to be operated with leverage, perhaps 
      using a rope and weight system.
  - keywords: "compartment compartments storage panel"
    description: |
      Set into the wall is a sealed maintenance compartment with a corroded lock. 
      The lock is ancient but appears functional - it would require an iron key to 
      open. Scratched into the metal is a symbol matching those on the valve 
      mechanism, suggesting this compartment contains parts or tools for the water 
      control system.
```

### Phase 3: Object Purpose Assignment

**Objective**: Ensure every object in the zone has a clear, meaningful purpose.

#### Object Categories:

1. **Combat Items** (weapons, armor)
   - Must have appropriate stats for zone level
   - Should fit zone theme (ancient tools in ruins, military gear in barracks)
   - May have special properties tied to storyline

2. **Consumables** (food, drink, healing items)
   - Should be appropriate to zone (fresh food in cities, dried food in dungeons)
   - May be quest items or required for survival in harsh zones

3. **Quest Items** (direct quest requirements)
   - Essential for completing specific quests
   - Should be clearly obtainable through described means
   - May be rare drops or found in specific locations

4. **Puzzle Items** (tools for solving environmental puzzles)
   - Enable interaction with zone mechanics
   - Should be clued through extra descriptions
   - Create "aha!" moments when purpose is discovered

5. **Loot** (valuable items for selling)
   - Provide economic reward for exploration
   - Should be thematically appropriate
   - May be found in hidden locations or on tough enemies

6. **Lore Items** (books, notes, artifacts with descriptions)
   - Provide backstory and world-building
   - May contain clues for puzzles or quest locations
   - Enhance immersion and reward curious players

#### Object Purpose Checklist:

For each object in the zone, determine:

- [ ] **Primary purpose**: What is this object's main function?
- [ ] **Acquisition method**: How does the player obtain it?
- [ ] **Use case**: When/where/how is it used?
- [ ] **Clue source**: How do players learn about its purpose?
- [ ] **Reward value**: What benefit does using/obtaining it provide?

#### Object Enhancement Guidelines:

1. **Repurpose Existing Objects**
   
   Before creating new objects, check if existing items can serve puzzle/quest needs:
   - Can an existing weapon also be a quest item?
   - Can a "flavor" object become a puzzle tool?
   - Can loot items double as quest objectives?

2. **Add Special Procedures for Puzzle Items**
   
   Objects used in puzzles may need special procedures:
   ```c
   // Example: Rope used with valve
   int spec_ancient_rope(struct char_data *ch, int cmd, char *arg) {
       if (cmd == CMD_USE) {
           // Check if in right room, have rope, etc.
           // Activate valve mechanism
           // Drain flooded chamber
       }
       return FALSE;
   }
   ```

3. **Create Object Interactions**
   
   Design objects that work together:
   - Key + locked compartment = access to cache
   - Rope + valve = drain mechanism
   - Torch + dark passage = reveal hidden details

4. **Make Purpose Clear Through Description**
   
   Object descriptions should hint at use:
   ```yaml
   objects:
     - vnum: 3215
       namelist: "rope ancient silk"
       short_desc: "a coil of strong silk rope"
       long_desc: "A coil of rope made from processed spider silk lies here."
       action_desc: |
         Examining the rope closely, you can see it's remarkably strong and flexible. 
         The ancient Martians used silk rope for heavy machinery - this could easily 
         support significant weight or provide leverage for moving stubborn mechanisms.
   ```

#### Example: Sewers Object Purpose Map

| Object | Current State | Purpose Assignment | Clues |
|--------|---------------|-------------------|--------|
| Dried Meat | Exists, used in Quest 3003 | Quest item for calot feeding | Quest giver mentions it, birds have it |
| Rope | Exists on spiders, no purpose | Puzzle item for valve mechanism | Web extra description mentions cutting rope, valve description mentions leverage |
| Iron Key | Exists, unclear purpose | Unlocks maintenance compartment | Key description mentions "maintenance," compartment description mentions "iron key" |
| Ancient Tools | Not yet created | Reward in drained cache, used for deeper sewer access | Compartment contains them, they're old engineering tools |
| Radium Lamp | Not yet created | Illuminates dark flooded chamber, reveals hidden passage | Found in tool cache, description mentions use in ancient engineering |

### Phase 4: Implementation Documentation

**Objective**: Create a detailed implementation plan that can be used by builders/coders to realize the deep discovery design.

#### Document Structure:

The implementation document should include:

1. **Zone Overview**
   - Zone number and name
   - Current state summary
   - Deep discovery theme and storyline
   - Target player levels and recommended approach

2. **Storyline Summary**
   - The zone's history and purpose
   - Current situation and conflicts
   - Key characters and their roles
   - Deep discovery narrative arc

3. **Room Modifications**
   
   For each room requiring changes:
   ```yaml
   Room: 3155 - Maintenance Chamber
   
   Current description:
   [paste current description]
   
   Proposed description additions:
   "Ancient machinery lines one wall, long since fallen silent. Sealed compartments 
   are visible along the eastern wall."
   
   New extra descriptions:
   - Keywords: "machinery valve wheel"
     Description: [full text]
   - Keywords: "compartment compartments"
     Description: [full text]
   
   Justification:
   Sets up valve puzzle and compartment discovery for deep discovery players.
   ```

4. **Object Changes**
   
   For each object:
   ```yaml
   Object: 3210 - Ancient Rope
   
   Current state: Drops from giant spiders, no specific purpose
   
   Modifications:
   - Update action_desc to hint at mechanical use
   - Add special procedure for valve interaction
   - Update namelist to include "silk rope ancient strong"
   
   Purpose: Puzzle item for operating valve mechanism in room 3155
   
   Code changes required:
   - Create spec_ancient_rope() in spec_procs.c
   - Add valve_mechanism_activate() function
   - Update room 3160 to change flags when valve activated
   
   Clues provided:
   - Web extra description mentions cutting rope
   - Valve extra description mentions leverage/rope system
   - Old tool diagram (lore item) shows rope-based valve operation
   ```

5. **New Content Requirements**
   
   List new content needed:
   - New objects to create (with full specifications)
   - New extra descriptions
   - New special procedures
   - New quest definitions (if applicable)
   - New room flag changes or door additions

6. **Quest Integration**
   
   If new quests are added:
   ```yaml
   Quest: 3199 - Drain the Depths
   
   Type: RETRIEVAL
   Giver: Maintenance Worker (mob 3065, new)
   Target: Ancient Valve Diagram (object 3299, new)
   Duration: 96 MUD hours (2 real hours)
   Rewards: 400 XP, 150 gold, Radium Lamp (object 3298)
   
   Quest flow:
   1. Player asks maintenance worker about sewers
   2. Worker mentions old valve system and missing diagram
   3. Player finds diagram in carrion bird nest (room 3158)
   4. Player returns diagram, receives lamp reward
   5. Lamp can be used to illuminate dark passage (room 3160)
   
   Dependencies:
   - Requires dried meat quest to be completed first (establishes trust)
   - Unlocks deeper sewer access
   ```

7. **Testing Checklist**
   
   Verification steps:
   - [ ] All extra descriptions keywords work
   - [ ] Objects can be found as described
   - [ ] Puzzle sequence can be completed
   - [ ] Clues are present and discoverable
   - [ ] Rewards are appropriate
   - [ ] No dead ends or broken references
   - [ ] Casual player path unaffected
   - [ ] Deep discovery path rewarding

8. **Player Experience Map**
   
   Create two flowcharts:
   
   **Casual Player Experience:**
   ```
   Enter sewers → Kill vermin → Find dried meat → Exit
   Time: 15-20 minutes
   Reward: Quest completion (300 XP, 75 gold)
   ```
   
   **Deep Discovery Experience:**
   ```
   Enter sewers → 
   Examine webs (find rope clue) → 
   Kill spiders, collect rope → 
   Examine machinery (find valve clue) → 
   Search nest (find key) → 
   Unlock compartment (find tools) → 
   Use rope with valve → 
   Drain chamber → 
   Access hidden passage → 
   Discover deeper sewers
   
   Time: 45-60 minutes
   Rewards: 
   - Ancient tools (unique equipment)
   - Access to deeper sewer zone
   - Additional encounters and loot
   - Satisfaction of solving puzzle
   ```

9. **Difficulty and Balance**
   
   Analysis:
   - Deep discovery path should be challenging but fair
   - Clues should be discoverable through systematic exploration
   - Puzzle should be solvable by reading extra descriptions
   - Rewards should justify the time investment
   - Should not break zone level balance

10. **Lore and Theme Consistency**
    
    Verification:
    - Does this fit with established Barsoom/zone lore?
    - Are descriptions consistent with existing tone?
    - Do new elements enhance or detract from atmosphere?
    - Are item names and descriptions thematically appropriate?

## Integration with Existing Systems

### Quest System Integration

Deep discovery design works with the existing quest system (see [QUESTING_DESIGN.md](docs/design/QUESTING_DESIGN.md)):

- **Discovery quests** (QUEST_EXPLORE): Reward finding hidden locations
- **Retrieval quests** (QUEST_RETRIEVAL): Can use puzzle items as quest objects
- **Hidden quests**: Not advertised by obvious quest givers, discovered through exploration

Example:
```yaml
quests:
  - qnum: 3199
    giver: 3065  # Maintenance worker (not obvious quest giver)
    type: 62     # RETRIEVAL
    duration: 96
    item: 3299   # Valve diagram
    flags: 0     # Hidden quest - no quest marker on NPC
    reward_exp: 400
    reward_gold: 150
    reward_item: 3298  # Radium lamp
    quest_text: |
      "You seem capable. I've been searching for the old engineering diagrams for 
      the valve system. The carrion birds may have carried one to their nests. 
      Find it, and I'll give you something useful."
    complete_text: |
      "Excellent! This is exactly what I needed. Take this radium lamp - it will 
      help you explore the darker passages down here."
```

### World Building Integration

Deep discovery follows YAML zone format (see [WORLD_BUILDING.md](docs/design/WORLD_BUILDING.md)):

- All modifications use standard YAML structure
- Extra descriptions use existing format
- Objects follow established patterns
- Changes are validated before building

### Special Procedures

Puzzle items may require special procedures:

```c
// In spec_procs.c

int spec_maintenance_valve(struct char_data *ch, int cmd, char *arg) {
    struct obj_data *obj;
    
    if (cmd != CMD_USE)
        return FALSE;
    
    // Check if player has rope
    if (!(obj = get_obj_in_list_vis(ch, "rope", ch->carrying))) {
        send_to_char("You need something to provide leverage.\n\r", ch);
        return TRUE;
    }
    
    // Check if in correct room
    if (ch->in_room != real_room(3155)) {
        return FALSE;
    }
    
    // Activate valve
    send_to_char("You secure the rope to the valve wheel and pull with all your might!\n\r", ch);
    act("$n uses a rope to turn an ancient valve mechanism!", 
        FALSE, ch, 0, 0, TO_ROOM);
    
    // Extract rope (consumed in use)
    extract_obj(obj);
    
    // Change room 3160 from flooded to drained
    // This would require additional game state management
    world[real_room(3160)].sector_type = SECT_INSIDE; // Was SECT_WATER_NOSWIM
    
    // Notify of change
    send_to_char("You hear the sound of rushing water from the south!\n\r", ch);
    
    return TRUE;
}
```

## Deep Discovery Best Practices

### Do's:

✅ **Reuse existing content** wherever possible
✅ **Create logical connections** between elements
✅ **Provide progressive clues** from subtle to clear
✅ **Reward thoroughness** with unique items or access
✅ **Maintain theme consistency** with zone and setting
✅ **Test the discovery path** to ensure it's solvable
✅ **Balance effort and reward** appropriately
✅ **Document everything** clearly for implementation

### Don'ts:

❌ **Don't make puzzles too obscure** - clues should be discoverable
❌ **Don't create dead ends** - every clue should lead somewhere
❌ **Don't break casual player experience** - basic path must remain viable
❌ **Don't add content that doesn't fit** the established lore
❌ **Don't make puzzles require meta-knowledge** - everything needed should be in-game
❌ **Don't forget to balance rewards** - unique but not overpowered
❌ **Don't leave objects without purpose** - every item should have a use
❌ **Don't create impossible interactions** - mechanics must be implementable

## Example: Complete Deep Discovery Plan

### Zone: Lesser Helium Sewers (Zone 31)

#### Phase 1: Storyline

**Zone History:**
The sewers were built 1,000 years ago by Helium's finest engineers as an advanced waste management and water reclamation system. They included maintenance passages, emergency drainage systems, and equipment caches for repairs. When Helium expanded, newer systems were built and these ancient sewers were abandoned. Over centuries, they became home to vermin, giant spiders, and carrion birds. The maintenance systems are still functional but forgotten.

**Current Situation:**
- Ulsio vermin infest the upper tunnels
- Giant spiders have woven webs in side passages
- Carrion birds nest in higher chambers, bringing back kills
- A flooded passage blocks access to the lower maintenance level
- Ancient machinery remains functional but inactive

**Key Elements:**
- Dried meat (from birds) - already used in Quest 3003
- Spider silk rope - can be harvested from webs
- Iron key - hidden in bird nest, opens maintenance compartment
- Maintenance compartment - contains ancient tools and diagrams
- Valve mechanism - drains flooded passage when operated with rope
- Flooded chamber - blocks lower sewer access until drained
- Lower sewer level - contains unique encounters and ancient cache

**Objectives:**

*Casual players:*
- Clear vermin for guard training quest (Quest 3001)
- Collect dried meat for beast handler (Quest 3003)

*Deep discovery players:*
- Discover maintenance system storyline
- Collect components (rope, key)
- Solve valve puzzle
- Access lower sewers
- Find ancient engineering cache with unique reward

#### Phase 2: Extra Descriptions

**Room 3151 - Main Sewer Tunnel**
```yaml
extra_descriptions:
  - keywords: "channel channels water"
    description: |
      The stone channels are precisely carved, showing the exceptional skill of 
      ancient Martian engineers. Along the eastern wall, partially obscured by 
      slime and debris, you notice what might be a maintenance access panel.
  - keywords: "panel access door maintenance"
    description: |
      The maintenance panel is made of corroded metal with an ancient lock. 
      It would require an iron key to open. Faded symbols on the panel match 
      markings you've seen on old Martian engineering equipment.
```

**Room 3158 - Carrion Bird Nest**
```yaml
extra_descriptions:
  - keywords: "nest debris remains"
    description: |
      The nest is a chaotic collection of bones, scraps of leather, and stolen 
      items the birds have collected. Among the debris, something metallic glints - 
      it looks like an old iron key, probably dropped here by a previous victim of 
      the birds.
```

**Room 3155 - Eastern Junction** (modified)
```yaml
extra_descriptions:
  - keywords: "machinery valve wheel mechanism control"
    description: |
      An ancient water control mechanism is built into the wall. At its center is a 
      large valve wheel, heavily corroded but still intact. The wheel is seized tight - 
      it would require significant leverage to turn. Above the wheel is a metal hook, 
      and grooves in the floor suggest this was designed to be operated using a rope-
      and-pulley system for mechanical advantage.
```

**Room 3160 - Southern Passage** (current: flooded)
```yaml
extra_descriptions:
  - keywords: "water flood drain"
    description: |
      The passage is completely flooded with stagnant water, too deep and foul to 
      wade through safely. The water level appears artificial - this section could 
      probably be drained if the ancient control systems were still functional.
```

#### Phase 3: Object Purposes

**Object 3210 - Ancient Rope**
```yaml
Current: Drops from giant spiders
Purpose: Puzzle item for valve mechanism
Modifications:
  - Update action_desc to hint at mechanical use
  - Add keywords: "silk rope ancient strong"
  - Special procedure for USE command at valve
Clues:
  - Web extra description mentions cutting rope
  - Valve extra description mentions leverage system
```

**Object 3215 - Iron Key** (existing)
```yaml
Current: Exists but unclear purpose
Purpose: Opens maintenance compartment panel
Modifications:
  - Update long_desc: "An old iron key with Martian engineering symbols."
  - Update action_desc: "This key shows signs of age but appears functional. The 
    symbols match those found on ancient Martian machinery and maintenance panels."
  - Ensure it's obtainable from carrion bird nest
Clues:
  - Key description mentions "machinery and maintenance panels"
  - Panel description mentions "iron key"
  - Nest extra description reveals key location
```

**Object 3298 - Radium Lamp** (new)
```yaml
Type: LIGHT
Purpose: Illuminates dark passages, quest reward
Stats:
  - Provides light in dark rooms
  - Lasts 50 hours of use
  - Can be refilled with radium (rare commodity)
Acquisition: Reward for valve diagram quest OR found in maintenance compartment
Description: "This ancient engineering lamp uses radium to produce a steady, 
eerie green glow that never flickers."
```

**Object 3299 - Valve Diagram** (new)
```yaml
Type: TREASURE
Purpose: Quest item for hidden quest
Location: Carrion bird nest (room 3158), rare chance
Description: "An ancient technical diagram showing the operation of water control 
valves, including detailed illustrations of the rope-and-leverage system used to 
turn seized mechanisms."
```

**Object 3295 - Ancient Tool Set** (new)
```yaml
Type: TREASURE (high value)
Purpose: Valuable reward for deep discovery
Location: Maintenance compartment (room 3151, after opened with key)
Stats:
  - Worth 500 gold
  - Can be sold or kept as trophy
  - Action description provides lore about ancient engineers
Description: "A set of precision engineering tools from the early days of Helium, 
carefully preserved in a sealed compartment. These would be valuable to collectors 
or modern engineers."
```

#### Phase 4: Implementation Plan

**Summary:**
Transform sewers from simple combat/quest zone into deep discovery area with engineering theme and valve puzzle.

**Required Changes:**

1. **Room Modifications:**
   - Room 3151: Add extra descriptions for channel, maintenance panel
   - Room 3155: Add machinery/valve extra descriptions
   - Room 3158: Add nest extra description revealing key
   - Room 3160: Add flooding extra description

2. **New Objects:**
   - Object 3298: Radium Lamp (reward item)
   - Object 3299: Valve Diagram (quest item)
   - Object 3295: Ancient Tool Set (treasure)

3. **Modified Objects:**
   - Object 3210: Rope - update descriptions, add special procedure
   - Object 3215: Iron Key - update descriptions, clarify purpose

4. **Special Procedures:**
   - `spec_maintenance_valve()` - handles rope + valve interaction
   - `spec_maintenance_panel()` - handles key + panel interaction
   - Update to room 3160 state management (flooded → drained)

5. **Optional Quest:**
   ```yaml
   Quest 3199 - The Valve System
   Type: RETRIEVAL
   Giver: New NPC "Maintenance Worker" (mob 3065) in room 3151
   Target: Valve Diagram (object 3299)
   Reward: Radium Lamp (object 3298), 400 XP, 150 gold
   ```

**Testing Checklist:**
- [ ] Can examine channels and find panel hint
- [ ] Can examine panel and learn about key requirement
- [ ] Can examine nest and find key
- [ ] Key successfully opens panel
- [ ] Tools are inside panel compartment
- [ ] Can examine machinery and learn about valve
- [ ] Rope can be used with valve (special procedure works)
- [ ] Room 3160 changes state when valve activated
- [ ] Can access lower sewers after draining
- [ ] Optional quest flow works correctly
- [ ] Casual player experience (basic quests) unaffected

**Player Experience:**

*Casual path:* 
15-20 minutes, complete existing quests

*Deep discovery path:*
1. Complete basic quests to learn sewers
2. Notice extra description hints
3. Examine webs → discover rope can be cut
4. Kill spiders, obtain rope (object 3210)
5. Search nest → find iron key (object 3215)
6. Examine channels → discover maintenance panel
7. Use key on panel → obtain ancient tools (object 3295)
8. Examine machinery → learn about valve system
9. Use rope with valve → activate drainage
10. Access room 3160 (now drained)
11. Discover lower sewer entrance
12. Optional: Find diagram for bonus quest/lamp

Total time: 45-60 minutes
Rewards: Unique items, zone access, puzzle satisfaction

## Conclusion

The Deep Discovery Design process transforms zones from simple combat arenas into rich, rewarding experiences for thorough players. By following this four-phase approach:

1. **Develop coherent storylines** that reuse existing content
2. **Add meaningful extra descriptions** that provide clues
3. **Give every object a purpose** (combat, quest, puzzle, loot, or lore)
4. **Create detailed implementation plans** for builders

We ensure that "completionist" players who explore every corner and examine every detail are rewarded with deeper understanding, unique items, and satisfying puzzle solutions - all while maintaining the quality experience for casual players who just want basic quests and combat.

This approach respects player effort, rewards curiosity, and creates a more immersive and interconnected game world.
