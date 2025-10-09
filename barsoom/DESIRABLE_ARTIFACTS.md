# Desirable Artifacts of Barsoom

This design document catalogs the most coveted artifacts, treasures, and unique items in the Barsoom MUD. These are the objects that players will quest for, fight over, and remember long after obtaining them. Each artifact is specified with complete game mechanics, level appropriateness, rarity limits, and spawn locations.

## Design Philosophy

**Artifact Distribution:**
- Items must feel earned and special, not randomly dropped
- Rarity limits prevent over-saturation and maintain value
- Level-appropriate placement ensures progression feels rewarding
- Spawn locations tie to lore and create compelling exploration goals

**Balance Principles:**
- Low-level artifacts provide useful bonuses without overshadowing progression
- Mid-level artifacts enable new playstyles or strategies
- High-level artifacts are game-changing but not game-breaking
- Unique artifacts have story significance beyond raw stats

**Acquisition Methods:**
- Quest rewards (primary method for major artifacts)
- Boss drops (for combat-focused artifacts)
- Exploration discoveries (for ancient/hidden artifacts)
- Puzzle solutions (for scientific/mysterious artifacts)
- Zone resets with strict limits (for renewable but rare items)

---

## Level 1-10: Novice Artifacts

These artifacts are appropriate for beginning adventurers exploring the easier regions of Barsoom. They provide modest but noticeable advantages.

### 1. Tars Tarkas's Practice Sword

**Description:** A well-worn training blade from the great Thark chieftain's early days. Still sharp and serviceable, it bears the marks of countless practice sessions.

**Game Specs:**
- **Type:** ITEM_WEAPON
- **Damage:** 1d8+1 (slightly better than starting equipment)
- **Weight:** 8 lbs
- **Value:** 500 gold
- **Affects:** None
- **Wear Location:** WIELD
- **Flags:** MAGIC (to hit magical creatures)
- **Object Values:** [3, 1, 8, 3] (weapon type 3 = slash)

**Level Range:** 1-10 (optimal for levels 3-6)

**Rarity:** RARE (max 3 in game world)

**Spawn Location:** Thark Territory (zone 1200), given as quest reward from Sola for helping protect white ape prisoners. Respawn: 30 minutes if all instances removed.

**Why Players Want It:** First easily-obtainable magical weapon for Warriors and Nobles. The connection to Tars Tarkas gives it prestige value. Better than starting equipment but not so powerful it trivializes early content.

---

### 2. Kantos Kan's Navigation Charts

**Description:** Detailed air charts showing safe routes between Helium and Zodanga, with notes on landmarks and emergency landing sites.

**Game Specs:**
- **Type:** ITEM_NOTE
- **Weight:** 1 lb
- **Value:** 300 gold
- **Affects:** +2 WIS when held
- **Wear Location:** HOLD
- **Flags:** MAGIC
- **Extra Description:** Reveals hidden room exits when examined (scripted effect)

**Level Range:** 1-10 (optimal for levels 2-8)

**Rarity:** RARE (max 5 in game world)

**Spawn Location:** Lesser Helium (zone 3600), found in the naval academy archives. Requires passing an easy Intelligence check or having Scholar class. Respawn: 45 minutes.

**Why Players Want It:** Useful for all classes. The +2 WIS helps Scientists and Nobles. The ability to reveal hidden exits aids exploration. Light weight makes it easy to carry.

---

### 3. Pilgrim's Gold Necklace

**Description:** A beautiful necklace seized from a pilgrim by the Therns. Gold chain with rubies, still bearing traces of its original owner's hopes.

**Game Specs:**
- **Type:** ITEM_TREASURE
- **Weight:** 1 lb
- **Value:** 800 gold
- **Affects:** +1 CHA
- **Wear Location:** NECK
- **Flags:** MAGIC, GLOW (faint)

**Level Range:** 1-10 (optimal for levels 4-9)

**Rarity:** COMMON in Valley Dor (max 10 instances), UNIQUE elsewhere

**Spawn Location:** Valley Dor area (when implemented), looted from Thern treasure hoards. Lesser versions can be found in Greater Helium noble quarters.

**Why Players Want It:** Good value for selling or wearing. The +1 CHA helps Nobles with their leadership abilities. Light and wearable. Story connection to the tragic pilgrims.

---

### 4. Sola's Lucky Anklet

**Description:** A delicate anklet worn by the compassionate Thark female. She claims it brought her good fortune.

**Game Specs:**
- **Type:** ITEM_WORN
- **Weight:** 0.5 lbs
- **Value:** 400 gold
- **Affects:** +1 DEX, +5% chance to resist tripping/bash
- **Wear Location:** ANKLE
- **Flags:** MAGIC

**Level Range:** 1-10 (optimal for levels 5-10)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Thark Territory, given as reward for completing a series of quests helping Sola protect weaker members of the tribe. One-time reward, does not respawn.

**Why Players Want It:** The only +DEX item easily available at low levels. The bash resistance is useful in PvE and PvP. Being unique gives it prestige. Connection to beloved character Sola.

---

### 5. Ancient Green Warrior's Helm

