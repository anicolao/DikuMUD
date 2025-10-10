# REEQUIP Feature Documentation

## Overview

The REEQUIP feature allows players who have lost all their equipment to receive basic starter gear from their guildmaster. This provides a safety net for players who have died and lost everything, allowing them to get back into the game without needing help from other players.

## How It Works

### Automatic Detection

When a player enters their guildmaster's room, the guildmaster checks if the player:
- Has no equipment worn
- Has no items in inventory
- Has less than 500 gold coins

If all these conditions are met, the guildmaster automatically says:

```
I see you have lost all of your fighting leathers. Use the command REEQUIP to gain some basic equipment.
```

### Using REEQUIP

When a player types `REEQUIP` while in their guildmaster's room, the system:

1. Verifies the player still qualifies (no equipment and < 500 gold)
2. Gives the player 4 items appropriate for their class
3. Displays a message confirming what equipment was received

## Equipment by Class

Each class receives four items tailored to their needs:

### Scientist (Magic User)
- **Glow crystal** (item 3531) - Light source
- **Water cask** (item 3500) - Water container
- **Simple leather harness** (item 3550) - Body armor
- **War mace** (item 3523) - Weapon

### Noble (Cleric)
- **Glow crystal** (item 3531) - Light source
- **Water cask** (item 3500) - Water container
- **Simple leather harness** (item 3550) - Body armor
- **War mace** (item 3523) - Weapon

### Assassin (Thief)
- **Glow crystal** (item 3531) - Light source
- **Water cask** (item 3500) - Water container
- **Simple leather harness** (item 3550) - Body armor
- **Fine stiletto** (item 3520) - Dagger weapon

### Warrior
- **Glow crystal** (item 3531) - Light source
- **Water cask** (item 3500) - Water container
- **Simple leather harness** (item 3550) - Body armor
- **Small shield** (item 3563) - Shield for defense

## Guildmaster Locations

The REEQUIP feature is available from the following guildmasters in Lesser Helium:

- **Science Master** (mob 3020) - For Scientists
- **High Priest** (mob 3021) - For Nobles
- **Shadow Master** (mob 3022) - For Assassins
- **War Master** (mob 3023) - For Warriors

## Technical Implementation

### Command Number
- REEQUIP is command #221 in the interpreter

### Modified Files
- `interpreter.c` - Added REEQUIP command definition
- `spec_procs.c` - Modified `guild()` function to handle REEQUIP logic

### Special Procedure Logic

The guild special procedure now handles three scenarios:

1. **Room Entry (cmd == 0)**: Checks if player qualifies for reequip and displays message
2. **REEQUIP Command (cmd == 221)**: Validates and gives equipment
3. **Practice Commands (cmd == 164, 170)**: Existing practice functionality (unchanged)

## Testing

A test script is provided at `dm-dist-alfa/test_reequip.sh` which verifies:
- Code compilation
- Command registration
- Equipment item existence
- Server boot with changes

Run the test with:
```bash
cd dm-dist-alfa
./test_reequip.sh
```

## Usage Example

```
> north
[You enter the Science Master's room]
The Science Master says, 'I see you have lost all of your fighting leathers. Use the command REEQUIP to gain some basic equipment.'

> reequip
The Science Master equips you with:
  a glow crystal
  a water cask
  a simple leather harness
  a war mace

> inventory
You are carrying:
  a war mace
  a simple leather harness
  a water cask
  a glow crystal
```

## Notes

- Equipment is given to inventory, not automatically worn
- Players can only use REEQUIP if they truly have no equipment
- The 500 gold threshold prevents abuse by wealthy players
- Items given are basic starter equipment, not powerful gear
- The feature encourages self-sufficiency for new or unlucky players
