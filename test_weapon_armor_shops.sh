#!/bin/bash
# Test script for weapon and armor shops in Lesser Helium

echo "=== Testing Weapon and Armor Shops in Lesser Helium ==="
echo ""

cd dm-dist-alfa

echo "1. Building world files..."
python3 ../tools/world_builder.py build-all lib lib/zones_yaml/*.yaml > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ World build successful"
else
    echo "   ✗ World build failed"
    exit 1
fi

echo ""
echo "2. Validating shops..."
python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld | grep -E "Shop #17|Shop #18" -A 12

echo ""
echo "3. Checking for missing shops warnings..."
MISSING_3003=$(python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld 2>&1 | grep "Mob 3003")
MISSING_3004=$(python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld 2>&1 | grep "Mob 3004")
MISSING_3011=$(python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld 2>&1 | grep "Room 3011")
MISSING_3020=$(python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld 2>&1 | grep "Room 3020")

if [ -z "$MISSING_3003" ]; then
    echo "   ✓ Mob 3003 (weaponsmith) no longer missing"
else
    echo "   ✗ Mob 3003 still reported as missing"
fi

if [ -z "$MISSING_3004" ]; then
    echo "   ✓ Mob 3004 (armorer) no longer missing"
else
    echo "   ✗ Mob 3004 still reported as missing"
fi

if [ -z "$MISSING_3011" ]; then
    echo "   ✓ Room 3011 (Weapon Smith) no longer missing"
else
    echo "   ✗ Room 3011 still reported as missing"
fi

if [ -z "$MISSING_3020" ]; then
    echo "   ✓ Room 3020 (Armory) no longer missing"
else
    echo "   ✗ Room 3020 still reported as missing"
fi

echo ""
echo "4. Checking shop inventory..."
echo "   Weapon Smith (Shop #17):"
grep -A 7 "^#17~" lib/tinyworld.shp | head -8 | tail -6 | while read vnum; do
    if [ ! -z "$vnum" ] && [ "$vnum" != "-1" ]; then
        OBJ_NAME=$(grep "^#$vnum$" lib/tinyworld.obj -A 2 | tail -1 | tr -d '~')
        if [ ! -z "$OBJ_NAME" ]; then
            echo "      - $vnum: $OBJ_NAME"
        fi
    fi
done

echo ""
echo "   Armory (Shop #18):"
grep -A 7 "^#18~" lib/tinyworld.shp | head -8 | tail -6 | while read vnum; do
    if [ ! -z "$vnum" ] && [ "$vnum" != "-1" ]; then
        OBJ_NAME=$(grep "^#$vnum$" lib/tinyworld.obj -A 2 | tail -1 | tr -d '~')
        if [ ! -z "$OBJ_NAME" ]; then
            echo "      - $vnum: $OBJ_NAME"
        fi
    fi
done

echo ""
echo "=== Test Complete ==="
echo ""
echo "To test in-game:"
echo "  1. Start server: ./dmserver 4242"
echo "  2. Connect: telnet localhost 4242"
echo "  3. Create character and login"
echo "  4. goto 3011"
echo "  5. list"
echo "  6. goto 3020"
echo "  7. list"
