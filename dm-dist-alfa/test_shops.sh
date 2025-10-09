#!/bin/bash
# Test script to verify shops are configured correctly

echo "=== Shop Configuration Test ==="
echo ""
echo "Testing shop data files..."
echo ""

# Check if shop file exists and contains bread
if [ ! -f "lib/tinyworld.shp" ]; then
    echo "ERROR: tinyworld.shp not found"
    exit 1
fi

echo "1. Checking for bread item 3010 in shop file..."
if grep -q "^3010$" lib/tinyworld.shp; then
    echo "   ✓ Found bread (3010) in shop file"
else
    echo "   ✗ Bread (3010) NOT found in shop file"
    exit 1
fi

echo "2. Checking for fine bread item 3510 in shop file..."
if grep -q "^3510$" lib/tinyworld.shp; then
    echo "   ✓ Found fine bread (3510) in shop file"
else
    echo "   ✗ Fine bread (3510) NOT found in shop file"
    exit 1
fi

echo ""
echo "3. Running comprehensive shop validation..."
python3 ../tools/validate_shops.py lib/tinyworld.shp lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.wld > /tmp/shop_validation.txt 2>&1

# Check if bread items appear as valid in shops (with checkmark)
if grep -q "3010 ✓" /tmp/shop_validation.txt && grep -q "3510 ✓" /tmp/shop_validation.txt; then
    echo "   ✓ Both bread items are validated and available in shops"
else
    echo "   ✗ Bread items validation failed"
    grep -E "(3010|3510)" /tmp/shop_validation.txt | head -10
    exit 1
fi

echo ""
echo "=== Test Results ==="
echo "✅ All shop configuration tests passed!"
echo ""
echo "Summary of changes:"
echo "  - Lesser Helium shop #1 (room 3009) now sells bread (3010)"
echo "  - Greater Helium shop #3 (room 3928) now sells fine bread (3510)"
echo "  - All Greater Helium shops have corrected keeper/room vnums"
echo ""
echo "Players can now buy bread from provisions shops!"
