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
- Do not add attribution trailers or co-authorship footers to commits or pull
  requests. Keep publication metadata free of tool branding and signatures.

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
- Review the final merge message explicitly. Squashing commits with different
  authors can introduce attribution footers even when the PR body has none.
- CI validates compiled artifacts but must not create commits on contributor
  branches. Rebuild, inspect and commit an outdated canonical PDF before merge.

## Keep scientific statements synchronized

The TCC manuscript owns the scientific narrative; versioned evidence artifacts
support its numerical and documentary claims. A change to either requires
reviewing every affected README, page, slide, storyboard, parallel export, and
image in the same pull request. Historical snapshots must remain explicitly dated.

Run `python scripts/sync_project_docs.py --write` for generated blocks. Review
manual summaries and images before `--record-review`, then run `--check` and
the relevant tests. The assisted review binding is not scientific approval.
See [the synchronization contract](docs/tcc/DOCUMENTATION_SYNC.md) for sources,
consumers, limitations, and the distinction between reviewed and published work.
