#!/bin/bash

echo "Checking message: $FIRST_LINE"
echo

# Check if message includes ticket id and a description.
if ! grep -q -E '^[FEAT | FIX]-?.{10}.+' "$1"; then
    echo "ERROR: Commit message have to contain word FEAT- or FIX on the first line."
    echo " eg. FEAT-add new feature or FIX-update unit tests"
    echo ""
    echo "Ensure it's meaningful - the length should be at least 11 characters."
    exit 1
fi
