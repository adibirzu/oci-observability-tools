> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-018.md`. Statuses and counts in this file are not authoritative.

# Draft position 18: Sigma logsource coverage and unmapped-source policy

Status: AUTHOR DRAFT (New source-backed gap draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

State which Sigma logsources are supported, map the network and container sources the pack already uses, and decide whether shipped examples may rely on placeholders.

## Scope

- logsource mapping table
- treatment of unmapped sources
- example rules and golden outputs

## Non-goals

- expanding the Sigma condition grammar
- tenant-specific Log Source names

## Source anchors

- catalog/sigma_field_map.json maps 4 logsources (windows/security, windows/sysmon, linux/auth, oci/audit)
- examples/sigma/dns.yml (network/dns) and network.yml (network/connection) convert with '<LOG_SOURCE>' and an unmapped warning (reproduced)
- references/ocl-cookbook.md already queries 'VCN Flow Logs' and 'Kubernetes Container Logs' sources

## Why this is a new PRD

The field-map specification defines the mapping format, not the list of supported sources or the policy for unmapped sources.

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 18.1 | Every shipped example rule converts with zero 'unmapped logsource' warnings, except one explicitly named negative fixture. | LS | proposed | 2 of 6 shipped examples warn today |
| 18.2 | Each added mapping cites the official Log Analytics source name from a registered documentation page. | ON | proposed | exact Log Source names are unverified offline |
| 18.3 | Golden outputs are regenerated deterministically and remain lint-clean. | LS | proposed | extends test_examples_are_deterministic_and_lint_clean |
| 18.4 | references/sigma-field-map.md states the supported logsource list and the unmapped behavior. | DOC | proposed | the reference is generated or hand-kept; confirm in review |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Reproduced conversions of dns.yml and network.yml at 7bcd39f.

## Unresolved tests and prerequisites

- Authoritative source names (online docs check).
- Owner decision: are dns/network examples intended negatives?

## Dependencies

- 3, 4, 16
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: catalog and examples unchanged between revisions; code/test changes need a lease.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Ask the source owner whether the two unmapped examples are intentional; draft the mapping table from documentation.
