#!/bin/bash

# FDA 510(k) Predicate Extraction Wrapper Script
# This script runs the Python extraction tool with proper path resolution

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The Python tool is expected to be in the parent of the plugin directory
# Plugin is at ~/.claude/plugins/fda-predicate-assistant
# Python tool is at the original project location

# Try to find the Python script
PYTHON_SCRIPT=""

# First, check if there's a configured path
if [ -f "$HOME/.claude/fda-predicate-assistant.local.md" ]; then
    CONFIGURED_PATH=$(grep -oP 'python_script_path:\s*\K.*' "$HOME/.claude/fda-predicate-assistant.local.md" 2>/dev/null | tr -d ' ')
    if [ -n "$CONFIGURED_PATH" ] && [ -f "$CONFIGURED_PATH" ]; then
        PYTHON_SCRIPT="$CONFIGURED_PATH"
    fi
fi

# Check common locations
if [ -z "$PYTHON_SCRIPT" ]; then
    POSSIBLE_PATHS=(
        "/mnt/c/510k/Python/PredicateExtraction/Test69a_final_ocr_smart_v2.py"
        "$SCRIPT_DIR/../../../Test69a_final_ocr_smart_v2.py"
        "./Test69a_final_ocr_smart_v2.py"
    )

    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -f "$path" ]; then
            PYTHON_SCRIPT="$path"
            break
        fi
    done
fi

if [ -z "$PYTHON_SCRIPT" ]; then
    echo "ERROR: Could not find Test69a_final_ocr_smart_v2.py"
    echo "Please set the path in ~/.claude/fda-predicate-assistant.local.md:"
    echo "  python_script_path: /path/to/Test69a_final_ocr_smart_v2.py"
    exit 1
fi

echo "Using extraction script: $PYTHON_SCRIPT"
echo "Arguments: $@"
echo ""

# Parse arguments
DIRECTORY=""
YEAR=""
PRODUCT_CODE=""
OCR_MODE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --year)
            YEAR="$2"
            shift 2
            ;;
        --product-code)
            PRODUCT_CODE="$2"
            shift 2
            ;;
        --ocr)
            OCR_MODE="$2"
            shift 2
            ;;
        *)
            if [ -z "$DIRECTORY" ]; then
                DIRECTORY="$1"
            fi
            shift
            ;;
    esac
done

# Build the Python command
CMD="python \"$PYTHON_SCRIPT\""

if [ -n "$DIRECTORY" ]; then
    CMD="$CMD --directory \"$DIRECTORY\""
fi

if [ -n "$YEAR" ]; then
    CMD="$CMD --year $YEAR"
fi

if [ -n "$PRODUCT_CODE" ]; then
    CMD="$CMD --product-code $PRODUCT_CODE"
fi

if [ -n "$OCR_MODE" ]; then
    CMD="$CMD --ocr $OCR_MODE"
fi

echo "Running: $CMD"
echo "=========================================="
echo ""

# Execute the command
eval $CMD
