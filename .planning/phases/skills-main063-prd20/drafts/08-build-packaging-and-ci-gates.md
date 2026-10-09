> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-008.md`. Statuses and counts in this file are not authoritative.

# Draft position 08: Build, packaging and CI evidence gates

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Define what 'green' means for source, built artifacts and CI so version text is never mistaken for acceptance.

## Scope

- make check composition
- wheel, sdist and editable contents
- CI matrix
- tool version policy

## Non-goals

- merge and release actions (position 20)
- full-history scanning (position 5)

## Source anchors

- PLAN.md §7 CI block, §9 T14, §10 item 5 (6628620, 7bcd39f)
- Makefile; pyproject.toml (setuptools>=68, Python>=3.10, four console scripts); MANIFEST.in; .github/workflows/ci.yml
- tests/test_packaging.py (2 test functions, 3 cases); CHANGELOG.md evidence boundaries; docs/agent-handoff.md (7bcd39f only)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 8.1 | ruff, both generator freshness checks, shellcheck, the redaction check and pytest all pass. | LS | evidenced | 7bcd39f scratch: ruff clean, both --check rc 0, redaction rc 0, 63 passed; shellcheck is a Linux CI step. 6628620 scratch: ruff reports 34 errors |
| 8.2 | Wheel, sdist and editable installs contain helpers, catalogs, skills, references, knowledge, examples, manifests and installer, exclude private/test/cache files, and run outside the source tree. | LS | evidenced | test_packaging.py: 3 cases pass in scratch (requires build, setuptools, wheel) |
| 8.3 | The ubuntu/macos x Python 3.10/3.12 matrix is green on the exact head. | CI | evidenced | runs 37969214474 (pull_request) and 37969210915 (push) at 7bcd39f: all four test jobs success. Main 6628620 push run 37930343836 failed; run 37963585765 at 6229bc9 failed (gitleaks credential input) |
| 8.4 | Lint and test tool versions are pinned. | LS | not_evidenced | pyproject uses ruff>=0.6 and pytest>=7; this lane used ruff 0.17.0 |
| 8.5 | The change reaches the default branch and CI is green on the merge head. | CI | not_evidenced | PR #1 open, mergeable_state clean; merge is not authorized in this lane |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Provider reads (read-only API): PR #1 head 7bcd39f, base 6628620, state open; gh-axi reports 10 checks passed, 0 failed.
- Scratch pytest at 7bcd39f emitted 2 setuptools deprecation warnings.

## Unresolved tests and prerequisites

- 8.5 depends on the supervisor-directed merge.
- 8.4 pin decision (source-owner call).
- The owner handover notes a separate Node 20 action warning; it is untriaged here.

## Dependencies

- 5, 6
- downstream: 20

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills-packaging-r9 (open PR #1, head 7bcd39f) for paths that branch changed.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Bind this PRD's evidence table to 7bcd39f with the receipts above; request the pin decision.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Split 'CI green' into three claims: offline suite, provider matrix, merge-head result.
- State that a declared version 0.1.0 is metadata, not a release (CHANGELOG already says so).
