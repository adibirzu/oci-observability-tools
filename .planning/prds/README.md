# Product requirement documents: oci-observability-tools

Authoritative index of the twenty author-draft PRDs in this directory. Drafts only: not reviewed, not accepted, not counted toward any review threshold, and never implementation or provider acceptance.

## Revision binding

- Acceptance baseline: current main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b).
- Alternate receipts: unmerged PR #1 head 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788). Positive results there are labelled with that exact revision and cannot claim current-main acceptance.
- PR #1 is not merged, cherry-picked, rebased or waited for.

## Count reconciliation (computed once from these files)

| Item | Count |
|---|---|
| Standalone PRD documents that existed before this set | 0 |
| PRDs in this set | 20 |
| Promotions of existing specifications | 14 |
| Documented new gaps | 6 |
| Acceptance criteria | 102 |
| Main status counts (evidenced / partial / not evidenced / contradicted / proposed) | 33/16/23/5/25 |
| PR #1 status counts (same order) | 38/16/23/0/25 |
| PRDs counted toward the 10 threshold | 0 |
| PRDs counted toward the 20 threshold | 0 |

Totals are re-derived from the PRD files by a separate verifier before the commit; the phase directory records the check.

## Index

| ID | Title | Type | Set | Criteria | Main (ev/part/none/contra/prop) | PR #1 (same order) | Next task |
|---|---|---|---|---|---|---|---|
| [PRD-001](PRD-001.md) | Skill authoring contract and bundle integrity | promotion | first 10 | 6 | 4/0/0/1/1 | 5/0/0/0/1 | P1; owner: repository owner |
| [PRD-002](PRD-002.md) | Capability catalog and deterministic service routing | promotion | first 10 | 5 | 3/0/2/0/0 | 3/0/2/0/0 | P1; owner: this lane (owned planning paths only) |
| [PRD-003](PRD-003.md) | OCL authoring skill and offline linter with MCP query sanitizer | promotion | first 10 | 5 | 2/2/1/0/0 | 2/2/1/0/0 | P2; owner: repository owner |
| [PRD-004](PRD-004.md) | Sigma-to-OCL detection conversion | promotion | first 10 | 6 | 4/1/1/0/0 | 4/1/1/0/0 | P2; owner: this lane (owned planning paths only) |
| [PRD-005](PRD-005.md) | Public-safety redaction gate and history safety | promotion | first 10 | 5 | 2/2/1/0/0 | 2/2/1/0/0 | P1; owner: repository owner |
| [PRD-006](PRD-006.md) | Reversible multi-harness installer | promotion | first 10 | 7 | 3/1/3/0/0 | 3/1/3/0/0 | P2; owner: repository owner |
| [PRD-007](PRD-007.md) | Cross-harness adapters and generated bundles (Claude, Codex, Gemini/Antigravity, ChatGPT) | promotion | first 10 | 5 | 2/1/1/1/0 | 3/1/1/0/0 | P1; owner: this lane (owned planning paths only) |
| [PRD-008](PRD-008.md) | Build, packaging and CI evidence gates | promotion | first 10 | 5 | 0/0/2/3/0 | 3/0/2/0/0 | P1; owner: repository owner |
| [PRD-009](PRD-009.md) | APM instrumentation and distributed tracing skills | promotion | first 10 | 6 | 2/2/2/0/0 | 2/2/2/0/0 | P1; owner: this lane (owned planning paths only) |
| [PRD-010](PRD-010.md) | Logging pipelines, CloudEvents normalization and streaming lag | promotion | first 10 | 5 | 2/1/2/0/0 | 2/1/2/0/0 | P2; owner: repository owner |
| [PRD-011](PRD-011.md) | Monitoring: MQL queries, alarms and notification routing | promotion | all 20 | 5 | 1/2/2/0/0 | 1/2/2/0/0 | P2; owner: this lane (owned planning paths only) |
| [PRD-012](PRD-012.md) | Database observability with Database Management and Operations Insights | promotion | all 20 | 5 | 2/2/1/0/0 | 2/2/1/0/0 | P3; owner: this lane (owned planning paths only) |
| [PRD-013](PRD-013.md) | Stack Monitoring and Management Agent operations | promotion | all 20 | 5 | 3/1/1/0/0 | 3/1/1/0/0 | P3; owner: repository owner |
| [PRD-014](PRD-014.md) | Observability maturity model L0-L4 | promotion | all 20 | 5 | 3/0/2/0/0 | 3/0/2/0/0 | P3; owner: repository owner |
| [PRD-015](PRD-015.md) | Live loaded-agent acceptance protocol (T16) | new gap | all 20 | 5 | 0/0/1/0/4 | 0/0/1/0/4 | P1; owner: repository owner |
| [PRD-016](PRD-016.md) | Catalog documentation link-liveness verification | new gap | all 20 | 5 | 0/0/1/0/4 | 0/0/1/0/4 | P1; owner: repository owner |
| [PRD-017](PRD-017.md) | Skill routing completeness, overlap boundaries and routing corpus | new gap | all 20 | 4 | 0/0/0/0/4 | 0/0/0/0/4 | P1; owner: repository owner |
| [PRD-018](PRD-018.md) | Sigma logsource coverage and unmapped-source policy | new gap | all 20 | 4 | 0/0/0/0/4 | 0/0/0/0/4 | P2; owner: repository owner |
| [PRD-019](PRD-019.md) | MQL offline validation and cookbook coverage | new gap | all 20 | 4 | 0/0/0/0/4 | 0/0/0/0/4 | P2; owner: this lane (owned planning paths only) after owner acceptance |
| [PRD-020](PRD-020.md) | Release readiness and provenance for v0.1.0 | new gap | all 20 | 5 | 0/1/0/0/4 | 0/1/0/0/4 | P3; owner: repository owner |

