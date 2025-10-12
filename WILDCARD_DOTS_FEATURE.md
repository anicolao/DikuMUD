# Wildcard Dots Feature

## Overview

The wildcard dots feature allows players to use dots (`.`) as wildcards when targeting mobs and objects in DikuMUD. This makes it easier to target entities with multi-word names without having to type spaces.

## Usage

### Basic Examples

Instead of typing spaces, you can use dots to target mobs and objects:

```
# Traditional targeting (still works)
kill red martian
get bronze coin
consider the red martian beggar

# With wildcard dots (new feature)
kill red.martian
get bronze.coin
consider the.red.martian.beggar
```

### How It Works

When you use dots in a target name, the game treats each dot-separated word as a requirement. The target must have ALL the words in its namelist to match.

For example, with a mob named "the red martian beggar traveler":
- `red.martian` matches ✓ (has both "red" and "martian")
- `red.beggar` matches ✓ (has both "red" and "beggar")
- `red.green` doesn't match ✗ (doesn't have "green")

### Numeric Targeting Still Works

The original numeric targeting syntax is preserved:
- `2.guard` targets the 2nd guard in the room
- `3.sword` picks up the 3rd sword

The system automatically detects whether the prefix before the first dot is a number or a word.

## Technical Implementation

### Modified Functions

The following functions in `handler.c` were updated to support wildcard dots:

1. **`get_number(char **name)`**: Modified to detect non-numeric prefixes and treat them as wildcards instead of returning an error
2. **`get_char_room_vis(...)`**: Split dot-separated terms and match all of them against mob names in the current room
3. **`get_char_vis(...)`**: Applied same logic for world-wide character targeting
4. **`get_obj_in_list_vis(...)`**: Applied same logic for object targeting in inventories and rooms
5. **`get_obj_vis(...)`**: Applied same logic for world-wide object targeting

### Algorithm

For each target name with dots (e.g., "red.martian.traveler"):
1. Split the name by dots into individual words
2. For each potential target, check if ALL words match the target's namelist
3. Use the existing `isname()` function to match individual words
4. Only return the target if all words match

### Example Matching Logic

```c
// Input: "red.martian"
// Target namelist: "traveler red martian merchant"

// Step 1: Split "red.martian" into ["red", "martian"]
// Step 2: Check if "red" matches namelist -> YES
// Step 3: Check if "martian" matches namelist -> YES  
// Result: MATCH ✓
```

## Testing

A comprehensive integration test was added in `tests/integration/test_wildcard_dots.yaml` that validates:
- Normal single-word targeting still works
- Dot-separated multi-word targeting works
- Various combinations of dots and words work correctly

All existing integration tests continue to pass, ensuring backward compatibility.

## Benefits

1. **Faster Typing**: No need to type spaces, which can be awkward in fast-paced combat
2. **Precision**: Can target specific mobs by specifying multiple distinguishing words
3. **Backward Compatible**: All existing commands and targeting methods still work
4. **Consistent**: Works for both character and object targeting across all visibility scopes

## Examples in Practice

### Combat
```
> consider red.martian
You would need some luck!

> kill red.martian
You hit the Red Martian Traveler hard.

> 2.red.martian
You hit the second Red Martian Traveler.
```

### Inventory Management
```
> get bronze.coin
You pick up a bronze coin.

> drop leather.armor
You drop the leather armor.

> give steel.sword warrior
You give a steel sword to the warrior.
```

### Spell Casting
```
> cast 'cure light' red.martian
You heal the Red Martian Traveler.
```

## Limitations

- The dot wildcard requires ALL specified words to match
- You cannot use dots to match partial words (e.g., "re.mar" won't match "red martian")
- Spaces in the original command are still treated as argument separators
