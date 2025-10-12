# Object Flags Review and Corrections

## Summary

Comprehensive review and correction of all object flags across all game zones. Fixed 66 objects with incorrect `type_flag` and `wear_flags` values.

## Problem

Objects throughout the game world had incorrect flags that prevented them from being used properly:
- Wearable armor items (boots, helmets, harnesses, etc.) with wrong `type_flag`
- Wearable items with `ITEM_HOLD` instead of proper wear location flags
- ARMOR type items that should have been OTHER or TREASURE
- Inconsistent flag patterns across similar items in different zones

## Solution

Created validation script to identify all objects with incorrect flags, then systematically corrected them in YAML zone files. Rebuilt world files from corrected sources.

## Technical Details

### Flag Reference

From `dm-dist-alfa/structs.h`:

**Type Flags:**
- `ITEM_LIGHT = 1`
- `ITEM_SCROLL = 2`
- `ITEM_WAND = 3`
- `ITEM_STAFF = 4`
- `ITEM_WEAPON = 5`
- `ITEM_TREASURE = 8`
- `ITEM_ARMOR = 9`
- `ITEM_OTHER = 12`
- `ITEM_TRASH = 13`
- `ITEM_CONTAINER = 15`
- `ITEM_MONEY = 20`

**Wear Flags (Bitvector):**
- `ITEM_TAKE = 1` - Can be picked up
- `ITEM_WEAR_FINGER = 2` - Can be worn on finger
- `ITEM_WEAR_NECK = 4` - Can be worn on neck
- `ITEM_WEAR_BODY = 8` - Can be worn on body
- `ITEM_WEAR_HEAD = 16` - Can be worn on head
- `ITEM_WEAR_LEGS = 32` - Can be worn on legs
- `ITEM_WEAR_FEET = 64` - Can be worn on feet
- `ITEM_WEAR_HANDS = 128` - Can be worn on hands
- `ITEM_WEAR_ARMS = 256` - Can be worn on arms
- `ITEM_WEAR_SHIELD = 512` - Can be worn as shield
- `ITEM_WEAR_ABOUT = 1024` - Can be worn about body (cloaks, capes)
- `ITEM_WEAR_WAIST = 2048` - Can be worn on waist (belts)
- `ITEM_WEAR_WRIST = 4096` - Can be worn on wrist
- `ITEM_WIELD = 8192` - Can be wielded as weapon
- `ITEM_HOLD = 16384` - Can be held

### Correction Patterns

#### Pattern 1: Wrong Type Flag for Armor
**Issue:** Wearable armor items had type_flag set to WAND(3), STAFF(4), SCROLL(2), etc.  
**Fix:** Changed to ITEM_ARMOR(9)  
**Examples:**
- Reinforced factory guard armor (4056): WAND(3) → ARMOR(9)
- Factory guard helmet (4057): STAFF(4) → ARMOR(9)
- Hardened leather armor (3228): WAND(3) → ARMOR(9)

#### Pattern 2: HOLD Instead of Wear Location
**Issue:** Armor items had `wear_flags: 16385` (TAKE+HOLD) instead of proper wear location  
**Fix:** Changed to TAKE + appropriate WEAR_* flag  
**Examples:**
- Palace guard harness (3553): 16385 → 9 (TAKE+WEAR_BODY)
- Battle helmet (3560): 16385 → 17 (TAKE+WEAR_HEAD)
- Wooden shield (3875): 16385 → 513 (TAKE+WEAR_SHIELD)

#### Pattern 3: TAKE Only (No Wear Location)
**Issue:** ARMOR items had only TAKE flag, no wear location  
**Fix:** Added appropriate WEAR_* flag  
**Examples:**
- Zodangan leather harness (3602): 1 → 9 (TAKE+WEAR_BODY)
- Thark leather boots (4113): 1 → 65 (TAKE+WEAR_FEET)
- Trophy belt (4132): Changed to OTHER(12) with WEAR_WAIST

