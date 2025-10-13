# Bronze Coins Fix - Sewer Coins Not Retrievable from Corpses

## Problem

Bronze, silver, and gold coins given to mobs in the sewers zone were not retrievable from corpses after killing the mobs. Players would see the coins in the corpse but could not pick them up.

## Root Cause

The coin objects in the sewers zone (vnums 3219, 3220, 3231) had `wear_flags: 0` instead of `wear_flags: 1` (ITEM_TAKE). Without the ITEM_TAKE flag, objects cannot be picked up by players.

## Technical Details

### Object Properties

In DikuMUD, objects have a `wear_flags` field that determines where they can be worn and whether they can be taken:
- Bit 1 (value 1) = ITEM_TAKE - Object can be picked up
- Without this bit, objects are non-takeable (like furniture)

### Code Behavior

When money is created dynamically in the code (via `create_money()` in handler.c), it properly sets:
```c
obj->obj_flags.wear_flags = ITEM_TAKE;
```

However, coin objects defined in the zone files and given to mobs via zone resets need to have the wear_flags set correctly in the data files.

### Affected Objects

The following coin objects in `sewers.yaml` were fixed:

| Vnum | Name | Old wear_flags | New wear_flags |
|------|------|----------------|----------------|
| 3219 | silver coins | 0 | 1 |
| 3220 | bronze coins | 0 | 1 |
| 3231 | gold coins | 0 | 1 |

### Zone Resets

These coin objects are given to various mobs in the sewers zone via 'G' (Give) commands in the zone reset list:
- Bronze coins (3220) given to ulsio rats (mob 3500)
- Silver coins (3219) given to larger ulsio and other creatures
- Gold coins (3231) given to higher-level creatures throughout the zone

## Solution

Changed `wear_flags: 0` to `wear_flags: 1` for all three coin objects in:
- `dm-dist-alfa/lib/zones_yaml/sewers.yaml`

The world files are rebuilt from YAML sources, so the change propagates to:
- `dm-dist-alfa/lib/tinyworld.obj`

## Verification

After the fix, the objects in `tinyworld.obj` show:
```
10 0 1
```

Where:
- 10 = type_flag (ITEM_MONEY)
- 0 = extra_flags
- 1 = wear_flags (ITEM_TAKE) ✓

## Impact

- Players can now retrieve bronze, silver, and gold coins from mob corpses in the sewers
- No code changes required - only data file updates
- Consistent with how dynamically-created money works in the game
- All existing coin loot in the sewers zone is now properly retrievable

## Files Changed

- `dm-dist-alfa/lib/zones_yaml/sewers.yaml` - Updated wear_flags for vnums 3219, 3220, 3231
- World files automatically rebuilt via `make worldfiles`

## Related Code

For reference, the money creation code in `dm-dist-alfa/handler.c` (line 1209):
```c
struct obj_data *create_money( int amount )
{
    // ... object creation ...
    obj->obj_flags.type_flag = ITEM_MONEY;
    obj->obj_flags.wear_flags = ITEM_TAKE;  // This makes it takeable
    // ...
}
```

This fix ensures that statically-defined coin objects match the behavior of dynamically-created coins.
