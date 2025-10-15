#!/usr/bin/env python3
"""
Validate that all objects in zone files are tested by the integration tests.

This script checks each zone's YAML file against its generated test to ensure
all objects are accounted for and can be picked up as intended.
"""

import yaml
import os
import sys

def main():
    # Paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zones_dir = os.path.join(repo_root, 'dm-dist-alfa', 'lib', 'zones_yaml')
    tests_dir = os.path.join(repo_root, 'tests', 'integration', 'zones')
    
    # Zones to check - must match the zone names used in generate_zone_object_tests.py
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
    
    print("=" * 70)
    print("Zone Object Coverage Validation")
    print("=" * 70)
    
    total_zones = 0
    total_objects = 0
    total_tested = 0
    zones_100_coverage = []
    zones_incomplete = []
    
    for zone_file, zone_test_name, zone_number in zones:
        zone_path = os.path.join(zones_dir, zone_file)
        if not os.path.exists(zone_path):
            print(f"⚠️  Zone {zone_number}: File not found - {zone_file}")
            continue
        
        # Load zone data
        with open(zone_path) as f:
            zone_data = yaml.safe_load(f)
        
        zone_name = zone_data['zone']['name']
        objects = zone_data.get('objects', [])
        
        # Load test file - use the test name from our mapping, not the zone YAML name
        safe_zone_name = zone_test_name.lower().replace(' ', '_').replace('-', '_')
        test_file = os.path.join(tests_dir, f'test_zone_{zone_number}_{safe_zone_name}_objects.yaml')
        
        if not os.path.exists(test_file):
            print(f"⚠️  Zone {zone_number} ({zone_name}): No test file found")
            continue
        
        with open(test_file) as f:
            test_data = yaml.safe_load(f)
        
        # Count tested objects
        tested_vnums = set()
        for step in test_data.get('steps', []):
            if step.get('action') == 'command' and step.get('command', '').startswith('load obj'):
                vnum = int(step['command'].split()[-1])
                tested_vnums.add(vnum)
        
        # Count all objects
        all_vnums = set(obj['vnum'] for obj in objects)
        
        # Calculate coverage
        coverage = len(tested_vnums) / len(all_vnums) * 100 if all_vnums else 0
        
        # Track stats
        total_zones += 1
        total_objects += len(all_vnums)
        total_tested += len(tested_vnums)
        
        # Display result
        status = "✅" if coverage == 100 else "⚠️ "
        print(f"{status} Zone {zone_number:2d} ({zone_name:25s}): {len(tested_vnums):3d}/{len(all_vnums):3d} objects ({coverage:5.1f}%)")
        
        if coverage == 100:
            zones_100_coverage.append(zone_name)
        else:
            zones_incomplete.append((zone_name, len(tested_vnums), len(all_vnums), coverage))
            
            # List untested objects if any
            untested = all_vnums - tested_vnums
            if untested and len(untested) <= 5:
                print(f"     Untested objects: {sorted(untested)}")
    
    # Summary
    print("=" * 70)
    print("Summary:")
    print(f"  Total zones checked: {total_zones}")
    print(f"  Total objects: {total_objects}")
    print(f"  Objects tested: {total_tested}")
    overall_coverage = total_tested / total_objects * 100 if total_objects else 0
    print(f"  Overall coverage: {overall_coverage:.1f}%")
    print()
    
    if zones_100_coverage:
        print(f"✅ Zones with 100% coverage ({len(zones_100_coverage)}):")
        for zone in zones_100_coverage:
            print(f"   - {zone}")
        print()
    
    if zones_incomplete:
        print(f"⚠️  Zones with incomplete coverage ({len(zones_incomplete)}):")
        for zone_name, tested, total, coverage in sorted(zones_incomplete, key=lambda x: x[3]):
            print(f"   - {zone_name:25s}: {tested:3d}/{total:3d} ({coverage:5.1f}%)")
    
    print("=" * 70)
    
    # Exit with error if coverage is not 100%
    if overall_coverage < 100:
        print(f"\n⚠️  Overall coverage is {overall_coverage:.1f}% - some objects are not being tested!")
        return 1
    else:
        print(f"\n✅ Perfect! All objects are being tested!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
