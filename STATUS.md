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
- preflight, conditional Docker production, validation and publication share one host orchestrator job;
- publication remains outside the SCAD container process and happens after that process exits.

Step 1 is complete: `tool.git-project` provides the released generic Moon affected preflight. Aggregate/upstream affected propagation discovered during Step 3 qualification was corrected generically and released as v0.2.6.

Step 2 is complete: `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency and requalified Build/Verify independence on exact main `082b0cecb47ba082899214751080adc54556e94c`.

Step 3 is complete: `tool.scad-project v0.13.0` provided the first reusable production workflow. Release source was exact main `da57820fdadd7d203091b6818984991f1548408f`.

Step 4 is complete: `template.scad-project` PR #29 consumed released v0.13.0 and merged as exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`. Final-head proofs retained README-only no-container, Verify-only impact without Build/Docs, and Build-side impact without Verify.

The Step-5 performance stop condition was fully evaluated in completed experiment #53. The resulting shared correction is complete:

- keep the immutable Docker SCAD runtime;
- `tool.git-project v0.2.7` exposes same-job generated-output publication from exact source `6234b7437b0dc0115642468f74d1f4a2c2214bef`;
- `tool.scad-project v0.13.1` provides one host orchestrator job around Moon preflight, conditional explicit Docker production, validation/staging and same-job host publication from exact source `28661fc040c4994e9c1d391285b7425c7a55252b`;
- relevant lifecycle measurements returned to about **41–45 s** in the experiment while keeping one SCAD container; README-only controls remained about **4–5 s** with zero containers.

Step 5 is **complete and released**: `lib.scad.clamps` PR #7 adopted released `tool.scad-project v0.13.1` and merged as exact qualified main `c5732944c8c2ba840a3f0f2f0a0638430a796cfd`. A missed release-closeout was corrected immediately afterwards: PR #14 recorded the existing qualified changes as `v0.1.3`, merged as exact release source `f0dbb82b477201646fc3e2173ccba96d70fb8920`, and release run `34974674991` passed Build, Verify and finalization. Annotated tag `v0.1.3` resolves to that exact source; immutable `rel/v0.1.3/build` and `rel/v0.1.3/verification` branches and GitHub Release assets exist.

Reference-library evidence:

- final PR-head relevant run `34971400621` — one host job, one explicit SCAD Docker process, OpenSCAD + PythonSCAD design/verification, current materialization and both host publications green; measured lifecycle about **45 s** with a ~20 s GHCR pull;
- README-only proof PR #11 / run `34971644925` — `affected=false`, reason `target-and-upstream-unaffected`; no image pull, Docker, staging or publication;
- docs-only proof PR #12 / run `34971733730` — retained affected-task evidence contains `scad.docs` and excludes `scad.verify`;
- Verify-only proof PR #13 / run `34971800074` — retained affected-task evidence contains `scad.verify` and excludes `scad.docs`;
- exact-main run `34972350665` — one host job/one Docker and both production publications green;
- `prod/build` and `prod/verification` both record exact qualified source `c5732944c8c2ba840a3f0f2f0a0638430a796cfd` and `tool.scad-project v0.13.1`;
- release-closeout PR #14 / run `34974591518` — changelog-only change correctly stopped after Moon preflight with zero SCAD containers;
- `v0.1.3` release run `34974674991` — exact-source Build and Verify green, immutable release branches published, annotated tag and GitHub Release/assets created from `f0dbb82b477201646fc3e2173ccba96d70fb8920`.

The first released v0.13.1 clamps run `34970821889` was also green but had a ~43.7 s GHCR pull outlier; producer work and publication remained short. The repeated final-head sample demonstrates that the earlier v0.13.0 ~64–65 s regression was caused by serial GitHub job boundaries and is no longer structural.

The next valid cross-project work is therefore:

1. **Next — Step 6 / `lib.scad.hub75`:** re-evaluate its actual repository graph, verification responsibilities, publication/release setup and current pins, then roll out the released single-host production model only where the owner boundaries still fit.
2. Requalify the HUB75 frame only if the shared/library change materially affects it.

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
