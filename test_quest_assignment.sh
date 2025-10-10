#!/bin/bash
# Test script to verify automatic quest giver assignment

set -e

echo "========================================"
echo "Quest Giver Assignment Test"
echo "========================================"
echo

cd dm-dist-alfa

echo "1. Building world files..."
make worldfiles > /dev/null 2>&1
echo "   ✓ World files built"
echo

echo "2. Checking quest file..."
if [ -f lib/tinyworld.qst ]; then
    quest_count=$(grep -c "^#[0-9]" lib/tinyworld.qst)
    echo "   ✓ Quest file exists with $quest_count quests"
else
    echo "   ✗ Quest file not found"
    exit 1
fi
echo

echo "3. Extracting quest giver vnums from quest file..."
quest_givers=$(awk '/^#[0-9]+/{getline; print $1}' lib/tinyworld.qst | sort -u | wc -l)
echo "   ✓ Found $quest_givers unique quest givers"
echo

echo "4. Building server..."
make dmserver > /dev/null 2>&1
echo "   ✓ Server built successfully"
echo

echo "5. Testing server boot and quest giver assignment..."
timeout 5 ./dmserver -p 5175 > /tmp/quest_server_output.txt 2>&1 || true

# Check if quests were loaded
if grep -q "quests loaded" /tmp/quest_server_output.txt; then
    loaded_quests=$(grep "quests loaded" /tmp/quest_server_output.txt | grep -o '[0-9]* quests loaded' | awk '{print $1}')
    echo "   ✓ Server loaded $loaded_quests quests"
else
    echo "   ✗ Server did not report loading quests"
    exit 1
fi

# Check if quest givers were assigned
if grep -q "quest givers assigned" /tmp/quest_server_output.txt; then
    assigned_givers=$(grep "quest givers assigned" /tmp/quest_server_output.txt | grep -o '[0-9]* quest givers assigned' | awk '{print $1}')
    echo "   ✓ Server assigned $assigned_givers quest givers"
else
    echo "   ✗ Server did not report assigning quest givers"
    exit 1
fi

# Verify the counts match
if [ "$loaded_quests" -eq "$assigned_givers" ]; then
    echo "   ✓ Quest count matches assigned givers count"
else
    echo "   ✗ Quest count ($loaded_quests) does not match assigned givers count ($assigned_givers)"
    exit 1
fi
echo

echo "6. Verifying no spec_assign.c hardcoding..."
if grep -q "mob_index\[real_mobile([0-9]*)\]\.func = quest_giver" spec_assign.c; then
    echo "   ✗ Found hardcoded quest_giver assignments in spec_assign.c"
    grep "quest_giver" spec_assign.c
    exit 1
else
    echo "   ✓ No hardcoded quest_giver assignments found"
fi
echo

echo "========================================"
echo "✓ ALL TESTS PASSED"
echo "========================================"
echo
echo "Quest giver assignment system is working correctly:"
echo "  • Quest file contains $quest_count quests"
echo "  • $quest_givers unique quest givers identified"
echo "  • All quest givers automatically assigned at boot time"
echo "  • No hardcoded assignments in spec_assign.c"
echo "  • Future quests can be added as pure data"
echo
