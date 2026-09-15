# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Active — provisional target architecture selected; validation in progress.**

Migration 004 proved and released a working common SCAD execution model, but its final review found that the visible Moon/task model had become too difficult to understand from a normal consumer repository and that the latency/resource trade-off was not yet good enough to accept as the final architecture.

Migration 005 has now completed the first architecture-reflection round and selected a provisional direction:

- keep Moon for repository-level change-impact selection and whole-capability result reuse;
- move standard SCAD Moon policy into shared `tool.scad-project` configuration and inherit it in consumers;
- expose only real project capabilities such as Design documentation, Presentation renders and Verification;
- keep SCons optional and fine-grained only inside capabilities whose project configuration selects it;
- keep current-run/publication information outside reusable source-derived task identity;
- keep one heavy hosted runner as the default, but evaluate latency **and** total runner/compute use separately.

Important measured findings behind that decision:

- old parallel relevant-change baseline: about **37 s** wall-clock with two simultaneous heavy jobs;
- final Migration-004 v0.13.1 topology: about **41–45 s** with one heavy job;
- repeated README-only controls: about **4.4–4.8 s**, zero SCAD containers;
- affected SCAD image acquisition commonly costs about **15–20 s** while the small clamps Moon/CAD graph is only around **5 s**;
- the original Moon warm-cache misses were caused by generated Python `__pycache__/*.pyc` entering broad tool inputs;
- after stabilising task inputs, Moon restored a complete clamps documentation result on a fresh runner (`cached, 2ms`) instead of rerendering for roughly four seconds;
- clamps uses the direct build engine and therefore creates no SCons object cache, while HUB75 explicitly uses SCons and does populate its normal SCons cache.

Resource efficiency is a first-class criterion. A faster design is not automatically better if it requires two simultaneous hosted VMs and duplicated image/setup work; a one-runner design is also not acceptable merely because it consumes less compute if it creates a large feedback regression.

Current validation gate before implementation:

- measure warm SCons reuse on HUB75;
- investigate SCAD image distribution/layer cost and realistic reuse options;
- decide normal-CI artifact retention policy;
- test safe Build/Verification publication concurrency or combination;
- prototype inherited shared Moon capability tasks;
- show the resulting clamps and HUB75 consumer configuration and apply the human-understandability test;
- estimate resulting latency and total runner/resource use.

Do not migrate the HUB75 frame before this validation gate is complete and the target architecture is confirmed.

Tracking issue: #55. Canonical scope: [Migration 005](migrations/005-scad-execution-architecture/README.md). Provisional target: [target architecture](migrations/005-scad-execution-architecture/target-architecture.md).

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

The real HUB75 frame was deliberately **not** migrated to the new model. It remains on `tool.scad-project v0.12.0` and `lib.scad.hub75 v0.1.3` until Migration 005 confirms the replacement architecture.

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
