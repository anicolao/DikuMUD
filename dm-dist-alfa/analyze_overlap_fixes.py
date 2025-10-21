#!/usr/bin/env python3
"""
Analyze zone overlaps and suggest fixes.
This script identifies which connections might be causing overlaps and suggests removals.
"""

import subprocess
import yaml
import re
from collections import defaultdict, deque

def load_zone_data(zone_file):
    """Load zone YAML data."""
    with open(zone_file, 'r') as f:
        return yaml.safe_load(f)

def get_overlaps(zone_index):
    """Get overlapping room pairs from validator."""
    result = subprocess.run(
        ['./zone_layout_validator', str(zone_index)],
        cwd='/home/runner/work/DikuMUD/DikuMUD/dm-dist-alfa',
        capture_output=True,
        text=True
    )
    
    overlaps = []
    for line in result.stdout.split('\n'):
        if 'ERROR: Rooms' in line and 'overlap' in line:
            match = re.search(r'vnum (\d+)\) and \d+ \(vnum (\d+)\)', line)
            if match:
                v1, v2 = int(match.group(1)), int(match.group(2))
                overlaps.append((v1, v2))
    
    return overlaps

def build_graph(data):
    """Build a graph of room connections."""
    graph = defaultdict(list)
    
    for room in data['rooms']:
        vnum = room['vnum']
        for exit in room['exits']:
            target = exit['to_room']
            direction = exit['direction']
            graph[vnum].append((target, direction))
    
    return graph

def find_common_ancestors(graph, room1, room2, start_room):
    """Find rooms that are ancestors of both room1 and room2."""
    def bfs_parents(target):
        """BFS to find all paths to target."""
        queue = deque([(start_room, [start_room])])
        visited = set([start_room])
        paths = []
        
        while queue:
            current, path = queue.popleft()
            
            if current == target:
                paths.append(path)
                continue
            
            for neighbor, _ in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return paths
    
    paths1 = bfs_parents(room1)
    paths2 = bfs_parents(room2)
    
    # Find common rooms in paths
    rooms1 = set()
    for path in paths1:
        rooms1.update(path[:-1])  # Exclude the target itself
    
    rooms2 = set()
    for path in paths2:
        rooms2.update(path[:-1])
    
    common = rooms1 & rooms2
    return common, paths1, paths2

def main():
    zone_index = 11
    zone_file = '/home/runner/work/DikuMUD/DikuMUD/dm-dist-alfa/lib/zones_yaml/greater_helium.yaml'
    
    print(f"=== Analyzing Zone {zone_index} Overlaps ===\n")
    
    data = load_zone_data(zone_file)
    graph = build_graph(data)
    overlaps = get_overlaps(zone_index)
    
    print(f"Found {len(overlaps)} overlapping room pairs\n")
    
    # Analyze each overlap
    start_room = 3900  # Grand Plaza
    
    for v1, v2 in overlaps[:5]:  # Analyze first 5 overlaps
        print(f"\n{'='*80}")
        print(f"Overlap: {v1} and {v2}")
        print(f"{'='*80}")
        
        common, paths1, paths2 = find_common_ancestors(graph, v1, v2, start_room)
        
        if paths1 and paths2:
            print(f"\nShortest path to {v1}: {' → '.join(map(str, paths1[0]))}")
            print(f"Shortest path to {v2}: {' → '.join(map(str, paths2[0]))}")
            
            if common:
                print(f"\nCommon ancestor rooms: {sorted(common)}")
                
                # Find where paths diverge
                for i, (r1, r2) in enumerate(zip(paths1[0], paths2[0])):
                    if r1 != r2:
                        print(f"\nPaths diverge at step {i}:")
                        if i > 0:
                            print(f"  Last common room: {paths1[0][i-1]}")
                        print(f"  Path 1 goes to: {r1}")
                        print(f"  Path 2 goes to: {r2}")
                        break
            else:
                print("\nNo common ancestors found (separate components)")

if __name__ == '__main__':
    main()
