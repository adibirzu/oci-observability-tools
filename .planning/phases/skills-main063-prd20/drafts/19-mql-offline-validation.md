> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-019.md`. Statuses and counts in this file are not authoritative.

# Draft position 19: MQL offline validation and cookbook coverage

Status: AUTHOR DRAFT (New source-backed gap draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Give MQL the same offline example-hygiene guarantee OCL already has, and complete the promised cookbook.

## Scope

- grammar check for metric[interval]{dimensions}.grouping().statistic()
- fence-tag convention for MQL blocks
- JSON output shape aligned with the OCL linter
- good and bad fixtures

## Non-goals

- executing queries
- validating metric names against a live namespace

## Source anchors

- Four helpers exist (catalog_query, ocl_lint, sigma_to_ocl, redaction_check); none validates MQL
- references/mql-cookbook.md: 2 queries in text fences; skills/oci-monitoring-mql and references/mql-syntax.md contain MQL examples
- PLAN.md §3 item 4 states the grammar; tests contain no MQL syntax assertion

## Why this is a new PRD

PLAN lists four helpers. MQL validation is neither required nor excluded, while MQL examples ship in two skills and two references.

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 19.1 | A helper reports errors for malformed interval, unbalanced braces or parentheses and unsupported statistic names, exiting non-zero on any error. | LS | proposed | no MQL helper exists |
| 19.2 | Every MQL block in skills/ and references/ (tagged mql) lints clean; the two cookbook blocks are retagged. | LS | proposed | cookbook blocks use text fences today |
| 19.3 | Fixtures cover at least one failing and one passing case per rule. | LS | proposed | mirrors OCL fixtures |
| 19.4 | Statistic and function names come from the registered MQL reference page and are cited. | ON | proposed | grammar details must be verified against the page |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Reproduced: tests directory has no MQL assertions beyond frontmatter and link checks.

## Unresolved tests and prerequisites

- Authoritative grammar from the MQL reference page.
- Owner acceptance of a fifth helper and its CLI name.

## Dependencies

- 1, 11
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: scripts/tests on PR-branch custody; code lease required.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Extract the grammar from the registered MQL page into the PRD before proposing rule ids.
