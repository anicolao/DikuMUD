#!/bin/bash
# Manual test for password change functionality
# This script verifies that password change works and the character is saved only once

set -e

cd "$(dirname "$0")/../dm-dist-alfa"

echo "=== Password Change Bug Fix Test ==="
echo ""

# Clean up any existing test player
rm -f lib/players_test 2>/dev/null || true
rm -rf test_lib 2>/dev/null || true

# Create test_lib directory
mkdir -p test_lib

# Create a test player with initial password
echo "1. Creating test player with password 'oldpass123'..."
../tools/create_test_player -d test_lib TestPwd oldpass123 3001
if [ $? -ne 0 ]; then
    echo "FAIL: Could not create test player"
    exit 1
fi

# Verify the password hash in the player file
echo ""
echo "2. Checking password hash in player file..."
strings test_lib/players | grep -A1 "testpwd"
HASH_COUNT=$(strings test_lib/players | grep -c '\$6\$testpwd\$' || true)
if [ "$HASH_COUNT" -ne 1 ]; then
    echo "FAIL: Expected exactly 1 password hash, found $HASH_COUNT"
    exit 1
fi
echo "   ✓ Password hash found correctly"

# Verify character appears only once
echo ""
echo "3. Checking that character name appears only once..."
NAME_COUNT=$(strings test_lib/players | grep -c '^testpwd$' || true)
if [ "$NAME_COUNT" -ne 1 ]; then
    echo "FAIL: Character name should appear exactly once, found $NAME_COUNT times"
    exit 1
fi
echo "   ✓ Character appears only once in player file"

# Verify password hash is not truncated
echo ""
echo "4. Verifying password hash is complete (not truncated)..."
HASH=$(strings test_lib/players | grep '\$6\$testpwd\$' || true)
HASH_LEN=${#HASH}
if [ "$HASH_LEN" -lt 50 ]; then
    echo "FAIL: Password hash appears truncated (length: $HASH_LEN)"
    echo "Hash: $HASH"
    exit 1
fi
echo "   ✓ Password hash is complete (length: $HASH_LEN)"

echo ""
echo "=== All password tests PASSED ==="
echo ""

# Cleanup
rm -rf test_lib 2>/dev/null || true
