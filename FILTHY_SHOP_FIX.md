# Fix for Filthy the Bartender Shop

## Problem
Filthy the Bartender (mob 3046) in Lesser Helium was not functioning as a shopkeeper. He existed in the game but had no shop configuration, so players could not buy drinks from him.

## Root Cause
Shop #12, which was supposed to be Filthy's shop, existed in the old `.shp` file format but was missing from the YAML zone configuration (`dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml`). Additionally, the shop had no products configured (all -1 values), making it non-functional.

## Solution
Added shop entry #12 for Filthy the Bartender in `lesser_helium.yaml` with the following configuration:

### Shop Details
- **Shop vnum**: 12
- **Keeper**: Mob 3046 (Filthy the Bartender)
- **Location**: Room 3048 (Poor Inn)
- **Hours**: Open 24 hours (0-28)
- **Products**: 
  - 3002 - a flask of wine
  - 3003 - a strong whiskey
  - 3004 - a flask of local wine
- **Buy multiplier**: 1.0 (standard pricing)
- **Sell multiplier**: 1.0 (standard pricing)
- **Buy types**: None (shop doesn't buy items from players)

### Shop Messages
Appropriate messages for a noisy, rough bar environment:
- "It's very noisy in here, what did you say you wanted to buy?"
- "Are you drunk or what ?? - NO CREDIT!"
- "I don't buy!" (for selling attempts)

## Changes Made

### 1. YAML Configuration (`dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml`)
Added complete shop entry for shop #12 at the end of the shops section (after shop #14).

### 2. Test Suite (`dm-dist-alfa/test_filthy_shop.sh`)
Created comprehensive test script that validates:
- Shop #12 exists in the generated shop file
- All three drink items are present
- Keeper and room associations are correct
- Shop validation passes without errors

## How the Shop System Works

1. **Shop Data Loading**: `boot_the_shops()` in `shop.c` reads the shop file
2. **Keeper Assignment**: `assign_the_shopkeepers()` in `shop.c` assigns the `shop_keeper` special procedure to all keeper mobs
3. **Player Interaction**: When players use commands like `list`, `buy <item>`, the `shop_keeper()` function handles the transactions

Filthy will now automatically respond to shop commands when players are in room 3048 (Poor Inn).

## Testing

All tests pass:
```bash
cd dm-dist-alfa
./test_shops.sh        # Original shop tests
./test_filthy_shop.sh  # Filthy-specific tests
```

## In-Game Usage

Players can now:
1. Go to room 3048 (Poor Inn in Lesser Helium)
2. Type `list` to see available drinks
3. Type `buy wine`, `buy whiskey`, or `buy 'local wine'` to purchase drinks
4. Drink items are consumable and provide various effects

## Thematic Appropriateness

The drink selection fits the "Poor Inn" theme:
- **Wine (3002)**: Basic flask of wine (10 gold)
- **Whiskey (3003)**: Strong Heliumetic whiskey (50 gold) 
- **Local wine (3004)**: Flask of local wine (20 gold)

These are rough, affordable drinks appropriate for a bartender named "Filthy" in a run-down establishment.
