#!/usr/bin/env python3
"""
DikuMUD World Validator

This tool validates YAML world data for consistency and correctness.
"""

import sys
import yaml
import re
from typing import List, Set, Dict, Any
from pathlib import Path


class WorldValidator:
    """Validates DikuMUD world data."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.all_rooms = set()
        self.all_mobs = set()
        self.all_objects = set()
        self.all_shops = {}  # shop_vnum -> zone_name
        self.shop_keepers = {}  # keeper_vnum -> shop_vnum
        self.quest_givers = {}  # giver_vnum -> [quest_vnums]
        self.zones = {}
        self.mobs_with_spec_flag = {}  # vnum -> zone_name
        
        # Mobiles with assigned special procedures in spec_assign.c
        # This list should be kept in sync with dm-dist-alfa/spec_assign.c
        self.assigned_spec_procedures = {
            1, 3005, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027,
            3060, 3061, 3062, 3066, 3067, 3143
        }
    
    def error(self, msg: str):
        """Add an error message."""
        self.errors.append(f"ERROR: {msg}")
    
    def warning(self, msg: str):
        """Add a warning message."""
        self.warnings.append(f"WARNING: {msg}")
    
    def validate_yaml_file(self, filename: str):
        """Validate a single YAML zone file."""
        try:
            with open(filename, 'r') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.error(f"Failed to parse {filename}: {e}")
            return
        
        zone_name = Path(filename).stem
        
        # Validate zone metadata
        if 'zone' not in data:
            self.error(f"{zone_name}: Missing zone metadata")
            return
        
        zone = data['zone']
        zone_num = zone.get('number')
        if zone_num is None:
            self.error(f"{zone_name}: Zone number missing")
        else:
            if zone_num in self.zones:
                self.error(f"{zone_name}: Duplicate zone number {zone_num}")
            self.zones[zone_num] = zone
        
        # Validate rooms
        rooms = data.get('rooms', [])
        room_vnums = set()
        for room in rooms:
            vnum = room.get('vnum')
            if vnum is None:
                self.error(f"{zone_name}: Room missing vnum")
                continue
            
            if vnum in room_vnums:
                self.error(f"{zone_name}: Duplicate room vnum {vnum}")
            if vnum in self.all_rooms:
                self.error(f"{zone_name}: Room {vnum} already defined in another zone")
            
            room_vnums.add(vnum)
            self.all_rooms.add(vnum)
            
            # Validate room fields
            if not room.get('name'):
                self.error(f"{zone_name}: Room {vnum} missing name")
            if 'description' not in room:
                self.error(f"{zone_name}: Room {vnum} missing description")
            if 'zone' not in room:
                self.error(f"{zone_name}: Room {vnum} missing zone field")
            
            # Validate exits
            for exit_data in room.get('exits', []):
                to_room = exit_data.get('to_room')
                if to_room and to_room != -1:
                    # We'll validate cross-references after loading all files
                    pass
        
        # Validate mobiles
        mobiles = data.get('mobiles', [])
        mob_vnums = set()
        for mob in mobiles:
            vnum = mob.get('vnum')
            if vnum is None:
                self.error(f"{zone_name}: Mobile missing vnum")
                continue
            
            if vnum in mob_vnums:
                self.error(f"{zone_name}: Duplicate mobile vnum {vnum}")
            if vnum in self.all_mobs:
                self.error(f"{zone_name}: Mobile {vnum} already defined in another zone")
            
            mob_vnums.add(vnum)
            self.all_mobs.add(vnum)
            
            # Validate mobile fields
            if not mob.get('namelist'):
                self.error(f"{zone_name}: Mobile {vnum} missing namelist")
            
            # Check for placeholder/invalid names
            namelist = mob.get('namelist', '')
            short_desc = mob.get('short_desc', '')
            long_desc = mob.get('long_desc', '')
            
            # Check for generic patterns like "mob3000", "mobile123", etc.
            if re.match(r'^(mob|mobile)\d+$', namelist.lower()):
                self.warning(f"{zone_name}: Mobile {vnum} has placeholder namelist: '{namelist}'")
            
            # Check for other placeholder patterns (using word boundaries)
            placeholder_patterns = [
                r'\bplaceholder\b', r'\bxxx\b', r'\btbd\b', r'\btodo\b', r'\bfixme\b',
                r'\bchangeme\b', r'\bgeneric mob\b', r'\btest mob\b'
            ]
            
            for pattern in placeholder_patterns:
                if re.search(pattern, namelist.lower()):
                    self.warning(f"{zone_name}: Mobile {vnum} has placeholder namelist: '{namelist}'")
                    break
                if re.search(pattern, short_desc.lower()):
                    self.warning(f"{zone_name}: Mobile {vnum} has placeholder short_desc: '{short_desc}'")
                    break
                if re.search(pattern, long_desc.lower()):
                    self.warning(f"{zone_name}: Mobile {vnum} has placeholder long_desc: '{long_desc}'")
                    break
            
            if mob.get('type') == 'simple' and 'simple' in mob:
                simple = mob['simple']
                # Validate dice notation
                for field in ['hp_dice', 'damage_dice']:
                    dice = simple.get(field, '')
                    if not re.match(r'^\d+d\d+[+-]\d+$', dice):
                        self.error(f"{zone_name}: Mobile {vnum} invalid {field}: {dice}")
            
            # Check for ACT_SPEC flag (bit 0, value 1) without assigned procedure
            action_flags = mob.get('action_flags', 0)
            if action_flags & 1:  # ACT_SPEC flag is set
                self.mobs_with_spec_flag[vnum] = zone_name
        
        # Validate objects
        objects = data.get('objects', [])
        obj_vnums = set()
        for obj in objects:
            vnum = obj.get('vnum')
            if vnum is None:
                self.error(f"{zone_name}: Object missing vnum")
                continue
            
            if vnum in obj_vnums:
                self.error(f"{zone_name}: Duplicate object vnum {vnum}")
            if vnum in self.all_objects:
                self.error(f"{zone_name}: Object {vnum} already defined in another zone")
            
            obj_vnums.add(vnum)
            self.all_objects.add(vnum)
            
            # Validate object fields
            if not obj.get('namelist'):
                self.error(f"{zone_name}: Object {vnum} missing namelist")
            
            # Check for placeholder/invalid names
            namelist = obj.get('namelist', '')
            short_desc = obj.get('short_desc', '')
            long_desc = obj.get('long_desc', '')
            
            # Check for generic patterns like "item3000", "object123", etc.
            if re.match(r'^(item|object|thing)\d+$', namelist.lower()):
                self.warning(f"{zone_name}: Object {vnum} has placeholder namelist: '{namelist}'")
            
            # Check for other placeholder patterns (using word boundaries)
            placeholder_patterns = [
                r'\bplaceholder\b', r'\bxxx\b', r'\btbd\b', r'\btodo\b', r'\bfixme\b',
                r'\bchangeme\b', r'\bgeneric item\b', r'\bgeneric object\b', r'\btest item\b'
            ]
            
            for pattern in placeholder_patterns:
                if re.search(pattern, namelist.lower()):
                    self.warning(f"{zone_name}: Object {vnum} has placeholder namelist: '{namelist}'")
                    break
                if re.search(pattern, short_desc.lower()):
                    self.warning(f"{zone_name}: Object {vnum} has placeholder short_desc: '{short_desc}'")
                    break
                if re.search(pattern, long_desc.lower()):
                    self.warning(f"{zone_name}: Object {vnum} has placeholder long_desc: '{long_desc}'")
                    break
            
            # Check affects
            affects = obj.get('affects', [])
            if len(affects) > 2:
                self.error(f"{zone_name}: Object {vnum} has more than 2 affects")
        
        # Validate shops
        shops = data.get('shops', [])
        for shop in shops:
            shop_vnum = shop.get('vnum')
            if shop_vnum is None:
                self.error(f"{zone_name}: Shop missing vnum")
                continue
            
            if shop_vnum in self.all_shops:
                self.error(f"{zone_name}: Duplicate shop vnum {shop_vnum} (already defined in {self.all_shops[shop_vnum]})")
            else:
                self.all_shops[shop_vnum] = zone_name
            
            # Track shop keeper
            keeper_vnum = shop.get('keeper')
            if keeper_vnum:
                self.shop_keepers[keeper_vnum] = shop_vnum
            
            # Validate shop keeper exists
            if keeper_vnum and keeper_vnum not in self.all_mobs:
                # We'll check this in cross-reference validation since mobs may not be loaded yet
                pass
            
            # Validate shop room exists
            room_vnum = shop.get('in_room')
            if room_vnum and room_vnum not in self.all_rooms:
                # We'll check this in cross-reference validation
                pass
        
        # Track quest givers
        quests = data.get('quests', [])
        for quest in quests:
            quest_vnum = quest.get('qnum')
            giver_vnum = quest.get('giver')
            if giver_vnum:
                if giver_vnum not in self.quest_givers:
                    self.quest_givers[giver_vnum] = []
                self.quest_givers[giver_vnum].append(quest_vnum)
        
        # Validate resets
        resets = data.get('resets', [])
        for i, reset in enumerate(resets):
            cmd = reset.get('command')
            if not cmd:
                self.error(f"{zone_name}: Reset {i} missing command")
                continue
            
            # We'll validate cross-references after loading all files
    
    def validate_cross_references(self, yaml_files: List[str]):
        """Validate cross-references between entities."""
        # Load all files again to check cross-references
        for filename in yaml_files:
            try:
                with open(filename, 'r') as f:
                    data = yaml.safe_load(f)
            except:
                continue
            
            zone_name = Path(filename).stem
            
            # Check room exits
            for room in data.get('rooms', []):
                for exit_data in room.get('exits', []):
                    to_room = exit_data.get('to_room')
                    if to_room and to_room != -1 and to_room not in self.all_rooms:
                        self.warning(f"{zone_name}: Room {room['vnum']} exit to non-existent room {to_room}")
            
            # Check reset commands
            for reset in data.get('resets', []):
                cmd = reset.get('command')
                if cmd == 'M':
                    # Mobile reset
                    mob_vnum = reset.get('arg1')
                    room_vnum = reset.get('arg3')
                    if mob_vnum and mob_vnum not in self.all_mobs:
                        self.error(f"{zone_name}: Reset references non-existent mobile {mob_vnum}")
                    if room_vnum and room_vnum not in self.all_rooms:
                        self.error(f"{zone_name}: Reset references non-existent room {room_vnum}")
                elif cmd == 'O':
                    # Object to room
                    obj_vnum = reset.get('arg1')
                    room_vnum = reset.get('arg3')
                    if obj_vnum and obj_vnum not in self.all_objects:
                        self.error(f"{zone_name}: Reset references non-existent object {obj_vnum}")
                    if room_vnum and room_vnum not in self.all_rooms:
                        self.error(f"{zone_name}: Reset references non-existent room {room_vnum}")
                elif cmd in ['G', 'E']:
                    # Give/Equip object to mobile
                    obj_vnum = reset.get('arg1')
                    if obj_vnum and obj_vnum not in self.all_objects:
                        self.error(f"{zone_name}: Reset references non-existent object {obj_vnum}")
                elif cmd == 'P':
                    # Put object in object
                    obj1 = reset.get('arg1')
                    obj2 = reset.get('arg3')
                    if obj1 and obj1 not in self.all_objects:
                        self.error(f"{zone_name}: Reset references non-existent object {obj1}")
                    if obj2 and obj2 not in self.all_objects:
                        self.error(f"{zone_name}: Reset references non-existent object {obj2}")
                elif cmd == 'D':
                    # Door state
                    room_vnum = reset.get('arg1')
                    if room_vnum and room_vnum not in self.all_rooms:
                        self.error(f"{zone_name}: Reset references non-existent room {room_vnum}")
            
            # Check shops
            for shop in data.get('shops', []):
                shop_vnum = shop.get('vnum')
                keeper_vnum = shop.get('keeper')
                room_vnum = shop.get('in_room')
                
                if keeper_vnum and keeper_vnum not in self.all_mobs:
                    self.error(f"{zone_name}: Shop {shop_vnum} references non-existent keeper mobile {keeper_vnum}")
                
                if room_vnum and room_vnum not in self.all_rooms:
                    self.error(f"{zone_name}: Shop {shop_vnum} references non-existent room {room_vnum}")
                
                # Check produced items
                for item_vnum in shop.get('producing', []):
                    if item_vnum > 0 and item_vnum not in self.all_objects:
                        self.error(f"{zone_name}: Shop {shop_vnum} produces non-existent object {item_vnum}")
    
    def validate_spec_procedures(self):
        """Validate that mobiles with ACT_SPEC flag have assigned procedures."""
        # Check for mobiles with ACT_SPEC flag but no assigned procedure
        for vnum, zone_name in self.mobs_with_spec_flag.items():
            if vnum not in self.assigned_spec_procedures:
                self.error(f"{zone_name}: Mobile {vnum} has ACT_SPEC flag but no special procedure assigned in spec_assign.c")
        
        # Check for assigned procedures without ACT_SPEC flag (less critical)
        for vnum in self.assigned_spec_procedures:
            if vnum in self.all_mobs and vnum not in self.mobs_with_spec_flag:
                zone_name = "unknown"
                for v, z in self.mobs_with_spec_flag.items():
                    if v == vnum:
                        zone_name = z
                        break
                self.warning(f"Mobile {vnum} has assigned special procedure but no ACT_SPEC flag")
    
    def validate_spec_procedure_collisions(self):
        """Validate that mobs don't have conflicting special procedure assignments.
        
        Each mob can only have ONE special procedure assigned. This checks for conflicts between:
        - Shopkeepers (shop special procedure)
        - Quest givers (quest_giver special procedure)
        - Hardcoded special procedures in spec_assign.c
        """
        # Check for shopkeeper vs quest giver conflicts
        for keeper_vnum, shop_vnum in self.shop_keepers.items():
            if keeper_vnum in self.quest_givers:
                quest_vnums = self.quest_givers[keeper_vnum]
                self.error(f"Mobile {keeper_vnum} is shopkeeper for shop #{shop_vnum} but also quest giver for quest(s) {quest_vnums}. "
                          f"Mob can only have ONE special procedure - shop will NOT work!")
        
        # Check for shopkeeper vs spec_assign.c conflicts
        for keeper_vnum, shop_vnum in self.shop_keepers.items():
            if keeper_vnum in self.assigned_spec_procedures:
                self.error(f"Mobile {keeper_vnum} is shopkeeper for shop #{shop_vnum} but also has hardcoded special procedure in spec_assign.c. "
                          f"Mob can only have ONE special procedure - shop will NOT work!")
        
        # Check for quest giver vs spec_assign.c conflicts
        for giver_vnum, quest_vnums in self.quest_givers.items():
            if giver_vnum in self.assigned_spec_procedures:
                self.error(f"Mobile {giver_vnum} is quest giver for quest(s) {quest_vnums} but also has hardcoded special procedure in spec_assign.c. "
                          f"Mob can only have ONE special procedure - quests will NOT work!")
    
    def validate_all(self, yaml_files: List[str]):
        """Validate all YAML zone files."""
        print(f"Validating {len(yaml_files)} zone files...")
        
        # First pass: load all data and check basic validity
        for filename in yaml_files:
            self.validate_yaml_file(filename)
        
        # Second pass: check cross-references
        self.validate_cross_references(yaml_files)
        
        # Third pass: check special procedure assignments
        self.validate_spec_procedures()
        
        # Fourth pass: check for special procedure collisions
        self.validate_spec_procedure_collisions()
        
        # Print results
        print(f"\nFound {len(self.all_rooms)} rooms, {len(self.all_mobs)} mobiles, {len(self.all_objects)} objects, {len(self.all_shops)} shops")
        print(f"Found {len(self.zones)} zones")
        
        if self.errors:
            print(f"\n{len(self.errors)} ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n{len(self.warnings)} WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✓ Validation passed! No errors or warnings found.")
            return 0
        elif self.errors:
            print(f"\n✗ Validation failed with {len(self.errors)} errors.")
            return 1
        else:
            print(f"\n⚠ Validation passed with {len(self.warnings)} warnings.")
            return 0


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_world.py <yaml_file1> [yaml_file2 ...]")
        sys.exit(1)
    
    yaml_files = sys.argv[1:]
    validator = WorldValidator()
    return validator.validate_all(yaml_files)


if __name__ == '__main__':
    sys.exit(main())
