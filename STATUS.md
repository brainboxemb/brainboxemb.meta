# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Active — architecture definition first.**

Migration 004 proved and released a working common SCAD execution model, but its final human-maintainability review found that the visible Moon/task model had become too difficult to understand from a normal consumer repository.

Migration 005 therefore starts with architecture, not rollout.

Current goal:

- describe the existing SCAD CI/execution flow in ordinary language;
- identify which visible task boundaries are essential and which are accidental/historical complexity;
- compare simpler target variants before implementing them;
- retain the useful Migration-004 properties where justified: unrelated changes should not start the SCAD runtime, Build and Verification remain independently meaningful, exact-source evidence remains trustworthy, and GitHub write credentials remain outside the SCAD runtime;
- use measured performance rather than vague claims when evaluating simplification.

Performance baseline inherited from Migration 004:

- old parallel relevant-change baseline: about **37 s** wall-clock, two heavy SCAD containers and roughly **68–70 runner-seconds**;
- first common v0.13.0 topology: **64–65 s** — a regression caused by serial GitHub job/artifact boundaries;
- final v0.13.1 topology: about **41–45 s**, one heavy SCAD container;
- repeated README-only controls: about **4.4–4.8 s**, **zero SCAD containers**;
- old job-level SCAD-container startup alone was observed around **17–30 s before checkout**.

The important conclusion is not “all builds became faster”. The large gain is avoiding the heavy SCAD path entirely when it is unnecessary and reducing duplicated heavy setup when it is necessary.

The first Migration-005 deliverable is a plain-language current architecture plus at least two simpler target variants. Do not migrate the HUB75 frame before that target architecture is selected.

Tracking issue: #55. Canonical scope: [Migration 005](migrations/005-scad-execution-architecture/README.md).

## Recently completed

### Migration 004 — SCAD repository execution model

**Complete.**

Migration 004 qualified the conditional-SCAD execution model through:

- `template.scad-project`;
- `lib.scad.clamps v0.1.3`;
- `lib.scad.hub75 v0.1.4`;
- shared `tool.git-project v0.2.7` and `tool.scad-project v0.13.1`.

It proved README-only zero-container behavior, one-container affected production, Build/Verification independence, conservative execution when comparison context is uncertain, and host-side publication after the SCAD process exits.

The real HUB75 frame was deliberately **not** migrated to the new model after the final maintainability review. It remains on `tool.scad-project v0.12.0` and `lib.scad.hub75 v0.1.3`; its eventual update belongs to Migration 005 after the architecture is simplified/clarified.

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

- **Moon as SCAD target engine** — issue #51. This remains separate; Migration 005 may reconsider visible orchestration boundaries, but it must not silently turn this parked engine-replacement question into an assumption.

## Other follow-ups

Useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52.

Generic performance/robustness follow-ups remain owner-local unless explicitly promoted:

- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency.
