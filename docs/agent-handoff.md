# OCI Observability Tools canonical agent handoff

Preparation snapshot: 2026-10-09 16:23:28 UTC.
This record describes the preserved author worktree before the gate trigger. Ignored checkpoints
and receipts stay in that worktree and are absent from isolated gate worktrees. During an active
run, the outer executor owns current pipeline status and delivery actions.
Host: **adi2**. Owner: `skills-packaging-r9` (preserved Firstmate worker).
Worktree: `<TASK_WORKTREE>`; its exact absolute binding is the private checkpoint
`worktree` field. Main corr=2d44b702da24b96e approved this split for this handover only.
Branch: `fm/skills-packaging-r9`.
Verified remote: `https://github.com/adibirzu/oci-observability-tools`, default branch `main`.
Original and freshly observed remote source: `662862029babf4acad6352ee5d83f4a79cd0f09b`.
Committed implementation / pre-handover source: `179116e2fc9195b745439908613f5a1d9e4238b1`.
The subsequent handover/delivery commit is recorded in the private checkpoint after commit,
so this document does not refer to its own commit hash.

## Recovery and ownership

This is the canonical Skills resume document designated by main corr=95e3fe884c8975a1.
The initial Skills source had no existing handover owner. OCI-DEMO handovers belong to a different
project and were not edited. The source ledgers are `PLAN.md` and `CHANGELOG.md`.
The completed scout report and supervisor completion review remain preserved and read-only in
Firstmate's `data/oci-skills-ready-k8/`; their source/local evidence is not release evidence.

Private checkpoint: `.task-private/skills-packaging-r9.checkpoint.json`.
The local `.task-private` symlink targets `.venv/task-private`; private receipts and dependencies
stay under `.venv/`, outside the distributable artifacts and existing public-tree scan scope.
Read this checkpoint and inbox, then reconcile fresh Git and remote state before resuming.

At handover preparation, committed implementation paths are clean. The exact owned untracked
public path is `docs/agent-handoff.md`; there are no owned tracked dirty paths.
Ignored local artifact roots are `.task-private`, `.venv/`, `build/`, and
`oci_observability_tools.egg-info/`. Nothing unrelated was dirty at launch. The checkpoint records
exact current owned paths before every planned stop and the eventual delivery identity.

## Completed implementation scope

- Setuptools explicitly packages `oci_observability_tools` and its executable `scripts` subpackage.
  Catalogs/schemas, all eleven skill bodies, linked references, ChatGPT knowledge, examples,
  installer, adapter manifests/context, README and license/NOTICE assets are included.
  Source scripts remain runnable. Wheel content checks reject private/test/cache inclusion.
- Wheel, sdist and editable-artifact regressions exercise actual installed catalog/OCL/redaction
  helpers and generator freshness outside the checkout. Full-dependency wheel and actual
  `pip install -e ...[dev]` installations were separately verified in fresh isolated venvs.
- ChatGPT output now contains all eleven existing bodies, including `oci-apm-tracing` and
  `oci-monitoring-mql`. Source/output name bijection, complete emitted bodies and linked references,
  deterministic regeneration, unregistered-source failure and obsolete-bundle freshness are tested.
- The observed 34 configured Ruff findings are corrected without suppressing rules or changing
  the 100-column limit. Full offline checks include shell lint and generated freshness in CI.
- PLAN/CHANGELOG counts and manifest/package distribution pointers match the verified remote.
  Declared version `0.1.0` is retained as metadata, with published-release/live-smoke claims pending.
- Project memory points to the authoritative package/verification files; the required maintenance
  section was added with `fm-ensure-agents-md.sh`, and Gemini context regenerated.

No service feature, provider change, additional worker, shared project-harness installation,
AGY runtime, source-copy recovery, merge, tag or release was performed.
Worker ancestry and isolated primary/reviewer/fixer configuration were verified as
`gpt-6.1-sol` with `xhigh`; independent pipeline review has not run yet.

## Commands, outcomes and evidence classes

All commands below are from this worktree unless noted. Tool dependencies and temporary files are
local to `.venv/`. No OCI clients or credentials are used.

