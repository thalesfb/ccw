#!/usr/bin/env python3
import re
import sys

TYPES = [
    'feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore', 'build', 'ci', 'revert'
]

GITMOJI_TO_TYPE = {
    ':sparkles:': 'feat',
    '✨': 'feat',
    ':bug:': 'fix',
    '🐛': 'fix',
    ':books:': 'docs',
    '📚': 'docs',
    ':lipstick:': 'style',
    '💄': 'style',
    ':recycle:': 'refactor',
    '♻️': 'refactor',
    ':zap:': 'perf',
    '⚡': 'perf',
    ':test_tube:': 'test',
    '🧪': 'test',
    ':wrench:': 'chore',
    '🔧': 'chore',
    ':fire:': 'chore',
    '🔥': 'chore',
    ':wastebasket:': 'chore',
    '🗑️': 'chore',
}

TYPE_RE = '|'.join(TYPES)

def normalize_header(header):
    # strip whitespace
    header = header.strip()
    if not header:
        return header
    # remove leading gitmoji shortcodes and emoji characters by scanning mapping keys
    for emo in GITMOJI_TO_TYPE.keys():
        if header.startswith(emo + ' ') or header.startswith(emo):
            header = header[len(emo):].strip()
            break
    # fallback to regex removal of any shortcodes or emoji ranges
    header = re.sub(r'^(?:(:[a-zA-Z0-9_+-]+:|[\U0001F300-\U0001FAFF\u2600-\u27BF])+\s*)+', '', header)
    # attempt direct emoji to type mapping
    for emo, t in GITMOJI_TO_TYPE.items():
        if header.startswith(emo + ' ') or header.startswith(emo):
            # strip emoji and whitespace
            header = header[len(emo):].strip()
            # ensure header starts with t:
            if not re.match(r'(?i)(' + TYPE_RE + r')(\(|:|\s)', header):
                header = f"{t}: {header}"
            break
    # find existing conventional type
    m = re.match(r'(?i)(' + TYPE_RE + r')(?:\(([^)]+)\))?\s*[:\s]+(.+)', header)
    if m:
        t = m.group(1).lower()
        scope = m.group(2)
        subject = m.group(3).strip()
        return f"{t}{f'({scope})' if scope else ''}: {subject}"
    # fallback: try to find a type word in header and convert
    m2 = re.search(r'(?i)(' + TYPE_RE + r')\b', header)
    if m2:
        t = m2.group(1).lower()
        # strip t from header
        subject = re.sub(re.escape(m2.group(0)), '', header, count=1).strip(': -')
        return f"{t}: {subject}"
    # if header starts with 'remove' or similar, map to 'chore'
    if re.match(r'(?i)remove\b[:\s].*', header):
        subject = re.sub(r'(?i)^remove\b[:\s]*', '', header).strip()
        return f"chore: {subject}"
    # no mapping found, return header unchanged
    return header

if __name__ == '__main__':
    # read header from stdin or arg
    if len(sys.argv) > 1:
        header = ' '.join(sys.argv[1:]).strip()
    else:
        header = sys.stdin.read().strip() or ''
    print(normalize_header(header))
