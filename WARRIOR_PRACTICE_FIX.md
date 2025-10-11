# Warrior Guildmaster Practice Fix

## Summary

Fixed the warrior guildmaster practice functionality that was not working due to incorrect command numbers in the guild special procedure. Created an integration test to validate the fix.

## Test Created

**File**: `tests/integration/test_warrior_guildmaster_practice.yaml`

This integration test validates that warriors can:
1. Use the practice command at the War Master's location to see available skills
2. Practice kick, bash, and rescue skills
3. Successfully consume practice sessions when practicing

## Issues Found and Fixed

### 1. Incorrect Practice Command Numbers

**Problem**: The guild special procedure in `spec_procs.c` was checking for practice command numbers 164 and 170, but the actual command numbers in `interpreter.c` are 165 and 171.

**Root Cause**: The command array in `interpreter.c` has comments that count as positions, causing the actual command numbers to be different from what was expected. The commands are:
- Position 165: "practice"
- Position 171: "practise" (British spelling)

**Fix**: Changed line 250 in `spec_procs.c`:
```c
// Before:
if ((cmd != 164) && (cmd != 170)) return(FALSE);

// After:
if ((cmd != 165) && (cmd != 171)) return(FALSE);
```

**File Modified**: `dm-dist-alfa/spec_procs.c`

**Impact**: This fix affects ALL guild special procedures, not just warriors. All classes (Scientists, Nobles, Assassins, and Warriors) can now properly practice their skills.

### 2. Test Characters Missing Practice Sessions

**Problem**: The `create_test_player` utility created test characters with 0 practice sessions, making it impossible to test the practice functionality.

**Fix**: Added logic to `create_test_player.c` to give characters practice sessions based on their level:
```c
/* Give practice sessions based on level (simulating level gains) */
/* Characters get practice sessions when they level up */
if (level > 1) {
    player.spells_to_learn = (level - 1) * 3;  /* Approximately 3 sessions per level */
} else {
    player.spells_to_learn = 0;
}
```

**File Modified**: `tools/create_test_player.c`

**Impact**: Test characters created with level > 1 now have practice sessions available, making it possible to test practice functionality in integration tests.

## Test Results

All practice-related tests now pass:
- Integration test: `tests/integration/test_warrior_guildmaster_practice.yaml` ✓

Warriors can now:
- See available skills (kick, bash, rescue) using the practice command
- Practice each skill successfully
- Have practice sessions consumed appropriately

## Classes Affected

This fix affects all character classes:
- **Scientists (Magic Users)**: Can now practice spells at the Science Master
- **Nobles (Clerics)**: Can now practice spells at the High Priest  
- **Assassins (Thieves)**: Can now practice skills at the Shadow Master
- **Warriors**: Can now practice skills at the War Master

## Guildmaster Locations

The practice functionality is available from the following guildmasters in Lesser Helium:

- **Science Master** (mob 3020) - For Scientists
- **High Priest** (mob 3021) - For Nobles
- **Shadow Master** (mob 3022) - For Assassins
- **War Master** (mob 3023) - For Warriors (room 3023 - Practice Yard)

## Warrior Skills

Warriors can practice the following combat skills:
- **kick** (skill #50) - Attack with a powerful kick
- **bash** (skill #51) - Bash opponent with shield
- **rescue** (skill #52) - Rescue groupmate from combat

## Technical Details

### Command Numbers

The command numbers are defined by the position in the `command[]` array in `interpreter.c`:
- Command 165: "practice" - used for practicing skills/spells
- Command 171: "practise" - British spelling variant

### Special Procedure Logic

The guild special procedure (`guild()` in `spec_procs.c`) handles three scenarios:
1. **Room Entry (cmd == 0)**: Checks if player qualifies for reequip
2. **REEQUIP Command (cmd == 221)**: Validates and gives equipment
3. **Practice Commands (cmd == 165, 171)**: Shows available skills/spells and handles practice

### Practice Session Mechanics

- New characters start with 0 practice sessions
- Characters gain practice sessions when leveling up (based on wisdom)
- Each practice attempt consumes 1 practice session
- Skills/spells have a maximum learned percentage (varies by class and skill)

## Related Files

- `dm-dist-alfa/spec_procs.c` - Guild special procedure (practice logic)
- `dm-dist-alfa/interpreter.c` - Command definitions and numbers
- `tools/create_test_player.c` - Test character creation utility
- `tests/integration/test_warrior_guildmaster_practice.yaml` - Integration test

## Future Enhancements

Potential improvements for practice functionality:
1. Add integration tests for other classes (Scientists, Nobles, Assassins)
2. Test maximum skill percentage limits
3. Test practice with insufficient sessions
4. Test practice with invalid skill names
