# Shop Inventory Validation

## Overview

This document describes the shop inventory validation system that ensures all shops in DikuMUD have proper inventory configuration and zone resets.

## Problem Statement

DikuMUD shops work by displaying items from the shopkeeper's carrying inventory. The shop configuration specifies which items the shop "produces" (can sell), but the actual inventory must be given to the shopkeeper via zone reset commands (G commands). If this isn't set up correctly, players will see empty shops or shops with mismatched inventory.

## Validation Checks

The `validate_world.py` tool performs three critical checks on shop inventory:

### 1. Empty Producing List

**Check**: Detects shops with no items for sale.

```python
# Filters out invalid/negative item vnums
valid_producing = [item for item in producing if item > 0]

if not valid_producing:
    ERROR: Shop has empty or invalid producing list
```

**Example Error**:
```
ERROR: Shop #99 in test_zone (keeper mob 9999) produces NOTHING! 
Shop has empty or invalid producing list. Players cannot buy anything from this shop!
```

### 2. Missing G Reset Commands

**Check**: Detects shopkeepers not given any inventory items via zone resets.

```python
if not given_items and producing:
    ERROR: Shopkeeper has no G reset commands to give inventory
```

**Example Error**:
```
ERROR: Shopkeeper mob 9998 (shop #98) has no G reset commands to give inventory! 
Shop produces [9998] but keeper is given nothing via zone resets. 
Players will see empty shop!
```

### 3. Inventory Mismatch

**Check**: Detects mismatches between shop producing list and keeper given items.

```python
missing_items = producing - given_items  # Items in shop but not given to keeper
extra_items = given_items - producing    # Items given but not in shop producing
```

**Example Errors**:
```
ERROR: Shopkeeper mob 3000 (shop #12) zone reset missing items! 
Shop produces [3040, 3041, 3042] but keeper only given [3040, 3041]. 
Missing: [3042]. Players won't see these items in shop!

ERROR: Shopkeeper mob 3001 (shop #8) zone reset has extra items. 
Shop produces [3010, 3011] but keeper given [3010, 3011, 3012]. 
Extra items: [3012]. These will show in shop but can't be restocked!
```

## Historical Issues

### Legacy .shp Files

Two shops were discovered with empty producing lists in the old .shp files:

1. **Shop #14** (greater_helium.shp)
   - Keeper: mob 3505
   - Room: 3524
   - Producing: -1, -1, -1, -1, -1, -1 (nothing!)

2. **Shop #15** (lesser_helium.shp)
   - Keeper: mob 3009
   - Room: 3034
   - Producing: -1, -1, -1, -1, -1, -1 (nothing!)

### Resolution

These shops have been fixed in the YAML world files:

1. **Shop #14** (now in lesser_helium.yaml)
   - Keeper: mob 3046 (Filthy the Bartender)
   - Room: 3048 (Poor Inn)
   - Produces: flask of wine (3002), strong whiskey (3003), flask of local wine (3004)
   - Integration test: `tests/integration/shops/test_shop_14_filthy_bartender.yaml`

2. **Shop #15** (now in lesser_helium.yaml)
   - Keeper: mob 3010 (Red Martian Leather Worker)
   - Room: 3035 (The Leather Worker's Shop)
   - Produces: studded armor pieces (3066-3071)
   - Integration test: `tests/integration/shops/test_shop_15_leather_worker_armor.yaml`

## Usage

### Running Validation

```bash
cd dm-dist-alfa
python3 ../tools/validate_world.py lib/zones_yaml/*.yaml
```

Validation runs automatically during world file building:

```bash
make build-worldfiles
```

### Testing with Problematic Data

Create a test YAML file with an empty shop:

```yaml
shops:
  - vnum: 99
    keeper: 9999
    in_room: 9999
    producing: []  # Empty!
    # ... other fields
```

Run validation:

```bash
python3 ../tools/validate_world.py test_broken_shop.yaml
```

Expected output:
```
ERROR: Shop #99 in test_broken_shop (keeper mob 9999) produces NOTHING!
```

## Current Status

As of October 2024:
- ✅ All 21 shops in YAML data pass validation
- ✅ No shops with empty producing lists
- ✅ All shopkeepers have proper G reset commands
- ✅ All inventory matches between shops and resets
- ✅ Integration tests exist for all functional shops

## Integration Tests

All shops have integration tests that verify:
1. Shopkeeper presence in correct room
2. Shop responds to 'list' command
3. Items can be purchased (where applicable)
4. Purchased items appear in inventory

See `tests/integration/shops/` for all shop tests.

## Related Tools

- `tools/validate_world.py` - Main validation tool
- `tools/validate_shops.py` - Legacy shop validation (for .shp files)
- `tools/world_builder.py` - Builds .shp files from YAML
- `tools/integration_test_runner.py` - Runs integration tests

## References

- SHOPKEEPER_INTEGRATION_TESTS.md - Comprehensive shop testing documentation
- validate_world.py source code - Implementation details
