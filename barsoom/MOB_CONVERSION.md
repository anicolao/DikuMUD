# Mob Conversion Summary for Lesser Helium

This document describes the conversion of all mobs in `tinyworld.mob` to Barsoom-themed creatures appropriate for Lesser Helium.

## Conversion Principles

All mobs have been converted to creatures that are **COMMON** in Lesser Helium according to the CREATURES.md reference:

1. **Red Martians** - The dominant population in Lesser Helium
2. **Calots** - Ten-legged watchdogs and guard beasts common in all Martian cities
3. **Martian Wildlife** - Small birds and other fauna adapted to Mars

## Category Conversions

### Human NPCs → Red Martians (42 conversions)

All human NPCs were converted to Red Martians with appropriate descriptions:
- Copper-red skin
- Coal-black hair (when described)
- Large, dark eyes
- Jeweled harnesses instead of clothing
- Centuries-old lifespans

**Examples:**
- Wizard → Red Martian Scientist (#3000)
- Baker → Red Martian Baker (#3001)
- City Guards → Red Martian City Guards (#3060, #3067, #3141)
- Guildmasters → Red Martian guild leaders (Science Master, High Priest, Shadow Master, War Master) (#3020-#3023)
- Mayor → Jed of Lesser Helium (#3143)
- All shopkeepers, merchants, guards, and service workers → Red Martian equivalents

### Dogs and Pets → Calots (7 conversions)

All dogs and domestic animals converted to calots with varying sizes and training:

1. **Fido** → Scavenging Calot (#3062) - small, foul-smelling street calot
2. **Kitten** → Young Calot Pup (#3090) - tiny calot pup
3. **Puppy** → Juvenile Calot (#3091) - small calot
4. **Beagle** → Adult Calot (#3092) - standard adult size, quick tracker
5. **Rottweiler** → War-Trained Calot (#3093) - large combat calot
6. **Wolf** → Hunting Calot (#3094) - large hunting breed
7. **Papi's Cat** → Papi's Favorite Calot (#3300) - exceptionally well-trained

All calots feature:
- Ten legs
- Hairless, leathery hide
- Frog-like heads
- Powerful jaws
- Varying sizes from pup to war-beast

### Birds → Martian Wildlife (4 conversions)

Earth birds converted to Martian adapted species:
- Swan → Martian Water Bird (#3121)
- Duckling → Young Water Bird (#3122)
- Sparrow → Small Martian Bird (#3123)
- Duck → Plump Water Bird (#3124)

### Special Creatures

1. **Puff** → Ancient White Banth (#1) - Legendary creature with otherworldly wisdom
2. **Reversed Dog** → Tolac (reversed calot) (#3066) - Strange experimental creature
3. **Zombies/Undead** → Reanimated Red Martian corpses (#3601, #3602) - Results of forbidden science

## Technical Details

### File Modified
- `dm-dist-alfa/lib/tinyworld.mob` - All 51 mob entries updated

### Changes Made
- Updated all mob keywords to include Barsoom-appropriate terms
- Rewrote short descriptions (room appearance text)
- Rewrote detailed descriptions to match Barsoom aesthetics
- Maintained all stat lines (combat values, gold, experience, etc.)
- Preserved all flags and behaviors

### Preserved Elements
- Mob virtual numbers (unchanged)
- Combat statistics and difficulty
- Special procedure assignments (shopkeepers, guards, etc.)
- Inventory and equipment
- Behavioral flags (aggressive, scavenger, etc.)

## Thematic Consistency

All conversions maintain consistency with Barsoom lore:

1. **Red Martians** in Lesser Helium are civilized, cultured citizens
2. **Calots** serve as guard beasts, companions, and pets
3. **No inappropriate creatures** - only species that would be COMMON in a red Martian city
4. **Copper-red skin** is universal for all red Martians
5. **Jeweled harnesses** replace traditional Earth clothing
6. **Ten-legged** anatomy for all calots (not four like Earth dogs)

## Verification

All mobs have been:
- Successfully compiled with the server
- Loaded into the game world
- Tested in-game to verify descriptions display correctly
- Confirmed to maintain their original functions (guards, shopkeepers, pets, etc.)

## Future Considerations

When additional zones are added to the game, other creature types from CREATURES.md can be introduced:
- **Green Martians** (Thark territory)
- **Thoats** (eight-legged riding beasts) - can be added to stables
- **Zitidars** (cargo beasts) - can be added to trade routes
- **Banths** (ten-legged predators) - for wilderness zones
- **Great White Apes** - for ruins and dangerous areas

For now, Lesser Helium contains only creatures appropriate for a civilized red Martian city-state.

## References

- `barsoom/summaries/CREATURES.md` - Primary source for creature descriptions
- `barsoom/LESSER_HELIUM.md` - Zone description and theme
- `GAMMA_DESIGN.md` - Technical documentation for .mob file format
