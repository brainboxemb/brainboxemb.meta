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

Migration 004 has a **mixed performance result**. It materially reduces unnecessary compute, but it does **not** improve relevant-change wall-clock latency on the small `lib.scad.clamps` reference repository.

### Headline comparison

| Topology | Relevant-change wall-clock | Heavy SCAD containers | Approx. runner use |
| --- | ---: | ---: | ---: |
| Old parallel Build + Verify | about **37 s** critical path | 2 | about **68–70 runner-seconds** |
| First common v0.13.0 implementation | about **64–65 s** | 1 | similar order, but serialized across jobs |
| Final v0.13.1 one-host implementation | about **41–45 s** | 1 | one mid-40-second host lifecycle |
| Final README-only path | about **4.4–4.8 s** | 0 | one short host pre-check |

For an affected change, the final implementation is therefore roughly **4–8 seconds slower** than the old ~37 s parallel baseline. Depending on the sample, that is roughly an **11–22% latency regression** for the person waiting for CI.

At the same time, it avoids running two heavy SCAD jobs in parallel and therefore materially reduces duplicated runner/container work.

Those are different metrics and must not be conflated.

## Where the time actually goes

`lib.scad.clamps` is deliberately useful as a reference because the CAD workload itself is small. That makes fixed CI overhead visible instead of hiding it behind a long render.

### Old v0.12 parallel model

The baseline used separate Build and Verify workflows on exact source `52048164db5e5da0b9522c758551bc3af65cae45`:

- Build run `34872343290`;
- Verify run `34872343227`.

Both jobs started together and therefore overlapped their expensive setup.

Representative in-job timing from the retained logs:

| Phase | Build | Verify | Critical-path effect |
| --- | ---: | ---: | --- |
| SCAD image pull + job-container creation | about **16.5 s** | about **18.0 s** | Runs in parallel, so user waits roughly for the slower ~18 s pull, not their sum. |
| Checkout + tool submodules | about **2.6 s** | about **2.5 s** | Also parallel. |
| Cache/tool/lint preparation before producer | about **3.2 s** | about **1.4 s** | Parallel. |
| Actual docs/build or verification work | about **3.3 s** | about **1.7 s** | Parallel; real CAD/domain work is only a few seconds. |
| Index/provenance/artifact/publication tail | about **6.2 s** | about **4.0 s** | Parallel between Build and Verify. |
| Cleanup | under **1 s** | under **1 s** | Parallel. |

The important observation is that **two ~17–18 s image pulls are expensive in runner resources, but they do not add ~35 s to user latency because they happen concurrently**.

The old model is therefore inefficient in total compute but reasonably fast in wall-clock terms for this small repository.

### Final v0.13.1 one-host model

Representative final candidate run: `34971400621`.

The exact job log shows approximately:

| Phase | Approx. elapsed time | What it does |
| --- | ---: | --- |
| Hosted-runner/action preparation | **1.9 s** | Prepare the reusable workflow/actions before its first step. |
| Resolve source + shallow checkout + exact base fetch | **1.9 s** | Prepare only the source/base commits needed for the decision. |
| Moon impact check + retained decision evidence | **4.7 s** | Restore the ~20 MB Moon runtime, ask whether SCAD work is affected, and upload decision evidence. |
| Moon/SCons cache restore + range preparation | **1.9 s** | Prepare reusable caches and the exact source range. |
| Pull the SCAD Docker image | **20.0 s** | By far the largest single item on the serial critical path. |
| Docker bootstrap + validation + production graph | **9.4 s** | Initialize tool submodules, validate tooling, then execute the graph. The Moon task graph itself reports only **5.132 s**; current materialization records about **6.349 s**. |
| Validate/stage + upload Build/Verification artifacts | **2.6 s** | Prepare both generated trees and retain workflow artifacts. |
| Publish Build then Verification | **4.4 s** | Two host-side generated-branch publications, currently sequential. |
| Post-job Moon cache save/cleanup | about **1.4 s** | Save orchestration cache and clean up. |

