#!/usr/bin/env bash
set -euo pipefail

CREDITS_LINE="# credits: https://github.com/deependujha"
ROOT_DIR="${1:-.}"

find "$ROOT_DIR/src" -type f -name "*.py" -print0 | while IFS= read -r -d '' file; do
    first_line="$(head -n 1 "$file" 2>/dev/null | tr -d '\r')"

    if [[ "$first_line" != "$CREDITS_LINE" ]]; then
        tmp_file="$(mktemp)"
        {
            printf '%s\n' "$CREDITS_LINE\n"
            cat "$file"
        } > "$tmp_file"
        mv "$tmp_file" "$file"
        echo "Updated: $file"
    fi
done
