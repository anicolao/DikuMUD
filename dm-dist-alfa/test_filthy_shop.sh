#!/bin/bash
# Test script to verify Filthy's shop is configured correctly

echo "=== Filthy the Bartender Shop Test ==="
echo ""
echo "Testing Filthy's shop configuration..."
echo ""

# Check if shop file exists
if [ ! -f "lib/tinyworld.shp" ]; then
    echo "ERROR: tinyworld.shp not found"
    exit 1
fi

echo "1. Checking for shop #12 (Filthy's shop)..."
if grep -q "^#12~" lib/tinyworld.shp; then
    echo "   ✓ Found shop #12 in shop file"
else
    echo "   ✗ Shop #12 NOT found in shop file"
    exit 1
fi

echo "2. Checking for wine (3002) in Filthy's shop..."
if grep -A5 "^#12~" lib/tinyworld.shp | grep -q "^3002$"; then
    echo "   ✓ Found wine (3002) in shop #12"
else
    echo "   ✗ Wine (3002) NOT found in shop #12"
    exit 1
fi

echo "3. Checking for whiskey (3003) in Filthy's shop..."
if grep -A5 "^#12~" lib/tinyworld.shp | grep -q "^3003$"; then
    echo "   ✓ Found whiskey (3003) in shop #12"
else
    echo "   ✗ Whiskey (3003) NOT found in shop #12"
    exit 1
fi

echo "4. Checking for local wine (3004) in Filthy's shop..."
if grep -A5 "^#12~" lib/tinyworld.shp | grep -q "^3004$"; then
    echo "   ✓ Found local wine (3004) in shop #12"
else
    echo "   ✗ Local wine (3004) NOT found in shop #12"
    exit 1
fi

echo ""
echo "5. Running comprehensive shop validation for shop #12..."
python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld > /tmp/filthy_shop_validation.txt 2>&1

# Check specifically for shop 12
if grep -q "Shop #12:" /tmp/filthy_shop_validation.txt; then
    # Verify keeper
    if grep -A2 "Shop #12:" /tmp/filthy_shop_validation.txt | grep -q "Keeper: mob 3046 ✓"; then
        echo "   ✓ Keeper (Filthy, mob 3046) validated"
    else
        echo "   ✗ Keeper validation failed"
        grep -A10 "Shop #12:" /tmp/filthy_shop_validation.txt
        exit 1
    fi
    
    # Verify room
    if grep -A3 "Shop #12:" /tmp/filthy_shop_validation.txt | grep -q "Room: 3048 ✓"; then
        echo "   ✓ Room (3048 - Poor Inn) validated"
    else
        echo "   ✗ Room validation failed"
        exit 1
    fi
    
    # Verify drinks
    if grep -A6 "Shop #12:" /tmp/filthy_shop_validation.txt | grep -q "3002 (a flask of wine) ✓"; then
        echo "   ✓ Wine item validated"
    else
        echo "   ✗ Wine item validation failed"
        exit 1
    fi
    
    if grep -A7 "Shop #12:" /tmp/filthy_shop_validation.txt | grep -q "3003 (a strong whiskey) ✓"; then
        echo "   ✓ Whiskey item validated"
    else
        echo "   ✗ Whiskey item validation failed"
        exit 1
    fi
    
    if grep -A8 "Shop #12:" /tmp/filthy_shop_validation.txt | grep -q "3004 (a flask of local wine) ✓"; then
        echo "   ✓ Local wine item validated"
    else
        echo "   ✗ Local wine item validation failed"
        exit 1
    fi
else
    echo "   ✗ Shop #12 not found in validation output"
    exit 1
fi

echo ""
echo "=== Test Results ==="
echo "✅ All Filthy's shop tests passed!"
echo ""
echo "Summary:"
echo "  - Filthy the Bartender (mob 3046) is now a shopkeeper"
echo "  - Shop #12 is located in room 3048 (Poor Inn)"
echo "  - Sells 3 drinks:"
echo "    • Wine (3002) - a flask of wine"
echo "    • Whiskey (3003) - a strong whiskey"  
echo "    • Local wine (3004) - a flask of local wine"
echo "  - Shop is open 24 hours"
echo ""
echo "Players can now buy drinks from Filthy the Bartender!"
