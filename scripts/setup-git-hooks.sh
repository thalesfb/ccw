#!/usr/bin/env bash
set -euo pipefail
HOOKS_DIR=".githooks"
mkdir -p "$HOOKS_DIR"
cp scripts/commit-msg "$HOOKS_DIR/commit-msg"
chmod +x "$HOOKS_DIR/commit-msg"
git config core.hooksPath "$HOOKS_DIR"
echo "Installed commit-msg hook at $HOOKS_DIR/commit-msg and configured git to use it"
echo "If you want to revert: git config --unset core.hooksPath; rm -rf $HOOKS_DIR"