| Command / receipt | Observed outcome | Evidence class |
|---|---|---|
| Baseline `python -m build --no-isolation` and `pip install --no-deps --no-build-isolation -e .` | Both failed flat-layout discovery at source 6628620; receipts in `.venv/evidence/baseline-*.log` | Reproduced local failure |
| Baseline `.venv/bin/python -m pytest -q` | 58 passed; zero skips | Original source behavior |
| Baseline `.venv/bin/python -m ruff check --no-cache .` | 34 findings: 25 E501, 8 I001, 1 F401 | Original configured lint failure |
| New regression tests before fixes | Failed on discovery, two omitted bodies, uncovered future source and stale extra bundles | Regression failure receipts |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 TMPDIR="$PWD/.venv/tmp" PATH="$PWD/.venv/bin:$PATH" make check` | Exit 0 including this handover: 63 passed, zero skips; Ruff, both freshness checks, shellcheck and redaction pass | Complete offline source gates |
| `TMPDIR="$PWD/.venv/tmp" .venv/bin/python -m build --no-isolation --outdir .venv/evidence/distributions` | Sdist and wheel built | Local artifacts |
| `TMPDIR="$PWD/.venv/tmp" .venv/min-backend/bin/python -m build --no-isolation --outdir .venv/evidence/min-backend-dist` | Sdist and wheel built using setuptools 68.0.0 | Declared minimum backend checked |
| `TMPDIR="$PWD/.venv/tmp" .venv/bin/python .venv/evidence/verify_installed.py` | Exit 0: wheel and actual editable install, declared dependencies and pip check, four helpers, generator checks, negative OCL exit and reversible temporary Codex installation pass | Isolated installed-artifact behavior |
| Temporary Codex installer in both installed environments | Eleven skill links; copied helper works; uninstall restores snapshot | Temporary installer only |
| `git diff --check` and staged redaction before source commit | Exit 0 | Local source safety |

Receipts: `.venv/evidence/handover-offline-gates.log` (final full gates),
`offline-gates.log`, `final-build.log`, `min-backend-build.log`,
`installed-behavior.log` and `installed-behavior.json`.
Installed wheel SHA-256: `2dfbb6de78c2a0b5ea61038438ff4db8a57ecba035fd46430adbc6e8bf134b54`.
Two upstream setuptools warnings remain: legacy license-table deprecation and editable import
precedence guidance. The >=68 backend floor is retained and tested. Local runtime was Linux
Python 3.12.3; Python 3.10 and macOS remain CI evidence to collect, not local pass claims.

## Gate custody and remaining acceptance

Main corr=3ecacac547eb8eb3 authorized reversible administrative gate wiring only after positive
old-gate idleness. The old repository inventory has zero runs, refs and writers, no Git locks,
and a clean primary main. Exact original binding/config, all old-gate file hashes and rollback are
preserved in the private checkpoint. The old bare gate remains unchanged; source branches and
origin were not changed. Only the specifically authorized no-mistakes remote binding was replaced.

Isolated gate home: `~/work/firstmate-homes/oci-observe/.no-mistakes/skills-r9`.
Exact expanded gate URL is in `gate_binding_result.exact_new_url` in the checkpoint;
its gate repository identity is `repos/64f73428a347.git` under that home.
The isolated doctor reports running daemon and Codex runnable; there is no trusted source-repo
agent override. The default shared daemon and personal global configuration were not changed.
Fresh `axi sync --check` returned `legacy_unbound`, `changed: false`, exit 1, because no successful
pipeline push exists yet. Firstmate inbox 006 confirms this is expected before the first pipeline
push; source custody remains with this worker, and no reset/force/sync change was attempted.

At snapshot time: pipeline run **none**, delivery PR **none**, and delivery branch unpushed.
Reconcile current run, PR and delivery identity through the owning worker before resuming.
Inherited exact-source CI [run 37930343836](https://github.com/adibirzu/oci-observability-tools/actions/runs/37930343836)
is failed at original source 6628620. Fresh delivery-head CI and independent review are pending.
Bounded fresh tag/release reads returned zero records; published release remains unverified.
Full-history gitleaks is unverified locally (executable absent); current-tree redaction is separate.
Actual shared-harness installation/load and live loaded-agent answers remain unverified. T16 is
open. Offline asset smoke and temporary installation do not establish that acceptance; AGY is excluded.

Implementation blockers: **none open**. The handover personal-path conflict was resolved by main
corr=2d44b702da24b96e: only a sanitized public reference is retained here; the exact absolute worktree
remains in the private checkpoint. No personal-path rule, allowlist exception or review was changed.
Independent pipeline gates and fresh delivery-head CI remain incomplete delivery scope.

## Exact next safe action

Before Firstmate's gate trigger, the preserved author worktree must reconcile the exact delivery
commit and clean public working-tree status with `.task-private/skills-packaging-r9.checkpoint.json`,
then stop committed-ready for the native `$no-mistakes` trigger. The full finalized accepted intent
is preserved privately as
`.task-private/accepted-intent.txt`, with its SHA-256 and original supervisor source in the checkpoint.
Do not start the pipeline or push before that trigger.

Once triggered, the owning worker uses the supervisor-prepared isolated `NM_HOME` for every
no-mistakes command. Phase agents return only their assigned result to the outer executor.
Read fresh AXI home/status and current version's `axi run --help`; preserve the full accepted task
intent and later rulings, including this canonical handover requirement. Independent pipeline
reviewers own all fixes during the active run. Respond to mechanical gates using AXI; escalate
ask-user findings only through a keyed Firstmate status and stop. Never use `--yes`, skip required
review/tests, merge, tag, release, restart a daemon, or install into actual shared harness roots.
Only gated branch push/PR is authorized. Delivery claims require exact pipeline-head CI green;
stop at the CI-ready result and hand the PR to Firstmate without waiting for merge.
