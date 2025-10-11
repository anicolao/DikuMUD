# Room Description Markers Implementation

## Overview

Room descriptions are now wrapped with special markers `---<` and `>--` to help MUD clients easily identify and parse room information.

## Format

```
---<Room Name
Room description text...
>--
Objects in room...
Mobiles in room...
```

## Example Output

### After Looking
```
---<The Temple of the Jeddak
   You are in the southern end of the temple hall of Lesser Helium's great temple.
The temple has been constructed from giant marble blocks, scarlet and yellow in
color, and most of the walls are covered by ancient murals depicting the history
of the red Martian race and the glory of Helium.
   Large steps lead down through the grand temple gate, descending from the elevated
platform upon which the temple is built to the temple plaza below.
>--
A tarnished copper lamp lies here, looking bright.

20H 100F 100V 100C T:75 Exits:NSD> 
```

### After Movement
```
---<By the Temple Altar
   You are by the temple altar in the northern end of Lesser Helium's great temple.
A huge altar carved from scarlet marble stands before you, and behind it is a
magnificent statue depicting the Jeddak of Helium in full ceremonial regalia.
>--

20H 100F 99V 100C T:75 Exits:S> 
```

## Use Cases

MUD clients can use these markers to:

1. **Custom Formatting**: Apply different styling to room descriptions vs. other text
2. **Automatic Mapping**: Parse room names and descriptions to build maps
3. **Text-to-Speech**: Identify room descriptions for voice output
4. **Accessibility**: Help screen readers distinguish room information
5. **Client Automation**: Trigger scripts or actions when entering rooms

## Implementation Details

### Code Changes

- **File**: `dm-dist-alfa/act.informative.c`
- **Function**: `do_look()`, case 8 (empty look command)
- **Lines Modified**: 3 lines added
  - Opening marker before room name
  - Closing marker after description, before objects/mobiles

### Behavior

- Markers appear for both explicit `look` commands and automatic room display after movement
- Markers are consistent whether room is empty or contains objects/mobiles
- Works in both brief and normal mode (brief mode shows markers but skips description text)
- No impact on existing functionality or other commands

## Testing

Integration test: `tests/integration/test_room_description_markers.yaml`

The test verifies:
- Opening marker `---<` appears before room name
- Closing marker `>--` appears after description
- Markers work with explicit look command
- Markers work after movement
- Room name is correctly displayed

All 13 integration tests pass, including the new marker test.

## Client Parsing Example

```python
import re

def parse_room_description(text):
    """Parse room description from MUD output."""
    pattern = r'---<([^\n]+)\n(.*?)>--'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        room_name = match.group(1).strip()
        room_description = match.group(2).strip()
        return room_name, room_description
    return None, None
```

## Backward Compatibility

The markers are purely additive and do not break existing functionality:
- Players using text-only clients will see the markers as part of the output
- The markers are short and unobtrusive: `---<` and `>--`
- All existing commands and features work exactly as before
- No changes to saved data formats or player files
