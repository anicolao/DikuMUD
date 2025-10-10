#!/bin/bash
# Test script to verify CONSIDER command is properly mapped

set -e

echo "========================================"
echo "CONSIDER Command Mapping Test"
echo "========================================"
echo

cd /home/runner/work/DikuMUD/DikuMUD/dm-dist-alfa

echo "1. Building server..."
make clean > /dev/null 2>&1
make dmserver > /dev/null 2>&1
echo "   ✓ Server built successfully"
echo

echo "2. Verifying CONSIDER command exists in command array..."
if grep -q '"consider"' interpreter.c; then
    echo "   ✓ CONSIDER command found in command list"
else
    echo "   ✗ CONSIDER command not found"
    exit 1
fi
echo

echo "3. Determining CONSIDER command position..."
CONSIDER_POS=$(python3 << 'EOF'
import re
with open('interpreter.c', 'r') as f:
    content = f.read()
start = content.find('char *command[]=')
end = content.find('};', start)
section = content[start:end]
commands = re.findall(r'"([^"]+)"', section)
for i, cmd in enumerate(commands, 1):
    if cmd == 'consider':
        print(i)
        break
EOF
)
echo "   ✓ CONSIDER command is at position $CONSIDER_POS"
echo

echo "4. Verifying COMMANDO mapping for position $CONSIDER_POS..."
if grep -q "COMMANDO($CONSIDER_POS,.*do_consider" interpreter.c; then
    echo "   ✓ COMMANDO($CONSIDER_POS) correctly maps to do_consider"
else
    echo "   ✗ COMMANDO($CONSIDER_POS) does not map to do_consider"
    echo "   Current mapping:"
    grep "COMMANDO($CONSIDER_POS," interpreter.c
    exit 1
fi
echo

echo "5. Verifying GROUP command is not at CONSIDER's position..."
ACTUAL_FUNC=$(python3 << EOF
import re
with open('interpreter.c', 'r') as f:
    content = f.read()
pattern = r'COMMANDO\($CONSIDER_POS,([^,]+),([^,]+),([^)]+)\)'
match = re.search(pattern, content)
if match:
    print(match.group(2).strip())
EOF
)

if [ "$ACTUAL_FUNC" = "do_consider" ]; then
    echo "   ✓ Correct function: COMMANDO($CONSIDER_POS) maps to $ACTUAL_FUNC"
elif [ "$ACTUAL_FUNC" = "do_group" ]; then
    echo "   ✗ Bug still present: COMMANDO($CONSIDER_POS) incorrectly maps to do_group!"
    exit 1
else
    echo "   ✗ Unexpected mapping: COMMANDO($CONSIDER_POS) maps to $ACTUAL_FUNC"
    exit 1
fi
echo

echo "6. Verifying GROUP command has correct mapping..."
GROUP_POS=$(python3 << 'EOF'
import re
with open('interpreter.c', 'r') as f:
    content = f.read()
start = content.find('char *command[]=')
end = content.find('};', start)
section = content[start:end]
commands = re.findall(r'"([^"]+)"', section)
for i, cmd in enumerate(commands, 1):
    if cmd == 'group':
        print(i)
        break
EOF
)

if grep -q "COMMANDO($GROUP_POS,.*do_group" interpreter.c; then
    echo "   ✓ GROUP command (position $GROUP_POS) correctly maps to do_group"
else
    echo "   ✗ GROUP command mapping is incorrect"
    exit 1
fi
echo

echo "7. Running command validation script..."
if python3 validate_commands.py > /tmp/validate_output.txt 2>&1; then
    echo "   ✓ All command mappings validated successfully"
else
    echo "   ✗ Command validation failed"
    cat /tmp/validate_output.txt
    exit 1
fi
echo

echo "8. Verifying do_consider function exists..."
if grep -q "void do_consider" act.informative.c; then
    echo "   ✓ do_consider function found in act.informative.c"
else
    echo "   ✗ do_consider function not found"
    exit 1
fi
echo

echo "========================================"
echo "✅ All CONSIDER command tests passed!"
echo "========================================"
echo
echo "Summary:"
echo "  - CONSIDER command is at position $CONSIDER_POS in the command array"
echo "  - COMMANDO($CONSIDER_POS) correctly maps to do_consider function"
echo "  - GROUP command is at position $GROUP_POS and correctly maps to do_group"
echo "  - Bug fix verified: 'consider' command will now execute do_consider, not do_group"
echo