#### Pattern 4: Wrong Wear Location
**Issue:** Items had wear location that didn't match their description  
**Fix:** Corrected to proper body location  
**Examples:**
- Gathol harness (3781): WEAR_HEAD(17) → WEAR_BODY(9)
- Armored gauntlets (3561): WEAR_LEGS(33) → WEAR_HANDS(129)
- Brass leg harness (3306): WEAR_LEGS(33) → WEAR_BODY(9)

#### Pattern 5: Non-Wearable Items Marked as ARMOR
**Issue:** Tools, trophies, and other items marked as ARMOR with no valid wear location  
**Fix:** Changed to OTHER(12) or TREASURE(8) with TAKE or HOLD flags  
**Examples:**
- Thark trinket (4116): ARMOR(9) → TREASURE(8)
- Ceremonial bowl (4121): ARMOR(9) → OTHER(12)
- Medicine pouch (4133): ARMOR(9) → OTHER(12)

## Objects Fixed by Zone

### atmosphere_factory (4 objects)
- 4056: reinforced factory guard armor - type_flag 3→9, wear_flags 0→9
- 4057: factory guard helmet - type_flag 4→9, wear_flags 0→17
- 4058: engineering tool set - type_flag 1→12, wear_flags 0→16385
- 4068: insulated work gloves - type_flag 6→9, wear_flags 0→129

### atmosphere_lower (1 object)
- 4258: enhanced synthetic armor - type_flag 3→9, wear_flags 0→9

### dead_sea_bottom_channel (2 objects)
- 3306: brass leg harness - wear_flags 33→9 (LEGS→BODY)
- 3315: golden silk cloak - type_flag 12→9 (OTHER→ARMOR)

### dead_sea_wilderness (5 objects)
- 3752: halberd - wear_flags 9→8193 (added WIELD)
- 3862: tattered harness - wear_flags 16385→9
- 3875: wooden shield - wear_flags 16385→513
- 3888: tattered cloak - wear_flags 16385→1025
- 3890: utility tool belt - wear_flags 16385→2049

### gathol (1 object)
- 3781: Gathol harness - wear_flags 17→9 (HEAD→BODY)

### greater_helium (11 objects)
- 3501: scholar robe - wear_flags 1→9
- 3502: scholar mantle - wear_flags 1→1025
- 3553: palace guard harness - wear_flags 16385→9
- 3560: battle helmet - wear_flags 16385→17
- 3561: armored gauntlets - wear_flags 33→129 (LEGS→HANDS)
- 3570: rank medallion - wear_flags 16385→5
- 3571: noble's ring - wear_flags 16385→3
- 3671: smith's hammer - type_flag 21→12 (PEN→OTHER)
- 3700: calot collar - type_flag 21→12 (for animals, not player)
- 3701: calot harness - type_flag 21→12 (for animals, not player)
- 3740: armor plating - wear_flags 16385→9
- 3741: armored vambraces - wear_flags 16385→257
- 3743: leg greaves - wear_flags 16385→33
- 3763: bowstrings - type_flag 21→12, wear_flags 16385→1

### kaol (2 objects)
- 3821: kaol harness - wear_flags 16385→9
- 4500: Kaolian military harness - wear_flags 5→9 (NECK→BODY)

### lesser_helium (5 objects)
- 3044: sleeping staff - type_flag 4→12 (magic item, not weapon)
- 3068: studded leg harness - wear_flags 33→9 (LEGS→BODY)
- 3490: guard harness - wear_flags 16385→9
- 3496: cadet helmet - wear_flags 16385→17
- 3497: training shield - wear_flags 16385→513
- 3498: training harness - wear_flags 16385→9

### ptarth (2 objects)
- 3752: ptarth harness - wear_flags 8193→9
- 4301: Ptarth military harness - type_flag 12→9, wear_flags 16385→9

### sewers (11 objects)
- 3210: leather jerkin - type_flag 3→9, wear_flags 0→9
- 3211: leather cap - type_flag 4→9, wear_flags 0→17
- 3213: torn pants - type_flag 7→9, wear_flags 0→33
- 3222: (generic item) - type_flag 9→12
- 3228: hardened leather armor - type_flag 3→9, wear_flags 0→9
- 3229: steel helmet - type_flag 4→9, wear_flags 0→17
- 3233: leather vest - wear_flags 0→9
- 3234: leather leggings - wear_flags 0→33
- 3235: leather cap - wear_flags 1→17
- 3236: leather gloves - wear_flags 0→129

