# Migration 004 — SCAD repository execution model

Status: **complete**

Tracking issue: [#49](https://github.com/brainboxemb/brainboxemb.meta/issues/49)

Successor: [Migration 005 — simplify the SCAD execution architecture](../005-scad-execution-architecture/README.md)

Detailed qualification: [evidence.md](evidence.md)

Performance measurements: [performance-evidence.md](performance-evidence.md)

Human-maintainability reflection: [reflection.md](reflection.md)

Original change request: [change-request.md](change-request.md)

## What Migration 004 set out to do

The practical problem was that SCAD repositories paid a large fixed CI cost even when little or no CAD work was required.

Migration 004 introduced and qualified a common repository-level execution model in which:

- a cheap host-side impact check happens before the expensive SCAD runtime starts;
- an unrelated change such as a root README edit starts **no SCAD container**;
- affected normal CI uses at most one immutable SCAD Docker process;
- Build and Verification remain independently meaningful capabilities;
- SCons remains the fine-grained SCAD target engine;
- generated-output publication happens on the host after the SCAD process exits;
- exact source/tooling evidence is retained for generated output.

The model was released and qualified through the reference template and both reusable SCAD libraries.

## Completed rollout

| Step | Owner | Result |
| --- | --- | --- |
| 1 | `tool.git-project` | Generic Moon/VCS affected pre-check released and qualified. |
| 2 | `template.scad-project` | Stale Verify → Build dependency removed; producer independence requalified. |
| 3 | `tool.scad-project` | Reusable production lifecycle released as v0.13.0. |
| 4 | `template.scad-project` | Released lifecycle qualified, including README-only zero-container behavior. |
| 5 | `lib.scad.clamps` | Reference library qualified; performance regression triggered measured redesign; final model released through `tool.scad-project v0.13.1`; clamps released as v0.1.3. |
| 6 | `lib.scad.hub75` | Richer library graph qualified on v0.13.1 and released as v0.1.4 without changing physical-verification content. |

The planned HUB75-frame rollout was intentionally **not** executed. The frame still uses `tool.scad-project v0.12.0` and `lib.scad.hub75 v0.1.3`. Before propagating the new model further, the Step-6 reflection found that the current Moon/task architecture had become too difficult to explain from a normal consumer repository. Rather than roll out complexity that may immediately be redesigned, that remaining consumer migration is handed to Migration 005.

## Final performance result

The performance outcome must be read in more than one dimension.

### Relevant SCAD changes

The retained `lib.scad.clamps` measurements are:

| Topology | Relevant-change wall-clock | Heavy SCAD containers | Approx. runner use |
| --- | ---: | ---: | ---: |
| Old parallel Build + Verify | about **37 s** critical path | 2 | about **68–70 runner-seconds** |
| First common v0.13.0 implementation | about **64–65 s** | 1 | similar order, but serialized across jobs |
| Final v0.13.1 one-host implementation | about **41–45 s** | 1 | roughly one 41–45 s host lifecycle |

So the final model did **not** make an ordinary relevant change faster than the old ~37 s parallel baseline. It did remove the accidental 64–65 s regression introduced by the first common implementation, and it reduced heavy runner/container duplication substantially.

### Unrelated changes

The largest user-visible gain is the path that should not run CAD at all.

Repeated README-only controls on the final topology completed the measured lifecycle in:

- **4.369 s**;
- **4.819 s**;
- **zero SCAD containers**.

Before the pre-container gate, observed SCAD job-container initialization alone cost roughly **17–30 s before checkout**. A README-only or otherwise unrelated change therefore no longer pays a tens-of-seconds heavy-runtime setup cost.

### What the performance result means

Migration 004 produced a material performance/resource improvement in these ways:

- unrelated changes stop after a few seconds instead of entering the heavy SCAD runtime;
- normal affected CI starts one heavy SCAD container instead of two separate Build/Verify containers;
- total runner/setup duplication is reduced materially;
- the first common-model regression from ~37 s to ~64–65 s was corrected back to ~41–45 s;
- publication overhead was reduced from separate serial jobs to roughly 4 s combined in the measured one-host samples.

It would be inaccurate to summarize this as “all builds became much faster”. The main win is **not doing expensive work when it is unnecessary**, plus lower compute/setup duplication when it is necessary.

The detailed measurements, exact runs and runtime experiment remain in [performance-evidence.md](performance-evidence.md).

## Why Migration 004 closes here

The technical execution-model goals are proven on the reference project and both reusable libraries, and the released artifacts/evidence exist.

The final reflection identified a different problem: the working model now contains too many concepts whose purpose is not obvious to a human maintainer. That is an architecture-quality problem, not another qualification step for this migration.

Keeping it inside Migration 004 would mix two different questions:

1. **004:** can we avoid unnecessary heavy CI and run the common model correctly?
2. **005:** can the resulting architecture be made simpler and understandable without losing the useful performance/reliability properties?

Migration 004 therefore closes with the current released model as a measured baseline. Migration 005 owns the architecture simplification and any later rollout to the HUB75 frame.

## Final qualified releases/state

- `tool.git-project v0.2.7` — same-job generated-output publication support;
- `tool.scad-project v0.13.1` — final one-host/conditional-Docker lifecycle;
- `lib.scad.clamps v0.1.3` — qualified reference library release;
- `lib.scad.hub75 v0.1.4` — qualified second-library release;
- HUB75 frame — deliberately left on its previous qualified v0.12.0/v0.1.3 setup for Migration 005.
