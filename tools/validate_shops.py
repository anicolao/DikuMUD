#!/usr/bin/env python3
"""
Shop Validation Tool for DikuMUD

Validates that all shops are correctly configured with:
- Existing keeper mobs
- Existing rooms
- Existing produced items
- Valid parameters
"""

import sys
import re
from pathlib import Path

def parse_shop_file(filename):
    """Parse a .shp file and return list of shops"""
    with open(filename, 'r') as f:
        content = f.read()
    
    shops = []
    # Split by shop markers, handling embedded format like "0#2~"
    parts = re.split(r'(#\d+~)', content)
    
    i = 1
    while i < len(parts):
        if parts[i].startswith('#'):
            shop_num = int(parts[i][1:-1])
            shop_data = parts[i+1] if i+1 < len(parts) else ""
            lines = [line.strip() for line in shop_data.split('\n') if line.strip() and not line.strip().startswith('$')]
            
            if len(lines) < 20:
                i += 2
                continue
                
            shop = {'num': shop_num}
            
            # Parse producing items (lines 0-5, up to 6 items, -1 terminates)
            shop['producing'] = []
            for j in range(min(6, len(lines))):
                try:
                    val = int(lines[j].split()[0])
                    if val > 0:
                        shop['producing'].append(val)
                except (ValueError, IndexError):
                    break
            
            # Parse profit margins (lines 6-7)
            try:
                shop['profit_buy'] = float(lines[6])
                shop['profit_sell'] = float(lines[7])
            except (ValueError, IndexError):
                shop['profit_buy'] = 0.0
                shop['profit_sell'] = 0.0
            
            # Parse trade types (lines 8-12, up to 5 types, 0/-1 terminates)
            shop['buy_types'] = []
            for j in range(8, min(13, len(lines))):
                try:
                    val = int(lines[j].split()[0])
                    if val > 0:
                        shop['buy_types'].append(val)
                except (ValueError, IndexError):
                    break
            
            # Skip 7 message lines (13-19)
            # Parse temper, keeper, with_who, room, hours (lines 20-29)
            try:
                shop['temper1'] = int(lines[20].split()[0])
                shop['temper2'] = int(lines[21].split()[0])
                shop['keeper'] = int(lines[22].split()[0])
                shop['with_who'] = int(lines[23].split()[0])
                shop['room'] = int(lines[24].split()[0])
                shop['open1'] = int(lines[25].split()[0])
                shop['close1'] = int(lines[26].split()[0])
                shop['open2'] = int(lines[27].split()[0])
                shop['close2'] = int(lines[28].split()[0])
            except (ValueError, IndexError) as e:
                print(f"  WARNING: Failed to parse shop #{shop_num} parameters: {e}")
            
            shops.append(shop)
        i += 2
    
    return shops

def load_vnums(filename, pattern):
    """Load vnum list from a file"""
    vnums = set()
    try:
        with open(filename, 'r') as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if match:
                    vnums.add(int(match.group(1)))
    except FileNotFoundError:
        pass
    return vnums

def load_object_names(filename):
    """Load object vnums and their short descriptions from obj file"""
    obj_names = {}
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                # Look for object vnum marker
                if line.startswith('#') and line[1:].isdigit():
                    vnum = int(line[1:])
                    i += 1
                    # Skip namelist line
                    if i < len(lines):
                        i += 1
                    # Get short description
                    if i < len(lines):
                        short_desc = lines[i].strip().rstrip('~')
                        obj_names[vnum] = short_desc
                i += 1
    except FileNotFoundError:
        pass
    return obj_names

def validate_shops(shop_file, mob_file, obj_file, wld_file):
    """Validate all shops in the shop file"""
    
    print("=== DikuMUD Shop Validation ===\n")
    
    # Load valid vnums from game files
    print("Loading mob vnums...")
    mobs = load_vnums(mob_file, r'^#(\d+)')
    print(f"  Found {len(mobs)} mobs")
    
    print("Loading object vnums...")
    objs = load_vnums(obj_file, r'^#(\d+)')
    print(f"  Found {len(objs)} objects")
    
    print("Loading object names...")
    obj_names = load_object_names(obj_file)
    print(f"  Loaded {len(obj_names)} object names")
    
    print("Loading room vnums...")
    rooms = load_vnums(wld_file, r'^#(\d+)')
    print(f"  Found {len(rooms)} rooms")
    
    print(f"\nParsing shop file: {shop_file}")
    shops = parse_shop_file(shop_file)
    print(f"  Found {len(shops)} shops\n")
    
    errors = 0
    warnings = 0
    
    for shop in shops:
        print(f"Shop #{shop['num']}:")
        
        # Check keeper mob
        keeper = shop.get('keeper')
        if keeper:
            if keeper not in mobs:
                print(f"  ERROR: Keeper mob {keeper} does not exist!")
                errors += 1
            else:
                print(f"  Keeper: mob {keeper} ✓")
        
        # Check room
        room = shop.get('room')
        if room:
            if room not in rooms:
                print(f"  ERROR: Shop room {room} does not exist!")
                errors += 1
            else:
                print(f"  Room: {room} ✓")
        
        # Check producing items
        producing = shop.get('producing', [])
        if not producing:
            print(f"  WARNING: Shop produces nothing (no items for sale)")
            warnings += 1
        else:
            print(f"  Produces {len(producing)} items:")
            for item_vnum in producing:
                if item_vnum not in objs:
                    print(f"    ERROR: Item {item_vnum} does not exist!")
                    errors += 1
                else:
                    obj_name = obj_names.get(item_vnum, "")
                    # Check for placeholder names
                    if obj_name.lower().startswith('object ') or obj_name.lower().startswith('item'):
                        print(f"    ERROR: Item {item_vnum} has placeholder name '{obj_name}'")
                        errors += 1
                    else:
                        print(f"    {item_vnum} ({obj_name}) ✓")
        
        # Check profit margins
        profit_buy = shop.get('profit_buy', 0.0)
        profit_sell = shop.get('profit_sell', 0.0)
        if profit_buy <= 0.0:
            print(f"  WARNING: Buy markup {profit_buy} should be positive")
            warnings += 1
        if profit_sell <= 0.0:
            print(f"  WARNING: Sell markup {profit_sell} should be positive")
            warnings += 1
        
        # Check hours
        hours = [shop.get('open1', 0), shop.get('close1', 0), 
                shop.get('open2', 0), shop.get('close2', 0)]
        if any(h < 0 or h > 23 for h in hours):
            print(f"  WARNING: Hours {hours} should be in range 0-23")
            warnings += 1
        
        print()
    
    print("=== Summary ===")
    print(f"Total shops: {len(shops)}")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")
    
    if errors > 0:
        print("\n❌ Validation FAILED - please fix errors above.")
        return 1
    elif warnings > 0:
        print("\n⚠️  Validation completed with warnings.")
        return 0
    else:
        print("\n✅ All shops validated successfully!")
        return 0

def main():
    if len(sys.argv) < 5:
        print("Usage: validate_shops.py <shop_file> <mob_file> <obj_file> <wld_file>")
        sys.exit(1)
    
    shop_file = sys.argv[1]
    mob_file = sys.argv[2]
    obj_file = sys.argv[3]
    wld_file = sys.argv[4]
    
    sys.exit(validate_shops(shop_file, mob_file, obj_file, wld_file))

if __name__ == '__main__':
    main()
