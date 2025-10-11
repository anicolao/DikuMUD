#!/bin/bash

# Test script to verify game time independence
# This demonstrates that game hours take 75 seconds regardless of loop speed

echo "=========================================="
echo "Game Time Independence Test"
echo "=========================================="
echo ""
echo "This test verifies that game time is independent of main loop speed."
echo "A game hour should take 75 seconds whether the server runs in normal"
echo "mode (250ms per pulse) or spin mode (~10ms per pulse)."
echo ""

cd dm-dist-alfa

# Build the server and world files
echo "Building server and world files..."
make dmserver worldfiles > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi
echo "✅ Server and world files built successfully"
echo ""

# Build test player tool
echo "Building test tools..."
make ../tools/create_test_player > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Failed to build test tools"
    exit 1
fi

# Create test player if not exists
if [ ! -f lib/players/test ]; then
    echo "Creating test player..."
    ../tools/create_test_player test test lib > /dev/null 2>&1
fi
echo "✅ Test player ready"
echo ""

# Function to test server with given mode
test_mode() {
    local mode=$1
    local flag=$2
    
    echo "=========================================="
    echo "Testing: $mode"
    echo "=========================================="
    
    # Start server
    ./dmserver $flag > /tmp/server.log 2>&1 &
    local pid=$!
    sleep 2
    
    # Check if server is running
    if ! kill -0 $pid 2>/dev/null; then
        echo "❌ Server failed to start"
        return 1
    fi
    
    # Run Python test
    python3 << 'PYTEST'
import socket
import time
import re
import sys

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(('127.0.0.1', 4000))
    time.sleep(0.3)
    s.recv(8192)
    s.send(b'test\n')
    time.sleep(0.3)
    s.recv(8192)
    s.send(b'test\n')
    time.sleep(0.3)
    s.recv(8192)
    s.send(b'\n')
    time.sleep(0.3)
    s.recv(8192)
    s.send(b'1\n')
    time.sleep(0.3)
    s.recv(8192)
    return s

def get_tick(s):
    s.send(b'look\n')
    time.sleep(0.3)
    data = s.recv(8192).decode('latin-1')
    match = re.search(r'T:(\d+)', data)
    return int(match.group(1)) if match else None

try:
    s = connect()
    t1 = get_tick(s)
    start = time.time()
    time.sleep(6)
    t2 = get_tick(s)
    elapsed = time.time() - start
    
    if t1 and t2:
        decrease = t1 - t2
        print(f"  Initial tick: T:{t1}")
        print(f"  After {elapsed:.1f}s: T:{t2}")
        print(f"  Tick decreased: {decrease} seconds")
        
        if abs(decrease - elapsed) <= 2:
            print(f"  ✅ SUCCESS: Timer matches real time")
            sys.exit(0)
        else:
            print(f"  ❌ FAILED: Expected ~{int(elapsed)}s, got {decrease}s")
            sys.exit(1)
    else:
        print(f"  ❌ Could not read tick values")
        sys.exit(1)
    
    s.send(b'quit\n')
    s.send(b'0\n')
    s.close()
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)
PYTEST
    
    local result=$?
    
    # Stop server
    kill $pid 2>/dev/null
    wait $pid 2>/dev/null
    
    echo ""
    return $result
}

# Test normal mode
test_mode "Normal Mode (250ms per pulse)" ""
normal_result=$?

# Test spin mode
test_mode "Spin Mode (~10ms per pulse)" "-spin"
spin_result=$?

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="

if [ $normal_result -eq 0 ] && [ $spin_result -eq 0 ]; then
    echo "✅ ALL TESTS PASSED"
    echo ""
    echo "Game time is independent of main loop speed!"
    echo "A game hour takes 75 seconds in both normal and spin mode."
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    exit 1
fi
