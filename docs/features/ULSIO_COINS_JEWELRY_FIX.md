# Ulsio Coins Jewelry Shop Fix

## Problem
Bronze, silver, and gold coins dropped by ulsio and other sewer creatures (objects 3220, 3219, 3231) were not sellable at any shop. Players had no clear indication of where to convert these coins from their treasure hunts into usable gold.

The coins were incorrectly typed as `ITEM_POTION` (type 10) instead of `ITEM_TREASURE` (type 8), which meant the jewelry shop wouldn't buy them despite coins being valuable items made of precious metals.

## Root Cause
In the original sewers.yaml zone file, the three coin objects were defined with:
- Bronze coins (3220): `type_flag: 10` (ITEM_POTION)
- Silver coins (3219): `type_flag: 10` (ITEM_POTION)
- Gold coins (3231): `type_flag: 10` (ITEM_POTION)

The jewelry shop (shop #21, room 3034) is configured to buy `type: 8` (ITEM_TREASURE), so it wouldn't accept the coins for purchase.

## Solution
Changed all three coin objects to `ITEM_TREASURE` (type 8) and added descriptive text making it clear these can be sold to jewelers:

### Changes Made

#### 1. Object Type Changes (`dm-dist-alfa/lib/zones_yaml/sewers.yaml`)

**Bronze Coins (3220):**
- Changed `type_flag: 10` → `type_flag: 8` (ITEM_POTION → ITEM_TREASURE)
- Added "jewelry" to namelist
- Added extra description: "These bronze coins appear to be Martian currency of lesser value. A jeweler would likely be interested in purchasing them for their metal content."

**Silver Coins (3219):**
- Changed `type_flag: 10` → `type_flag: 8` (ITEM_POTION → ITEM_TREASURE)
- Added "jewelry" to namelist
- Added extra description: "These silver coins appear to be Martian currency of some value. A jeweler would likely be interested in purchasing them for their precious metal content."

**Gold Coins (3231):**
- Changed `type_flag: 10` → `type_flag: 8` (ITEM_POTION → ITEM_TREASURE)
- Added "jewelry" to namelist
- Added extra description: "These gold coins are valuable Martian currency. A jeweler would gladly purchase them for their precious metal content."

## How It Works

1. **Item Classification**: Coins are now classified as treasure items (type 8), matching other valuable items like gems and jewelry.

2. **Shop Compatibility**: The Red Martian Jeweller craftsman (mob 3009) in room 3034 buys treasure items (type 8), so coins are now sellable there.

3. **Player Guidance**: The extra descriptions explicitly mention that jewelers would buy these coins, guiding players to the jewelry shop.

## In-Game Usage

Players can now:
1. Kill ulsio and other sewer creatures to collect bronze, silver, and gold coins
2. Examine the coins to read "A jeweler would [be interested/gladly purchase them]"
3. Navigate to room 3034 (The Jeweler's Shop in Lesser Helium)
4. Type `value bronze` (or `silver` or `gold`) to check the sell price
5. Type `sell bronze` (or `silver` or `gold`) to sell the coins for gold

### Example Session
```
> kill ulsio
You attack an ulsio!
[combat ensues]
An ulsio is DEAD!

> get all corpse
You get bronze coins from the corpse of an ulsio.

> examine bronze
These bronze coins appear to be Martian currency of lesser value. A jeweler
would likely be interested in purchasing them for their metal content.

> goto 3034
The Jeweler's Shop

> value bronze
The Red Martian Jeweller craftsman tells you 'I'll give you 75 gold coins for that!'

> sell bronze
The Red Martian Jeweller craftsman tells you 'You'll get 75 gold coins for it!'
You now have 75 gold coins.
```

## Shop Configuration

The jewelry shop (shop #21) accepts these coins because:
- **Buy types**: `[8]` - ITEM_TREASURE
- **Sell markup**: 0.5x (shopkeeper pays 50% of item value)
- **Location**: Room 3034 (The Jeweler's Shop)
- **Keeper**: Mob 3009 (Red Martian Jeweller craftsman)
- **Hours**: 0-28 (always open)

## Affected Creatures

The following sewer creatures drop coins that can now be sold:
- Ulsio (mob 3500): Bronze coins (3220)
- Large ulsio (mob 3501): Silver coins (3219)
- Ulsio swarm (mob 3506): Gold coins (3231), silver coins (3219)
- Various other sewer creatures: Mixed coins

## Files Changed

- `dm-dist-alfa/lib/zones_yaml/sewers.yaml` - Updated coin object definitions
- World files automatically rebuilt via `make worldfiles`

## Testing

Created integration test:
- `tests/integration/test_ulsio_coins_jewelry_shop.yaml` - Validates that coins can be valued and sold at the jewelry shop

## Related Features

- **CRAFTSMAN_JEWELRY_SHOP_FIX.md**: Documents the jewelry shop configuration
- **BRONZE_COINS_FIX.md**: Documents the fix for coin wear_flags (making coins takeable)

## Thematic Appropriateness

This fix makes sense thematically:
- Coins made of precious metals (bronze, silver, gold) are valuable for their material content
- A jeweler who works with precious metals would naturally buy coins for melting/refinement
- This provides a clear gameplay loop: hunt monsters → collect treasure → sell to appropriate merchant

## Impact

- Players can now monetize their sewer exploration
- Clear indication of where to sell treasure items
- Consistent with other treasure items (gems, jewelry) being sellable at the jewelry shop
- Improves new player experience by providing obvious treasure conversion path
