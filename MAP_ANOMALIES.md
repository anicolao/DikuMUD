# Map Spatial Anomalies

This document tracks intentional spatial anomalies in zone designs where rooms deliberately violate Euclidean geometry for gameplay or thematic reasons.

## Zone 4: Southern Approach to Atmosphere Factory (rooms 3056-3149)

**Type:** Non-Euclidean Maze / Serpentine Path  
**Errors:** 29 inconsistent coordinate errors  
**Status:** Intentional design - DO NOT FIX

### Description:
The southern approach features a deliberate zigzag or serpentine corridor design where connected rooms have intentionally inconsistent spatial coordinates. This creates a disorienting maze-like effect appropriate for a dangerous approach path.

### Specific Anomalies:
- Room pairs (3107/3108, 3110/3111, 3113/3114, etc.) form an east-west zigzag pattern
- Each subsequent pair is offset by one coordinate unit, creating a winding path
- The design prevents players from mapping the area using simple directional coordinates
- This is characteristic of maze zones where confusion is part of the challenge

### Rationale:
Intentional game design to create a challenging, disorienting approach to the Atmosphere Factory. The spatial confusion adds difficulty and atmosphere to this dangerous route.

---

## Zone 7: Zodanga - Enemy City (rooms 3206-3649)

**Type:** Room Overlaps + Unreachable Teleport Destinations  
**Errors:** 1 inconsistent coordinate, 6 overlaps, 17 unreachable rooms  
**Status:** Partially intentional - some anomalies may be design choices

### Description:
Zodanga contains multiple spatial anomalies that appear to be a mix of intentional design and potential errors.

### Unreachable Rooms (3609, 3628-3629, 3636-3646):
These 13 rooms are unreachable from the starting point and many have one-way gates back to accessible areas. This suggests they are:
- Teleport destinations (magic portals, traps, etc.)
- Secret areas accessible by special means
- Prisoner cells or restricted areas

**Status:** Likely intentional - these appear to be special-access areas

### Room Overlaps:
- Rooms 3612/3618 overlap at (2,0,0)
- Rooms 3613/3621 overlap at (1,-1,0)  
- Rooms 3614/3615 overlap at (2,1,0)
- Rooms 3616/3624 overlap at (2,-1,0)
- Rooms 3623/3632 overlap at (-1,-1,0)
- Rooms 3625/3626 overlap at (1,-2,0)

**Status:** Requires investigation - these may represent:
- Parallel paths to same location (like secret passages)
- Errors in exit definitions
- Intentional "impossible space" design

---

## Zone 3: Lesser Helium (rooms 1203-3055)

**Type:** Room Overlaps + Inconsistent Coordinates  
**Errors:** 3 inconsistent coordinates, 13 overlaps, 3 unreachable rooms  
**Status:** Mixed - requires detailed analysis

### Major Issues:
- Multiple rooms at same coordinates suggest parallel path design
- Some inconsistencies in coordinate assignments
- A few unreachable rooms that may be special-access areas

**Status:** Needs further investigation to distinguish intentional from erroneous anomalies

---

## Zone 9: Dead Sea Wilderness (rooms 3750-3779)

**Type:** Inconsistent Coordinates + Overlaps  
**Errors:** 7 inconsistent coordinates, 1 overlap, 5 unreachable rooms  
**Status:** Likely intentional non-Euclidean wilderness design

### Description:
The Dead Sea wilderness appears to have an intentionally confusing layout where paths don't follow normal geometry. This creates a sense of being lost in a vast, disorienting wilderness.

### Rationale:
Wilderness zones often use non-standard geometry to simulate the confusion and difficulty of navigation in hostile terrain.

---

## Zone 11: Greater Helium (rooms 3790-3999)

**Type:** Room Overlaps + One-Way Gates  
**Errors:** 11 overlaps, 37 one-way gates, 59 unreachable rooms  
**Status:** Complex design with many special features

### Description:
Greater Helium has extensive use of:
- One-way passages (trap doors, slides, special entrances)
- Unreachable rooms (likely teleport destinations, restricted areas)
- Overlapping rooms (parallel secret passages?)

**Status:** This large, complex zone requires detailed analysis. Many features appear intentional but need verification.

---

## Zone 12: Thark Territory (rooms 4000-4049)

**Type:** Inconsistent Coordinates + Overlaps  
**Errors:** 2 inconsistent coordinates, 6 overlaps, 13 unreachable rooms  
**Status:** Likely intentional tribal territory design

---

## Zone 13: Atmosphere Factory - Main Levels (rooms 4050-4149)

**Type:** Room Overlaps + Unreachable Areas  
**Errors:** 2 inconsistent coordinates, 12 overlaps, 30 unreachable rooms  
**Status:** Complex facility with restricted areas

### Description:
The Atmosphere Factory appears to have:
- Multiple levels/sections with overlapping coordinates
- Restricted areas only accessible by special means
- Possible elevator/lift connections not using standard exits

**Status:** Facility design likely intentional but needs verification

---

## Zone 14: Atmosphere Factory - Lower Levels (rooms 4150-4199)

**Type:** Inconsistent Coordinates + Overlaps + Unreachable Areas  
**Errors:** 4 inconsistent coordinates, 2 overlaps, 18 unreachable rooms  
**Status:** Lower facility levels with restricted access

---

## General Patterns Observed

### 1. Maze Zones
Zones designed as mazes (like Zone 4) intentionally use non-Euclidean geometry to confuse players. These should NOT be "fixed" as the confusion is part of the design.

### 2. Secret/Parallel Paths
Some overlapping rooms represent alternative routes to the same location:
- Hidden passages
- Secret doors
- Alternative entrances
These are intentional design choices.

### 3. Teleport Destinations
Unreachable rooms with one-way exits back to the main zone are typically:
- Teleport/portal destinations
- Trap outcomes
- Special magic transport locations

### 4. Restricted Areas
Large facilities (Atmosphere Factory, cities) have unreachable rooms that represent:
- Locked/barred areas
- Areas requiring keys or special access
- Future expansion areas

## Validation Strategy

For each remaining anomaly:
1. Check if it follows a maze/confusion pattern → Document as intentional
2. Check if rooms are unreachable with one-way returns → Likely teleport/trap destinations
3. Check if overlaps represent parallel paths → May be intentional secret routes
4. Only "fix" clear errors where exits are obviously wrong

## Notes

- DO NOT attempt to "fix" Zone 4's maze design
- Most unreachable rooms are likely intentional special-access areas
- Room overlaps need case-by-case analysis
- One-way gates are often intentional (trap doors, slides, secret passages)
