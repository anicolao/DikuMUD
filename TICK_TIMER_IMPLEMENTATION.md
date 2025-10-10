# Tick Timer Implementation

## Overview

Added a countdown timer to the player prompt that displays the number of seconds remaining until the next game tick. The timer counts down from 75 seconds to 0 and then resets.

## Implementation Details

### Files Modified

- **`dm-dist-alfa/comm.c`** - Modified to add global pulse tracking and update `make_prompt()` function

### Changes Made

1. **Global Pulse Counter**
   - Moved `pulse` from a local variable in `game_loop()` to a global variable
   - This allows `make_prompt()` to access the current pulse count
   
2. **Tick Timer Calculation**
   - Added calculation in `make_prompt()` to determine seconds until next tick
   - Formula: `secs_to_tick = (tick_pulse - (pulse % tick_pulse)) / 4`
   - Where `tick_pulse = SECS_PER_MUD_HOUR * 4 = 300 pulses = 75 seconds`
   - Pulse increments every 0.25 seconds, so divide by 4 to get seconds

3. **Prompt Format Update**
   - Updated both combat and non-combat prompts to include `T:XX` before Exits
   - Format: `%dH %dF %dV %dC T:%d Exits:%s>`

## Prompt Examples

### Without Combat
```
5H 100F 82V 0C T:27 Exits:NSD>
```

### With Combat
```
45H 30F 60V 100C T:33 Exits:N [Warrior:pretty hurt] [troll:just a scratch]>
```

## Technical Details

### Tick Timing
- Game ticks occur every 75 seconds (SECS_PER_MUD_HOUR)
- The pulse counter increments every 0.25 seconds (4 pulses per second)
- Ticks happen at pulse % 300 == 0
- The timer shows real seconds, not pulses

### Code Structure

```c
/* Global pulse counter */
int pulse = 0;       /* global pulse counter for tick timing */

/* In make_prompt() */
extern int pulse;
int tick_pulse, secs_to_tick;

/* Calculate seconds until next tick */
tick_pulse = SECS_PER_MUD_HOUR * 4;  /* 300 pulses = 75 seconds */
secs_to_tick = (tick_pulse - (pulse % tick_pulse)) / 4;
```

## Testing

The implementation was tested by:
1. Building the dmserver
2. Connecting with a test character
3. Observing the timer countdown over multiple seconds
4. Verifying the countdown rate (1 real second = 1 timer second)

Sample test output showing countdown:
```
T:61 (initial)
T:58 (3 seconds later)
T:56 (2 seconds later)
T:53 (3 seconds later)
T:51 (2 seconds later)
T:48 (3 seconds later)
```

The timer accurately counts down from 75 to 0, then resets to 75 for the next cycle.

## Benefits

- Players can see exactly when the next tick will occur
- Helps with timing regeneration, zone resets, and other tick-based events
- Minimal code changes (only 12 lines added/modified)
- No impact on game performance

## Compatibility

- Works with both combat and non-combat prompts
- Maintains all existing prompt functionality
- No changes required to other game systems
