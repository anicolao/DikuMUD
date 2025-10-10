#!/usr/bin/env python3
"""
Validate that command names in the command[] array match the COMMANDO() mappings
in interpreter.c to ensure commands are wired up correctly.
"""
import re
import sys

def parse_commands_array(filename):
    """Parse the command[] array to get command names indexed by position."""
    commands = {}
    in_array = False
    position = 1  # Commands start at position 1
    
    with open(filename, 'r') as f:
        for line in f:
            if 'char *command[]=' in line:
                in_array = True
                continue
            if in_array:
                if line.strip() == '};':
                    break
                # Match command name like: "north", or "reequip",   /* 221 */
                match = re.search(r'"([^"]+)"', line)
                if match:
                    cmd_name = match.group(1)
                    # Check for explicit position comment
                    comment_match = re.search(r'/\*\s*(\d+)\s*\*/', line)
                    if comment_match:
                        explicit_pos = int(comment_match.group(1))
                        if explicit_pos != position:
                            print(f"Warning: Command '{cmd_name}' has comment {explicit_pos} but is at position {position}")
                    
                    if cmd_name != '\\n':  # Ignore the terminator
                        commands[position] = cmd_name
                        position += 1
    
    return commands

def parse_commando_mappings(filename):
    """Parse COMMANDO() macro calls to get function mappings."""
    mappings = {}
    
    with open(filename, 'r') as f:
        content = f.read()
        
    # Find all COMMANDO calls: COMMANDO(number, position, function, level)
    pattern = r'COMMANDO\((\d+),([^,]+),([^,]+),([^)]+)\)'
    for match in re.finditer(pattern, content):
        cmd_num = int(match.group(1))
        position = match.group(2).strip()
        function = match.group(3).strip()
        level = match.group(4).strip()
        
        # Store the last definition (later definitions override earlier ones)
        mappings[cmd_num] = {
            'position': position,
            'function': function,
            'level': level
        }
    
    return mappings

def validate_mappings(commands, mappings):
    """Validate that all commands have proper COMMANDO mappings."""
    errors = []
    warnings = []
    
    # Check for commands without mappings
    for cmd_num, cmd_name in sorted(commands.items()):
        if cmd_num not in mappings:
            errors.append(f"Command #{cmd_num} '{cmd_name}' has no COMMANDO mapping")
        elif mappings[cmd_num]['function'] == '0':
            errors.append(f"Command #{cmd_num} '{cmd_name}' has NULL function pointer")
    
    # Check for duplicate mappings
    seen_mappings = {}
    with open('interpreter.c', 'r') as f:
        content = f.read()
    
    pattern = r'COMMANDO\((\d+),'
    for match in re.finditer(pattern, content):
        cmd_num = int(match.group(1))
        if cmd_num in seen_mappings:
            seen_mappings[cmd_num] += 1
        else:
            seen_mappings[cmd_num] = 1
    
    for cmd_num, count in sorted(seen_mappings.items()):
        if count > 1:
            cmd_name = commands.get(cmd_num, '???')
            warnings.append(f"Command #{cmd_num} '{cmd_name}' has {count} COMMANDO definitions (last one wins)")
    
    # Special check for REEQUIP (221) - it's OK to map to do_not_here
    # because it's handled by the guild special procedure in spec_procs.c
    # The check is to ensure it exists and has a mapping
    if 221 in commands and commands[221] == 'reequip':
        if 221 not in mappings:
            errors.append(f"Command #221 'reequip' has no COMMANDO mapping")
    
    # Special check for ZONE (222) - should map to do_zone
    if 222 in commands and commands[222] == 'zone':
        if 222 not in mappings:
            errors.append(f"Command #222 'zone' has no COMMANDO mapping")
        elif mappings[222]['function'] != 'do_zone':
            errors.append(f"Command #222 'zone' should map to do_zone but maps to {mappings[222]['function']}")
    
    return errors, warnings

def main():
    filename = 'interpreter.c'
    
    print("=" * 60)
    print("Command Mapping Validation")
    print("=" * 60)
    print()
    
    commands = parse_commands_array(filename)
    print(f"Found {len(commands)} commands in command[] array")
    
    mappings = parse_commando_mappings(filename)
    print(f"Found {len(mappings)} COMMANDO mappings")
    print()
    
    errors, warnings = validate_mappings(commands, mappings)
    
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()
    
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ✗ {error}")
        print()
        print("=" * 60)
        print("❌ Validation FAILED")
        print("=" * 60)
        return 1
    else:
        print("=" * 60)
        print("✅ All commands properly mapped!")
        print("=" * 60)
        return 0

if __name__ == '__main__':
    sys.exit(main())
