> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-010.md`. Statuses and counts in this file are not authoritative.

# Draft position 10: Logging pipelines, CloudEvents normalization and streaming lag

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Guide log, event and stream routing with Connector Hub, normalize CloudEvents payloads and avoid data loss through checkpointing.

## Scope

- log classes and Connector Hub matrix
- CloudEvents field mapping and de-duplication
- offset and checkpoint rules
- IAM policy shape with placeholders

## Non-goals

- live connector behavior
- log parsing (position 3)

## Source anchors

- PLAN.md §3 item 5 (6628620, 7bcd39f)
- skills/oci-logging-pipelines/SKILL.md (78 lines); references/pipelines-patterns.md (140 lines)
- examples/cloudevents/{created,legacy}.json; catalog services logging, events, service-connector-hub, streaming
- tests/test_skills_frontmatter.py::test_deepened_skills_content_and_concepts (keyword presence)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 10.1 | The skill and reference contain Connector Hub, CloudEvents, Streaming, checkpoint and dynamic-group, and the headings 'Connector Hub Routing Matrix', 'CloudEvents Normalization', 'Streaming Lag and Checkpointing' and the term UnconsumedMessages. | LS | evidenced | keyword-presence assertions only |
| 10.2 | Normalization maps specversion, type, source, id, time and data, folds legacy eventType/cloudEventsVersion into them and de-duplicates on id. | DOC | partial | documented; the two example payloads are read by no behavior test (only package-data inclusion) |
| 10.3 | The lag alert threshold is defined. | DOC | not_evidenced | PLAN says 'alert when lag exceeds N minutes' without defining N |
| 10.4 | IAM examples use placeholders and no OCIDs. | LS | evidenced | redaction gate |
| 10.5 | A connector delivers records end to end in a live tenancy. | OCI | not_evidenced | out of v1 scope |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: related tests pass.

## Unresolved tests and prerequisites

- 10.3 needs a stated default or an explicit 'operator-chosen' rule.
- 10.2 has no executable check.

## Dependencies

- 1, 2
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills/, references/ and examples/ unchanged between revisions.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Define N or mark it operator-chosen; propose a fixture-based CloudEvents example check as a test-to-add.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Replace keyword-presence evidence with behavior-level criteria where an executable check is feasible offline.
