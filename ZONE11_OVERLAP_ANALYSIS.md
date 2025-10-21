# Zone 11 (Greater Helium) Overlap Analysis

## Summary

Zone 11 has 18 room overlaps caused by conflicting spatial layouts of multiple interconnected areas. The zone was designed with an "abstract" connectivity model that doesn't map to strict euclidean 3D space.

## Root Cause

All overlaps stem from room 3900 (Grand Plaza), which serves as a central hub with 6 exits:
- NORTH to 3901 (Palace)
- EAST to 3910 (Temple District)
- SOUTH to 3920 (Market District)
- WEST - (not currently connected)
- UP to 3906 (Ascending Stairway)
- DOWN to 3964 (Airship Landing)

The areas reached via these exits have internal layouts (grids of rooms) that create spatial conflicts when calculated in 3D coordinates.

## Detailed Overlap Analysis

### Ground Level Overlaps (Z=0)
1. **3912 vs 3921** at (1,-1,0)
   - 3912: Boulevard of Heroes (Temple District)
   - 3921: Eastern Market Row (Market District)
   - Path divergence: 3900 → EAST vs SOUTH

2. **3913 vs 3924** at (2,-1,0)
   - 3913: Eastern Boulevard (Temple District)
   - 3924: Master Jeweler (Market District)
   - Same pattern - parallel streets

3. **3914 vs 3925** at (1,-2,0)
   - 3914: Noble Quarter Entrance (Temple District)
   - 3925: Leather Worker's Shop (Market District)
   - Same pattern - parallel streets

### Level 1 Overlaps (Z=1)
4. **3908 vs 3941** at (1,-1,1)
   - Via different vertical paths (3920→UP→3907 vs 3900→UP→3906→EAST→3940)

5. **3918 vs 3963** at (3,-1,1)
6. **3943 vs 3962** at (2,-1,1)

### Level 2 Overlaps (Z=2)
7. **3909 vs 3954** at (1,0,2)
8. **3919 vs 3942** at (1,-1,2)
9. **3953 vs 3979** at (0,0,2)

### Level 3 Overlaps (Z=3) - MOST PROBLEMATIC
10-17. **8 different overlaps** at various (x,y,3) coordinates
- Scientific Academy Plaza area vs Residential District area
- Multiple vertical structures converging

### Level 4 Overlap (Z=4)
18. **3993 vs 3996** at (1,1,4)

## Recommended Solution

The cleanest fix requires restructuring the Temple District (3910-3919) to not expand southward, eliminating its spatial conflict with the Market District:

### Changes Needed:

1. **Remove connection: 3910 ↔ 3912**
   - Breaks the southward expansion of Temple District

2. **Add alternative access to Temple District southern section:**
   - Option A: Connect 3912 to 3991 (Merchant Guild Hall) via new WEST/EAST exits
   - Option B: Connect 3912 to another ground-level room that doesn't create overlaps
   - Option C: Connect 3998 (Music Hall) to an accessible room, then keep 3998↔3912 connection

3. **Similarly handle vertical structure conflicts:**
   - Remove or redirect connections between overlapping vertical paths
   - May require making some upper-level areas have alternate access routes

## Impact Assessment

- **Pros**: Fixes all 18 overlaps, makes zone spatially consistent
- **Cons**: Changes intended connectivity, some areas may feel less naturally connected
- **Complexity**: Requires ~6-10 connection changes minimum

## Alternative Approach

If preserving exact connectivity is critical, consider:
1. Accepting some overlaps as "portals" or "non-euclidean passages"
2. Modifying the zone_layout_validator to support "portal" room flags
3. Completely redesigning one of the conflicting districts

## Files for Analysis

- `find_room_paths.c` - Traces paths to any room
- `analyze_overlaps.py` - Shows paths to all overlapping rooms
- `analyze_overlap_fixes.py` - Identifies divergence points

## Next Steps

1. Decide on acceptable level of connectivity changes
2. Implement the minimal set of changes to fix overlaps
3. Test with zone_layout_validator
4. Verify no new warnings introduced
5. Playtest to ensure areas remain accessible and logical
