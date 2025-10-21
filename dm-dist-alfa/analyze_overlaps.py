#!/usr/bin/env python3
"""
Analyze overlapping rooms in a zone by showing paths to each overlapping room.
This helps understand the spatial layout conflicts.
"""

import subprocess
import sys
import re

def get_overlapping_pairs(zone_index):
    """Run zone_layout_validator and extract overlapping room pairs."""
    result = subprocess.run(
        ['./zone_layout_validator', str(zone_index)],
        cwd='/home/runner/work/DikuMUD/DikuMUD/dm-dist-alfa',
        capture_output=True,
        text=True
    )
    
    overlaps = []
    for line in result.stdout.split('\n'):
        if 'ERROR: Rooms' in line and 'overlap' in line:
            # Extract vnums from: "ERROR: Rooms 250 (vnum 3908) and 283 (vnum 3941) overlap at coordinates (1,-1,1)!"
            match = re.search(r'vnum (\d+)\) and \d+ \(vnum (\d+)\) overlap at coordinates \(([^)]+)\)', line)
            if match:
                vnum1, vnum2, coords = match.groups()
                overlaps.append((int(vnum1), int(vnum2), coords))
    
    return overlaps

def get_paths_for_rooms(zone_index, vnums):
    """Run find_room_paths and extract paths."""
    cmd = ['./find_room_paths', str(zone_index)] + [str(v) for v in vnums]
    result = subprocess.run(
        cmd,
        cwd='/home/runner/work/DikuMUD/DikuMUD/dm-dist-alfa',
        capture_output=True,
        text=True
    )
    
    paths = {}
    current_vnum = None
    current_path = []
    
    for line in result.stdout.split('\n'):
        if line.startswith('Path to room'):
            if current_vnum is not None:
                paths[current_vnum] = current_path
            match = re.search(r'Path to room (\d+):', line)
            if match:
                current_vnum = int(match.group(1))
                current_path = []
        elif line.strip().startswith('Step') or line.strip().startswith('Start:'):
            current_path.append(line.strip())
    
    if current_vnum is not None:
        paths[current_vnum] = current_path
    
    return paths

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_overlaps.py <zone_index>")
        sys.exit(1)
    
    zone_index = int(sys.argv[1])
    
    print(f"=== Analyzing Zone {zone_index} Overlaps ===\n")
    
    overlaps = get_overlapping_pairs(zone_index)
    
    if not overlaps:
        print("No overlaps found!")
        return
    
    print(f"Found {len(overlaps)} overlapping room pairs:\n")
    
    # Get all unique vnums
    all_vnums = set()
    for vnum1, vnum2, _ in overlaps:
        all_vnums.add(vnum1)
        all_vnums.add(vnum2)
    
    # Get paths for all rooms at once
    paths = get_paths_for_rooms(zone_index, sorted(all_vnums))
    
    # Print analysis for each overlapping pair
    for i, (vnum1, vnum2, coords) in enumerate(overlaps, 1):
        print(f"{i}. Rooms {vnum1} and {vnum2} overlap at coordinates {coords}")
        print()
        
        if vnum1 in paths:
            print(f"   Path to room {vnum1}:")
            for step in paths[vnum1]:
                print(f"      {step}")
            print()
        
        if vnum2 in paths:
            print(f"   Path to room {vnum2}:")
            for step in paths[vnum2]:
                print(f"      {step}")
            print()
        
        print("-" * 80)
        print()

if __name__ == '__main__':
    main()
