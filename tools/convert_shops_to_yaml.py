#!/usr/bin/env python3
"""
Convert legacy .shp shop files to YAML format.
"""

import sys
import re
import yaml
from pathlib import Path

def parse_shop_file(shp_file):
    """Parse a .shp file and return list of shop dictionaries."""
    shops = []
    
    with open(shp_file, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for shop start marker (can be embedded like "0#2~")
        shop_match = None
        if '#' in line and line.endswith('~') and not line.startswith('$'):
            # Extract shop number from formats like "#1~" or "0#2~"
            match = re.search(r'#(\d+)~', line)
            if match:
                shop_match = match
        
        if shop_match:
            shop_num = int(shop_match.group(1))
            shop = {'vnum': shop_num}
            i += 1
            
            # Check if this is compressed format (zodanga style)
            # In compressed format, producing items are on the same line as other data
            if i < len(lines):
                next_line = lines[i].strip()
                # If next line contains a space and starts with digits, it might be compressed
                if ' ' in next_line and any(c.isdigit() for c in next_line.split()[0]):
                    # Try to detect if this is compressed format (has non-digit text)
                    parts = next_line.split()
                    if len(parts) > 6 and any(not p.replace('-', '').replace('.', '').isdigit() for p in parts[-3:]):
                        # This is compressed format - skip for now
                        print(f"Warning: Shop {shop_num} uses compressed format - skipping")
                        i += 1
                        continue
            
            # Parse producing items (up to 6, terminated by -1)
            producing = []
            for _ in range(6):
                if i >= len(lines):
                    break
                line_val = lines[i].strip()
                if not line_val or line_val.startswith('#') or line_val.startswith('$'):
                    break
                try:
                    val = int(line_val.split()[0])
                    i += 1
                    if val >= 0:
                        producing.append(val)
                except ValueError:
                    # Hit a non-integer, probably profit line
                    break
            shop['producing'] = producing
            
            # Parse profit margins
            if i < len(lines):
                shop['profit_buy'] = float(lines[i].strip())
                i += 1
            if i < len(lines):
                shop['profit_sell'] = float(lines[i].strip())
                i += 1
            
            # Parse trade types (up to 5, terminated by -1 or 0)
            buy_types = []
            for _ in range(5):
                if i >= len(lines):
                    break
                val = int(lines[i].strip().split()[0])
                i += 1
                if val > 0:
                    buy_types.append(val)
            shop['buy_types'] = buy_types
            
            # Parse 7 message strings (each ends with ~)
            messages = []
            for _ in range(7):
                msg = ""
                while i < len(lines):
                    line = lines[i]
                    i += 1
                    msg += line
                    if line.rstrip().endswith('~'):
                        # Remove the ~ and strip
                        msg = msg.rstrip()[:-1]
                        break
                messages.append(msg)
            
            shop['messages'] = {
                'no_such_item1': messages[0],
                'no_such_item2': messages[1],
                'do_not_buy': messages[2],
                'missing_cash1': messages[3],
                'missing_cash2': messages[4],
                'message_buy': messages[5],
                'message_sell': messages[6]
            }
            
            # Parse temper1, temper2
            if i < len(lines):
                shop['temper1'] = int(lines[i].strip())
                i += 1
            if i < len(lines):
                shop['temper2'] = int(lines[i].strip())
                i += 1
            
            # Parse keeper, with_who, room
            if i < len(lines):
                shop['keeper'] = int(lines[i].strip())
                i += 1
            if i < len(lines):
                shop['with_who'] = int(lines[i].strip())
                i += 1
            if i < len(lines):
                shop['in_room'] = int(lines[i].strip())
                i += 1
            
            # Parse hours
            if i < len(lines):
                shop['open1'] = int(lines[i].strip())
                i += 1
            if i < len(lines):
                shop['close1'] = int(lines[i].strip())
                i += 1
            if i < len(lines):
                shop['open2'] = int(lines[i].strip())
                i += 1
            if i < len(lines):
                # Handle embedded shop marker like "0#2~" or EOF like "0$~"
                val = lines[i].strip()
                if '#' in val:
                    shop['close2'] = int(val.split('#')[0])
                elif '$' in val:
                    shop['close2'] = int(val.split('$')[0])
                else:
                    shop['close2'] = int(val)
                i += 1
            
            shops.append(shop)
        elif line.startswith('$'):
            # EOF marker
            break
        else:
            i += 1
    
    return shops

def convert_zone_shops(zone_dir, zone_name):
    """Convert shops for a specific zone."""
    shp_file = zone_dir / 'zones' / f'{zone_name}.shp'
    yaml_file = zone_dir / 'zones_yaml' / f'{zone_name}.yaml'
    
    if not shp_file.exists():
        print(f"Warning: {shp_file} not found")
        return
    
    if not yaml_file.exists():
        print(f"Warning: {yaml_file} not found")
        return
    
    # Parse shops from .shp file
    shops = parse_shop_file(shp_file)
    
    if not shops:
        print(f"{zone_name}: No shops found")
        return
    
    # Load existing YAML
    with open(yaml_file, 'r') as f:
        zone_data = yaml.safe_load(f)
    
    # Update shops section
    zone_data['shops'] = shops
    
    # Write back to YAML
    with open(yaml_file, 'w') as f:
        yaml.dump(zone_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"{zone_name}: Converted {len(shops)} shops")

def main():
    repo_root = Path(__file__).parent.parent
    zone_dir = repo_root / 'dm-dist-alfa' / 'lib'
    
    # List of zones to convert
    zones = [
        'limbo', 'zone_1200', 'lesser_helium', 'dead_sea_bottom_channel',
        'southern_approach', 'dead_sea_wilderness', 'greater_helium',
        'zodanga', 'thark_territory', 'atmosphere_factory',
        'atmosphere_lower', 'system'
    ]
    
    for zone in zones:
        convert_zone_shops(zone_dir, zone)

if __name__ == '__main__':
    main()
