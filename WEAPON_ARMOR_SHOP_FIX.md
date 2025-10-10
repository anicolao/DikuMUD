# Weapon and Armor Shop Fix - October 2025

## Problem
The weapon smith and armor shops in Lesser Helium were not working. Players could not use the `list` command in rooms 3011 (The Weapon Smith) and 3020 (The Armory).

## Root Cause Analysis

### Missing Shops
The original Lesser Helium zone had shops configured in the old `.shp` format:
- Shop #2: Weaponsmith (mob 3003) in room 3011
- Shop #4: Armorer (mob 3004) in room 3020

These shops were **not migrated** to the YAML format when the zone was converted, leaving two functional shop rooms with keeper mobs but no shop configurations.

### Incorrect Reset Commands
Even after adding the shop configurations, the zone reset commands were loading the wrong items into the shopkeepers' inventories:
- Weaponsmith (mob 3003) was being given light sources (objects 3020-3024) instead of weapons
- Armorer (mob 3004) was being given light sources (objects 3072-3098) instead of armor

This happened because the object vnums in the old `.shp` file referred to objects that had been renumbered or replaced during zone development.

## Solution

### 1. Enhanced Shop Validation Tool (`tools/validate_shops.py`)

Added comprehensive detection of missing shops:

#### New Helper Functions
- `load_mob_names()`: Extracts mob short descriptions from `.mob` files
- `load_room_names()`: Extracts room names from `.wld` files

#### Missing Shop Detection
The validator now checks for:

**Potential Shopkeeper Mobs Without Shops:**
- Searches mob names for shopkeeper keywords: 'merchant', 'shopkeeper', 'grocer', 'baker', 'butcher', 'armorer', 'weaponsmith', 'blacksmith', 'jeweler', 'tailor', 'bartender', 'innkeeper', 'vendor', 'trader', 'dealer', 'seller', etc.
- Reports mobs that match keywords but have no shops assigned

**Potential Shop Rooms Without Shops:**
- Searches room names for shop keywords: 'shop', 'store', 'merchant', 'armory', 'weapon smith', 'jeweler', 'tailor', 'baker', 'butcher', 'tavern', 'inn', 'trader', 'market', etc.
- Reports rooms that match keywords but have no shops assigned

#### Enhanced Output
The validator now displays:
- Keeper mob names (not just vnums)
- Room names (not just vnums)
- Clear warnings about potential missing shops

### 2. Added Missing Shop Configurations

**Shop #17 - Weapon Smith**
- **Keeper**: Mob 3003 (the Red Martian Weaponsmith)
- **Room**: 3011 (The Weapon Smith)
- **Products**:
  - 3520: a fine stiletto
  - 3521: a quality short sword
  - 3522: a Warlord's longsword
  - 3590: a radium pistol
  - 3591: a radium rifle
  - 3226: a fine steel dagger
- **Buy Types**: 5 (weapon), 6 (fireweapon), 7 (missile)
- **Profit Margins**: 1.3 buy, 0.4 sell

**Shop #18 - Armory**
- **Keeper**: Mob 3004 (the Red Martian Harness-Maker)
- **Room**: 3020 (The Armory)
- **Products**:
  - 3066: a studded chest harness
  - 3067: a studded helm
  - 3068: a studded leg harness
  - 3069: a pair of studded boots
  - 3070: a pair of studded gloves
  - 3071: a pair of studded sleeves
- **Buy Types**: 9 (armor)
- **Profit Margins**: 1.0 buy, 0.5 sell

### 3. Fixed Zone Reset Commands

**Weaponsmith (Mob 3003)**
Changed from:
```yaml
- command: G
  arg1: 3020  # radium lamp (wrong!)
- command: G
  arg1: 3021  # radium lamp (wrong!)
# ... more lamps
```