The full runner log window is about **48 s** including runner/action preparation and post-job cleanup; the retained reusable-workflow measurements used for the migration comparison are about **41–45 s**, because their measurement boundary is narrower. Both views tell the same story about where time is spent.

### Why one container is not faster here

Going from two containers to one sounds like it should halve setup latency, but that is not what the old topology did.

Old:

```text
                 +-- Build:  pull image -> ~3 s producer -> publish --+
change ----------|                                                |---- done
                 +-- Verify: pull image -> ~2 s producer -> publish --+
                         both heavy paths run in parallel
```

Final v0.13.1:

```text
change
  -> checkout/base
  -> Moon impact check
  -> cache preparation
  -> pull one image
  -> bootstrap
  -> ~5 s producer graph
  -> upload artifacts
  -> publish Build
  -> publish Verification
  -> done
```

The final model saves **resource duplication**, but it also places almost all infrastructure on one serial critical path.

For a tiny CAD workload, the new items on that path matter:

- roughly **4.7 s** impact-check/evidence work;
- roughly **1.9 s** cache/range preparation;
- a **20 s** image pull that can no longer overlap a second job;
- roughly **4.4 s** sequential publication after production.

The actual SCAD/docs/verification graph is only around **5 s**. The majority of the total time is therefore CI/runtime orchestration rather than CAD computation.

## Unrelated changes are the clear win

Repeated README-only controls on the final topology completed in:

- **4.369 s**;
- **4.819 s**;
- **zero SCAD containers**.

Before the pre-container check, job-level SCAD-container initialization alone was observed around **17–30 s before checkout**. A README-only or otherwise unrelated change no longer pays that cost at all.

That is the clearest latency improvement produced by Migration 004.

## Performance verdict

Migration 004 should **not** be summarized as a general CI speed-up.

It achieved three things:

1. **Strong win for unaffected changes.** They fall from a heavy container path measured in tens of seconds to roughly 4–5 s with zero SCAD containers.
2. **Strong resource-efficiency win for affected changes.** Two heavy Build/Verify containers/runners became one host lifecycle with one heavy container.
3. **Small but real wall-clock regression for affected changes on the simple reference library.** The person waiting for relevant CI moved from roughly 37 s to roughly 41–45 s.

The first v0.13.0 common topology was much worse at 64–65 s and was correctly rejected/reworked. v0.13.1 removed that structural regression but did **not** beat the old parallel latency baseline.

This matters for Migration 005: the next architecture must treat the ~37 s old relevant-change latency as a real baseline, not merely celebrate container-count reduction. For small repositories, most time is infrastructure. Any additional architecture or evidence step must justify its place on the critical path.

The full experiment and exact retained measurements remain in [performance-evidence.md](performance-evidence.md).

## Why Migration 004 closes here

The technical execution-model goals are proven on the reference project and both reusable libraries, and the released artifacts/evidence exist.

The final reflection identified a different problem: the working model now contains too many concepts whose purpose is not obvious to a human maintainer. The performance breakdown adds a second reason not to roll it out mechanically: the architecture reduces resource duplication but still adds relevant-change latency on the small reference repository.

Keeping that redesign inside Migration 004 would mix two different questions:

1. **004:** can we avoid unnecessary heavy CI, eliminate the worst duplicated setup, and run the common model correctly?
2. **005:** can the resulting architecture be made simpler **and faster on the relevant critical path** without losing its useful correctness/security properties?

Migration 004 therefore closes with the current released model as a measured baseline rather than declaring it the final architecture. Migration 005 owns architecture simplification, critical-path reassessment and any later rollout to the HUB75 frame.

## Final qualified releases/state

- `tool.git-project v0.2.7` — same-job generated-output publication support;
- `tool.scad-project v0.13.1` — final one-host/conditional-Docker lifecycle;
- `lib.scad.clamps v0.1.3` — qualified reference library release;
- `lib.scad.hub75 v0.1.4` — qualified second-library release;
- HUB75 frame — deliberately left on its previous qualified v0.12.0/v0.1.3 setup for Migration 005.