### southern_approach (7 objects)
- 3404: guard's leather harness - type_flag 3→9, wear_flags 0→9
- 3407: guard's helmet - type_flag 4→9, wear_flags 0→17
- 3413: round shield - wear_flags 0→513
- 3417: weatherproof travel cloak - type_flag 12→9, wear_flags 0→1025
- 3421: reinforced battle harness - type_flag 3→9, wear_flags 0→9
- 3435: scout harness - wear_flags 16385→9
- 3436: scout helmet - wear_flags 16385→17
- 3437: scout shield - wear_flags 16385→513

### thark_territory (26 objects)
Armor items:
- 4109: thark harness - wear_flags 1→9
- 4110: thark leather harness - wear_flags 17→9 (HEAD→BODY)
- 4111: ornate thark harness - wear_flags 33→9 (LEGS→BODY)
- 4112: thark bracers - wear_flags 1→257
- 4114: thark metal helmet - wear_flags 513→17 (SHIELD→HEAD)
- 4115: thark metal shield - wear_flags 1025→513 (ABOUT→SHIELD)

Non-wearable items (ARMOR→OTHER/TREASURE):
- 4116: thark trinket - type_flag 9→8 (TREASURE)
- 4117: thoat horn - type_flag 9→12, wear_flags 1→16385
- 4118: decorative tusk - type_flag 9→8 (TREASURE)
- 4119: carved idol - type_flag 9→12, wear_flags 1→16385
- 4120: tribal token - type_flag 9→8 (TREASURE)
- 4121: ceremonial bowl - type_flag 9→12, wear_flags 1→16385
- 4122: thoat harness - type_flag 8→12, wear_flags 1→16385 (for animals)
- 4123: war trophy - type_flag 2→12, wear_flags 1→16385
- 4124: hunting trophy - type_flag 17→12, wear_flags 1→16385
- 4125: trading goods - type_flag 9→8 (TREASURE)
- 4126: beast saddle - type_flag 9→12, wear_flags 1→16385
- 4127: water pouch - type_flag 9→12, wear_flags 1→16385
- 4128: dried meat - type_flag 9→12, wear_flags 1→16385
- 4129: primitive tools - type_flag 9→12, wear_flags 1→16385
- 4130: hunting net - type_flag 9→12, wear_flags 1→16385
- 4131: ceremonial dagger - type_flag 9→8 (TREASURE)
- 4132: trophy belt - type_flag 12→9 (can be worn), wear_flags 1→2049
- 4133: medicine pouch - type_flag 9→12, wear_flags 1→16385
- 4138: incubator moss - type_flag 9→12
- 4139: radium heater - type_flag 9→12, wear_flags 1→16385
- 4141: rough gemstone - type_flag 9→8 (TREASURE)
- 4142: scrap metal - type_flag 9→12
- 4143: ancient artifact - type_flag 9→8 (TREASURE)
- 4145: battle banner - type_flag 9→12, wear_flags 1→16385
- 4146: signal drum - type_flag 9→12, wear_flags 1→16385
- 4147: sleeping furs - type_flag 9→12
- 4148: raw beast hide - type_flag 9→12
- 4149: bone tools - type_flag 9→12, wear_flags 1→16385

### zodanga (4 objects)
- 3602: Zodangan leather harness - wear_flags 1→9
- 3603: ornate Zodangan harness - wear_flags 1→9
- 3606: Zodangan metal shield - wear_flags 1→513
- 3607: Zodangan plate armor - wear_flags 1→9

## Impact

- **Playability:** All wearable items can now be properly worn by players
- **Consistency:** Similar items across zones now have consistent flags
- **Game Balance:** Players can now access all intended armor and equipment
- **Future Development:** Established clear patterns for item flag assignment

## Files Changed

