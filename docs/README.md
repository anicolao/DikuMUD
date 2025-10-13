# DikuMUD Documentation

This directory contains all documentation for the DikuMUD project.

## Directory Structure

### `original/`
Contains the original DikuMUD documentation files from the 1990s release. These documents describe the core systems and architecture of the original game.

Key files:
- `database.doc` - Database format and loading
- `dbsup.doc` - Database supplementary information
- `running.doc` - How to run the server
- `license.doc` - LGPL licensing information
- `interpreter.doc` - Command interpreter design
- `shops.doc` - Shop system documentation
- `spells.doc` - Magic system documentation

### `features/`
Documentation for features that have been added or modified since the original release:
- Combat prompt enhancements
- Game time independence
- Shop fixes and improvements
- Warrior/Scientist practice fixes
- Item fixes (boots, bronze coins, etc.)
- Reequip feature
- Tick timer
- Wildcard dots feature
- Exit summaries
- Room markers

### `testing/`
Documentation related to the testing framework and test infrastructure:
- Integration test framework design and implementation
- Test writing guides
- Shopkeeper integration tests
- Quest integration tests
- Zone object tests
- Test fixes and improvements

### `design/`
Design documents for major features and systems:
- Quest system design and implementation
- Zone expansions (Kaol, Ptarth, etc.)
- World building guides and optimization
- File format specifications (YAML schema, file formats)
- Object flags review
- Spec procedure fixes

### `milestones/`
Project milestone tracking and completion guides:
- Milestone completion documentation
- Phase completion summaries
- Validation status
- Solution summaries
- Future work ("What's Next")

## Running Tests

All tests are integrated into the build system. To run all tests:

```bash
cd dm-dist-alfa
make all
```

The `make all` target will:
1. Validate command mappings
2. Build the server and utilities
3. Build world files
4. Run all integration tests (66 YAML-based tests)

Integration tests are located in `tests/integration/` and cover:
- Shop functionality
- Item functionality
- Quest system
- Zone objects
- Game mechanics (combat, experience, time, etc.)

## Building the Game

See `original/running.doc` for basic information about running the server.

Quick start:
```bash
cd dm-dist-alfa
make all        # Build and test
./dmserver      # Run server on port 4000
```

## Contributing

When adding new features:
1. Add feature documentation to `docs/features/`
2. Add integration tests to `tests/integration/`
3. Update relevant design documents in `docs/design/`
4. Ensure `make all` passes all tests
