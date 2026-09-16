# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Active — template, both representative canaries and the first real downstream consumer are complete; downstream rollout and parallel hardening continue.**

Migration 005 replaces the lifecycle-heavy Migration-004 Moon topology with a capability-oriented model. The shared foundations, reference consumer, both intended canary execution modes and the real HUB75 display-frame consumer are now proven on migrated repositories.

Current released foundations:

- `docker.scad-toolchain v0.5.0` — OpenSCAD-focused and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one generic Moon query;
- `tool.scad-project v0.14.3` / `b86b2be325f64847b8d91b7f2596bfd4e4ffb7f2` — inherited SCAD capabilities, configuration/runtime/cache planning, one-runtime normal production and stable optional Moon output handling.

Reference consumer:

- `template.scad-project` Migration implementation merged in PR #37;
- full reference integration run `35020468894` green;
- source-family Moon impact boundaries corrected in PR #39;
- immutable **v0.0.4** released from `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9` with Build, Verification, STL and checksum assets.

Representative canaries:

- **`lib.scad.clamps` — full/dual runtime + direct engine:** PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`; migrated `main` run `35065375255` green; README-only zero-runtime run `35065514152` green with planner setup, caches, runtime pull, Docker materialization, finishing and publication all skipped; immutable **v0.1.4** released.
- **`lib.scad.hub75` — OpenSCAD-focused runtime + SCons:** PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`; migrated `main` run `35065383879` green; README-only zero-runtime run `35065524524` green with the same heavy stages skipped; immutable **v0.1.5** released from `e0432a9533a08a1c0d9e87225c22f3f66b632531`.

First real downstream consumer:

- **`2026-009-01.cad.HUB75-display-frame`:** Migration PR #33 merged as `61da023ff0f6bc353687b55a8158e75ebd70b046`, pinned to `tool.scad-project v0.14.3`, `tool.git-project v0.2.8`, the focused OpenSCAD v0.5.0 runtime and `lib.scad.hub75 v0.1.5`;
- full migration qualification run `35067070855` built 68 Design, 32 Build and 51 Verification targets with zero errors and successful Build/Verification publication;
- final branch run `35069083479` was green and hydrated all three Moon capability outputs from cache;
- post-merge `main` run `35069411142` was green;
- evidence-only PR #34 / run `35069504915` proved the migrated consumer's README-only zero-runtime path with Moon `status=success`, `affected=false`, reason `target-and-upstream-unaffected`, affected task ids `[]`, and planner/cache/runtime/Docker/publication stages all skipped. PR #34 was closed without merge.

The selected model keeps:

- Moon for repository-level change-impact selection and whole-capability result reuse;
- standard SCAD Moon policy in shared `tool.scad-project` configuration, inherited by consumers;
- only real project capabilities such as Design documentation, Presentation renders and Verification in the maintainer-facing graph;
- SCons optional and fine-grained only inside capabilities whose project configuration selects it;
- current-run/publication information outside reusable source-derived task identity;
- one heavy hosted runner as the normal default, while latency **and** total runner/compute use remain separate acceptance criteria.

Source-affected capabilities and publication-safe materialization are not always identical. If documentation and presentation output both belong to one complete Build publication tree, a docs-only change may hydrate an unchanged contributor through Moon so replacing the Build branch cannot delete unchanged files. That hydration remains non-affected work and its cost must be counted separately.

Important measured findings behind the design include:

- old parallel relevant-change baseline: about **37 s** wall-clock with two simultaneous heavy jobs;
- final Migration-004 v0.13.1 topology: about **41–45 s** with one heavy job;
- README-only controls remain able to stop before CAD runtime entirely;
- affected SCAD image acquisition commonly costs about **15–20 s** while a small Moon/CAD graph may take only a few seconds;
- broad generated Python inputs previously destabilised Moon hashes; source-family/stable shared inputs are therefore important;
- clamps proves direct execution without unused SCons transport;
- HUB75 proves the focused OpenSCAD image plus useful normal SCons transport;
- the focused runtime avoids about **121 MB / 27%** of compressed full-image distribution in the measured image pair;
- Build and Verification publishers can overlap on one runner without introducing another hosted VM.

Current rollout state:

1. **template.scad-project** — complete and released as v0.0.4;
2. **lib.scad.clamps** — complete and released as v0.1.4;
3. **lib.scad.hub75** — complete and released as v0.1.5;
4. **2026-009-01.cad.HUB75-display-frame** — first real downstream consumer complete on the released v0.14.3 architecture;
5. **remaining downstream SCAD consumers** — continue owner by owner from the repository map and Step-7 criteria rather than assuming the frame completes the whole downstream rollout.

A parallel hardening track is active as `tool.scad-project#60` / PR #61. It fixes the shallow base-gitlink comparison gap exposed by tool-version upgrade PRs and adds durable producer/materialization/snapshot timing plus direct generated-output navigation to retained raw Moon/producer logs. The work **does not reopen the completed canaries or frame baseline**. Qualification remains owner tests and patch release first, then `template.scad-project` as the first consumer; only after that should existing consumers be considered for a repin.

Tracking issue: #55. Canonical scope: [Migration 005](migrations/005-scad-execution-architecture/README.md). Selected design: [validated target architecture](migrations/005-scad-execution-architecture/05-target-architecture.md). Active order: [implementation plan](migrations/005-scad-execution-architecture/06-implementation-plan.md).

## Recently completed

### Migration 004 — SCAD repository execution model

**Complete.**

Migration 004 qualified the conditional-SCAD execution model through:

- `template.scad-project`;
- `lib.scad.clamps v0.1.3`;
- `lib.scad.hub75 v0.1.4`;
- shared `tool.git-project v0.2.7` and `tool.scad-project v0.13.1`.

It proved README-only zero-container behavior, one-container affected production, Build/Verification independence, conservative execution when comparison context is uncertain, and host-side publication after the SCAD process exits.

Its final performance conclusion is deliberately mixed: it strongly reduced unnecessary heavy work and duplicated compute, but the one-runner relevant clamps path remained slower in wall-clock time than the old two-job parallel baseline. Those open architecture/performance questions moved to Migration 005 rather than being hidden inside a “complete” label.

At Migration-004 completion the real HUB75 frame was deliberately **not** migrated. Migration 005 later moved that consumer only after the replacement architecture had passed the template and both canary modes.

See [Migration 004](migrations/004-scad-repository-execution-model/README.md), [qualification evidence](migrations/004-scad-repository-execution-model/evidence.md), [performance evidence](migrations/004-scad-repository-execution-model/performance-evidence.md) and the retained [reflection](migrations/004-scad-repository-execution-model/reflection.md).

### Migration 003 — roll out `tool.scad-project v0.12.0` through SCAD consumers

**Complete.**

The released SCAD tool was qualified through the template, both SCAD libraries and finally the real HUB75 frame project.

### Migration 002 — check build decisions after a SCAD build

**Complete.**

`tool.scad-project` provides an explicit post-build audit that compares changed paths with dependency evidence already recorded for each SCons target.

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

## Parked experiment

- **Moon as SCAD target engine** — issue #51. This remains separate. Migration 005 keeps SCons as the fine-grained target engine where selected and must not silently turn this parked replacement experiment into an assumption.

## Other follow-ups

Useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52.

Generic performance/robustness follow-ups remain owner-local unless explicitly promoted:

- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency.