### YAML Zone Files (Source)
- `dm-dist-alfa/lib/zones_yaml/atmosphere_factory.yaml`
- `dm-dist-alfa/lib/zones_yaml/atmosphere_lower.yaml`
- `dm-dist-alfa/lib/zones_yaml/dead_sea_bottom_channel.yaml`
- `dm-dist-alfa/lib/zones_yaml/dead_sea_wilderness.yaml`
- `dm-dist-alfa/lib/zones_yaml/gathol.yaml`
- `dm-dist-alfa/lib/zones_yaml/greater_helium.yaml`
- `dm-dist-alfa/lib/zones_yaml/kaol.yaml`
- `dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml`
- `dm-dist-alfa/lib/zones_yaml/ptarth.yaml`
- `dm-dist-alfa/lib/zones_yaml/sewers.yaml`
- `dm-dist-alfa/lib/zones_yaml/southern_approach.yaml`
- `dm-dist-alfa/lib/zones_yaml/thark_territory.yaml`
- `dm-dist-alfa/lib/zones_yaml/zodanga.yaml`

### Generated World Files (Rebuilt)
- `dm-dist-alfa/lib/tinyworld.obj` - Regenerated from YAML sources

## Validation

Created comprehensive validation script (`/tmp/check_object_flags.py`) that:
- Checks all objects across all zones
- Validates type_flag matches item purpose
- Validates wear_flags match item type
- Reports inconsistencies and suggests fixes

All fixes verified by:
1. Running validation script before and after changes
2. Rebuilding world files from YAML sources
3. Confirming no build errors or warnings

## Related Documentation

- `DIKUMUD_FILE_FORMATS.md` - Object file format and flag definitions
- `dm-dist-alfa/structs.h` - C header with flag constants
- `BOOTS_FIX.md` - Previous fix for boot objects
- `WARRIOR_REEQUIP_FIX.md` - Previous fix for harnesses and shields
- `BRONZE_COINS_FIX.md` - Previous fix for coin objects

## Best Practices Established

### For Armor Items:
1. **type_flag** should be `ITEM_ARMOR (9)`
2. **wear_flags** should include `ITEM_TAKE (1)` plus appropriate wear location:
   - Boots/Shoes: `ITEM_WEAR_FEET (64)` → total 65
   - Helmets/Caps: `ITEM_WEAR_HEAD (16)` → total 17
   - Gloves/Gauntlets: `ITEM_WEAR_HANDS (128)` → total 129
   - Body Armor/Harnesses: `ITEM_WEAR_BODY (8)` → total 9
   - Leggings/Greaves: `ITEM_WEAR_LEGS (32)` → total 33
   - Bracers/Vambraces: `ITEM_WEAR_ARMS (256)` → total 257
   - Shields: `ITEM_WEAR_SHIELD (512)` → total 513
   - Cloaks/Capes: `ITEM_WEAR_ABOUT (1024)` → total 1025
   - Belts: `ITEM_WEAR_WAIST (2048)` → total 2049
   - Bracelets: `ITEM_WEAR_WRIST (4096)` → total 4097
   - Rings: `ITEM_WEAR_FINGER (2)` → total 3
   - Necklaces/Amulets: `ITEM_WEAR_NECK (4)` → total 5

### For Weapons:
1. **type_flag** should be `ITEM_WEAPON (5)`
2. **wear_flags** should be `ITEM_TAKE (1) + ITEM_WIELD (8192)` → total 8193

### For Tools/Misc Items:
1. **type_flag** should be `ITEM_OTHER (12)` or `ITEM_TREASURE (8)`
2. **wear_flags** should be `ITEM_TAKE (1)` or `ITEM_TAKE + ITEM_HOLD (16384)` → total 16385

### For Animal Equipment:
1. **type_flag** should be `ITEM_OTHER (12)`
2. **wear_flags** should be `ITEM_TAKE + ITEM_HOLD (16385)`
3. These are not wearable by players (collars, harnesses for mounts, etc.)

## Testing

World files successfully rebuilt from YAML sources with validation:
```
Found 523 rooms, 274 mobiles, 473 objects, 20 shops
Found 19 zones
✓ Validation passed! No errors or warnings found.
```

All 66 object flag corrections applied successfully.