**Description:** A massive helm sized for a four-armed green Martian warrior. Ancient and battle-scarred but still protective.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 5 lbs
- **Value:** 600 gold
- **Affects:** AC -2 (better armor), +1 CON
- **Wear Location:** HEAD
- **Flags:** MAGIC
- **Restrictions:** Warriors only (too heavy/awkward for other classes)

**Level Range:** 1-10 (optimal for levels 6-10)

**Rarity:** RARE (max 4 in game world)

**Spawn Location:** Thark Territory dead city ruins, Warhoon territory, or dropped by green jeddak bosses. Respawn: 60 minutes.

**Why Players Want It:** Best head armor available at this level range for Warriors. The +CON helps survivability. Distinctive green Martian aesthetic. Class restriction makes it feel special for Warriors.

---

### 6. Dejah Thoris's Study Notes

**Description:** Pages from the princess's astronomy and science journals, filled with equations and observations.

**Game Specs:**
- **Type:** ITEM_NOTE
- **Weight:** 1 lb
- **Value:** 700 gold
- **Affects:** +2 INT when held, +10% to scientific skill checks
- **Wear Location:** HOLD
- **Flags:** MAGIC, GLOW (soft golden light)

**Level Range:** 1-10 (optimal for levels 5-10)

**Rarity:** RARE (max 3 in game world)

**Spawn Location:** Greater Helium royal palace library. Requires completing a fetch quest for the librarian. Respawn: 90 minutes.

**Why Players Want It:** Excellent for Scientists. The +2 INT affects spell/ability success rates. Skill bonus helps with crafting/repair/identification. Connection to Dejah Thoris. Can be used while wielding a weapon.

---

### 7. Radium Lamp of Unusual Brightness

**Description:** A superior radium lamp that shines brighter and longer than common models.

**Game Specs:**
- **Type:** ITEM_LIGHT
- **Weight:** 3 lbs
- **Value:** 300 gold
- **Affects:** Illuminates 2 rooms away (vs normal 1), +1 to spot hidden/detect invisible
- **Wear Location:** LIGHT
- **Flags:** MAGIC, GLOW
- **Object Values:** [0, 0, 500, 0] (500 hours of light)

**Level Range:** 1-10 (useful at all levels)

**Rarity:** RARE (max 8 in game world)

**Spawn Location:** Greater Helium marketplace, Lesser Helium craftsman shops, Atmosphere Factory. Can be purchased for 300 gold or found as minor loot. Respawn: 30 minutes.

**Why Players Want It:** Essential for dungeon delving. Extra range prevents ambushes. Long duration reduces micromanagement. The spot bonus helps find secrets. Relatively inexpensive makes it accessible.

---

## Level 11-20: Journeyman Artifacts

These artifacts represent significant power increases and enable new strategies. Players at this level are exploring dangerous territories and facing serious challenges.

### 8. Gor Hajus's Assassin Blade

**Description:** The famed blade of the legendary assassin of Toonol. Short, perfectly balanced, and wickedly sharp.

**Game Specs:**
- **Type:** ITEM_WEAPON
- **Weight:** 4 lbs
- **Value:** 3000 gold
- **Damage:** 2d6+2
- **Affects:** +2 DEX when wielded, Backstab damage multiplier +1 (x3 becomes x4)
- **Wear Location:** WIELD
- **Flags:** MAGIC, HUM
- **Restrictions:** Assassins preferred (others can use but without DEX bonus)

**Level Range:** 11-20 (optimal for levels 12-18)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Toonol (when zone implemented), found in Gor Hajus's secret cache after completing his questline about regaining his body. One-time reward.

**Why Players Want It:** Best assassin weapon in this level range. The backstab multiplier boost is significant. +2 DEX helps all Assassin abilities. Being unique makes it a status symbol. Strong lore connection.

---

### 9. Crown of a Lesser Jeddak

**Description:** The crown of a city-state ruler. Not as grand as the Warlord's crown, but still a symbol of legitimate authority.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 2 lbs
- **Value:** 5000 gold
- **Affects:** +2 CHA, +1 WIS, AC -1, Charm person spell 3x/day
- **Wear Location:** HEAD
- **Flags:** MAGIC, GLOW, ANTI_EVIL
- **Restrictions:** Nobles preferred (others can wear but CHA bonus reduced to +1)

**Level Range:** 11-20 (optimal for levels 14-20)

**Rarity:** RARE (max 3 in game world - different cities have different crowns)

