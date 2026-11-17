> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-015.md`. Statuses and counts in this file are not authoritative.

# Draft position 15: Live loaded-agent acceptance protocol (T16)

Status: AUTHOR DRAFT (New source-backed gap draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Specify how a real loaded-agent answer is obtained, recorded and judged for each supported harness, so the smoke acceptance cannot be satisfied by offline asset checks.

## Scope

- per-harness run procedure
- result record fields
- pass/fail rule
- identity and authorization records

## Non-goals

- running the smoke (needs authorization)
- Antigravity runtime (excluded by the owner)
- OCI tenancy access

## Source anchors

- PLAN.md §9 T16 and §10 item 9 (unchecked at both revisions)
- CHANGELOG.md 'Evidence boundaries' and docs/agent-handoff.md (7bcd39f): T16 is open; AGY excluded
- tests/test_harness_smoke.py is an offline asset check only

## Why this is a new PRD

PLAN T16 names the smoke prompt and pass condition in one sentence. No protocol, record schema or run count exists in any document.

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 15.1 | For each of Claude Code, Codex, Gemini CLI and ChatGPT a record exists with: harness name and version, installation method, exact prompt 'Which OCI service should I use to trace a slow API?', full answer, date, and account/model identity. | RT | not_evidenced | no record exists; this PRD defines the record schema |
| 15.2 | PROPOSED pass rule: the answer routes to APM and cites the APMOTEL page in every one of 3 independent runs per harness (run count is a source-owner choice). | RT | proposed | PLAN states one prompt and the pass condition but no run count |
| 15.3 | Records are free of tenant identifiers, credentials and personal paths (redaction gate passes on the record). | LS | proposed | applies the existing gate |
| 15.4 | Offline asset results and live results are reported in separate sections of the CHANGELOG evidence record. | DOC | proposed | CHANGELOG already separates the two; this criterion keeps it so |
| 15.5 | Any installation into a shared harness root is preceded by recorded owner authorization. | DOC | proposed | handover records that no shared-root installation was authorized so far |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Existing: offline routing and asset test only (test_harness_smoke).

## Unresolved tests and prerequisites

- Authenticated accounts for four harnesses.
- Owner authorization for real installation and for provider runs.
- Run-count threshold (15.2).

## Dependencies

- 2, 6, 7
- downstream: 20

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: new document; no source custody conflict.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Present the record schema and run-count proposal for owner decision; do not execute any harness run.
