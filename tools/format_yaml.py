#!/usr/bin/env python3
"""
Format YAML zone files to use literal block scalars for multi-line strings.

This tool improves the readability of YAML zone files by converting
multi-line strings from escaped format to YAML's literal block scalar format.
"""

import sys
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString


def convert_multiline_to_literal(data):
    """
    Recursively convert multi-line strings to literal block scalars.
    
    Multi-line strings (containing \\n) are converted to use YAML's | format
    which is much more readable than escaped strings.
    """
    if isinstance(data, dict):
        return {k: convert_multiline_to_literal(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_multiline_to_literal(item) for item in data]
    elif isinstance(data, str) and '\n' in data:
        # Convert multi-line strings to literal scalars
        return LiteralScalarString(data)
    else:
        return data


def format_yaml_file(yaml_file, backup=True):
    """
    Format a YAML file to use literal block scalars.
    
    Args:
        yaml_file: Path to the YAML file to format
        backup: If True, create a .bak backup before formatting
    
    Returns:
        True if successful, False otherwise
    """
    yaml_file = Path(yaml_file)
    
    if not yaml_file.exists():
        print(f"Error: {yaml_file} not found", file=sys.stderr)
        return False
    
    # Initialize ruamel.yaml with appropriate settings
    yaml = YAML()
    yaml.preserve_quotes = False
    yaml.default_flow_style = False
    yaml.width = 4096  # Prevent line wrapping
    yaml.indent(mapping=2, sequence=2, offset=0)
    
    try:
        # Load the YAML file
        with open(yaml_file, 'r') as f:
            data = yaml.load(f)
        
        # Convert multi-line strings to literal scalars
        data = convert_multiline_to_literal(data)
        
        # Create backup if requested
        if backup:
            backup_file = yaml_file.with_suffix(yaml_file.suffix + '.bak')
            yaml_file.rename(backup_file)
            print(f"Created backup: {backup_file}")
        
        # Write formatted YAML
        with open(yaml_file, 'w') as f:
            yaml.dump(data, f)
        
        print(f"Formatted: {yaml_file}")
        return True
        
    except Exception as e:
        print(f"Error formatting {yaml_file}: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: format_yaml.py <yaml_file> [--no-backup]")
        print("\nFormat YAML files to use literal block scalars for multi-line strings.")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    backup = '--no-backup' not in sys.argv
    
    success = format_yaml_file(yaml_file, backup=backup)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
