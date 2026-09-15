# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 004 — SCAD repository execution model

**Active.**

The migration aligns current SCAD projects and libraries on one understandable production lifecycle:

- Moon as repository-level orchestration and affected/preflight layer;
- SCons retained as the qualified fine-grained SCAD target engine;
- Build and Verify remain logically independent;
- README-only or otherwise unaffected changes start no SCAD container;
- affected normal CI uses one immutable SCAD Docker execution environment;
- preflight, conditional Docker production, validation and publication should share one host orchestrator job;
- publication remains outside the SCAD container process and happens after that process exits.

Step 1 is complete: `tool.git-project` provides the released generic Moon affected preflight. Aggregate/upstream affected propagation discovered during Step 3 qualification was corrected generically and released as v0.2.6.

Step 2 is complete: `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency and requalified Build/Verify independence on exact main `082b0cecb47ba082899214751080adc54556e94c`.

Step 3 is complete: `tool.scad-project v0.13.0` provides the first reusable production workflow. Release source is exact main `da57820fdadd7d203091b6818984991f1548408f`; release run `34938168129` and released-tag Test run `34938179069` passed.

Step 4 is complete: `template.scad-project` PR #29 consumed released v0.13.0 and merged as exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`. Final-head proofs retained README-only no-container, Verify-only impact without Build/Docs, and Build-side impact without Verify.

Step 5 is **active but paused for a shared tooling correction** in `lib.scad.clamps` PR #7. Candidate `bb071329e1d6c764d09f87ecd2cc78d42ac73679` is functionally green: one SCAD container, library-specific docs/verification, current aggregate materialization and host publication; isolated proofs retain README-only, docs-only and Verify-only affected semantics.

The Step-5 performance stop condition has now been fully evaluated in completed experiment #53. The decision is:

- keep the immutable Docker SCAD runtime;
- reject cached-host OpenSCAD as the production runtime;
- replace the released multi-job lifecycle with **one host orchestrator job** that runs Moon preflight, conditionally executes exactly one `docker run`, validates/stages output after the container exits, and publishes from the same host job.

Repeated exact-candidate lifecycle measurements:

- current released topology: about **64–65 s** relevant feedback;
- selected single-host topology: **41.024 s** and **45.169 s** measured relevant lifecycle;
- README-only controls: **4.369 s** and **4.819 s**, both with zero container starts;
- old parallel Build/Verify baseline: about 37 s, but with two heavy containers.

The next valid cross-project work is therefore not in `lib.scad.clamps` itself:

1. **Next — `tool.git-project`:** factor the existing generated-output publication safety contract into a reusable same-job action/script; keep the existing reusable publication workflow as a thin wrapper; qualify and release the capability.
2. **Then — `tool.scad-project`:** consume the released publisher primitive and release the one-host-job SCAD lifecycle with conditional Docker execution, exact-source/materialization checks and conservative missing-base fallback.
3. **Then resume Step 5 — `lib.scad.clamps`:** update PR #7 to the released topology and repeat the retained functional/performance qualification.
4. Step 6 (`lib.scad.hub75`) remains blocked until Step 5 completes.

Tracking issue: #49. Completed performance experiment: #53. See [Migration 004](migrations/004-scad-repository-execution-model/README.md), its [qualification evidence](migrations/004-scad-repository-execution-model/evidence.md), and the retained [Step-5 performance evidence](migrations/004-scad-repository-execution-model/performance-evidence.md).

## Recently completed

### Migration 003 — roll out `tool.scad-project v0.12.0` through SCAD consumers

**Complete.**

The released SCAD tool was qualified through the template, both reusable SCAD libraries, and finally the real HUB75 frame project.

Current qualified versions include:

- `tool.scad-project v0.12.0`;
- `lib.scad.clamps v0.1.2`;
- `lib.scad.hub75 v0.1.3`;
- `2026-009-01.cad.HUB75-display-frame` on tool v0.12.0 + HUB75 library v0.1.3.

The separate physical-verification work in `lib.scad.hub75` is project-local work, not a continuation of this migration.

See [Migration 003](migrations/003-scad-v0.12-rollout/README.md) and its [qualification evidence](migrations/003-scad-v0.12-rollout/evidence.md).

### Migration 002 — check build decisions after a SCAD build

**Complete.**

`tool.scad-project` provides an explicit post-build audit that compares changed paths with dependency evidence already recorded for each SCons target.

See [Migration 002](migrations/002-scad-build-decision-audit/README.md) and its [qualification evidence](migrations/002-scad-build-decision-audit/evidence.md).

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

`tech.scad` and `meta.scad-projects` are private archives.

See [Migration 001](migrations/001-brainboxemb-meta/README.md) for its history and evidence.

## Parked experiment

- **Moon as SCAD target engine** — issue #51. This is explicitly outside Migration 004; SCons remains the target engine during the execution-model migration.

## Other follow-ups

Useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52.

Generic performance/robustness follow-ups discovered while executing Migration 004 remain owner-local and non-blocking unless explicitly promoted by the active migration:

- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency.
