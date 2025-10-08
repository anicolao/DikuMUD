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

### thark_territory (Zone 40)
- Virtual numbers: 4000-4099
- Ancient ruined city occupied by the Thark horde
- Allied green Martian territory
- Includes: Council Chambers, Warrior Guild, Noble Guild, School, Arena, Thoat Pens, Ancient Ruins
- Features Tars Tarkas, Sola, and other key NPCs

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
4. dead_sea_bottom_channel
5. dead_sea_wilderness
6. greater_helium
7. thark_territory
8. system

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
