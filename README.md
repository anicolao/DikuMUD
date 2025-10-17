# DikuMUD - Barsoom Universe

## About This Project

We plan to run an original **Gamma DikuMUD** and build a new universe based on **Barsoom** from Edgar Rice Burroughs' classic Mars series. This ambitious project aims to bring the exotic world of John Carter's adventures to life in a multi-user dungeon environment.

### What is Barsoom?

Barsoom is Edgar Rice Burroughs' fictional representation of Mars, featuring:
- Diverse cultures and civilizations (Red Martians, Green Martians, and more)
- Exotic creatures and landscapes
- Ancient cities and advanced technology
- Epic adventures and heroic tales

Our goal is to create an immersive MUD experience that captures the spirit and wonder of Barsoom.

## Join Our Community

**Want to contribute?** We're looking for builders, coders, and Barsoom enthusiasts!

🎮 **Join our Discord:** https://discord.gg/MeNQzXNCfb

Whether you're interested in world-building, coding, or just want to follow the development, join our Discord community as a first step. All contributors are welcome!

## About the Original DikuMUD

This repository contains the original DikuMUD Alfa and Gamma releases. DikuMUD was created by Hans Henrik Staerfeldt, Katja Nyboe, Tom Madsen, Michael Seifert, and Sebastian Hammer.

Please note the LGPL additions to licensing which you'll find in the docs/original/license.doc document.

Original Alfa release uploaded by Michael Seifert on 2020-02-03 20:02

## Development Tools

### Zone Layout Validator

The zone_layout_validator tool helps ensure spatial consistency in zone designs by:
- Walking through all rooms using breadth-first search
- Assigning (x, y, z) coordinates based on exit directions
- Detecting rooms with inconsistent coordinates
- Identifying overlapping rooms in the spatial layout

**Usage:**
```bash
cd dm-dist-alfa
make zone_layout_validator
./zone_layout_validator           # Validate all zones
./zone_layout_validator <zone>    # Validate specific zone
```

See `dm-dist-alfa/doc/zone_layout_validator.doc` for detailed documentation.
