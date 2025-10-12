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

When you use dots in a target name, the game uses a priority-based matching system:

**Priority 1: Exact short_description match**
- If the entire search string matches the mob's short description exactly (case-insensitive), it's matched immediately
- Example: `a Red Martian Traveler` exactly matches a mob with that short_desc

**Priority 2: All words in namelist**
- The target must have ALL dot-separated words in its namelist
- Example: With namelist "the red martian beggar traveler":
  - `red.martian` matches ✓ (has both "red" and "martian" in namelist)
  - `red.beggar` matches ✓ (has both "red" and "beggar" in namelist)
  - `red.green` doesn't match ✗ (doesn't have "green")

**Priority 3: All words in short_description**
- If not matched by namelist, the game checks if ALL words appear in the short description
- Example: Mob with short_desc "a Red Martian Traveler":
  - `Martian.Traveler` matches ✓ (both words in short_desc)
  - `Red.Beggar` doesn't match ✗ ("Beggar" not in short_desc)

### Numeric Targeting Still Works

The original numeric targeting syntax is preserved:
- `2.guard` targets the 2nd guard in the room
- `3.sword` picks up the 3rd sword

The system automatically detects whether the prefix before the first dot is a number or a word.

## Technical Implementation

### Modified Functions

The following functions in `handler.c` were updated to support wildcard dots:

1. **`get_number(char **name)`**: Modified to detect non-numeric prefixes and treat them as wildcards instead of returning an error
2. **`all_words_match(...)`**: Helper function to check if all dot-separated words match a target string
3. **`wildcard_match_char(...)`**: Priority-based matching for characters (exact short_desc, namelist, short_desc words)
4. **`wildcard_match_obj(...)`**: Priority-based matching for objects (exact short_desc, namelist, short_desc words)
5. **`get_char_room_vis(...)`**: Uses wildcard matching for characters in the current room
6. **`get_char_vis(...)`**: Uses wildcard matching for world-wide character targeting
7. **`get_obj_in_list_vis(...)`**: Uses wildcard matching for object targeting in inventories and rooms
8. **`get_obj_vis(...)`**: Uses wildcard matching for world-wide object targeting

### Algorithm

For each target name with dots (e.g., "red.martian.traveler"):

**Priority 1: Exact Short Description Match**
- Check if the entire search string matches the target's short_description exactly (case-insensitive)
- If matched, return immediately (highest priority)

**Priority 2: Namelist Word Matching**
- Split the search string by dots into individual words
- For each word, check if it matches any word in the target's namelist using `isname()`
- All words must match for the target to be selected

**Priority 3: Short Description Word Matching**
- If not matched by namelist, check if all dot-separated words appear in the short_description
- Similar to namelist matching but uses the short_description field instead

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

> consider a Red Martian Traveler
Easy.
(Exact short_desc match - highest priority)

> consider Martian.Traveler
The perfect match!
(Short_desc word match - works even if not in namelist)
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
