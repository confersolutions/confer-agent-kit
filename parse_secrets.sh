#!/bin/bash
# Wrapper script to parse secrets from stdin or file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/secrets_parser.py"

if [ "$#" -eq 0 ]; then
    # Read from stdin
    python3 "$PYTHON_SCRIPT"
else
    # Read from file
    python3 "$PYTHON_SCRIPT" "$1"
fi

