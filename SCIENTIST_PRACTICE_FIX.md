# Scientist Practice Fix

## Issue
The scientist practice command had two problems:
1. Error messages said "spell" instead of "technology"
2. The guildmaster lists "force projector" as available, but practice 'force projector' says "You do not know of this technology..."

## Root Causes
The guild() function in spec_procs.c had two issues:

1. **Terminology:** Used outdated "spell" terminology from before the Barsoom reskinning. All references to "spells" needed to be changed to "technologies" for scientist and noble classes.

2. **Quote Handling:** The function didn't strip quotes from technology names. When users typed `practice 'force projector'` (with quotes, as used with the `activate` command), the function was searching for "'force projector'" (including the quotes) instead of "force projector", causing all technology practice attempts to fail.

## Changes Made
Updated `dm-dist-alfa/spec_procs.c`:

1. **Scientist (CLASS_MAGIC_USER) class:**
   - Line 138: Changed "spells" to "technologies" in list message
   - Lines 151, 155: Changed "spell" to "technology" in error messages
   - **Added quote stripping logic** to handle technology names with quotes (e.g., `practice 'force projector'`)

2. **Noble (CLASS_CLERIC) class:**
   - Line 223: Changed "spells" to "technologies" in list message
   - Lines 235, 239: Changed "spell" to "technology" in error messages
   - **Added quote stripping logic** to handle technology names with quotes

3. **Thief class (bonus fix):**
   - Line 194: Changed "spell" to "skill" in error message (was incorrect even before reskinning)

## Verification
Build completed successfully:
```bash
cd dm-dist-alfa && make dmserver
```

## Manual Testing Steps
To verify the fix works in-game:

1. Start the server: `./dmserver`
2. Create a scientist character
3. Go to the scientist guild
4. Type `practice` to see the list - should say "technologies"
5. Try `practice 'force projector'` - should either practice it or say "You do not know of this technology..." (not "spell")
6. Try an invalid technology name like `practice 'invalid'` - should say "You do not know of this technology..."

## Related Files
- `dm-dist-alfa/spec_procs.c` - Guild practice function
- `dm-dist-alfa/spell_parser.c` - Technology/spell name definitions
- `barsoom/RESKINNING_SUMMARY.md` - Overall reskinning documentation

## Technical Details

The quote stripping logic works as follows:
```c
if (*arg == '\'') {
    int len;
    arg++; /* Skip opening quote */
    for(len=0; arg[len] && arg[len] != '\''; len++)
        ;
    if (arg[len] == '\'') {
        arg[len] = '\0'; /* Null-terminate at closing quote */
    }
}
```

This matches the pattern used in the `activate` (cast) command in spell_parser.c, ensuring consistent behavior between activating and practicing technologies.

## Notes
This fix addresses both the terminology inconsistency from the original Barsoom reskinning work and the critical functional bug where quote handling prevented technology practice from working at all.
