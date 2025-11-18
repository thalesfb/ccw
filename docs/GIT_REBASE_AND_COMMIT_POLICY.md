## Git Flow, Rebase, and Commit Message Policy

This document describes the recommended developer workflow and how we keep a clean commit history.

1. Best practice for feature branches:
   - Update local main: `git fetch origin && git checkout main && git pull --rebase origin main`
   - Create branch from main: `git checkout -b feature/something`

2. Keep your branch up-to-date using rebase:
   - Regularly run: `git fetch origin && git rebase origin/main` to minimize merge conflicts.
   - Resolve conflicts during a rebase, e.g., `git add <file>` and `git rebase --continue`.

3. Before creating a pull request:
   - Rebase and squash your commits if appropriate: `git rebase -i origin/main`.
   - Clean and standardize commit messages using Conventional Commits.

4. Pull Requests merging:
   - Prefer 'Rebase and merge' or 'Squash and merge' on GitHub.
   - Avoid merge commits (`git merge`) on main unless necessary.

5. Enforcing commit message standard:
   - We provide a `scripts/commit-msg` hook to validate message format locally. Install with `scripts/setup-git-hooks.sh`.
   - CI may run checks to reject PRs with invalid commit messages.

6. Rewriting existing commit messages (optional & destructive):
   - Maintainers may rewrite history to normalize commit messages or remove sensitive/large files using `git-filter-repo` or the BFG, as described in `docs/REMOVE_LARGE_FILE.md`.
   - This will require force push and communication with collaborators.
