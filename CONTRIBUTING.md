# Contributing

We use Gitmoji with Conventional Commits for commit subjects.

## Commit format

```text
:emoji_code: type(scope): imperative subject
```

- Use one Gitmoji shortcode, such as `:sparkles:`, `:bug:`, or `:books:`;
  do not use a Unicode emoji in the subject.
- Use a Conventional Commit type: `feat`, `fix`, `docs`, `style`, `refactor`,
  `perf`, `test`, `build`, `ci`, `chore`, or `revert`.
- Keep the complete first line at or below 72 characters.
- Write the subject and optional body in English; use an imperative verb.
- Separate an optional body from the subject with a blank line. Keep body lines
  at or below 100 characters and explain why when useful.

Examples:

```text
:sparkles: feat(research): add source-page claim traceability
:bug: fix(tcc): reconcile evidence and claims
:books: docs(contributing): standardize Gitmoji commit guidance
```

## Pull request workflow

- Fetch the latest `main` and rebase the feature branch when appropriate.
- Keep commits focused and reviewable; preserve authorship when rewriting
  history.
- Run the relevant tests and validations before pushing.
- Prefer rebase or squash merging for pull requests.
