#!/bin/bash
# Test the deduplicate_players tool

set -e

cd "$(dirname "$0")/../dm-dist-alfa"

echo "=== Player File Deduplication Tool Test ==="
echo ""

# Build the tools if they don't exist
if [ ! -f ../tools/create_test_player ]; then
    echo "Building create_test_player tool..."
    make ../tools/create_test_player > /dev/null 2>&1
    echo "   ✓ create_test_player built successfully"
    echo ""
fi

if [ ! -f ../tools/deduplicate_players ]; then
    echo "Building deduplicate_players tool..."
    make ../tools/deduplicate_players > /dev/null 2>&1
    echo "   ✓ deduplicate_players built successfully"
    echo ""
fi

# Clean up any existing test files
rm -rf test_dedup_lib 2>/dev/null || true
mkdir -p test_dedup_lib

echo "1. Creating test player file with duplicates..."

# Create individual player files
../tools/create_test_player -d test_dedup_lib Player1 pass1 3001 > /dev/null 2>&1
mv test_dedup_lib/players test_dedup_lib/player1.dat
echo "   Created Player1"

../tools/create_test_player -d test_dedup_lib Player2 pass2 3001 > /dev/null 2>&1
mv test_dedup_lib/players test_dedup_lib/player2.dat
echo "   Created Player2"

../tools/create_test_player -d test_dedup_lib Player3 pass3 3001 > /dev/null 2>&1
mv test_dedup_lib/players test_dedup_lib/player3.dat
echo "   Created Player3"

# Build composite file: Player1 + Player2 + Player2 (duplicate) + Player3
cat test_dedup_lib/player1.dat test_dedup_lib/player2.dat test_dedup_lib/player2.dat test_dedup_lib/player3.dat > test_dedup_lib/players
echo "   Created composite file with Player2 duplicated (simulating bug)"

# Show player file status before deduplication
echo ""
echo "2. Player file before deduplication:"
PLAYER_COUNT=$(strings test_dedup_lib/players | grep -c '^player[123]$' || true)
echo "   Total player name entries: $PLAYER_COUNT"
echo "   Expected: 4 (Player1, Player2 x2, Player3)"

# Count each player
P1_COUNT=$(strings test_dedup_lib/players | grep -c '^player1$' || true)
P2_COUNT=$(strings test_dedup_lib/players | grep -c '^player2$' || true)
P3_COUNT=$(strings test_dedup_lib/players | grep -c '^player3$' || true)
echo "   Player1 appears: $P1_COUNT time(s)"
echo "   Player2 appears: $P2_COUNT time(s)"
echo "   Player3 appears: $P3_COUNT time(s)"

if [ "$P2_COUNT" -ne 2 ]; then
    echo "FAIL: Player2 should appear twice"
    exit 1
fi

echo ""
echo "3. Running deduplication tool..."
cd test_dedup_lib
../../tools/deduplicate_players players
cd ..

echo ""
echo "4. Verifying deduplication results..."

# Check that backup was created
if [ ! -f test_dedup_lib/players.backup ]; then
    echo "FAIL: Backup file not created"
    exit 1
fi
echo "   ✓ Backup file created"

# Check that deduplicated file was created
if [ ! -f test_dedup_lib/players.dedup ]; then
    echo "FAIL: Deduplicated file not created"
    exit 1
fi
echo "   ✓ Deduplicated file created"

# Verify deduplicated file has no duplicates
DEDUP_COUNT=$(strings test_dedup_lib/players.dedup | grep -c '^player[123]$' || true)
echo "   Deduplicated file player entries: $DEDUP_COUNT"

if [ "$DEDUP_COUNT" -ne 3 ]; then
    echo "FAIL: Expected 3 unique players in deduplicated file, found $DEDUP_COUNT"
    exit 1
fi

# Count each player in deduplicated file
P1_DEDUP=$(strings test_dedup_lib/players.dedup | grep -c '^player1$' || true)
P2_DEDUP=$(strings test_dedup_lib/players.dedup | grep -c '^player2$' || true)
P3_DEDUP=$(strings test_dedup_lib/players.dedup | grep -c '^player3$' || true)
echo "   Player1 appears: $P1_DEDUP time(s)"
echo "   Player2 appears: $P2_DEDUP time(s)"
echo "   Player3 appears: $P3_DEDUP time(s)"

if [ "$P1_DEDUP" -ne 1 ] || [ "$P2_DEDUP" -ne 1 ] || [ "$P3_DEDUP" -ne 1 ]; then
    echo "FAIL: Each player should appear exactly once in deduplicated file"
    exit 1
fi

echo "   ✓ All players appear exactly once"

echo ""
echo "5. Testing with clean file (no duplicates)..."
# Test that the tool correctly handles a file with no duplicates
rm -rf test_dedup_lib
mkdir -p test_dedup_lib
../tools/create_test_player -d test_dedup_lib CleanPlayer cleanpass 3001 > /dev/null 2>&1

cd test_dedup_lib
../../tools/deduplicate_players players > /tmp/dedup_clean_output.txt 2>&1
cd ..

if grep -q "No duplicates found" /tmp/dedup_clean_output.txt; then
    echo "   ✓ Tool correctly detected no duplicates"
else
    echo "FAIL: Tool should detect no duplicates in clean file"
    cat /tmp/dedup_clean_output.txt
    exit 1
fi

echo ""
echo "=== All deduplication tests PASSED ==="
echo ""

# Cleanup
rm -rf test_dedup_lib 2>/dev/null || true
rm -f /tmp/dedup_clean_output.txt 2>/dev/null || true
