# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

There is currently **no active cross-project migration**.

Migration 005 has completed its current-generation SCAD rollout and final evidence review. A new migration must be selected explicitly; proposed or owner-local follow-ups do not start automatically.

## Recently completed

### Migration 005 — simplify the SCAD execution architecture

**Complete.**

Migration 005 replaced the lifecycle-heavy Migration-004 Moon topology with a capability-oriented current-generation SCAD model and qualified it through every public repository currently classified with `project_infrastructure.provider: tool.scad-project`.

Final released shared foundations:

- `docker.scad-toolchain v0.5.0` — OpenSCAD-focused and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one generic Moon query;
- `tool.scad-project v0.14.7` / `3935e5f86fe309b8908a05554f7ada336a6d6886` — inherited capabilities, precise shallow tool-gitlink comparison, configuration/runtime/cache planning, semantic reusable-workflow refs, one-runtime normal production, durable timing/log evidence and exact host publication provenance.

Completed current-generation consumers:

1. **`template.scad-project`** — final v0.14.7 reference qualification run `35085388134`; merged as `cb1e3e50e5e56644153cdf74b54b5da1e747c8d8`; post-merge main run `35085631904`; README-only zero-runtime probe `35085786014`.
2. **`lib.scad.clamps`** — migration PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`; immutable v0.1.4 released; zero-runtime run `35065514152`.
3. **`lib.scad.hub75`** — migration PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`; immutable v0.1.5 released from `e0432a9533a08a1c0d9e87225c22f3f66b632531`; zero-runtime run `35065524524`.
4. **`2026-009-01.cad.HUB75-display-frame`** — migration PR #33 merged as `61da023ff0f6bc353687b55a8158e75ebd70b046`; post-merge main run `35069411142`; README-only zero-runtime probe `35069504915`.

The canonical repository catalog classifies the remaining CAD repositories as **classic** standalone/shared-actions projects. Moving those repositories to `tool.scad-project` would be a separate project-infrastructure-generation migration, not unfinished Migration-005 rollout.

Final resource/performance evidence is deliberately mixed rather than rounded into one success number:

| Scenario | Final observation | Budget result |
| --- | ---: | --- |
| clamps affected canary | ~41.9 s | meets low/mid-40 s target |
| HUB75 warm/cached canary | ~32.2 s | meets low/mid-30 s target |
| clamps README-only | ~9.2 s, zero CAD/runtime | structural goal met; 4–6 s latency target missed |
| HUB75 README-only | ~7.6 s, zero CAD/runtime | structural goal met; 4–6 s latency target missed |
| template README-only | ~9.9 s, zero CAD/runtime | structural goal met; 4–6 s latency target missed |
| template full v0.14.7 reference path | 41.059 s to prepared snapshot | durable phase evidence retained |

The remaining unrelated-change latency is dominated by fixed GitHub Actions setup plus the generic ~20 MB Moon-runtime restore/query path. It is a non-blocking generic preflight optimisation opportunity; it does not require another SCAD execution-architecture rewrite.

The selected model now keeps:

- one generic Moon affected query before CAD runtime acquisition;
- zero CAD work for unrelated changes;
- one hosted production job and at most one CAD runtime for normal affected work;
- capability-appropriate focused or full runtime selection;
- Moon for whole-capability reuse and optional SCons only for configured fine-grained target reuse;
- no unused SCons transport for direct projects or command-only Verification;
- no duplicate complete normal Build/Verification Actions artifacts by default;
- Build and Verification publication allowed to overlap on the same runner;
- current run/publication metadata outside source-derived Moon identity;
- semantic released reusable-workflow refs plus exact checked-out gitlink identity;
- exact PR-head source provenance in publication, run-context, materialization and producer evidence.

Tracking issue: #55. Closeout issue: #63. Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md). Durable architecture: [SCAD technical architecture](domains/scad/architecture.md).

### Migration 004 — SCAD repository execution model

**Complete.**

Migration 004 qualified the conditional-SCAD execution model through the template and both reusable SCAD libraries. Its measured wall-clock/resource trade-offs became the starting point for Migration 005 rather than being hidden inside a success label.

See [Migration 004](migrations/004-scad-repository-execution-model/README.md), [qualification evidence](migrations/004-scad-repository-execution-model/evidence.md) and [performance evidence](migrations/004-scad-repository-execution-model/performance-evidence.md).

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

- **Moon as SCAD target engine** — issue #51. Migration 005 deliberately retained SCons as the fine-grained target engine where selected; this parked experiment remains separate.

## Other follow-ups

Useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52.

Generic performance/robustness follow-ups remain owner-local unless explicitly promoted:

- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency;
- generic unrelated-change preflight latency — fixed Actions/Moon-runtime overhead remains an optimisation opportunity after Migration 005 and does not reopen it.
