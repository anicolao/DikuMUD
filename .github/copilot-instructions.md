# Copilot Instructions for DikuMUD

## Repository Overview

This is the original DikuMUD Alfa release - a historic Multi-User Dungeon (MUD) game from the early 1990s. This codebase is a preserved artifact of gaming history and should be treated with respect for its legacy nature.

## Technology Stack

- **Language**: C (ANSI C, early 90s style)
- **Build System**: Make
- **Platform**: Unix/Linux (originally BSD 4.3)
- **Dependencies**: libcrypt

## Key Principles

1. **Preserve Historical Code**: This is a historical codebase. Maintain the original coding style and structure unless explicitly asked to modernize.

2. **Minimal Changes**: When making modifications, preserve the original character and structure of the code. Avoid unnecessary refactoring.

3. **Licensing Awareness**: All code must respect the LGPL licensing terms described in `doc/license.doc`. Always reference this when making changes.

## Building the Project

```bash
cd dm-dist-alfa
make
```

This builds two executables:
- `dmserver` - The main MUD server
- `delplay` - Player deletion utility

## Code Style

The codebase follows 1990s C conventions:

- Tab-based indentation
- K&R-style bracing
- No modern C99/C11 features
- Minimal use of comments (code was written when comments were considered unnecessary for "obvious" logic)
- Liberal use of global variables (common in early MUD codebases)
- Function declarations without prototypes in many places

## Compiler Flags

The makefile uses specific flags to handle legacy code patterns:
- `-Wno-error=deprecated-declarations`
- `-Wno-error=implicit-function-declaration`
- `-Wno-error=char-subscripts`
- Various warnings suppressed for backwards compatibility

These flags are intentional - do not attempt to "fix" all warnings without understanding the historical context.

## File Organization

- `dm-dist-alfa/*.c` - Source files (41 files)
- `dm-dist-alfa/*.h` - Header files (9 files)
- `dm-dist-alfa/lib/` - Game data files (zones, objects, mobs)
- `dm-dist-alfa/doc/` - Original documentation

### Key Modules

- `comm.c` - Network communication and main game loop
- `interpreter.c` - Command parsing and execution
- `db.c` - Database loading and world management
- `act.*.c` - Player action handlers
- `spell*.c` - Magic system
- `fight.c` - Combat system
- `handler.c` - Object/character manipulation utilities

## Common Tasks

### Adding New Commands

1. Add function prototype in appropriate `act.*.c` file
2. Implement the command function
3. Register in `interpreter.c` command table

### Modifying Game Data

Game data is in `lib/` directory:
- `.wld` files - Room definitions
- `.mob` files - Mobile (NPC) definitions  
- `.obj` files - Object definitions
- `.zon` files - Zone reset commands

### Testing Changes

No automated tests exist. Testing requires:
1. Compile with `make`
2. Run `./dmserver`
3. Connect via telnet to test functionality
4. Verify with in-game commands

## Important Notes

1. **Testing**: This is legacy code without test infrastructure currently. Manual testing is required by running `./dmserver` and connecting via telnet. However, we are adding test framework code as the codebase is extended, so new features should include appropriate tests.

2. **Buffer Safety**: The original code predates modern security practices and contains unsafe buffer operations like `strcpy` and `sprintf`. **New code must always use safe alternatives** like `strncpy`, `snprintf`, etc. When updating existing functions, it is acceptable and encouraged to convert existing operations to safer versions.

3. **Global State**: Heavy use of global variables is intentional design for this era of MUD development.

4. **Documentation**: Always check `doc/*.doc` files for understanding subsystems before making changes.

5. **Compatibility**: Changes should maintain compatibility with the original DikuMUD world files and save formats when possible.

## When Making Changes

- Understand the historical context
- **Always run `make all` in `dm-dist-alfa/` directory before committing changes** to ensure no regressions are introduced
- Test thoroughly through actual gameplay
- Document any modern security fixes clearly
- Preserve the original DikuMUD experience
- Reference relevant `.doc` files in commit messages

## Resources

- Original README: `dm-dist-alfa/README`
- License information: `doc/license.doc`
- Running the game: `doc/running.doc`
- Database format: `doc/database.doc`, `doc/dbsup.doc`
- Command system: `doc/interpreter.doc`

## Contact

For questions about this historical codebase, refer to the credits file or the repository maintainer.
