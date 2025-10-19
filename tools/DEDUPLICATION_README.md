# Player File Deduplication Tool

## Purpose

This tool fixes player files that have duplicate character entries. The duplication bug (now fixed) caused characters to be saved twice when they were first created, leading to wasted space and potential confusion.

## When to Use

Use this tool if you have an **existing player file** from before the password encoding bug fix was applied. The bug fix prevents new duplicates from being created, but doesn't remove existing duplicates from the player file.

You can check if your player file has duplicates by running:
```bash
cd dm-dist-alfa
strings lib/players | grep -i "^playername$" | sort | uniq -c
```

If any player name appears more than once, you have duplicates that this tool can remove.

## Building

From the `dm-dist-alfa` directory:
```bash
make ../tools/deduplicate_players
```

## Usage

### Basic Usage (from dm-dist-alfa directory)

```bash
# The tool operates on lib/players by default
../tools/deduplicate_players
```

### Custom Player File

```bash
# Specify a different player file
../tools/deduplicate_players path/to/players
```

## What It Does

1. **Reads** all entries from the player file
2. **Analyzes** and groups entries by character name (case-insensitive)
3. **Identifies** duplicate entries for each character
4. **Selects** the best entry for each character:
   - Prioritizes highest level
   - If levels are equal, uses most recent login
5. **Creates** a backup of the original file (`players.backup`)
6. **Writes** a deduplicated file (`players.dedup`)
7. **Reports** what was found and fixed

## Output Example

```
==========================================================
Player File Deduplication Tool
==========================================================

Reading player file: lib/players
Read 150 player entries from file

Analyzing for duplicates...
  Player 'talox': 2 duplicate entries found
  Player 'conan': 2 duplicate entries found

Total duplicate entries to remove: 2

Creating backup: lib/players.backup
Writing deduplicated file: lib/players.dedup
  Kept best entry for 'talox' (level 5, last logon: 1729200000)
  Kept best entry for 'conan' (level 10, last logon: 1729250000)

==========================================================
Deduplication Summary:
==========================================================
  Original entries:     150
  Duplicates removed:   2
  Final entries:        148

Files created:
  Backup:              lib/players.backup
  Deduplicated file:   lib/players.dedup

To apply the changes:
  1. Stop the MUD server if running
  2. Run: mv lib/players.dedup lib/players
  3. Verify the file works correctly
  4. If everything works, you can delete: lib/players.backup

✓ Deduplication complete!
==========================================================
```

## Applying the Changes

The tool is **safe** - it doesn't modify your original player file. Instead:

1. **Stop the MUD server** if it's running
2. **Review** the output to see what will change
3. **Apply** the deduplicated file:
   ```bash
   mv lib/players.dedup lib/players
   ```
4. **Start** the server and **verify** players can log in
5. **Keep** the backup (`lib/players.backup`) until you're confident everything works
6. **Delete** the backup once verified:
   ```bash
   rm lib/players.backup
   ```

## If No Duplicates Found

If the tool reports "No duplicates found", your player file is already clean and no action is needed.

## Safety Features

- **Never modifies** the original player file
- **Always creates** a backup before any changes
- **Writes to a new file** (`players.dedup`) that you must manually apply
- **Selects the best entry** based on level and last login time
- **Preserves all player data** - no information is lost

## Testing

Run the test suite to verify the tool works correctly:
```bash
cd /path/to/DikuMUD
./tests/test_deduplicate_players.sh
```

## Related

This tool addresses duplicate entries created by the bug fixed in PR #XXX. If you're starting fresh or haven't experienced duplicate player issues, you don't need this tool.
