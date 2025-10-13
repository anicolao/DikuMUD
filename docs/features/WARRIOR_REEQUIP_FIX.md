# Warrior Reequip Integration Test and Database Fixes

## Summary

Created an integration test for the warrior reequip functionality and fixed multiple database issues that prevented warriors from properly equipping their gear.

## Test Created

**File**: `tests/integration/test_warrior_reequip.yaml`

This integration test validates that warriors can:
1. Use the reequip command to receive equipment from the War Master
2. Wield their weapon (quality short sword)
3. Wear the leather harness on their body
4. Wear the shield
5. Hold the glow crystal (light source)

## Issues Found and Fixed

### 1. Warriors Missing Weapon

**Problem**: Warriors were only receiving 4 items (glow crystal, water cask, harness, shield) but no weapon, unlike other classes who all received weapons.

**Fix**: Added quality short sword (item 3521) to warrior equipment in `spec_procs.c`:
```c
obj = read_object(3521, VIRTUAL);
if (obj) obj_to_char(obj, ch);
```

**File Modified**: `dm-dist-alfa/spec_procs.c`

### 2. Harness Had Wrong Wear Flags

**Problem**: The simple leather harness (and other harnesses) had `wear_flags: 16385` which means ITEM_HOLD + ITEM_TAKE, but harnesses should be wearable on the body.

**Fix**: Changed wear_flags to `9` (ITEM_WEAR_BODY + ITEM_TAKE) for:
- Simple leather harness (item 3550)
- Quality battle harness (item 3551)
- Jeweled noble harness (item 3552)

**File Modified**: `dm-dist-alfa/lib/zones_yaml/greater_helium.yaml`

### 3. Shields Had Wrong Wear Flags

**Problem**: Shields had `wear_flags: 16385` which means ITEM_HOLD + ITEM_TAKE, but shields should be wearable as shields.

**Fix**: Changed wear_flags to `513` (ITEM_WEAR_SHIELD + ITEM_TAKE) for:
- Small shield (item 3563)
- Large shield (item 3564)

**File Modified**: `dm-dist-alfa/lib/zones_yaml/greater_helium.yaml`

## Wear Flags Reference

From `dm-dist-alfa/structs.h`:
- `ITEM_TAKE = 1` - Can be picked up
- `ITEM_WEAR_BODY = 8` - Can be worn on body
- `ITEM_WEAR_SHIELD = 512` - Can be worn as shield
- `ITEM_WIELD = 8192` - Can be wielded as weapon
- `ITEM_HOLD = 16384` - Can be held

## Documentation Updates

Updated the following files to reflect warrior equipment changes:
- `REEQUIP_FEATURE.md` - Added quality short sword to warrior equipment list
- `dm-dist-alfa/test_reequip.sh` - Updated summary and item count

## Test Results

All tests now pass:
- Integration test: `tests/integration/test_warrior_reequip.yaml` ✓
- Unit test: `dm-dist-alfa/test_reequip.sh` ✓

Warriors can now:
- Receive complete equipment set including weapon
- Wear harness on body
- Wear shield properly
- Wield their sword
- Hold the glow crystal for light

## Impact

These fixes ensure that:
1. Warriors are properly equipped with a weapon like other classes
2. All armor items can be worn correctly
3. The reequip feature works as designed for all classes
4. New players choosing the warrior class have a complete starting equipment set