Changed to:
```yaml
- command: G
  arg1: 3520  # fine stiletto
- command: G
  arg1: 3521  # quality short sword
- command: G
  arg1: 3522  # Warlord's longsword
- command: G
  arg1: 3590  # radium pistol
- command: G
  arg1: 3591  # radium rifle
- command: G
  arg1: 3226  # fine steel dagger
```

**Armorer (Mob 3004)**
Removed all light source items (3072-3098) and kept only armor items (3066-3071).

## Files Modified

1. **`tools/validate_shops.py`**
   - Added `load_mob_names()` function
   - Added `load_room_names()` function
   - Added missing shop detection with keyword matching
   - Enhanced output to show mob/room names

2. **`dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml`**
   - Added shop #17 (weaponsmith) configuration
   - Added shop #18 (armorer) configuration
   - Fixed reset commands for mob 3003 (weaponsmith)
   - Fixed reset commands for mob 3004 (armorer)

## Testing

### Validation
```bash
cd /home/runner/work/DikuMUD/DikuMUD
python3 tools/validate_shops.py dm-dist-alfa/lib/tinyworld.shp \
    dm-dist-alfa/lib/tinyworld.mob \
    dm-dist-alfa/lib/tinyworld.obj \
    dm-dist-alfa/lib/tinyworld.wld
```

**Results:**
- Shop #17 and #18 validate successfully
- Mob 3003 and 3004 no longer appear in "missing shops" warnings
- Room 3011 and 3020 no longer appear in "missing shops" warnings
- Total shops increased from 16 to 18

### In-Game Testing

**Weapon Smith (Room 3011):**
```
> goto 3011
The Weapon Smith
   You are inside a weapon smith's shop.  Swords, daggers, and radium pistols line
the walls.  A small notice is carved on the counter.
A Red Martian weaponsmith works at his forge.

> list
You can buy:
A fine steel dagger for 650 gold coins.
A radium rifle for 454 gold coins.
A radium pistol for 260 gold coins.
A Warlord's longsword for 909 gold coins.
A quality short sword for 91 gold coins.
A fine stiletto for 19 gold coins.
```

**Armory (Room 3020):**
```
> goto 3020
The Armory
   The armory displays all kinds of armor on the walls and in cases.  You see
leather harnesses, metal helmets, and protective gear typical of Martian warriors.
To the north is the main concourse.  A notice is carved on the wall.
A Red Martian harness-maker stands at his workbench.

> list
You can buy:
A pair of studded sleeves for 100 gold coins.
A pair of studded gloves for 100 gold coins.
A pair of studded boots for 100 gold coins.
A studded leg harness for 100 gold coins.
A studded helm for 100 gold coins.
A studded chest harness for 200 gold coins.
```

## Important Notes

### Shop Item Loading
In DikuMUD, shops work by:
1. The shop configuration defines which items the shop produces
2. The zone reset commands load those items into the keeper's inventory
3. Players can only buy items the keeper is carrying
4. The `list` command shows items from the keeper's inventory that match the shop's production list

**Critical**: Both the shop configuration AND zone reset commands must reference the same object vnums, or the shop will appear empty or show the wrong items.

### Future Shop Creation
When adding new shops:
1. Define the shop in the YAML with correct `producing` vnums
2. Add zone reset commands to give those exact vnums to the keeper mob
3. Run `validate_shops.py` to verify configuration
4. Test in-game with the `list` command

### Other Potential Missing Shops
The validation tool identified other mobs and rooms that might need shops:
- Zodangan weaponsmith (mob 3607) - may need shop in Zodanga
- Thark Weaponsmith (mob 4091) - may need shop in Thark Territory
- Various merchants and innkeepers in other zones

These should be evaluated and added as needed.

## Summary
Both the weapon smith and armor shop in Lesser Helium are now fully functional. Players can:
- Visit room 3011 to buy weapons from the weaponsmith
- Visit room 3020 to buy armor from the armorer
- Use the `list` command to see available items
- Use the `buy` command to purchase items

The enhanced validation tool will help prevent similar issues in the future by detecting missing shop configurations during world building.
