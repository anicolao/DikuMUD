#!/usr/bin/env python3
"""
Generate integration tests for zone objects.

This script creates one test per zone that validates all objects in the zone
are properly configured - lights can be held, weapons can be wielded, armor
can be worn, shields can be worn.
"""

import yaml
import os
import sys

# Item type constants
ITEM_LIGHT = 1
ITEM_WEAPON = 5
ITEM_TREASURE = 8
ITEM_ARMOR = 9
ITEM_FOOD = 11
ITEM_CONTAINER = 12
ITEM_CONTAINER_LOCKABLE = 15
ITEM_MONEY = 16
ITEM_DRINKCON = 17
ITEM_KEY = 18

# Wear flag constants
ITEM_TAKE = 1
ITEM_WIELD = 8192
ITEM_HOLD = 16384
ITEM_WEAR_SHIELD = 512
ITEM_WEAR_BODY = 8
ITEM_WEAR_HEAD = 16
ITEM_WEAR_LEGS = 32
ITEM_WEAR_FEET = 64
ITEM_WEAR_HANDS = 128
ITEM_WEAR_ARMS = 256
ITEM_WEAR_ABOUT = 1024
ITEM_WEAR_WAISTE = 2048
ITEM_WEAR_WRIST = 4096
ITEM_WEAR_NECK = 4
ITEM_WEAR_FINGER = 2

def get_wear_command(wear_flags):
    """Determine the appropriate wear command based on wear flags."""
    # Check for shield first
    if wear_flags & ITEM_WEAR_SHIELD:
        return "wear", "shield"
    # Check other wear locations
    if wear_flags & ITEM_WEAR_BODY:
        return "wear", "body"
    if wear_flags & ITEM_WEAR_HEAD:
        return "wear", "head"
    if wear_flags & ITEM_WEAR_LEGS:
        return "wear", "legs"
    if wear_flags & ITEM_WEAR_FEET:
        return "wear", "feet"
    if wear_flags & ITEM_WEAR_HANDS:
        return "wear", "hands"
    if wear_flags & ITEM_WEAR_ARMS:
        return "wear", "arms"
    if wear_flags & ITEM_WEAR_ABOUT:
        return "wear", "about"
    if wear_flags & ITEM_WEAR_WAISTE:
        return "wear", "waist"
    if wear_flags & ITEM_WEAR_WRIST:
        return "wear", "wrist"
    if wear_flags & ITEM_WEAR_NECK:
        return "wear", "neck"
    if wear_flags & ITEM_WEAR_FINGER:
        return "wear", "finger"
    return "wear", None

def get_best_keyword(namelist, short_desc, all_objects_in_zone):
    """Get the best keyword from a namelist for testing.
    
    Prefers keywords that are unique and specific to this object,
    avoiding zone-wide generic keywords that might match multiple objects.
    """
    if not namelist:
        return None
    
    keywords = namelist.split()
    if not keywords:
        return None
    
    # Count how many objects in the zone use each keyword
    keyword_counts = {}
    for keyword in keywords:
        count = 0
        for obj in all_objects_in_zone:
            obj_namelist = obj.get('namelist', '')
            if keyword in obj_namelist.split():
                count += 1
        keyword_counts[keyword] = count
    
    # Prefer keywords that appear in fewer objects (more specific)
    # Also prefer keywords that appear in the short description
    if short_desc:
        short_lower = short_desc.lower()
        # Sort by: 1) appears in short desc, 2) used by fewer objects, 3) length
        def keyword_score(kw):
            in_desc = 1 if kw.lower() in short_lower else 0
            uniqueness = -keyword_counts.get(kw, 999)  # Negative so fewer is better
            length = len(kw)
            return (in_desc, uniqueness, length)
        
        keywords_sorted = sorted(keywords, key=keyword_score, reverse=True)
        return keywords_sorted[0]
    
    # Fall back to most unique keyword
    return min(keywords, key=lambda k: keyword_counts.get(k, 999))

