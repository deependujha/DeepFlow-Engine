#!/usr/bin/env bash
set -euo pipefail

PYPROJECT_FILE="pyproject.toml"

if [[ ! -f "$PYPROJECT_FILE" ]]; then
    echo "Error: pyproject.toml not found"
    exit 1
fi

# Extract version (e.g., 0.1.5)
CURRENT_VERSION=$(grep '^version = ' "$PYPROJECT_FILE" | sed -E 's/version = "([^"]+)"/\1/')

IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

if [[ -z "$MAJOR" || -z "$MINOR" || -z "$PATCH" ]]; then
    echo "Error: invalid version format"
    exit 1
fi

# Bump patch
PATCH=$((PATCH + 1))

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
BRANCH_NAME="bump/v${NEW_VERSION}"

echo "Current version: $CURRENT_VERSION"
echo "New version: $NEW_VERSION"
echo "Branch: $BRANCH_NAME"

# Create branch
git switch -c "$BRANCH_NAME"

# Update version in pyproject.toml
sed -i.bak -E "s/^version = \".*\"/version = \"${NEW_VERSION}\"/" "$PYPROJECT_FILE"
rm "${PYPROJECT_FILE}.bak"

# Commit changes
git add "$PYPROJECT_FILE"
git commit -m "chore: bump version to v${NEW_VERSION}"

# Push branch
git push origin "$BRANCH_NAME"

echo "✅ Done. Branch '$BRANCH_NAME' pushed."
