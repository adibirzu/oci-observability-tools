> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-005.md`. Statuses and counts in this file are not authoritative.

# Draft position 05: Public-safety redaction gate and history safety

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Keep every committed artifact free of tenant identifiers, real endpoints, personal paths and secrets, now and across history.

## Scope

- redaction rule set and allowlist policy
- pre-commit and CI gates
- leak-response procedure
- scope of the whole-repository test

## Non-goals

- runtime redaction by assistants (position 7 and AGENTS.md safety rules)

## Source anchors

- PLAN.md §8 items 1-8; §10 items 6 and 10 (6628620, 7bcd39f)
- scripts/redaction_check.py (13 rule ids incl. OCID, IP_ADDRESS, EMAIL, PERSONAL_PATH, SECRET_VALUE, APM_ENDPOINT); .redaction-allow (empty)
- .gitleaks.toml; .pre-commit-config.yaml; CONTRIBUTING.md 'Leak response'; SECURITY.md; ci.yml gitleaks step
- tests/test_redaction.py (4)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 5.1 | redaction_check.py over the tracked tree exits 0. | LS | evidenced | rc 0 on 7bcd39f scratch extract; CI redaction step green on both events at 7bcd39f |
| 5.2 | The leaky fixture triggers every rule, the clean fixture triggers none, and an allowlist entry without a reason is rejected. | LS | evidenced | test_constructed_leaks_trigger_every_rule, test_clean_fixture_is_clean, test_allowlist_requires_reason |
| 5.3 | test_whole_repository_is_public_safe passes in any working copy, not only a pristine clone. | LS | partial | passes in CI clones; reproduced failing here: redaction_check on this worktree exits 1 on an ignored local file (.claude/settings.local.json, PERSONAL_PATH). Scope choice (worktree vs git ls-files) is an open source-owner call |
| 5.4 | A secret scan over the complete commit history reports zero findings. | CI | not_evidenced | the gitleaks CI step ran green at 7bcd39f, but its scan range (event range vs full history) is not established by repo evidence; local gitleaks executable is absent; owner handover records full-history scanning as unverified |
| 5.5 | The pre-commit hooks run the staged redaction check and gitleaks. | DOC | partial | .pre-commit-config.yaml declares both hooks; no test or run exercises them |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: redaction rc 0; pytest 63 passed.
- CI runs 37969214474 (pull_request) and 37969210915 (push) at 7bcd39f: success.

## Unresolved tests and prerequisites

- 5.4 needs a gitleaks run over full history with a receipt (tool installation or a CI mode that scans history).
- 5.3 scope decision.

## Dependencies

- none upstream
- downstream: 8, 20

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: CONTRIBUTING.md and SECURITY.md unchanged; ci.yml/tests on PR-branch custody.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Obtain a full-history secret-scan receipt; ask the source owner to decide the whole-repository test scope (5.3).

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Specify the scan range of the CI gitleaks step explicitly and bind it to a pinned tool version.
- Turn PLAN §8 items 1-8 into numbered, individually testable requirements.
