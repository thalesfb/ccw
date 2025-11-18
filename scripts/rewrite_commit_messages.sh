#!/usr/bin/env bash
set -euo pipefail

echo "This script rewrites commit messages using git-filter-repo's message-callback."
echo "It will not run automatically; it only prepares the command."

if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "git-filter-repo is not installed. Install via 'pip install git-filter-repo' and re-run." >&2
  exit 1
fi

BACKUP_BRANCH="backup-main-$(date +%Y%m%d%H%M%S)"
git branch "$BACKUP_BRANCH"
echo "Created backup branch: $BACKUP_BRANCH"

cat > /tmp/message_normalize.py <<'PY'
import re

types = [
    'feat','fix','docs','style','refactor','perf','test','chore','build','ci','revert'
]
type_re = '|'.join(types)

def message_callback(message):
    try:
        text = message.decode('utf-8')
    except Exception:
        return message
    lines = text.split('\n')
    header = lines[0]
    # Remove leading emoji shortcodes like :sparkles:
    header = re.sub(r'^(?:[:][a-zA-Z0-9_+-]+[:]\s*)+', '', header)
    # Remove leading emojis (unicode) - rough: non-ascii at start
    header = re.sub(r'^[^\w]+', '', header)
    # Find conventional type
    m = re.search(r'(?i)(' + type_re + r')(?:\(|:)', header)
    if not m:
        # try to find type followed by space e.g., feat message
        m = re.search(r'(?i)(' + type_re + r')\s+', header)
    if m:
        t = m.group(1).lower()
        # get position after t
        pos = m.end()
        rest = header[pos:]
        rest = re.sub(r'^[:\)\s]+', '', rest)
        # if scope is like feat(scope): ensure parentheses captured
        scope = None
        scope_m = re.match(r'\s*\(([^)]+)\)\s*[:]?\s*(.*)', rest)
        if scope_m:
            scope = scope_m.group(1)
            subject = scope_m.group(2)
        else:
            # subject is rest after optional colon or space
            subject = re.sub(r'^[:\s]+', '', rest)
        if not subject:
            # try find trailing part after ': '
            if ':' in header:
                subject = header.split(':',1)[1].strip()
        new_header = t + (f'({scope})' if scope else '') + ': ' + subject
        lines[0] = new_header
        new_text = '\n'.join(lines)
        return new_text.encode('utf-8')
    # no match, keep as is
    return message
PY

echo "To run the rewrite, use the following command (preview first):"
echo "git filter-repo --message-callback /tmp/message_normalize.py --replace-refs delete-no-add"
echo "Preview (no-op) by running filter-repo on a clone or backup branch."
echo "Be careful: this rewrites history and requires a force push after verification."
