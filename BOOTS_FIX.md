# Boots Fix - Boots Not Wearable

## Problem

Multiple boot items across different zones were not wearable by players. Players could not pick up or wear these boots, making them useless as equipment.

## Root Cause

The boot objects had incorrect flags:

1. **Sewers and Southern Approach boots** had:
   - `type_flag: 2` (ITEM_SCROLL) instead of `9` (ITEM_ARMOR)
   - `wear_flags: 0` instead of `65` (ITEM_TAKE + ITEM_WEAR_FEET)

2. **Greater Helium and Dead Sea boots** had:
   - `wear_flags: 16385` (ITEM_HOLD + ITEM_TAKE) instead of `65` (ITEM_TAKE + ITEM_WEAR_FEET)

3. **Thark Territory boots** had:
   - `wear_flags: 1` (ITEM_TAKE only) instead of `65` (ITEM_TAKE + ITEM_WEAR_FEET)

Without the correct flags, boots could not be worn on feet, and in some cases couldn't even be picked up.

## Technical Details

### Correct Boot Configuration

According to `dm-dist-alfa/structs.h`:
- `ITEM_TAKE = 1` - Can be picked up
- `ITEM_WEAR_FEET = 64` - Can be worn on feet
- Combined: `65` - Can be taken AND worn on feet

Boots should be:
- `type_flag: 9` (ITEM_ARMOR)
- `wear_flags: 65` (ITEM_TAKE + ITEM_WEAR_FEET)

### Affected Objects

The following boot objects were fixed:

| Vnum | Name | Zone | Old type_flag | New type_flag | Old wear_flags | New wear_flags |
|------|------|------|---------------|---------------|----------------|----------------|
| 3212 | leather boots (muddy) | sewers | 2 | 9 | 0 | 65 |
| 3408 | leather travel boots | southern_approach | 2 | 9 | 0 | 65 |
| 3562 | combat boots | greater_helium | 9 | 9 | 16385 | 65 |
| 3889 | worn boots | dead_sea_wilderness | 9 | 9 | 16385 | 65 |
| 4113 | Thark leather boots | thark_territory | 9 | 9 | 1 | 65 |

### Reference Boot

The correctly configured boots in lesser_helium.yaml (vnum 3069) were used as reference:
```yaml
type_flag: 9
wear_flags: 65
```

## Solution

Changed the following files in `dm-dist-alfa/lib/zones_yaml/`:
- `sewers.yaml` - Updated vnum 3212 (muddy leather boots)
- `southern_approach.yaml` - Updated vnum 3408 (leather travel boots)
- `greater_helium.yaml` - Updated vnum 3562 (combat boots)
- `dead_sea_wilderness.yaml` - Updated vnum 3889 (worn boots)
- `thark_territory.yaml` - Updated vnum 4113 (Thark leather boots)

The world files are rebuilt from YAML sources, so the changes propagate to:
- `dm-dist-alfa/lib/tinyworld.obj`

## Verification

After the fix, all boot objects in `tinyworld.obj` show:
```
9 0 65
```

Where:
- 9 = type_flag (ITEM_ARMOR) ✓
- 0 = extra_flags
- 65 = wear_flags (ITEM_TAKE + ITEM_WEAR_FEET) ✓

## Impact

- Players can now pick up and wear all boots across all zones
- Boots function properly as foot armor
- Consistent with other properly-configured armor items in the game
- All 5 affected boot items now work as intended

## Files Changed

- `dm-dist-alfa/lib/zones_yaml/sewers.yaml` - Updated wear_flags and type_flag for vnum 3212
- `dm-dist-alfa/lib/zones_yaml/southern_approach.yaml` - Updated wear_flags and type_flag for vnum 3408
- `dm-dist-alfa/lib/zones_yaml/greater_helium.yaml` - Updated wear_flags for vnum 3562
- `dm-dist-alfa/lib/zones_yaml/dead_sea_wilderness.yaml` - Updated wear_flags for vnum 3889
- `dm-dist-alfa/lib/zones_yaml/thark_territory.yaml` - Updated wear_flags for vnum 4113
- World files automatically rebuilt via `make worldfiles`

## Related Documentation

This fix follows the same pattern as:
- `BRONZE_COINS_FIX.md` - Fixed coins with wear_flags: 0
- `WARRIOR_REEQUIP_FIX.md` - Fixed harnesses and shields with incorrect wear_flags

## See Also

- `DIKUMUD_FILE_FORMATS.md` - Wear flags documentation
- `dm-dist-alfa/structs.h` - Flag definitions
