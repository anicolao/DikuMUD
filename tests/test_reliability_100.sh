#!/bin/bash
# Test script to verify experience_gain test reliability
# Runs the test 100 times and reports pass/fail statistics

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/../dm-dist-alfa" || exit 1

echo "Running experience_gain test 100 times to verify reliability..."
echo "This may take several minutes..."
echo ""

pass=0
fail=0
total=100

for i in $(seq 1 $total); do
    result=$(python3 ../tools/integration_test_runner.py ./dmserver ../tests/integration/test_experience_gain.yaml 2>&1 | grep -E "(PASSED|FAILED)" | tail -1)
    
    if echo "$result" | grep -q "PASSED"; then
        ((pass++))
    else
        ((fail++))
        echo "Run $i: FAILED"
    fi
    
    # Progress update every 10 runs
    if [ $((i % 10)) -eq 0 ]; then
        echo "Progress: $i/$total (Passed: $pass, Failed: $fail)"
    fi
done

echo ""
echo "=========================================="
echo "Final Results:"
echo "=========================================="
echo "Total runs:  $total"
echo "Passed:      $pass"
echo "Failed:      $fail"
echo "Success rate: $((pass * 100 / total))%"
echo ""

if [ $fail -eq 0 ]; then
    echo "✅ All tests passed! The experience_gain test is 100% reliable."
    exit 0
else
    echo "❌ Some tests failed. Review the failures above."
    exit 1
fi
