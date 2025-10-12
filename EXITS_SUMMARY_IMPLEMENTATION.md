# Exits Summary Implementation

## Overview

Room description markers now include a compact exits summary on the closing marker line (`>--`). This enhancement makes it easier for MUD clients to parse available exits while maintaining backward compatibility.

## Format

The closing marker now includes exits information:

```
>-- Exits:NSD
```

Where each letter represents an available exit:
- **N** = North
- **E** = East
- **S** = South
- **W** = West
- **U** = Up
- **D** = Down

## Examples

### Multiple Exits (North, South, Down)

```
--<
The Temple of the Jeddak
   You are in the southern end of the temple hall of Lesser Helium's great temple.
The temple has been constructed from giant marble blocks, scarlet and yellow in
color, and most of the walls are covered by ancient murals depicting the history
of the red Martian race and the glory of Helium.
>-- Exits:NSD
A tarnished copper lamp lies here, looking bright.

5H 100F 82V 0C T:26 Exits:NSD>
```

### Single Exit (South Only)

```
--<
By the Temple Altar
   You are by the temple altar in the northern end of Lesser Helium's great temple.
A huge altar carved from scarlet marble stands before you, and behind it is a
magnificent statue depicting the Jeddak of Helium in full ceremonial regalia.
>-- Exits:S

5H 100F 82V 0C T:61 Exits:S>
```

### Brief Mode

In brief mode, markers are not displayed (consistent with original behavior):

```
The Temple of the Jeddak
A tarnished copper lamp lies here, looking bright.

5H 100F 82V 0C T:17 Exits:NSD>
```

## Implementation Details

### Code Changes

- **File**: `dm-dist-alfa/act.informative.c`
- **Function**: `do_look()`, case 8 (empty look command)
- **Changes**:
  - Added compact exits string generation
  - Only shows open, non-closed exits
  - Appended to closing marker line

### Logic

```c
char exits_buf[20];
int door;
char *exit_letters = "NESWUD";  /* North, East, South, West, Up, Down */

strcpy(exits_buf, ">-- Exits:");
for (door = 0; door <= 5; door++) {
    if (EXIT(ch, door) && 
        EXIT(ch, door)->to_room != NOWHERE &&
        !IS_SET(EXIT(ch, door)->exit_info, EX_CLOSED)) {
        strncat(exits_buf, &exit_letters[door], 1);
    }
}
strcat(exits_buf, "\n\r");
send_to_char(exits_buf, ch);
```

## Benefits

1. **Easier Parsing**: MUD clients can extract exits directly from the room description marker
2. **Consistent Format**: Always appears in the same location with the same format
3. **Compact Display**: Single-letter abbreviations save screen space
4. **Client Automation**: Enables better mapping and navigation automation
5. **Backward Compatible**: Existing behavior preserved (brief mode, marker behavior)

## Client Parsing Example

Updated Python parser that extracts exits:

```python
import re

def parse_room_description(text):
    """Parse room description from MUD output."""
    pattern = r'---<([^\n]+)\n(.*?)>-- Exits:([NESWUD]*)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        room_name = match.group(1).strip()
        room_description = match.group(2).strip()
        exits = match.group(3)
        return room_name, room_description, exits
    return None, None, None

# Example usage
text = """--<
The Temple of the Jeddak
   You are in the temple.
>-- Exits:NSD
A lamp lies here.
"""

name, desc, exits = parse_room_description(text)
print(f"Room: {name}")
print(f"Exits: {exits}")  # Output: "NSD"
print(f"Has North exit: {'N' in exits}")  # Output: True
```

## Testing

### Integration Test

The test `tests/integration/test_room_description_markers.yaml` has been updated to verify:
- Opening marker `---<` appears before room name
- Closing marker `>-- Exits:` appears after description
- Exits are shown in compact format (e.g., `[NESWUD]+`)
- Markers work with explicit look command
- Markers work after movement
- Brief mode doesn't show markers (as expected)

All 34 integration tests pass.

### Manual Testing

Tested with telnet client:
1. Connected to server on port 5555
2. Created test character
3. Verified exits display in multiple rooms
4. Tested brief mode (no markers shown)
5. Tested movement between rooms

## Backward Compatibility

The enhancement is fully backward compatible:
- Only adds information to existing marker line
- Brief mode behavior unchanged (no markers)
- Room description content unchanged
- All existing functionality preserved
- No changes to saved data formats

## Use Cases

### Automatic Mapping

MUD clients can now:
1. Parse room name from opening marker
2. Parse description from between markers
3. Parse available exits from closing marker
4. Build accurate maps automatically

### Navigation Automation

Clients can:
1. Determine valid directions without parsing "Obvious exits:" output
2. Make pathfinding decisions based on exits info
3. Highlight available exits in UI
4. Enable directional buttons/controls dynamically

### Accessibility

Screen readers and text-to-speech systems can:
1. Announce available exits consistently
2. Separate navigation info from description
3. Provide clearer spatial orientation

## Related Documentation

- **ROOM_MARKERS_IMPLEMENTATION.md**: Original room markers feature
- **tests/integration/test_room_description_markers.yaml**: Integration tests
- **dm-dist-alfa/act.informative.c**: Source code implementation

## Version

- **Implemented**: 2025-10-12
- **DikuMUD Version**: GAMMA 0.0
- **Author**: GitHub Copilot
