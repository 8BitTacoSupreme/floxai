#!/bin/bash

# List of packages to test
packages=(
    "python3"
    "nodejs"
    "git"
    "curl"
    "sqlite"
    "jq"
    "tree"
    "python3Packages.pip"
    "python3Packages.setuptools"
)

echo "Testing packages for Flox availability:"
echo "======================================="

for pkg in "${packages[@]}"; do
    echo -n "Testing $pkg... "
    
    # Try to search for the package
    if flox search "$pkg" --json 2>/dev/null | grep -q "\"name\""; then
        echo "✓ Found"
    else
        # Try alternative names
        base=$(echo $pkg | cut -d. -f1)
        if flox search "$base" --json 2>/dev/null | grep -q "\"name\""; then
            echo "⚠ Found as '$base'"
        else
            echo "✗ Not found"
        fi
    fi
done
