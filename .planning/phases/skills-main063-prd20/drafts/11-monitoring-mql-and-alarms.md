> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-011.md`. Statuses and counts in this file are not authoritative.

# Draft position 11: Monitoring: MQL queries, alarms and notification routing

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Teach correct MQL authoring, threshold, split-metric and absence alarms, and alarm-to-notification routing.

## Scope

- MQL grammar statement
- alarm properties (pending duration, severity, repeat, message format)
- custom metric namespace and dimension guidance
- alarm to Notifications routing

## Non-goals

- MQL validation tooling (position 19)
- skill routing (position 17)
- live alarm behavior

## Source anchors

- PLAN.md §3 item 4 (full spec); item 11 at 7bcd39f is pointer-only
- skills/oci-monitoring-alarms/SKILL.md (44 lines); skills/oci-monitoring-mql/SKILL.md (63 lines)
- references/mql-syntax.md (119), references/mql-cookbook.md (13); catalog services monitoring, notifications
- tests/test_skills_frontmatter.py (frontmatter, links, docs, redaction only)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 11.1 | Both skills cite only the registered MON, MQL, ALARM, CUSTMET and NOTIF pages. | LS | evidenced | test_skills_official_docs_urls_registered |
| 11.2 | The documents state the grammar metric[interval]{dimensions}.grouping().statistic() and cover threshold, absence, pending duration, severity, repeat notification and message format. | DOC | partial | present by inspection; no keyword or structure assertion exists for these two skills |
| 11.3 | Every MQL example in skills and references is syntactically valid. | LS | not_evidenced | no MQL validator exists; mql-cookbook.md holds 2 queries in text fences that no test reads |
| 11.4 | A boundary between oci-monitoring-alarms and oci-monitoring-mql is specified. | DOC | partial | both cite the same five pages; one 'Related skills' sentence is the only boundary |
| 11.5 | A configured alarm evaluates and notifies in a live tenancy. | OCI | not_evidenced | out of v1 scope |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: frontmatter, link, docs and redaction tests pass for both skills.

## Unresolved tests and prerequisites

- 11.3 -> position 19.
- 11.4 -> position 17.
- PLAN promised a fuller mql-cookbook; the shipped file is 13 lines.

## Dependencies

- 1, 2
- downstream: 17, 19

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills/ and references/ unchanged between revisions.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Write the missing scope/acceptance spec for oci-monitoring-mql and a boundary statement versus oci-monitoring-alarms.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Define the minimum cookbook content (query count, dimension coverage) that PLAN only names.
