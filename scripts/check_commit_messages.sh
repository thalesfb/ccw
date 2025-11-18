#!/usr/bin/env bash
set -euo pipefail

echo "Checking commit messages for Conventional Commit compliance..."
PATTERN='^(feat|fix|docs|style|refactor|perf|test|chore|build|ci|revert)(\([a-zA-Z0-9_\-/.]+\))?:\s.+'
git log --pretty=format:'%h %s' --no-merges --all | while IFS= read -r line; do
  hash=$(echo "$line" | awk '{print $1}')
  msg=$(echo "$line" | cut -d' ' -f2-)
  if ! echo "$msg" | grep -Eq "$PATTERN"; then
    echo "$hash: $msg"
  fi
done
