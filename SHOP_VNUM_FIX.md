# Shop Vnum Fix - October 2025

## Problem
After adding fountains and waterskins to the game, guildmasters and some shops stopped working properly.

## Root Cause
Shop vnums were duplicated across multiple zones:
- Lesser Helium had shops with vnums: 1, 3, 5, 7, 9, 11, 12, 14
- Greater Helium had shops with vnums: 1, 3, 5, 7, 9, 11, 13
- Thark Territory had shop with vnum: 1

When the world builder combined all zones into `tinyworld.shp`, duplicate shop vnums caused later definitions to overwrite earlier ones in the file. This resulted in only the last shop with each vnum being loaded by the server, breaking many shops and their associated shopkeepers (including guildmasters).

## Solution

### 1. Enhanced World Validation
Added shop validation to `tools/validate_world.py`:
- Tracks all shop vnums globally in `all_shops` dictionary
- Detects duplicate shop vnums across zones
- Validates shop keeper mobile references
- Validates shop room references
- Validates produced object references
- Includes shop count in validation summary

### 2. Renumbered Shop Vnums
Assigned globally unique vnums to all shops:

**Greater Helium** (7 shops):
- Shop 1: keeper=3911, room=3941
- Shop 2: keeper=3902, room=3928
- Shop 3: keeper=3943, room=3916
- Shop 4: keeper=3944, room=3935
- Shop 5: keeper=3900, room=3933
- Shop 6: keeper=3911, room=3941
- Shop 7: keeper=3906, room=3925

**Lesser Helium** (8 shops):
- Shop 8: keeper=3001, room=3009
- Shop 9: keeper=3002, room=3010
- Shop 10: keeper=3042, room=3018
- Shop 11: keeper=3045, room=3022
- Shop 12: keeper=3000, room=3033
- Shop 13: keeper=3100, room=3106
- Shop 14: keeper=3046, room=3048
- Shop 15: keeper=3010, room=3035

**Thark Territory** (1 shop):
- Shop 16: keeper=4090, room=4040

## Verification
1. World validation now passes with no errors
2. Built tinyworld.shp contains 16 unique shop vnums
3. Server starts successfully without errors
4. Tested shops in-game (provisions merchant) - list command works
5. Tested guildmaster functionality - practice command works

## Important Notes
- **Shop vnums must be globally unique**, just like room vnums, mobile vnums, and object vnums
- Shop vnums do not need to follow zone-based numbering conventions (unlike rooms/mobs/objects)
- When adding new shops, ensure the vnum is not used by any other shop in any zone
- Run `python3 tools/validate_world.py dm-dist-alfa/lib/zones_yaml/*.yaml` to verify uniqueness

## Future Additions
When adding new shops:
1. Check the highest shop vnum currently in use: `grep -h "^- vnum:" dm-dist-alfa/lib/zones_yaml/*.yaml | grep -A1 "^shops:" | grep vnum | sort -n | tail -1`
2. Use the next available sequential number
3. Run validation to confirm no duplicates

## Files Modified
- `tools/validate_world.py` - Added shop validation
- `dm-dist-alfa/lib/zones_yaml/greater_helium.yaml` - Renumbered shops 1,3,5,7,9,11,13 → 1,2,3,4,5,6,7
- `dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml` - Renumbered shops 1,3,5,7,9,11,12,14 → 8,9,10,11,12,13,14,15
- `dm-dist-alfa/lib/zones_yaml/thark_territory.yaml` - Renumbered shop 1 → 16
