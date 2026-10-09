> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-016.md`. Statuses and counts in this file are not authoritative.

# Draft position 16: Catalog documentation link-liveness verification

Status: AUTHOR DRAFT (New source-backed gap draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Replace the stub with a verifiable online check so documentation links are proven live on a date, while the test suite stays offline.

## Scope

- URL set taken from the catalog only
- status and redirect classification
- dated receipt format
- exit codes
- offline unit tests with an injected fetcher

## Non-goals

- running in the default offline gate
- checking page content semantics beyond reachability (an optional later extension)

## Source anchors

- Makefile 'linkcheck' target is an echo stub (6628620, 7bcd39f)
- PLAN.md §9 T15 and §10 item 3 require HTTP 200 for every catalog URL; README states linkcheck is manual and online
- catalog/services.json: 27 doc entries, checkedAt 2026-10-09; tests/conftest.py blocks sockets for the suite

## Why this is a new PRD

Linkcheck is named in PLAN and README, but no document says what the check must do, and the Makefile target is an echo stub.

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 16.1 | make linkcheck requests every one of the catalog's doc URLs and exits non-zero when any returns a non-success final status. | ON | not_evidenced | current target prints a message and exits 0 |
| 16.2 | Only hosts already allowed by the documentation-URL test are requested. | LS | proposed | reuses the allowed-host list |
| 16.3 | The classifier (success, redirect to success, client error, server error, timeout) is covered by offline tests using an injected fetcher; the suite still blocks sockets. | LS | proposed | keeps conftest network block intact |
| 16.4 | A dated receipt records URL count, per-URL final status and the check date, and is referenced from the CHANGELOG evidence section. | ON | proposed | the PLAN's 2026-10-09 curl claim has no receipt |
| 16.5 | The check is not part of make check or the CI offline matrix. | LS | proposed | README/PLAN already define linkcheck as manual |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Reproduced: the Makefile target body is an echo only; no other linkcheck implementation in the tree.

## Unresolved tests and prerequisites

- Network egress to the documentation host from an authorized environment.
- Source-owner decision on whether a scheduled, non-gating CI run is acceptable.

## Dependencies

- 2
- downstream: 9 (example-shape check), 20

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: Makefile and tests are on PR-branch custody; a code lease is required to implement.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Request an implementation lease after owner acceptance; define the receipt format first.
