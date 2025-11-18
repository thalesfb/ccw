#!/usr/bin/env bash
set -euo pipefail

FILE_TO_REMOVE="research/systematic_review.sqlite"

echo "Backup current branch refs to backup branch:"
git branch backup-main-$(date +%Y%m%d%H%M%S)

echo "Rewriting history to remove $FILE_TO_REMOVE..."
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch $FILE_TO_REMOVE" --prune-empty --tag-name-filter cat -- --all

echo "Cleaning up refs/original and performing garbage collection..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "To publish rewritten history, run:"
echo "  git push --force origin main"
echo "NOTE: This is a destructive action that affects collaborators."

exit 0
