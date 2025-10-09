# Zone Files Directory

This directory contains the modularized zone files for DikuMUD. Each zone has separate files for different content types.

## Structure

Each zone consists of five files:
- `<zone_name>.wld` - World/Room definitions
- `<zone_name>.mob` - Mobile (NPC) definitions
- `<zone_name>.obj` - Object definitions
- `<zone_name>.zon` - Zone reset commands
- `<zone_name>.shp` - Shop definitions

## Current Zones

### limbo (Zone 0)
- Virtual numbers: 0-2
- Special system zone with void and limbo rooms
- Contains Puff the ancient white banth

### zone_1200 (Zone 1200)
- Virtual numbers: 1200-1202
- Immortal/wizard hangout rooms
- Chat Room, Moses' Hangout, Centre of the Universe

### lesser_helium (Zone 30)
- Virtual numbers: 3000-3099
- Main starting zone for players
- Twin city of Helium on Barsoom (Mars)
- Includes: Temple District, Market Plaza, Guild Quarter, shops, inns

### sewers (Zone 31)
- Virtual numbers: 3150-3189
- Ancient sewer system beneath Lesser Helium
- Accessible from the Waste Disposal area (room 3030)
- Target levels: 1-4
- Features: 40 rooms of tunnels and dens
- Creatures: Ulsio (rats), carrion birds, spiders, slimes, centipedes
- Two secret passages lead to deeper, more dangerous areas
- Rewards: Basic weapons, food, coins, and better loot in deep sections
- Corresponds to the "Sewers" of original Midgaard design

### dead_sea_bottom_channel (Zone 32)
- Virtual numbers: 3200-3299
- Ancient dried waterway beneath Lesser Helium
- Connection between surface and sea bottom

### dead_sea_wilderness (Zone 33)
- Virtual numbers: 3750-3899
- Dangerous wilderness between the Twin Cities
- Connecting zone with predators and encounters

### greater_helium (Zone 35)
- Virtual numbers: 3900-3999
- The larger Twin City, home of John Carter
- Major city zone with 100 rooms

### zodanga (Zone 36)
- Virtual numbers: 3600-3649
- Enemy city-state to Helium
- Ruled by Than Kosis and Prince Sab Than
- Dark, militaristic atmosphere with espionage quarter
- 50-room zone focusing on political intrigue

### zodanga_wilderness (Zone 38)
- Virtual numbers: 3650-3749
- Wilderness connector between Zodanga and Gathol
- Dangerous dead sea bottom plains with predators
- Zodangan scouts patrol eastern areas
- Gathol scouts patrol western areas
- Ancient ruins and traveler rest stops
- Target levels: 14-22

### gathol (Zone 37)
- Virtual numbers: 4200-4299
- Allied city-state ruled by Gahan of Gathol
- Sophisticated culture emphasizing beauty and honor
- Famous for jetan (Martian chess) tradition
- Features Gahan, palace, and cultural districts
- Safe haven for players allied with Helium
- Target levels: 12-20

### ptarth (Zone 39)
- Virtual numbers: 4300-4399
- Allied city-state ruled by Thuvan Dihn
- Home of Princess Thuvia with her unique banth-controlling abilities
- Diplomatic center and military stronghold
- Features throne room, palace gardens, military district
- Safe haven for players allied with Helium
- Target levels: 15-23

### gathol_ptarth_wilderness (Zone 43)
- Virtual numbers: 4400-4499
- Wilderness connector between Gathol and Ptarth
- Allied territory with cooperative patrols from both cities
- Features halfway waystation, ancient ruins, banth hunting grounds
- Some banths influenced by Thuvia's mental powers
- Target levels: 15-23

### kaol (Zone 44)
- Virtual numbers: 4500-4599
- Allied city-state ruled by Jeddak Kulan Tith
- Known for honor, military excellence, and ethical conduct
- Features Court of Honor, royal palace, training grounds
- Home of Kulan Tith who nobly released Thuvia from betrothal
- Safe haven for players allied with Helium
- Target levels: 18-26

### ptarth_kaol_wilderness (Zone 45)
- Virtual numbers: 4600-4699
- Wilderness connector between Ptarth and Kaol
- Allied territory with cooperative patrols from both cities
- Features joint waystation, ancient ruins, dangerous predator zones
- Great banths, white apes, and calots as major threats
- Demonstrates practical alliance benefits through security cooperation
- Target levels: 18-26

### thark_territory (Zone 40)
- Virtual numbers: 4000-4099
- Ancient ruined city occupied by the Thark horde
- Allied green Martian territory
- Includes: Council Chambers, Warrior Guild, Noble Guild, School, Arena, Thoat Pens, Ancient Ruins
- Features Tars Tarkas, Sola, and other key NPCs

### southern_approach (Zone 34)
- Virtual numbers: 3100-3149
- Connector zone from Lesser Helium to the Atmosphere Factory
- Several hundred miles of dead sea bottom journey
- Encounters with predators and travelers
- Target levels: 3-6

### atmosphere_factory (Zone 41)
- Virtual numbers: 4100-4149
- Main levels of the Atmosphere Factory
- Critical Mars infrastructure producing oxygen for the entire planet
- Engineering quarters, processing halls, power core
- Features Chief Engineer Vor Daj, Master Mechanic Tavia, Security Commander Jat Or
- Target levels: 4-8

### atmosphere_lower (Zone 42)
- Virtual numbers: 4150-4199
- Secret lower levels with forbidden research
- Renegade scientists led by Ras Thavas
- Biological, cybernetic, and power experiments
- Ancient archives and the First Engineer
- Target levels: 8-12

### system (Zone 90)
- Zone file terminator
- Contains end-of-file marker `$~`

## Build Process

The makefile automatically assembles the master `tinyworld.*` files from these zone files:

```bash
make worldfiles
```

This concatenates the zone files in the correct order:
1. limbo
2. zone_1200
3. lesser_helium
4. sewers
5. dead_sea_bottom_channel
6. southern_approach
7. dead_sea_wilderness
8. greater_helium
9. zodanga
10. zodanga_wilderness
11. gathol
12. ptarth
13. gathol_ptarth_wilderness
14. kaol
15. ptarth_kaol_wilderness
16. thark_territory
17. atmosphere_factory
18. atmosphere_lower
19. system

## Adding New Zones

To add a new zone:

1. Create the five zone files in this directory using the naming convention `<zone_name>.*`
2. Update the `ZONE_ORDER` variable in the makefile to include your zone in the correct position
3. Ensure zone numbers don't overlap with existing zones
4. Build with `make worldfiles` to test

## File Format Notes

- Each file type has its own format documented in `GAMMA_DESIGN.md`
- Room/mob/object entries start with `#<vnum>` and end with `S`
- Zone entries start with `#<zone_num>` and end with `S`
- Shop entries start with `#<shop_num>~` and end with terminal newline
- Empty zone files are allowed (e.g., `limbo.shp` has no shops)
