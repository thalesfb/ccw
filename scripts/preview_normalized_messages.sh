#!/usr/bin/env bash
set -euo pipefail

echo "Previewing normalized commit messages (no rewrite)."
echo "Showing non-conforming commit headers and their normalized version (up to 200)."

git log --pretty=format:'%h %s' --no-merges -n 200 | while IFS= read -r line; do
  hash=$(echo "$line" | awk '{print $1}')
  header=$(echo "$line" | cut -d' ' -f2-)
  normalized=$(echo "$header" | python3 scripts/message_normalize.py)
  if [ "$header" != "$normalized" ]; then
    printf "%s\n  OLD: %s\n  NEW: %s\n\n" "$hash" "$header" "$normalized"
  fi
done