def generate_test_for_zone(zone_file, zone_name, zone_number, output_dir):
    """Generate a test YAML file for a zone."""
    
    with open(zone_file) as f:
        data = yaml.safe_load(f)
    
    objects = data.get('objects', [])
    
    # Categorize objects
    testable_objects = []
    skipped_objects = []
    
    for obj in objects:
        type_flag = obj.get('type_flag', 0)
        wear_flags = obj.get('wear_flags', 0)
        vnum = obj.get('vnum')
        namelist = obj.get('namelist', '')
        short_desc = obj.get('short_desc', '')
        
        # Skip empty objects
        if not namelist:
            continue
        
        keyword = get_best_keyword(namelist, short_desc, objects)
        if not keyword:
            continue
        
        # Check if object is takeable - this is fundamental for most objects
        if not (wear_flags & ITEM_TAKE):
            # Track objects that should probably be takeable but aren't
            if type_flag in [ITEM_FOOD, ITEM_DRINKCON, ITEM_KEY, ITEM_CONTAINER, ITEM_CONTAINER_LOCKABLE, ITEM_LIGHT, ITEM_TREASURE, ITEM_MONEY]:
                skipped_objects.append({
                    'vnum': vnum,
                    'keyword': keyword,
                    'short_desc': short_desc,
                    'type_flag': type_flag,
                    'reason': 'Missing ITEM_TAKE flag'
                })
        
        # Determine object category and action
        # Check for shield first (before armor) since shields can be type ARMOR
        if wear_flags & ITEM_WEAR_SHIELD:
            testable_objects.append({
                'vnum': vnum,
                'keyword': keyword,
                'short_desc': short_desc,
                'action': 'wear',
                'expected_pattern': 'start using|wear',
                'type': 'shield'
            })
        elif type_flag == ITEM_WEAPON and (wear_flags & ITEM_WIELD):
            testable_objects.append({
                'vnum': vnum,
                'keyword': keyword,
                'short_desc': short_desc,
                'action': 'wield',
                'expected_pattern': 'OK|wield',
                'type': 'weapon'
            })
        elif type_flag == ITEM_LIGHT and (wear_flags & ITEM_HOLD):
            testable_objects.append({
                'vnum': vnum,
                'keyword': keyword,
                'short_desc': short_desc,
                'action': 'hold',
                'expected_pattern': 'OK|hold|light',
                'type': 'light'
            })
        elif type_flag == ITEM_ARMOR:
            # Check if it has actual armor wear flags (not just TAKE or HOLD)
            armor_wear_flags = (ITEM_WEAR_BODY | ITEM_WEAR_HEAD | ITEM_WEAR_LEGS | 
                              ITEM_WEAR_FEET | ITEM_WEAR_HANDS | ITEM_WEAR_ARMS | 
                              ITEM_WEAR_ABOUT | ITEM_WEAR_WAISTE | ITEM_WEAR_WRIST | 
                              ITEM_WEAR_NECK | ITEM_WEAR_FINGER)
            if wear_flags & armor_wear_flags:
                wear_cmd, wear_loc = get_wear_command(wear_flags)
                testable_objects.append({
                    'vnum': vnum,
                    'keyword': keyword,
                    'short_desc': short_desc,
                    'action': wear_cmd,
                    'expected_pattern': r'ok\.?|You.*wear',  # More specific to avoid matching "can't wear"
                    'type': 'armor',
                    'wear_location': wear_loc
                })
        # Add support for other takeable object types
        elif (wear_flags & ITEM_TAKE) and type_flag in [ITEM_FOOD, ITEM_DRINKCON, ITEM_KEY, ITEM_CONTAINER, ITEM_CONTAINER_LOCKABLE, ITEM_TREASURE, ITEM_MONEY]:
            # These objects can be picked up and dropped but don't have specific use commands to test
            # We'll just verify they can be picked up
            type_name = {
                ITEM_FOOD: 'food',
                ITEM_DRINKCON: 'drink',
                ITEM_KEY: 'key',
                ITEM_CONTAINER: 'container',
                ITEM_CONTAINER_LOCKABLE: 'container',
                ITEM_TREASURE: 'treasure',
                ITEM_MONEY: 'money'
            }.get(type_flag, 'item')
            testable_objects.append({
                'vnum': vnum,
                'keyword': keyword,
                'short_desc': short_desc,
                'action': None,  # No specific action beyond get/drop
                'expected_pattern': None,
                'type': type_name
            })
        # Special case for lights that are just takeable but not holdable
        elif type_flag == ITEM_LIGHT and (wear_flags & ITEM_TAKE):
            testable_objects.append({
                'vnum': vnum,
                'keyword': keyword,
                'short_desc': short_desc,
                'action': None,  # Can't hold it, but can pick it up
                'expected_pattern': None,
                'type': 'light_item'
            })
    
    if not testable_objects:
        print(f"  No testable objects found in {zone_name}, skipping")
        return None
    
    # Report skipped objects
    if skipped_objects:
        print(f"  WARNING: {len(skipped_objects)} objects skipped (missing ITEM_TAKE flag):")
        for obj in skipped_objects:
            type_name = {
                ITEM_FOOD: 'FOOD',
                ITEM_DRINKCON: 'DRINKCON',
                ITEM_KEY: 'KEY',
                ITEM_CONTAINER: 'CONTAINER',
                ITEM_CONTAINER_LOCKABLE: 'CONTAINER(lockable)',
                ITEM_LIGHT: 'LIGHT',
                ITEM_TREASURE: 'TREASURE',
                ITEM_MONEY: 'MONEY'
            }.get(obj['type_flag'], f"TYPE_{obj['type_flag']}")
            print(f"    - vnum {obj['vnum']}: {obj['short_desc']} ({type_name})")
    
    # Use room 1200 (The Chat Room) as starting room for all tests
    # This is a reliable, isolated room that is always lit and has no mob interference
    start_room = 1200
    
    # Generate test structure
    test = {
        'test': {
            'id': f'test_zone_{zone_number}_objects',
            'description': f'Verify all objects in {zone_name} are properly configured and can be used',
            'author': 'Integration Test Framework',
            'created': '2025-10-13',
            'tags': ['zone_test', 'object_validation', zone_name.lower().replace(' ', '_')]
        },
        'setup': {
            'character': {
                'name': 'TestWizard',
                'password': 'test',
                'class': 'warrior',
                'level': 34,  # Wizard level
            },
            'start_room': start_room,
            'gold': 0
        },
        'steps': []
    }
    
    # Add initial look
    test['steps'].append({
        'action': 'look',
        'description': f'Verify starting location in {zone_name}'
    })
    
    # Add steps for each object
    for obj in testable_objects:
        vnum = obj['vnum']
        keyword = obj['keyword']
        obj_type = obj['type']
        action = obj['action']
        expected = obj['expected_pattern']
        
        # Load object
        test['steps'].append({
            'action': 'command',
            'command': f'load obj {vnum}',
            'description': f'Load {obj_type} {vnum} ({keyword})',
            'expected': [
                {'pattern': r'ok\.?'}
            ]
        })
        
        # Get all
        test['steps'].append({
            'action': 'command',
            'command': 'get all',
            'description': f'Pick up the {obj_type}',
            'expected': [
                {'pattern': keyword}
            ]
        })
        
        # Use the object appropriately (if it has a specific action)
        if action:
            # Make pattern more flexible - "ok" with optional period
            if expected and ('OK' in expected or 'Ok' in expected):
                expected = expected.replace('OK', r'ok\.?').replace('Ok', r'ok\.?')
            test['steps'].append({
                'action': 'command',
                'command': f'{action} {keyword}',
                'description': f'{action.capitalize()} the {obj_type}',
                'expected': [
                    {'pattern': expected}
                ]
            })
            
            # Remove it (only for objects that were used)
            test['steps'].append({
                'action': 'command',
                'command': f'remove {keyword}',
                'description': f'Remove the {obj_type}',
                'expected': [
                    {'pattern': 'stop using|stop|remove'}
                ]
            })
        
        # Drop it
        test['steps'].append({
            'action': 'command',
            'command': f'drop {keyword}',
            'description': f'Drop the {obj_type}',
            'expected': [
                {'pattern': 'drop'}
            ]
        })
        
        # Purge it
        test['steps'].append({
            'action': 'command',
            'command': f'purge {keyword}',
            'description': f'Purge the {obj_type}',
            'expected': [
                {'pattern': r'ok\.?|destroy'}
            ]
        })
    
    # Add result section
    # Count object types
    type_counts = {}
    for o in testable_objects:
        obj_type = o["type"]
        type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
    
    type_summary = ', '.join([f'{t} ({c})' for t, c in sorted(type_counts.items())])
    
    test['result'] = {
        'should_pass': True,
        'description': f'All {len(testable_objects)} objects in {zone_name} should be properly configured',
        'notes': f'This test validates that all usable objects in {zone_name} can be:\n'
                 f'  - Loaded by a wizard\n'
                 f'  - Picked up\n'
                 f'  - Used appropriately (wielded, worn, held, etc.)\n'
                 f'  - Dropped\n'
                 f'  - Purged\n'
                 f'\n'
                 f'Total objects in zone: {len(objects)}\n'
                 f'Objects tested: {len(testable_objects)}\n'
                 f'Object types: {type_summary}'
    }
    
    # Write to file
    safe_zone_name = zone_name.lower().replace(' ', '_').replace('-', '_')
    output_file = os.path.join(output_dir, f'test_zone_{zone_number}_{safe_zone_name}_objects.yaml')
    
    with open(output_file, 'w') as f:
        yaml.dump(test, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"  Created test: {output_file}")
    print(f"    {len(testable_objects)} objects to test (out of {len(objects)} total objects)")
    
    # Calculate coverage
    coverage = (len(testable_objects) / len(objects) * 100) if objects else 0
    if coverage < 100:
        untested_count = len(objects) - len(testable_objects) - len(skipped_objects)
        if untested_count > 0:
            print(f"    Coverage: {coverage:.1f}% ({untested_count} objects not tested, not flagged as skipped)")
    
    return output_file

