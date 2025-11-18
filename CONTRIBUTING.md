## Contributing

We prefer a clean Git history and standardized commit messages. This repo uses the Conventional Commits style:

- format: `type(scope): subject` (e.g., `feat(cli): add --verbose flag`)
- `type` is one of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`, `revert`.
- Optional `scope` describes the area affected.
- Keep the subject short (50 chars recommended) and in English/Portuguese as appropriate.

Examples:
- `feat(research): add excel export for included papers`
- `fix(db): prevent duplicate insertion`

Commit message body:
- Use the body to explain the *what* and *why* in more detail if needed.
- Use `BREAKING CHANGE: ` prefix in the body/footer when the change is not backwards-compatible.

Workflow policy — prefer rebase instead of merge:
- Fetch latest main: `git fetch origin`
- Update your branch with rebase: `git rebase origin/main`
- If there are conflicts, resolve them and continue: `git add .` then `git rebase --continue`
- Prefer 'Rebase and merge' or 'Squash and merge' on GitHub for pull requests.
