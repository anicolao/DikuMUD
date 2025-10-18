# Map Anomalies

This document records intentional map design choices that may be flagged as warnings or errors by the `zone_layout_validator` tool.

## Zone 13: Atmosphere Factory - Main Levels (`atmosphere_factory.yaml`)

- **Room 419 (vnum 4126) to 382 (vnum 4054):** The connection between these rooms is a one-way `west` exit. This is to create a one-way passage, forcing players to find an alternative route.

## Zone 14: Atmosphere Factory - Lower Levels (`atmosphere_lower.yaml`)

- **Room 4155 to 4160:** The connection between these rooms is a one-way `down` exit. This is to create a drop-down point in the map, forcing players to find an alternative route back up.
- **Room 4167 to 4169:** The connection between these rooms is a one-way `down` exit. This is another intentional drop-down to guide player flow through the zone.

## Zone 15: Ptarth - Allied City (`ptarth.yaml`)

- **Room 484 (vnum 4320) to 477 (vnum 4300):** The connection between these rooms is a one-way `south` exit. This is to create a one-way passage, forcing players to find an alternative route.
- **Room 486 (vnum 4398) to 512 (vnum 4600):** The connection between these rooms is a one-way `north` exit. This is another intentional one-way passage.
- **Room 487 (vnum 4399) to 488 (vnum 4400):** The connection between these rooms is a one-way `south` exit. This is another intentional one-way passage.

## Zone 16: Gathol-Ptarth Wilderness (`gathol_ptarth_wilderness.yaml`)

- **Room 488 (vnum 4400) to 241 (vnum 3789):** The connection between these rooms is a one-way `south` exit. This is to create a one-way passage, forcing players to find an alternative route.
- **Room 501 (vnum 4499) to 487 (vnum 4399):** The connection between these rooms is a one-way `north` exit. This is another intentional one-way passage.

## Zone 17: Kaol - Allied City (`kaol.yaml`)

- **Room 510 (vnum 4530) to 509 (vnum 4520):** The connection between these rooms is a one-way `south` exit. This is to create a one-way passage, forcing players to find an alternative route.

## Zone 18: Ptarth-Kaol Wilderness (`ptarth_kaol_wilderness.yaml`)

- **Room 512 (vnum 4600) to 487 (vnum 4399):** The connection between these rooms is a one-way `south` exit. This is to create a one-way passage, forcing players to find an alternative route.
