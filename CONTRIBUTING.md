# Contributing

Use Python 3.10 or newer. Create a virtual environment, install the development dependencies, and run `make check` before opening a pull request. Keep helpers offline and examples synthetic.

Every skill must retain valid YAML frontmatter, the required section order, and fewer than 500 lines. Add official documentation links to the catalog before citing them.

## Leak response

If sensitive data enters a commit, stop and do not push a follow-up "fix" commit. Remove it from history with `git filter-repo --replace-text`, rerun the full redaction and secret scans, and only then push the rewritten history.

By contributing, you agree that your contribution is licensed under Apache-2.0.
