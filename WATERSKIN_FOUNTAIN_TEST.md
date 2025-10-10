# Waterskin and Fountain Feature Test Guide

## Overview
This document describes how to test the new waterskin and fountain feature added to DikuMUD.

## Features Added
1. **Fountains**: Immovable water sources in major city plazas
2. **Waterskins**: Purchasable containers that can be filled from fountains
3. **Drink Command**: Enhanced to work with objects in the room (not just carried)
4. **Fill Command**: New command to fill waterskins from fountains

## Test Locations

### Lesser Helium
- **Fountain Location**: Market Plaza (room 3014)
- **Waterskin Shop**: Provisions Merchant (room 3009, shop #1)

### Greater Helium
- **Fountain Location**: Market District Plaza (room 3920)
- **Waterskin Shop**: Provisions Merchant (room 3928, shop #3)

## Test Scenarios

### Test 1: Drinking from Fountain
1. Navigate to Market Plaza (room 3014 in Lesser Helium or 3920 in Greater Helium)
2. Type: `look`
   - **Expected**: Should see "A water fountain provides fresh water here." (Lesser Helium)
   - **Expected**: Should see "A beautiful marble fountain provides fresh water here." (Greater Helium)
3. Type: `look fountain`
   - **Expected**: Should see the fountain's description
4. Type: `drink fountain`
   - **Expected**: "You drink the water."
   - **Expected**: Thirst condition should improve
5. Type: `drink fountain` (repeat multiple times)
   - **Expected**: Each time you should be able to drink
   - **Expected**: Fountain should never run empty

### Test 2: Purchasing Waterskin
1. Navigate to Provisions Merchant shop
2. Type: `list`
   - **Expected**: Should see "a leather waterskin" in the list
3. Type: `buy waterskin`
   - **Expected**: "You buy a leather waterskin."
   - **Expected**: Costs 30 gold coins
4. Type: `inventory`
   - **Expected**: Should see "a leather waterskin" in your inventory

### Test 3: Filling Waterskin from Fountain
1. Make sure you have an empty waterskin in inventory
2. Navigate to a room with a fountain
3. Type: `fill waterskin fountain`
   - **Expected**: "You fill a leather waterskin from a fountain."
   - **Expected**: Message to room: "$n fills a leather waterskin from a fountain."
4. Type: `look waterskin`
   - **Expected**: Should show it contains water (name should include "water")

### Test 4: Drinking from Waterskin
1. Make sure you have a filled waterskin
2. Type: `drink waterskin`
   - **Expected**: "You drink the water."
   - **Expected**: Thirst condition should improve
3. Repeat drinking until empty
   - **Expected**: Eventually get "It's empty already."

### Test 5: Refilling Waterskin
1. Empty waterskin in inventory
2. At fountain location
3. Type: `fill waterskin fountain`
   - **Expected**: Should fill successfully
4. Type: `drink waterskin`
   - **Expected**: Should be able to drink again

### Test 6: Error Conditions
1. Try `fill waterskin fountain` when not at fountain:
   - **Expected**: "You can't find it!"
2. Try `fill bread fountain`:
   - **Expected**: "You can't fill that!"
3. Try `fill waterskin waterskin`:
   - **Expected**: "You can't find it!" (can't fill from carried item)
4. Try `drink waterskin` with empty waterskin:
   - **Expected**: "It's empty already."

## Expected Behavior Summary

### Fountains
- **Location**: Fixed in room (not takeable)
- **Capacity**: 50 units
- **Content**: Always full of water
- **Behavior**: Never depletes when drunk from
- **Commands**: Can `drink fountain` and `fill waterskin fountain`

### Waterskins
- **Location**: Purchasable from provisions shops
- **Cost**: 30 gold coins
- **Capacity**: 10 units
- **Initial State**: Empty when purchased
- **Behavior**: Depletes when drunk from, can be refilled
- **Commands**: Can `buy waterskin`, `fill waterskin fountain`, `drink waterskin`

## Technical Details

### Object VNums
- Lesser Helium fountain: 3135
- Lesser Helium waterskin: 3138
- Greater Helium fountain: 3775
- Greater Helium waterskin: 3774

### Object Properties
**Fountains:**
- Type: ITEM_DRINKCON (17)
- Wear flags: 0 (not takeable)
- Value[0]: 50 (max capacity)
- Value[1]: 50 (current amount)
- Value[2]: 0 (liquid type = water)
- Value[3]: 0 (not poisoned)

**Waterskins:**
- Type: ITEM_DRINKCON (17)
- Wear flags: 1 (takeable)
- Value[0]: 10 (max capacity)
- Value[1]: 0 (current amount - starts empty)
- Value[2]: 0 (liquid type - will be set to water when filled)
- Value[3]: 0 (not poisoned)

## Commands Reference

- `look` - See room description including fountain
- `look fountain` - Examine fountain details
- `drink fountain` - Drink directly from fountain
- `list` - See shop inventory
- `buy waterskin` - Purchase a waterskin
- `fill waterskin fountain` - Fill waterskin from fountain
- `drink waterskin` - Drink from your waterskin
- `inventory` - Check what you're carrying

## Notes
- Fountains are designed to be inexhaustible water sources
- Waterskins provide portable water for travel
- This is particularly thematic for the Barsoom setting where water is precious
- Players can carry multiple waterskins if desired
- Fill command only works with objects in the room (like fountains)
