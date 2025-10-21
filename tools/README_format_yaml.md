# YAML Formatting Tool

## Overview

The `format_yaml.py` tool reformats YAML zone files to use literal block scalars for multi-line strings, making them much more readable and maintainable. The tool is configured to match standard editor formatting conventions.

## Problem

Originally, YAML files used escaped newlines in quoted strings:

```yaml
description: "   You are in the temple.\nThe walls are covered in murals.\n   Steps lead down."
```

This format is hard to read and edit.

## Solution

The tool converts multi-line strings to use YAML's literal block scalar format (`|`):

```yaml
description: |2-
     You are in the temple.
  The walls are covered in murals.
     Steps lead down.
```

## Formatting Standards

The tool produces YAML with these formatting conventions:

1. **List indentation**: List items (`-`) are indented 2 spaces from their parent key
2. **List content**: Properties within list items are indented 4 spaces from the parent key  
3. **Nested lists**: Follow the same pattern recursively
4. **Empty strings**: Use double quotes (`""`) instead of single quotes
5. **Multi-line strings**: Use literal block scalars (`|`) for readability

### Example

```yaml
rooms:
  - vnum: 3001
    name: The Temple
    exits:
      - direction: 0
        keywords: ""
        to_room: 3002
```

## Usage

```bash
# Format a single YAML file (creates .bak backup)
python3 tools/format_yaml.py dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml

# Format without creating a backup
python3 tools/format_yaml.py dm-dist-alfa/lib/zones_yaml/lesser_helium.yaml --no-backup
```

## Dependencies

The tool requires `ruamel.yaml`:

```bash
pip install ruamel.yaml
```

## Validation

After formatting, always validate the world:

```bash
cd dm-dist-alfa
make validate-world
make build-worldfiles
```

## Technical Details

- Uses `ruamel.yaml` library which provides better control over YAML formatting than PyYAML
- Automatically detects multi-line strings (containing `\n`) and converts them to literal block scalars
- Empty strings are explicitly formatted with double quotes
- Indent settings: `mapping=2, sequence=4, offset=2` for consistent formatting
- Preserves the semantic meaning of the YAML (content is identical)
- Only changes the presentation format
- Compatible with all existing YAML parsing tools (PyYAML, ruamel.yaml, etc.)

## Example

Applied to `lesser_helium.yaml`:
- Before: 5222 lines with escaped newlines and quoted strings
- After: 5222 lines with literal block scalars and proper indentation
- Validation: ✓ Passes all tests
- Build: ✓ Successfully builds world files
