# Flavor Text Update Guidelines for Technology Reskinning

## Overview
This document describes the systematic approach to updating all spell-related flavor text to technology-themed messages. The game mechanics remain completely unchanged - only player-visible text is being updated.

## Files Requiring Updates

### Primary Implementation Files
1. **magic.c** - Core spell effect implementations
2. **spells1.c** - Offensive spell implementations  
3. **spells2.c** - Support spell implementations
4. **spell_parser.c** - Already updated with technology names
5. **handler.c** - May contain spell wear-off messages

### Help and Documentation
1. **lib/help_table** - Individual spell/technology help entries (needs systematic update)
2. **lib/help** - Main help file (already updated)

## Update Pattern

### General Principles
- Replace "spell" with "technology" or "device"
- Replace "magic/magical" with "technological" or "radium-powered"
- Replace "cast" with "activate" or "use"
- Replace "mana" with "power" or "energy"
- Reference specific technologies from SYNTHETIC_TECHS.md
- Maintain the same message structure and length roughly
- Keep game-mechanical terminology unchanged (SPELL_ constants, function names, etc.)

### Common Message Patterns

#### Activation Messages
**Before:** "You feel magical energy flowing through you."
**After:** "Your device hums as radium power flows through it."

**Before:** "You cast X spell."
**After:** "You activate the X device."

#### Effect Messages
**Before:** "You feel someone protecting you." (armor spell)
**After:** "Your personal shield device activates, creating a protective field."

**Before:** "$n slowly fade out of existence." (teleport)
**After:** "$n shimmers and vanishes as matter transmission occurs."

**Before:** "Your eyes tingle." (detect magic)
**After:** "Your optical enhancement device activates."

#### Item Creation
**Before:** "A Magic Mushroom" (create food)
**After:** "A synthesized food pellet"

**Before:** "$p suddenly appears."
**After:** "$p is synthesized by the device."

#### Invisibility
**Before:** "$n slowly fade out of existence."
**After:** "$n fades from view as the invisibility cloak activates."

**Before:** "You vanish."
**After:** "You vanish as your invisibility cloak bends light around you."

### Technology-Specific Terminology

Use these terms from SYNTHETIC_TECHS.md when updating messages:

1. **Personal Shield** (armor) - "force field", "protective barrier"
2. **Matter Transmitter** (teleport) - "transmission", "materialization"
3. **Invisibility Cloak** (invisibility) - "light bending", "optical distortion"
4. **Thermal Projector** (burning hands) - "heat ray", "thermal energy"
5. **Arc Projector** (lightning bolt) - "electrical discharge", "arc"
6. **Regeneration Chamber** (heal) - "tissue regeneration", "cellular repair"
7. **Neural Controller** (charm) - "neural command projection"
8. **Life Detector** (sense life) - "bio-scanner", "life signs"
9. **Technology Scanner** (detect magic) - "radium signature detection"
10. **Toxin Injector** (poison) - "toxin delivery system"

### Mechanical Terms to Keep Unchanged

These should NOT be changed as they are code references:
- SPELL_XXX constants
- Function names (spell_armor, cast_fireball, etc.)
- Variable names in code
- File names
- Structure member names

## Status

### Completed Updates
- [x] spell_parser.c - Command messages
- [x] spell_parser.c - Spell name array
- [x] spell_parser.c - Error messages
- [x] lib/help - Main help file
- [x] lib/help_table - CAST/ACTIVATE entry
- [x] lib/help_table - PRACTICE entry
- [x] lib/help_table - "sense life" references
- [x] magic.c - ALL player-visible messages (100% complete)
- [x] spells1.c - ALL player-visible messages (100% complete)
- [x] spells2.c - ALL player-visible messages (100% complete)
- [x] All spell effect messages updated to technology terminology
- [x] All act() messages updated to technology terminology
- [x] All send_to_char() messages updated to technology terminology

### Remaining Updates Needed

#### lib/help_table (individual technology entries)
Each spell needs its help entry updated:
- Change "cast 'spell name'" to "activate 'tech name'"
- Update description to use technology terminology
- Reference appropriate technology from SYNTHETIC_TECHS.md
- Keep mechanical details (duration, accumulation, etc.)

Examples needed for all 44+ spells/technologies.

## Implementation Strategy

Given the volume of changes (hundreds of text strings across multiple files), the recommended approach is:

1. **Systematic File-by-File Update**: Go through each file methodically
2. **Search and Replace Patterns**: Use careful search/replace for common patterns
3. **Manual Review**: Check each message for context appropriateness
4. **Testing**: Build after each file to catch any syntax errors
5. **In-Game Testing**: Actually activate technologies to verify messages look right

## Notes

- The core reskinning is complete (commands, spell names, key infrastructure)
- The game is fully playable with technology terminology
- Remaining flavor text updates are polish and immersion
- All game mechanics function identically
- No save file compatibility issues
- World files unchanged

## Future Work

Consider creating a script or tool to:
1. Extract all send_to_char/act messages from source files
2. Present them for batch translation
3. Apply the translations back to source files
4. This would speed up the remaining hundreds of message updates
