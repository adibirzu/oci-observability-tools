## Summary

Describe the user-visible change and its offline behavior.

## Checklist

- [ ] `python scripts/redaction_check.py .` reports no findings.
- [ ] New or changed official URLs are registered in `catalog/services.json`.
- [ ] Every `SKILL.md` remains below 500 lines with valid frontmatter.
- [ ] Generated files pass both `--check` commands.
- [ ] `python -m pytest -q` passes without network access.
- [ ] Examples contain placeholders and documentation-only addresses.