def main():
    # Paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zones_dir = os.path.join(repo_root, 'dm-dist-alfa', 'lib', 'zones_yaml')
    output_dir = os.path.join(repo_root, 'tests', 'integration', 'zones')
    
    # Zones to process
    zones = [
        ('lesser_helium.yaml', 'Lesser Helium', 30),
        ('sewers.yaml', 'Sewers', 31),
        ('dead_sea_bottom_channel.yaml', 'Dead Sea Bottom Channel', 32),
        ('southern_approach.yaml', 'Southern Approach', 34),
        ('dead_sea_wilderness.yaml', 'Dead Sea Wilderness', 33),
        ('greater_helium.yaml', 'Greater Helium', 35),
        ('zodanga.yaml', 'Zodanga', 36),
        ('gathol.yaml', 'Gathol', 37),
        ('ptarth.yaml', 'Ptarth', 39),
        ('kaol.yaml', 'Kaol', 44),
        ('thark_territory.yaml', 'Thark Territory', 40),
        ('atmosphere_factory.yaml', 'Atmosphere Factory', 41),
        ('atmosphere_lower.yaml', 'Atmosphere Lower', 42),
    ]
    
    print(f"Generating zone object tests...")
    print(f"Output directory: {output_dir}")
    
    created = 0
    total_objects = 0
    total_tested = 0
    zones_with_issues = []
    
    for zone_file, zone_name, zone_number in zones:
        zone_path = os.path.join(zones_dir, zone_file)
        if not os.path.exists(zone_path):
            print(f"  Warning: {zone_path} not found, skipping")
            continue
        
        print(f"\nProcessing {zone_name}...")
        
        # Count objects in this zone
        with open(zone_path) as f:
            data = yaml.safe_load(f)
            zone_obj_count = len(data.get('objects', []))
        
        result = generate_test_for_zone(zone_path, zone_name, zone_number, output_dir)
        if result:
            created += 1
            # Read the generated test to get tested object count
            with open(result) as f:
                test_data = yaml.safe_load(f)
                notes = test_data.get('result', {}).get('notes', '')
                # Parse "Objects tested: X" from notes
                import re
                match = re.search(r'Objects tested: (\d+)', notes)
                if match:
                    tested_count = int(match.group(1))
                    total_tested += tested_count
                    total_objects += zone_obj_count
                    
                    # Track zones that don't have 100% coverage
                    if tested_count < zone_obj_count:
                        zones_with_issues.append((zone_name, tested_count, zone_obj_count))
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  {created} test files created successfully!")
    print(f"  Total objects across all zones: {total_objects}")
    print(f"  Total objects tested: {total_tested}")
    print(f"  Overall coverage: {(total_tested/total_objects*100):.1f}%")
    
    if zones_with_issues:
        print(f"\n⚠️  Zones with incomplete coverage:")
        for zone_name, tested, total in zones_with_issues:
            coverage = tested / total * 100 if total > 0 else 0
            print(f"    - {zone_name}: {tested}/{total} objects ({coverage:.1f}%)")
    else:
        print(f"\n✅ All zones have 100% object coverage!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