Review sets: the first 10 are PRD-001 to PRD-010. The all-20 set is PRD-001 to PRD-020. Reviewers must differ from the author. This lane creates no agents.

## Evidence classes

- **LS**: local static/offline check: unit test, lint, schema, generator freshness or a deterministic local computation. No network, provider or harness.
- **CI**: remote provider CI result bound to an exact head SHA. Runs the same offline suite on provider runners; not product runtime acceptance.
- **DOC**: documentary evidence by inspection (text present or absent); no machine check.
- **ON**: online verification of public Oracle documentation (reachability or content). Not implemented today.
- **RT**: authenticated harness runtime acceptance: a real Claude Code, Codex, Gemini CLI or ChatGPT session loading the assets. Needs accounts and owner authorization.
- **OCI**: authenticated OCI tenancy or service acceptance. Excluded from v1 scope by PLAN section 1 non-goals; no PRD claims it.

## Status values

- **evidenced**: evidence of the stated class exists at that revision and was observed or reproduced.
- **partial**: some, but not all, of the criterion is evidenced at that revision.
- **not_evidenced**: the criterion belongs to an existing specification but no evidence exists at that revision.
- **contradicted**: observed evidence at that revision shows the criterion is not satisfied.
- **proposed**: a new contract choice proposed by this set; it is not part of any existing specification and needs an owner decision.

## Priorities

- **P1**: needed before the PRD can be accepted or its decision can be taken
- **P2**: improves precision or testability
- **P3**: low priority or dependent on other PRDs

## Rules for this set

- Local protocol and static results (classes LS, DOC) are kept apart from provider CI (CI), online documentation (ON), authenticated harness runtime (RT) and OCI tenancy (OCI) acceptance.
- Criteria prefixed PROPOSAL are new contract choices with a named decision owner and next task. They are not requirements until the owner accepts them.
- No scanner, test or contract is weakened to improve a count. No criterion is marked satisfied because a document or a version string says so.
- Source documents (PLAN.md, AGENTS.md, the handover, code, tests and configuration) are read-only for this set.
