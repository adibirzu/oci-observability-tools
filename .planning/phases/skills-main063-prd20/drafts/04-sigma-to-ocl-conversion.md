> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-004.md`. Statuses and counts in this file are not authoritative.

# Draft position 04: Sigma-to-OCL detection conversion

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Convert supported Sigma rules into deterministic, lint-clean OCL with explicit warnings for anything unmapped.

## Scope

- modifier mapping
- supported condition grammar
- quoting and escaping
- aggregation tail and requires_aggregation
- output key order and determinism

## Non-goals

- scheduled-search execution
- logsource coverage expansion (position 18)

## Source anchors

- PLAN.md §3 item 8; §4 sigma_field_map; §5 sigma_to_ocl (6628620, 7bcd39f)
- catalog/sigma_field_map.json (13 fields, 4 logsources) and schema; references/sigma-field-map.md
- skills/oci-detections-sigma/SKILL.md (69 lines); examples/sigma/*.yml (6 rules)
- scripts/sigma_to_ocl.py; tests/test_sigma_to_ocl.py (5); tests/fixtures/sigma

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 4.1 | Output is byte-identical across two runs and passes ocl_lint with zero errors for all six shipped example rules. | LS | evidenced | test_examples_are_deterministic_and_lint_clean |
| 4.2 | Modifier mapping matches the PLAN table (equality, contains, startswith, endswith, re, contains\|all, list with =, list with like). | LS | evidenced | test_typing_modifiers_lists_and_all with tests/fixtures/sigma/expected/modifiers.json |
| 4.3 | Supported conditions are exactly: X, a and b, a or b, a and not b, 1 of sel*, all of them; anything else raises UnsupportedSigma. | LS | partial | unsupported-condition and 'and not' cases tested; the 'a or b' and 'all of them' branches are not separately enumerated |
| 4.4 | 'O'Brien' becomes 'O''Brien'; an unknown field yields a warning; an unmapped logsource yields '<LOG_SOURCE>' plus a warning. | LS | evidenced | test_and_not_unknown_field_quote_and_unmapped_logsource (uses a synthetic custom/app logsource) |
| 4.5 | count() with timeframe appends a stats tail, sets requires_aggregation=true and warns about the schedule interval. | LS | evidenced | test_aggregation_and_timeframe |
| 4.6 | A converted rule detects in a live Log Analytics scheduled search. | OCI | not_evidenced | out of v1 scope; no tenancy access |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: all Sigma tests pass.
- Reproduced: examples/sigma/dns.yml and network.yml convert with '<LOG_SOURCE>' and an 'unmapped logsource' warning.

## Unresolved tests and prerequisites

- 4.3 enumeration; 4.6 deferred.
- Whether the two unmapped shipped examples are intentional negatives is undecided (see position 18).

## Dependencies

- 3 (lint)
- downstream: 18

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: PLAN.md/scripts/tests on PR-branch custody; catalog/, examples/ and skills/ unchanged.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Write the normative supported-Sigma subset and version it; list the 'or' and 'all of them' cases to assert.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- State the supported Sigma subset once; today it is split between PLAN §5 and the skill.
- Record the field map as a convention requiring verification against each tenant's Log Source definitions (already stated in the reference; promote it to a requirement).
