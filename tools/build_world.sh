#!/bin/bash
# Build DikuMUD world files from YAML sources

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILDER="$SCRIPT_DIR/world_builder.py"

# Get parameters
OUTPUT_DIR="$1"
FILE_TYPE="$2"
shift 2
YAML_FILES=("$@")

# Determine output filename
case "$FILE_TYPE" in
    wld) OUTPUT_FILE="$OUTPUT_DIR/tinyworld.wld" ;;
    mob) OUTPUT_FILE="$OUTPUT_DIR/tinyworld.mob" ;;
    obj) OUTPUT_FILE="$OUTPUT_DIR/tinyworld.obj" ;;
    zon) OUTPUT_FILE="$OUTPUT_DIR/tinyworld.zon" ;;
    shp) OUTPUT_FILE="$OUTPUT_DIR/tinyworld.shp" ;;
    *) echo "Unknown file type: $FILE_TYPE"; exit 1 ;;
esac

# Build the file
echo "Building $OUTPUT_FILE from ${#YAML_FILES[@]} zone files..."
python3 "$BUILDER" build "$FILE_TYPE" "$OUTPUT_FILE" "${YAML_FILES[@]}"
