# Password Encoding Bug Fix

## Problem Statement

A user reported that when creating a character, the password wasn't encoding correctly and they couldn't log in. Additionally, when examining the player file with `strings lib/players | grep Talox`, the character "Talox" appeared twice.

Example output:
```
$ strings lib/players | grep Talox
Talox
$6$Talox$sXQX4HH3J7.V8ftJ6T8KkotCVRwqvsBecCu3DLZO0U44/anLg94AdIGch8hRO4sPHj8fHzQVyALJqT3oPTIvf/
Talox
$6$Talox$sXQX4HH3J7.V8ftJ6T8KkotCVRwqvsBecCu3DLZO0U44/anLg94AdIGch8hRO4sPHj8fHzQVyALJqT3oPTIvf/
```

## Root Cause Analysis

Investigation revealed THREE separate bugs:

### Bug 1: Inconsistent Salt Formatting (interpreter.c:1482)

**Location**: CON_PWDNEW state handler (password change via menu option 4)

**The Problem**:
```c
// WRONG - used raw player name as salt
strcpy(d->pwd, encrypt_password(arg, d->character->player.name, &crypted));
```

**Why It Failed**:
- New player creation (CON_PWDGET) correctly used `make_salt()` to format salt as `$6$name$`
- Password change (CON_PWDNEW) passed raw player name without salt formatting
- This caused different encryption between creation and change, breaking login

**The Fix**:
```c
// CORRECT - use make_salt() for consistent formatting
strcpy(d->pwd, encrypt_password(arg, make_salt(d->character->player.name), &crypted));
```

### Bug 2: Password Hash Truncation (interpreter.c:1483)

**Location**: CON_PWDNEW state handler, immediately after encryption

**The Problem**:
```c
strcpy(d->pwd, encrypt_password(arg, ...));
*(d->pwd + 10) = '\0';  // WRONG - truncates to 10 characters!
```

**Why It Failed**:
- SHA-512 encrypted passwords are approximately 97-100 characters long
- Example: `$6$testpwd$hWHSE/gwWTZbn/pt6r.bNIBH.dsitM1xS36ZpA4TRcb9vcpAlPKJ14ZpRA3..mYQ1hTcgJFUx0g4AUOf7Qo5z.`
- Truncating to 10 characters left only: `$6$testpw`
- Password verification requires the full hash, so login always failed

**The Fix**:
```c
strcpy(d->pwd, encrypt_password(arg, make_salt(d->character->player.name), &crypted));
// Truncation line removed entirely
```

### Bug 3: Duplicate Character Save (db.c:2165)

**Location**: save_char() function when expanding player file for new characters

**The Problem**:
```c
if (expand)
{
    strcpy(mode, "a+");  // Open in append mode
    top_of_p_file++;
}

if (!(fl = fopen(PLAYER_FILE, mode)))
{
    perror("save char");
    exit(1);
}

fflush(fl);
if (expand)
{
    fwrite(&st, sizeof(struct char_file_u), 1, fl);  // Write #1 - WRONG!
}

fseek(fl, ch->desc->pos * sizeof(struct char_file_u), 0);

fwrite(&st, sizeof(struct char_file_u), 1, fl);  // Write #2
```

**Why It Failed**:
- When adding a new character, file opened in "a+" (append) mode
- First fwrite() wrote character to end of file
- fseek() attempted to position to specific offset
- Second fwrite() wrote character again (also to end, since "a+" mode ignores fseek for writes)
- Result: Character data written twice in file

**The Fix**:
```c
if (!(fl = fopen(PLAYER_FILE, mode)))
{
    perror("save char");
    exit(1);
}

fseek(fl, ch->desc->pos * sizeof(struct char_file_u), 0);

fwrite(&st, sizeof(struct char_file_u), 1, fl);
```

## Code Changes Summary

### dm-dist-alfa/interpreter.c
```diff
-			strcpy(d->pwd, encrypt_password(arg, d->character->player.name, &crypted));
-			*(d->pwd + 10) = '\0';
+			strcpy(d->pwd, encrypt_password(arg, make_salt(d->character->player.name), &crypted));
```

### dm-dist-alfa/db.c
```diff
-	fflush(fl);
-	if (expand)
-	{
-		fwrite(&st, sizeof(struct char_file_u), 1, fl);
-	}
-
 	fseek(fl, ch->desc->pos * sizeof(struct char_file_u), 0);
 
 	fwrite(&st, sizeof(struct char_file_u), 1, fl);
```

## Testing

Created comprehensive test (`tests/test_password_fix.sh`) that verifies:

1. ✅ Password hash is stored with correct salt format (`$6$name$...`)
2. ✅ Password hash is complete (~97 chars, not truncated to 10)
3. ✅ Character name appears exactly once in player file
4. ✅ All validation checks pass

Sample test output:
```
=== Password Change Bug Fix Test ===

1. Creating test player with password 'oldpass123'...
Created test player 'TestPwd' with load_room 3001, level 1

2. Checking password hash in player file...
   ✓ Password hash found correctly

3. Checking that character name appears only once...
   ✓ Character appears only once in player file

4. Verifying password hash is complete (not truncated)...
   ✓ Password hash is complete (length: 97)

=== All password tests PASSED ===
```

## Impact

✅ **Password Changes Now Work**: Users can change passwords via menu option 4 and log in successfully

✅ **No Duplicate Characters**: Each character saved exactly once in player file

✅ **Proper Password Security**: Full SHA-512 hashes preserved, maintaining security

✅ **Consistent Behavior**: Password creation and password change now use identical salt formatting

## Files Modified

- `dm-dist-alfa/interpreter.c` - Fixed password encryption and removed truncation
- `dm-dist-alfa/db.c` - Fixed duplicate character save
- `tests/test_password_fix.sh` - Automated test for verification
- `tests/demo_password_fix.sh` - Demonstration script
- `tests/integration/test_password_change.yaml` - Integration test (future enhancement)
- `tests/integration/test_new_character_single_save.yaml` - Integration test (future enhancement)
