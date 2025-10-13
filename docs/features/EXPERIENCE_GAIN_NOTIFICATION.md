# Experience Gain Notification on Kill

## Summary

This enhancement adds explicit notification to players when they gain experience from killing a creature. Previously, players only saw "You receive your share of experience." without knowing the actual amount gained.

## Changes Made

### Modified Files
- `dm-dist-alfa/fight.c`

### Specific Changes

1. **Group Experience (group_gain function)**
   - Changed generic message "You receive your share of experience." to show actual amount
   - Now displays: "You gained XX experience."
   - Applied to both group leader and followers

2. **Solo Experience (damage function)**
   - Added experience gain message for solo kills
   - Displays: "You gained XX experience."
   - Shows immediately after killing blow lands

## Implementation Details

The changes were made in two locations:

### Group Combat (`group_gain` function, lines 343-360)
```c
// For group leader
sprintf(buf, "You gained %d experience.", share);
send_to_char(buf, k);
send_to_char("\n\r", k);

// For group followers  
sprintf(buf, "You gained %d experience.", share);
send_to_char(buf, f->follower);
send_to_char("\n\r", f->follower);
```

### Solo Combat (`damage` function, lines 662-664)
```c
sprintf(buf, "You gained %d experience.", exp);
send_to_char(buf, ch);
send_to_char("\n\r", ch);
```

## Code Style

The implementation follows DikuMUD's historical coding style:
- Uses `sprintf` and `send_to_char` for output (standard for 1990s C)
- Manual newline handling with "\n\r"
- Minimal comments (as per original codebase style)
- Uses existing `buf` variable from function scope

## Testing Notes

### What Was Tested
- Code compiles successfully without errors or warnings
- Changes are minimal and surgical - only affecting message output
- Logic flow remains unchanged

### Testing Considerations
- God-level `kill` command (level >= 24) bypasses normal damage flow and calls `raw_kill` directly
- To see experience messages in-game, use characters below level 21 (experience gain limit)
- Testing requires actual combat through `hit` command or finding aggressive mobs

### Integration Test
Created `tests/integration/test_experience_gain.yaml` for automated testing framework.

## Backward Compatibility

- No changes to data structures or protocols
- No changes to experience calculation algorithms  
- No changes to saved player data format
- Fully backward compatible with existing worlds

## Future Enhancements

Potential improvements:
- Show experience per hit during combat (not just on kill)
- Color-code large vs small experience gains
- Add experience summary at end of combat
- Track and display experience per gaming session
