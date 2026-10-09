> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-006.md`. Statuses and counts in this file are not authoritative.

# Draft position 06: Reversible multi-harness installer

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Install the skill bundle into Claude, Codex, Gemini and Antigravity locations and remove exactly what was installed.

## Scope

- --dry-run, --uninstall, --list
- target directories and override variables
- manifest-based reversibility
- exit codes

## Non-goals

- harness runtime loading (position 15)
- Windows shells

## Source anchors

- PLAN.md §5 install.sh contract (6628620, 7bcd39f)
- install.sh (unchanged between 6628620 and 7bcd39f); README install sections; AGENTS.md install line
- tests/test_install_dryrun.py (3 tests)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 6.1 | --dry-run for claude, codex, gemini and antigravity exits 0, prints WOULD copy/link lines and creates no files. | LS | evidenced | test_dry_run_writes_nothing |
| 6.2 | An unknown harness exits 2. | LS | evidenced | test_unknown_harness_exits_two |
| 6.3 | Install then --uninstall into a temporary HOME restores the file-tree snapshot for all four harnesses. | LS | evidenced | test_install_then_uninstall_restores_tree (both bash-gated tests return early when bash is absent) |
| 6.4 | The installer never overwrites a path it did not create; it warns and skips. | LS | not_evidenced | no test seeds a conflicting path |
| 6.5 | The four environment overrides (CLAUDE_SKILLS_DIR, CODEX_SKILLS_DIR, AGY_SKILLS_DIR, GEMINI_EXT_DIR) are honored. | LS | not_evidenced | declared in install.sh; no test sets them |
| 6.6 | shellcheck is clean and the script is bash 3.2 compatible. | CI | partial | shellcheck runs on the Linux CI job (green at 7bcd39f); bash 3.2 compatibility is not demonstrated by any evidence read |
| 6.7 | A real installation into shared harness roots is loaded by the harness. | RT | not_evidenced | only temporary-HOME installation was exercised; AGY runtime excluded by the owner |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: three installer tests pass.
- Note: criteria-lane index at 6628620 stated the round trip was not run; the round trip is in fact exercised by test_install_then_uninstall_restores_tree.

## Unresolved tests and prerequisites

- 6.4, 6.5, 6.6 (bash 3.2) lack tests; 6.7 needs authenticated harnesses and authorization for real installs.

## Dependencies

- 1
- downstream: 15

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: no active writer observed on these paths (main 6628620 and branch 7bcd39f identical).
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Specify 6.4 and 6.5 as tests-to-add; defer 6.7 to position 15.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Separate temporary-HOME reversibility (testable offline) from real-root installation (needs authorization).
