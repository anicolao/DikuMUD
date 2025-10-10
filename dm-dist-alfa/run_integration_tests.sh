#!/bin/bash
# Integration Test Runner for DikuMUD
#
# Usage:
#   ./run_integration_tests.sh [options] [test_file...]
#
# Options:
#   --verbose         Show detailed output
#   --help            Show this help message
#
# Examples:
#   ./run_integration_tests.sh                    # Run all tests
#   ./run_integration_tests.sh shops/             # Run shop tests  
#   ./run_integration_tests.sh bug_3003*.yaml     # Run specific test

set -e

# Configuration
TEST_DIR="../tests/integration"
SERVER_PATH="./dmserver"
RUNNER_SCRIPT="../tools/integration_test_runner.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse command line arguments
VERBOSE=0
TEST_PATTERN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=1
            shift
            ;;
        --help)
            head -n 14 "$0" | tail -n +2
            exit 0
            ;;
        *)
            TEST_PATTERN="$1"
            shift
            ;;
    esac
done

echo "=========================================="
echo "DikuMUD Integration Test Suite"
echo "=========================================="
echo ""

# Check if server exists
if [ ! -f "$SERVER_PATH" ]; then
    echo -e "${RED}✗ Error: Server not found at $SERVER_PATH${NC}"
    echo "  Please build the server first: make dmserver"
    exit 1
fi

# Check if Python script exists
if [ ! -f "$RUNNER_SCRIPT" ]; then
    echo -e "${RED}✗ Error: Test runner not found at $RUNNER_SCRIPT${NC}"
    exit 1
fi

# Check if test directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}✗ Error: Test directory not found at $TEST_DIR${NC}"
    exit 1
fi

# Run tests
FAILED=0
PASSED=0
TOTAL=0

if [ -z "$TEST_PATTERN" ]; then
    # Run all tests
    echo "Running all tests in: $TEST_DIR"
    echo ""
    
    for test_file in $(find "$TEST_DIR" -name "*.yaml" -type f 2>/dev/null | sort); do
        TOTAL=$((TOTAL + 1))
        echo "Running test: ${test_file#$TEST_DIR/}"
        
        if python3 "$RUNNER_SCRIPT" "$SERVER_PATH" "$test_file"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        echo ""
    done
else
    # Run specific test(s)
    for test_file in $(find "$TEST_DIR" -name "$TEST_PATTERN" -o -path "$TEST_DIR/$TEST_PATTERN" 2>/dev/null | sort); do
        if [ -f "$test_file" ]; then
            TOTAL=$((TOTAL + 1))
            echo "Running test: ${test_file#$TEST_DIR/}"
            
            if python3 "$RUNNER_SCRIPT" "$SERVER_PATH" "$test_file"; then
                PASSED=$((PASSED + 1))
            else
                FAILED=$((FAILED + 1))
            fi
            echo ""
        fi
    done
fi

# Print summary
echo "=========================================="
echo "Test Results Summary"
echo "=========================================="
echo "Total:  $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED test(s) failed${NC}"
    exit 1
fi
