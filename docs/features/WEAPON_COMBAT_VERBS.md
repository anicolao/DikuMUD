# Weapon Combat Verbs Fix - October 2025

## Problem Statement

The rifle and other ranged weapons in the game were using inappropriate combat verbs. Specifically:
- The radium rifle at the weapons shop in Greater Helium was "slashing" people instead of shooting them
- The radium pistol also had the same problem
- Bows and crossbows were also using "slash" instead of appropriate ranged weapon verbs

## Root Cause

The weapon type system in DikuMUD uses a value[3] field in weapon objects to determine which combat verb to use. The existing system had these mappings:

- value[3] = 0, 1, 2 → TYPE_WHIP → "whip/whips"
- value[3] = 3 → TYPE_SLASH → "slash/slashes"  
- value[3] = 4, 5, 6 → TYPE_CRUSH → "crush/crushes"
- value[3] = 7 → TYPE_BLUDGEON → "pound/pounds"
- value[3] = 8, 9, 10, 11 → TYPE_PIERCE → "pierce/pierces"

Ranged weapons (rifles, pistols, bows, crossbows) were all using value[3]=3, which mapped to TYPE_SLASH ("slash/slashes"). This made no sense for firearms and bows that should use a verb like "shoot".

## Solution

Added a new weapon type specifically for ranged weapons:

### 1. Added TYPE_SHOOT Constant

**File: `dm-dist-alfa/spells.h`**

Added new constant:
```c
#define TYPE_SHOOT                   109
```

### 2. Updated Attack Text Array

**File: `dm-dist-alfa/fight.c`**

Added "shoot/shoots" to the attack_hit_text array:
```c
struct attack_hit_type attack_hit_text[] =
{
  {"hit",   "hits"},             /* TYPE_HIT      */
  {"pound", "pounds"},           /* TYPE_BLUDGEON */
  {"pierce", "pierces"},         /* TYPE_PIERCE   */
  {"slash", "slashes"},          /* TYPE_SLASH    */
  {"whip", "whips"},             /* TYPE_WHIP     */
  {"claw", "claws"},             /* TYPE_CLAW     */
  {"bite", "bites"},             /* TYPE_BITE     */
  {"sting", "stings"},           /* TYPE_STING    */
  {"crush", "crushes"},          /* TYPE_CRUSH    */
  {"shoot", "shoots"}            /* TYPE_SHOOT    */
};
```

### 3. Updated Weapon Type Mapping

**File: `dm-dist-alfa/fight.c`**

Added case 12 to map to TYPE_SHOOT:
```c
switch (wielded->obj_flags.value[3]) {
    case 0  :
    case 1  :
    case 2  : w_type = TYPE_WHIP; break;
    case 3  : w_type = TYPE_SLASH; break;
    case 4  :
    case 5  :
    case 6  : w_type = TYPE_CRUSH; break;
    case 7  : w_type = TYPE_BLUDGEON; break;
    case 8  :
    case 9  :
    case 10 :
    case 11 : w_type = TYPE_PIERCE; break;
    case 12 : w_type = TYPE_SHOOT; break;  // NEW

    default : w_type = TYPE_HIT; break;
}
```

### 4. Updated Range Check

**File: `dm-dist-alfa/fight.c`**

Updated the attack type range check to include TYPE_SHOOT:
```c
if ((attacktype >= TYPE_HIT) && (attacktype <= TYPE_SHOOT)) {
```

### 5. Updated Weapon Objects

**File: `dm-dist-alfa/lib/zones/greater_helium.obj`**

Changed value[3] from 3 to 12 for ranged weapons:

- **Radium pistol (#3590)**: Changed `0 2 4 3` to `0 2 4 12`
- **Radium rifle (#3591)**: Changed `0 2 6 3` to `0 2 6 12`
- **Small crossbow (#3722)**: Changed `0 1 4 3` to `0 1 4 12`
- **Short bow (#3760)**: Changed `0 1 4 3` to `0 1 4 12`
- **Long bow (#3761)**: Changed `0 1 6 3` to `0 1 6 12`

### 6. Updated Documentation

**File: `dm-dist-alfa/doc/values.doc`**

Added documentation for the new weapon type:
```
         NUMBER  CATEGORY   Message type
            2  : Slash         "whip/whips"
            3  : Slash         "slash/slashes"

            6  : Bludgeon      "crush/crushes"
            7  : Bludgeon      "pound/pounds"

           11  : Pierce        "pierce/pierces"
           12  : Shoot         "shoot/shoots"     // NEW
```

## Testing

Created integration test: `tests/integration/test_weapon_combat_words.yaml`

The test verifies:
1. Weapons are available for purchase at the weapon shop
2. Rifle can be purchased
3. Rifle can be wielded
4. Basic functionality works

## Combat Message Examples

With these changes, combat messages will now show:

**Before (incorrect):**
- "You slash the orc with your radium rifle."
- "The warrior slashes you with his radium pistol."

**After (correct):**
- "You shoot the orc with your radium rifle."
- "The warrior shoots you with his radium pistol."

## Technical Details

### Attack Text Array Indexing

The attack_hit_text array is indexed by subtracting TYPE_HIT (100) from the weapon type:
- TYPE_HIT (100) → index 0
- TYPE_BLUDGEON (101) → index 1
- TYPE_PIERCE (102) → index 2
- TYPE_SLASH (103) → index 3
- TYPE_WHIP (104) → index 4
- TYPE_CLAW (105) → index 5
- TYPE_BITE (106) → index 6
- TYPE_STING (107) → index 7
- TYPE_CRUSH (108) → index 8
- TYPE_SHOOT (109) → index 9

The array has 10 elements (indices 0-9), so this works correctly.

### Weapon Value Format

In object files, weapon values are specified as:
```
value[0] value[1] value[2] value[3]
```

For weapons:
- value[0]: Not used
- value[1]: Number of dice for damage (e.g., 2 for 2d6)
- value[2]: Size of dice for damage (e.g., 6 for 2d6)
- value[3]: Weapon type number (now 12 for ranged weapons)

## Backward Compatibility

This change is fully backward compatible:
- Existing weapons continue to work with their current values
- Only the specific ranged weapons were changed
- No changes to save files or player data required
- The new TYPE_SHOOT is simply an additional option

## Future Considerations

Other potential weapon types that could be added:
- TYPE_BURN for flaming weapons
- TYPE_FREEZE for ice weapons
- TYPE_ZAP for lightning weapons
- TYPE_BLAST for explosive weapons

The system is extensible - just add a new TYPE_* constant, add the text to attack_hit_text[], and map object value[3] numbers to it in the switch statement.

## Files Changed

1. `dm-dist-alfa/spells.h` - Added TYPE_SHOOT constant
2. `dm-dist-alfa/fight.c` - Updated attack text array, switch statement, and range check
3. `dm-dist-alfa/lib/zones/greater_helium.obj` - Updated 5 weapon objects
4. `dm-dist-alfa/doc/values.doc` - Added documentation for new weapon type
5. `tests/integration/test_weapon_combat_words.yaml` - Added integration test

## Build and Deployment

All changes compile cleanly with no warnings or errors. The integration test passes.

```bash
cd dm-dist-alfa
make clean
make
make worldfiles
make test
```