**Spawn Location:** Zodanga palace throne room (Sab Than's crown), Ptarth palace, or Kaol palace. Drops from jeddak bosses or obtained through royal succession questlines. Does not respawn once looted.

**Why Players Want It:** Excellent for Noble class. Multiple stat bonuses. The charm spell is useful utility. Anti-evil restriction means it must be earned through good actions. Each crown is tied to a major city's storyline.

---

### 10. Ras Thavas's Surgical Kit

**Description:** A complete set of the Master Mind's precision instruments. The tools that have performed countless brain transplants.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 8 lbs
- **Value:** 4000 gold
- **Affects:** +3 INT when held, +20% to surgery/healing skill checks, Cure Serious Wounds spell 5x/day
- **Wear Location:** HOLD
- **Flags:** MAGIC, HUM (faint mechanical sound)
- **Restrictions:** Scientists only

**Level Range:** 11-20 (optimal for levels 11-20)

**Rarity:** RARE (max 2 in game world)

**Spawn Location:** Toonol laboratories. One can be earned by completing a difficult series of quests for Ras Thavas. Another might be stolen from a competitor's lab. Respawn: Never (must be earned through quests).

**Why Players Want It:** Essential for high-level Scientist gameplay. The healing spell makes Scientists viable party healers. +INT improves all scientific abilities. The skill bonus is significant for success rates. Heavy but worth carrying.

---

### 11. Tara's Escape Harness

**Description:** The jeweled harness worn by Tara of Helium when she escaped from Manator. Enhanced with hidden compartments and emergency tools.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 6 lbs
- **Value:** 3500 gold
- **Affects:** +1 DEX, +1 CHA, AC -2, Invisibility spell 1x/day, Hidden knife (1d4 damage, always available)
- **Wear Location:** BODY
- **Flags:** MAGIC, GLOW
- **Anti-flags:** ANTI_MALE (sized for female characters)

**Level Range:** 11-20 (optimal for levels 13-19)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Manator palace, found in Tara's former prison chamber after defeating O-Mai the Cruel. One-time reward.

**Why Players Want It:** Excellent multi-purpose item. Good AC for non-warriors. The invisibility spell is clutch for escapes. Hidden knife is a backup weapon. Strong connection to Tara's dramatic escape. Gender restriction makes it special for female PCs.

---

### 12. Phor Tak's Invisibility Device (Lesser)

**Description:** One of the brilliant but mad inventor's earlier invisibility prototypes. Not as reliable as his later work, but functional.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 4 lbs
- **Value:** 6000 gold
- **Affects:** Invisibility spell 3x/day (15 minute duration), 10% chance of malfunction (becomes visible for 1 round)
- **Wear Location:** HOLD or attach to BODY
- **Flags:** MAGIC, HUM (mechanical whirring)

**Level Range:** 11-20 (optimal for levels 15-20)

**Rarity:** RARE (max 4 in game world)

**Spawn Location:** Jhama (Phor Tak's city), found in laboratories or workshops. Some may have been stolen and are held by thieves or spies. Respawn: 120 minutes if all instances removed.

**Why Players Want It:** Invisibility is powerful for all classes. Multiple uses per day. The malfunction adds risk/reward. Less powerful than the unique perfect version. Ties into Phor Tak's storyline.

---

### 13. Carthoris's Directional Compass (Replica)

**Description:** A working replica of the prince's revolutionary navigation device. Not as sophisticated as the original but still impressive.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 5 lbs
- **Value:** 4500 gold
- **Affects:** +2 WIS when held, Reveals map of current zone, Auto-navigation within current zone (move to any room without walking)
- **Wear Location:** HOLD
- **Flags:** MAGIC, HUM (ticking/clicking sounds)
- **Restrictions:** Scientists and Nobles preferred (others can use with reduced effectiveness)

**Level Range:** 11-20 (optimal for levels 12-18)

**Rarity:** RARE (max 5 in game world)

**Spawn Location:** Greater Helium palace workshops, can be commissioned from master craftsmen for 4500 gold plus materials quest. Respawn: Never (must be crafted through quest).

**Why Players Want It:** Excellent exploration aid. Zone maps are very useful. Auto-navigation saves time and reduces danger. Lore connection to Carthoris. Useful for all classes but especially Scientists/Nobles.

---

### 14. Kantos Kan's Naval Cutlass

**Description:** The trusted blade of Helium's greatest naval commander. Battle-tested and reliable.

**Game Specs:**
- **Type:** ITEM_WEAPON
- **Weight:** 7 lbs
- **Value:** 3200 gold
- **Damage:** 2d8+1
- **Affects:** +1 STR when wielded, +10% to hit when fighting on airships or ships
- **Wear Location:** WIELD
- **Flags:** MAGIC, GLOW (faint red)

**Level Range:** 11-20 (optimal for levels 13-19)

**Rarity:** RARE (max 3 in game world)

**Spawn Location:** Greater Helium naval academy, awarded for completing naval training quests or obtained from naval battles. Respawn: 90 minutes.

**Why Players Want It:** Strong damage for mid-level Warriors. The +STR bonus is universally useful. The shipboard bonus encourages airship combat encounters. Kantos Kan connection. Helium prestige item.

---

### 15. Thuvia's Bracelet of Loyalty

**Description:** A delicate bracelet given to Thuvia by her father. It bears the crest of Ptarth and symbolizes family bonds.

**Game Specs:**
- **Type:** ITEM_WORN
- **Weight:** 0.5 lbs
- **Value:** 2800 gold
- **Affects:** +2 CHA, +1 WIS, Charm Person 2x/day, +10% to resist fear effects
- **Wear Location:** WRIST
- **Flags:** MAGIC, GLOW (soft blue)

**Level Range:** 11-20 (optimal for levels 11-17)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Ptarth palace (when zone implemented), given as a reward for completing Thuvia's storyline quest involving Kulan Tith and Carthoris. One-time reward.

**Why Players Want It:** Excellent for Nobles. Good stat combination. Charm spell is useful. Fear resistance helps in many encounters. Light weight. Strong emotional lore connection to Thuvia's story.

---

## Level 21-30: Expert Artifacts

These artifacts are powerful tools for experienced adventurers tackling the most dangerous zones and enemies. They significantly alter playstyle and enable advanced strategies.

### 16. Sword of John Carter

**Description:** One of the legendary Earthman's favored blades. Perfectly balanced, impossibly sharp, and bearing the marks of countless battles against Barsoom's greatest warriors.

**Game Specs:**
- **Type:** ITEM_WEAPON
- **Weight:** 6 lbs
- **Value:** 15000 gold
- **Damage:** 3d8+3
- **Affects:** +3 STR, +2 DEX, +20 HP, Haste 1x/day (doubles attacks for 5 rounds)
- **Wear Location:** WIELD
- **Flags:** MAGIC, GLOW (bright red), GOOD (alignment attuned)
- **Anti-flags:** ANTI_EVIL (burns evil wielders for 2d6 damage per round)

**Level Range:** 21-30 (optimal for levels 22-28)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Greater Helium royal palace, deep in John Carter's personal quarters. Requires completing the major "Warlord's Trust" questline proving yourself worthy. One-time reward that never respawns.

**Why Players Want It:** Best sword available before epic level. Multiple stat bonuses. Excellent damage. Haste ability is game-changing. Strong lore significance. The evil restriction ensures only heroes wield it. Ultimate Warrior trophy.

---

### 17. Crown of the Warlord

**Description:** The supreme symbol of authority over all Mars. Forged from the metals of all Martian races and set with jewels representing every nation. Worn only by John Carter, Warlord of Barsoom.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 3 lbs
- **Value:** PRICELESS (cannot be sold)
- **Affects:** +3 CHA, +3 WIS, +2 INT, +2 STR, AC -3, Command 5x/day (charm + fear on enemies), Inspire Allies 3x/day (+2 to all rolls for party, 10 rounds)
- **Wear Location:** HEAD
- **Flags:** MAGIC, GLOW (brilliant multi-colored), GOOD, ANTI_DROP (cannot drop or give away)
- **Anti-flags:** ANTI_EVIL (instant death if worn by evil character)
- **Restrictions:** Level 25+ only, must have earned through completing main questline

**Level Range:** 25-30+ (optimal for level 28+)

**Rarity:** UNIQUE (only 1 in game, only 1 player can possess at a time)

**Spawn Location:** Not a drop - awarded by John Carter himself as the culmination of the game's primary questline. Requires uniting the races of Mars and defeating a world-threatening menace. If the player dies or retires, the crown returns to John Carter for the next worthy hero.

**Why Players Want It:** Ultimate artifact of the game. Multiple powerful bonuses. Game-changing abilities. Cannot be lost easily. Represents completion of main story. Status symbol visible to all players. Wearing it marks you as the server's champion.

---

### 18. Ras Thavas's Master Surgical Set

**Description:** The complete collection of the Master Mind's instruments, including rare tools found nowhere else. Capable of performing brain transplants, creating synthetic men, and other near-miraculous procedures.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 12 lbs
- **Value:** 20000 gold
- **Affects:** +4 INT, +2 WIS, +30% to all medical skill checks, Heal 10x/day, Cure Disease/Poison 5x/day, Restore Lost Limbs 1x/week, Brain Transfer ritual enabled
- **Wear Location:** HOLD (two-handed when in use)
- **Flags:** MAGIC, HUM (complex mechanical sounds)
- **Restrictions:** Scientists only, Level 22+

**Level Range:** 22-30+ (optimal for levels 22+)

**Rarity:** UNIQUE (only 1 complete set in game)

**Spawn Location:** Toonol, Ras Thavas's private laboratory. Must complete the entire Master Mind questline, demonstrating surgical skill and ethical judgment. The questline involves difficult moral choices. One-time reward.

**Why Players Want It:** Makes Scientist the premier healing class. Enables unique roleplay (brain transfers). Restore limbs is game-changing. Exceptional stat bonuses. The weight is a meaningful trade-off. Ties into one of Barsoom's most memorable storylines.

---

### 19. Phor Tak's Perfect Invisibility Device

**Description:** The mad genius's ultimate achievement. Unlike his earlier prototypes, this version has no flaws or chance of malfunction.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 3 lbs
- **Value:** 25000 gold
- **Affects:** Invisibility at will (no charges, toggle on/off), Invisible while attacking (first strike from invisibility), +3 DEX, Perfect Stealth (+50% to sneak/hide)
- **Wear Location:** HOLD or BODY (can be integrated into harness)
- **Flags:** MAGIC, HUM (nearly silent)

**Level Range:** 21-30 (optimal for levels 23-29)

**Rarity:** UNIQUE (only 1 perfect device in game)

**Spawn Location:** Jhama, in Phor Tak's heavily trapped personal laboratory. Requires solving complex puzzles and surviving deadly defenses. Or, can be stolen from Tul Axtar's forces who took it from Phor Tak. Either path is extremely difficult.

**Why Players Want It:** Best stealth item in game. Unlimited invisibility is incredibly powerful. Attacking while invisible is game-changing for Assassins. +DEX is useful. Lightweight. Major questline reward. Ties into book "A Fighting Man of Mars."

---

### 20. The Atmosphere Plant Master Control Rod

**Description:** The ancient device that controls all life on Mars. This is not the original (which cannot be moved) but a master override key that grants control authority.

**Game Specs:**
- **Type:** ITEM_KEY
- **Weight:** 5 lbs
- **Value:** PRICELESS (world-changing artifact)
- **Affects:** Grants access to Atmosphere Plant control room, Allows operation of plant controls, +2 INT, +2 WIS, Breathable Air 3x/day (party-wide safe breathing in any environment for 1 hour)
- **Wear Location:** HOLD
- **Flags:** MAGIC, GLOW (pulsing red), ANTI_DROP
- **Restrictions:** Must complete Atmosphere Plant questline, Level 24+

**Level Range:** 24-30+ (optimal for level 26+)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Atmosphere Factory (zone 5000), hidden in the deepest chamber after defeating the corrupted guardian AI. Requires solving engineering puzzles and surviving environmental hazards. Part of a critical world-saving questline.

**Why Players Want It:** Story significance (controls Mars's air). Access to unique zones. Party-wide buff is very useful. The questline is memorable. Holding it marks you as someone who saved the world. Can be used as leverage in negotiations.

---

### 21. Harness of the Jeddak of Jeddaks

**Description:** The ceremonial battle harness worn by the ruler of all Mars. Crafted from the finest materials of every Martian race, it combines protection with majestic appearance.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 8 lbs
- **Value:** 18000 gold
- **Affects:** +2 STR, +2 CON, +2 CHA, AC -4, +25 HP, Damage Resistance 10%, Aura of Command (enemies morale -2, allies morale +2)
- **Wear Location:** BODY
- **Flags:** MAGIC, GLOW (multi-colored radiance), GOOD
- **Anti-flags:** ANTI_EVIL

**Level Range:** 21-30 (optimal for levels 23-30)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Greater Helium, awarded by Tardos Mors (Jeddak of Helium) for completing the "Unification of Mars" questline that requires earning the respect of multiple Martian races. One-time reward.

**Why Players Want It:** Best body armor for Warriors and Nobles. Multiple stat bonuses. Damage resistance is powerful. Aura affects all combats. Excellent AC. Lore significance. Visual indication of high status.

---

### 22. Thuvia's Phantom Bowl

**Description:** An ancient Lotharian artifact connected to the creation of phantom creatures. With proper training, it allows the user to manifest phantom warriors.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 4 lbs
- **Value:** 12000 gold
- **Affects:** +2 WIS, +2 CHA, Summon Phantom Warrior 3x/day (warrior with 75% of summoner's combat ability, lasts 30 minutes), Phantom bowmen 1x/day (3 archers, 20 minutes)
- **Wear Location:** HOLD
- **Flags:** MAGIC, GLOW (ghostly green)
- **Restrictions:** Nobles and Scientists preferred, others must pass INT check to use

**Level Range:** 21-30 (optimal for levels 21-28)

**Rarity:** RARE (max 2 in game world)

**Spawn Location:** Lotharian ruins (when zone implemented), found in ancient temples after completing puzzles about the nature of reality and belief. Alternatively, one might be held by Tario's descendant. Respawn: Never.

**Why Players Want It:** Summons are powerful force multipliers. Ties into memorable Lotharian storyline. Good for solo players. Nobles get extra value from CHA bonus. Unique mechanics. Ancient mystery vibe.

---

### 23. Dejah Thoris's Star Charts

**Description:** The princess's personal astronomical charts, containing her groundbreaking calculations and observations of Mars's moons and surrounding space.

**Game Specs:**
- **Type:** ITEM_NOTE
- **Weight:** 2 lbs
- **Value:** 8000 gold
- **Affects:** +3 INT, +2 WIS when held, Perfect Navigation (never get lost, always know location), Predict Events 1x/day (learn one future event relevant to current quest), Astral Knowledge (+20% to all knowledge checks)
- **Wear Location:** HOLD
- **Flags:** MAGIC, GLOW (silvery starlight)

**Level Range:** 21-30 (optimal for levels 22-29)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Greater Helium royal observatory, given by Dejah Thoris herself after completing her personal questline involving astronomical crisis threatening Mars. Requires high INT to understand her work.

**Why Players Want It:** Excellent for Scientists. Perfect navigation is huge QoL improvement. Predict Events is powerful for quest planning. Strong connection to Dejah Thoris. Light weight. Multiple useful bonuses.

---

### 24. Matai Shang's Ring of Command

**Description:** The Holy Hekkador's ring of authority over the Thern faith. Set with a massive white diamond, it radiates false divinity.

**Game Specs:**
- **Type:** ITEM_WORN
- **Weight:** 0.2 lbs
- **Value:** 10000 gold
- **Affects:** +3 CHA, Command 4x/day (charm), Aura of Authority (NPCs more likely to cooperate, merchants give better prices), Detect Alignment (passive, see alignment of all creatures)
- **Wear Location:** FINGER
- **Flags:** MAGIC, GLOW (white light), EVIL (despite appearing holy)
- **Anti-flags:** Can be worn by any alignment but good-aligned wearers lose CHA bonus

**Level Range:** 21-30 (optimal for levels 23-28)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Valley Dor, taken from Matai Shang after defeating him or found in the Temple of Issus after exposing the Thern fraud. Part of the "Gods of Mars" questline.

**Why Players Want It:** Excellent for Nobles. Merchant benefits save gold. Detect Alignment is very useful. Lightweight. The evil nature creates interesting roleplay. Desecrating this symbol of fraud is satisfying.

---

## Level 31+: Legendary Artifacts

These artifacts are for the most accomplished heroes of Barsoom. They represent the pinnacle of power and are tied to the most epic storylines.

### 25. The Radium Rifle of Zodanga's Arsenal

**Description:** The finest radium rifle ever produced, built by Zodanga's master craftsmen at the height of their power. Its explosive projectiles and exceptional range make it legendary.

**Game Specs:**
- **Type:** ITEM_WEAPON (ranged)
- **Weight:** 10 lbs
- **Value:** 30000 gold
- **Damage:** 4d10+4 (explosive projectiles)
- **Affects:** +2 DEX, +50% range (can shoot from further away), Explosive Shot 5x/day (hits target + all adjacent enemies), Never jams or needs reloading
- **Wear Location:** WIELD (two-handed)
- **Flags:** MAGIC, HUM (crackling radium energy), GOOD
- **Restrictions:** Level 31+, must have Ranged Weapons mastery

**Level Range:** 31+ (optimal for levels 31-40)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Zodanga armory, found in the deepest vault after defeating Sab Than and liberating the city. Part of the endgame Zodanga questline. One-time reward.

**Why Players Want It:** Best ranged weapon in game. Enormous damage. Explosive shots are devastating. Quality-of-life improvements (no reloading). Taking it from Zodanga is symbolically important.

---

### 26. Issus's Stolen Crown

**Description:** The false goddess's crown, stripped from her corpse. Massive, gaudy, and dripping with stolen jewels representing centuries of pilgrims' wealth.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 5 lbs
- **Value:** 50000 gold (but most vendors won't buy it due to infamy)
- **Affects:** +4 CHA (intimidation-based), +2 WIS, AC -2, Terror 3x/day (mass fear effect), Pilgrims' Curse (wearers haunted by visions of Issus's victims, -1 WIS at night, +2 WIS during day)
- **Wear Location:** HEAD
- **Flags:** MAGIC, GLOW (sickly green), EVIL, CURSED
- **Anti-flags:** ANTI_GOOD (good-aligned wearers take 1d6 damage per hour from guilt)

**Level Range:** 31+ (optimal for levels 32+, if you can handle the curse)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Temple of Issus, looted from the false goddess's corpse after the climactic battle. Part of the "Gods of Mars" endgame questline.

**Why Players Want It:** Incredible stats despite the curse. Terror ability is powerful. Symbolic victory over Issus. The curse adds interesting roleplay. High value. Visible sign of defeating a "god." Evil characters can use without penalty.

**Special Note:** Can be purified through a difficult ritual, removing curse and evil flag but reducing bonuses to +3 CHA, +1 WIS. Purified version is GOOD-flagged.

---

### 27. The Ninth Ray Generator (Portable)

**Description:** An impossible achievement—a portable version of the ninth ray technology that propels airships. This experimental device can propel the user through the air like a personal flying machine.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 15 lbs
- **Value:** 40000 gold
- **Affects:** Flight at will (toggle on/off, fly at will like an airship), +2 DEX while flying, Hover (can stop in mid-air), Speed Burst 3x/day (double movement speed for 10 minutes), Air Combat +20% (bonuses to fighting while flying)
- **Wear Location:** BODY (worn as backpack) or HOLD
- **Flags:** MAGIC, HUM (loud mechanical whirring)
- **Restrictions:** Scientists only, Level 33+, high risk of explosion if damaged in combat (10% chance per hit taken)

**Level Range:** 33+ (optimal for levels 33-40)

**Rarity:** UNIQUE (only 1 functioning prototype in game)

**Spawn Location:** Created by the player through an epic Scientists-only questline involving recovering ancient plans, gathering rare materials (including ninth ray samples), and conducting dangerous experiments. Failure results in explosions. Multiple attempts may be needed.

**Why Players Want It:** Personal flight is game-changing. Access to areas others cannot reach. Unique to Scientists. The creation questline is memorable. Risk of explosion adds tension. Visual spectacle.

---

### 28. Tars Tarkas's Jeddak Harness

**Description:** The battle harness of the Jeddak of Thark, greatest of green Martian warriors. Sized for a fifteen-foot, four-armed warrior but magically adjusts to fit.

**Game Specs:**
- **Type:** ITEM_ARMOR
- **Weight:** 12 lbs
- **Value:** 35000 gold
- **Affects:** +4 STR, +3 CON, +2 DEX, AC -5, +50 HP, Extra Attack 1x/day (gain additional attack per round for 10 rounds, simulating four arms), Toughness (damage resistance 15%), Intimidate (enemies flee if morale check fails)
- **Wear Location:** BODY
- **Flags:** MAGIC, GLOW (fierce green), GOOD
- **Restrictions:** Warriors preferred, Level 32+

**Level Range:** 32+ (optimal for levels 32-40)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Thark Territory, given by Tars Tarkas himself after completing his personal questline involving uniting the green hordes and defending against a major threat. Must have earned his deep respect through repeated acts of honor and bravery.

**Why Players Want It:** Best armor for Warriors. Multiple excellent bonuses. Extra Attack ability is incredible. Damage resistance is powerful. Connection to Tars Tarkas is meaningful. Green Martian aesthetic is iconic.

---

### 29. The Temple of the Sun Control Mechanism

**Description:** The ancient device that controls the rotation of the Temple of the Sun, a slowly revolving structure that holds its occupants prisoner for a full Martian year.

**Game Specs:**
- **Type:** ITEM_KEY/TOOL
- **Weight:** 8 lbs
- **Value:** PRICELESS (unique historical artifact)
- **Affects:** Controls Temple rotation (can change speed, direction, or stop), Time Manipulation 1x/week (slow or hasten time in immediate area, 10 minute duration), +3 INT, +3 WIS, Ancient Knowledge (learn lore about ancient Mars automatically)
- **Wear Location:** HOLD (two-handed when operating)
- **Flags:** MAGIC, GLOW (rhythmic pulsing), ANCIENT, ANTI_DROP
- **Restrictions:** Level 35+, must have completed Temple of the Sun questline

**Level Range:** 35+ (optimal for level 35-40)

**Rarity:** UNIQUE (only 1 in game)

**Spawn Location:** Temple of the Sun, found in the central mechanism chamber after solving the temple's ancient puzzles and rescuing those trapped within. Part of a dramatic rescue questline.

**Why Players Want It:** Time manipulation is unique and powerful. Story significance (saves trapped characters). Ancient knowledge provides lore. Controls an entire zone. Multiple stat bonuses. Connection to memorable storyline.

---

### 30. The Warlord's Battle Standard

**Description:** John Carter's personal banner, flown from his flagship. Seeing this standard fly has rallied countless Martians to victory against impossible odds.

**Game Specs:**
- **Type:** ITEM_TOOL
- **Weight:** 6 lbs
- **Value:** PRICELESS (symbol of Mars united)
- **Affects:** Rally 5x/day (all allies within sight gain +3 to all rolls, immunity to fear, +25% HP regeneration for 15 minutes), Inspire Courage 3x/day (mass morale boost), Summon Aid 1x/week (call NPCs of Mars to your location for a desperate battle), +2 CHA, +2 STR, Visible from great distance (acts as beacon)
- **Wear Location:** WIELD or BACK
- **Flags:** MAGIC, GLOW (brilliant red and gold), GOOD, ANTI_DROP
- **Anti-flags:** ANTI_EVIL
- **Restrictions:** Level 38+, must be named champion of Mars, can only be wielded by current Warlord's designated general

**Level Range:** 38+ (optimal for level 38-50)

**Rarity:** UNIQUE (only 1 in game, passed between worthy commanders)

**Spawn Location:** Awarded by John Carter as the final reward for completing the ultimate questline of uniting all Mars against an extinction-level threat. Represents being named Carter's second-in-command. If holder dies or proves unworthy, it returns to Carter.

**Why Players Want It:** Ultimate support item. Rally ability is game-changing for group content. Summon Aid can turn desperate battles. Symbol of ultimate achievement. Visible proof of being Mars's greatest hero. The questline to earn it is the game's pinnacle.

---

## Summary Table: Artifact Distribution

### By Level Range:
- **Level 1-10:** 7 artifacts (5 RARE, 2 UNIQUE)
- **Level 11-20:** 8 artifacts (6 RARE, 2 UNIQUE)
- **Level 21-30:** 9 artifacts (1 RARE, 8 UNIQUE)
- **Level 31+:** 6 artifacts (0 RARE, 6 UNIQUE)

**Total: 30 artifacts (12 RARE allowing multiples, 18 UNIQUE single-instance)**

### By Class Preference:
- **Warriors:** 8 artifacts primarily useful
- **Scientists:** 7 artifacts primarily useful
- **Nobles:** 8 artifacts primarily useful
- **Assassins:** 3 artifacts primarily useful
- **Universal/Multiple Classes:** 4 artifacts

### By Rarity Limits (Total Instances in World):
- **UNIQUE (1):** 18 artifacts
- **RARE (2-5):** 12 artifacts
- **Maximum simultaneous artifact instances:** 54

### By Acquisition Method:
- **Quest Rewards:** 20 artifacts (major storyline completion)
- **Boss Drops:** 4 artifacts (jeddaks, false gods, military leaders)
- **Crafting/Purchase:** 2 artifacts (requires resources + skill)
- **Exploration Discovery:** 4 artifacts (finding hidden locations)

### By Spawn Location Zone:
- **Greater Helium:** 7 artifacts
- **Thark Territory:** 4 artifacts
- **Toonol:** 3 artifacts
- **Valley Dor/Thern Territory:** 3 artifacts
- **Zodanga:** 2 artifacts
- **Atmosphere Factory:** 2 artifacts
- **Other zones:** 9 artifacts

---

## Implementation Notes

### Zone Reset Behavior:

**UNIQUE Artifacts:**
- Max existing: 1 in world
- If flag: 1 (only spawn if none exist)
- Respawn: Never automatically (only through questline reset or GM intervention)

**RARE Artifacts:**
- Max existing: 2-10 depending on item (specified per artifact)
- If flag: 0 (spawn up to limit independently)
- Respawn: 30-120 minutes depending on power level

### Object Value Fields:

**Weapons:**
- value[0]: unused or magic bonus
- value[1]: number of damage dice
- value[2]: size of damage dice
- value[3]: weapon type (1=slice, 2=pierce, 3=slash, 4=bludgeon)

**Armor:**
- value[0]: AC bonus (negative numbers are better)
- value[1-3]: unused or special properties

**Tools:**
- value[0]: charges remaining (or -1 for unlimited)
- value[1]: spell number or effect type
- value[2]: level of effect
- value[3]: special flags

### Affect Locations:

Common affects used by artifacts:
- APPLY_STR: Strength bonus
- APPLY_DEX: Dexterity bonus
- APPLY_INT: Intelligence bonus
- APPLY_WIS: Wisdom bonus
- APPLY_CON: Constitution bonus
- APPLY_CHA: Charisma bonus
- APPLY_AC: Armor class modification (negative is better)
- APPLY_HITROLL: Bonus to hit in combat
- APPLY_DAMROLL: Bonus damage in combat
- APPLY_HIT: Maximum hit points bonus
- APPLY_MANA: Maximum mana bonus

### Special Procedures:

Several artifacts require special procedure functions:
- **Invisibility Devices:** Toggle invisibility flag on user
- **Directional Compass:** Custom navigation commands
- **Phantom Bowl:** Summon phantom creatures
- **Ninth Ray Generator:** Custom flight movement
- **Battle Standard:** AOE buff application
- **Surgical Kits:** Enable special healing commands

### Balance Philosophy:

**Power Curve:**
- Level 1-10 artifacts provide +1-2 to primary stat, basic abilities
- Level 11-20 artifacts provide +2-3 to primary stat, useful spell-like abilities
- Level 21-30 artifacts provide +3-4 to multiple stats, powerful spell-like abilities
- Level 31+ artifacts provide +4+ to multiple stats, game-changing unique abilities

**Acquisition Difficulty:**
- Low-level artifacts: Simple quests, common drops, purchasable
- Mid-level artifacts: Multi-part quests, mini-boss drops, puzzle solving
- High-level artifacts: Epic questlines, major boss defeats, extreme challenges
- Legendary artifacts: Ultimate questlines representing dozens of hours of play

**Lore Integration:**
Every artifact ties into Barsoom's rich history and characters. Players don't just get "+3 sword"—they get "John Carter's sword" with all the meaning that carries. This creates emotional investment and makes artifacts memorable beyond their stats.

---

## Future Expansion

Additional artifacts can be added as new zones and storylines are implemented:

**Potential Future Artifacts:**
- Salensus Oll's Scepter of Okar (yellow Martian polar artifact)
- Gahan's Jetan Prize (Chessmen of Mars reference)
- The Great Rift Compass (for underground navigation)
- Hormad Vat Control Rod (Synthetic Men of Mars)
- Bal Tab's Lucky Token (Master Mind of Mars)
- The Eye of Matai Shang (additional Thern artifact)
- Tul Axtar's Fleet Admiral's Harness (Fighting Man of Mars)
- Ancient First Born Tridents (naval weapons)
- Lotharian Reality Generator (advanced phantom creation)
- The Last Atmosphere Plant Blueprint (ancient knowledge)

Each expansion zone should include 2-4 unique artifacts to maintain player interest and provide goals for exploring new content.

---

## Conclusion

These 30 artifacts provide compelling goals for players at every level of the game. They are carefully balanced to feel powerful without breaking game mechanics, and each has strong ties to Barsoom's lore. The distribution ensures all classes and playstyles have desirable goals, while the rarity system prevents over-saturation and maintains each item's special feeling.

The acquisition methods emphasize memorable quests and achievements over random drops, creating stories that players will remember and share. Earning John Carter's sword or the Crown of the Warlord represents significant accomplishment, not just lucky loot rolls.

As zones are added and storylines expanded, new artifacts can be introduced following these same principles: lore-appropriate, level-appropriate, mechanically interesting, and requiring meaningful effort to obtain.
