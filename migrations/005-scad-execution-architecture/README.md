# Migration 005 — understand, document and simplify the SCAD execution architecture

Status: **active — provisional target selected, validation in progress**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Durable working set

- [Current architecture in plain language](current-architecture.md)
- [Architecture reflection](architecture-reflection.md)
- [Measured evidence](measurements.md)
- [Architecture alternatives and decision](target-variants.md)
- [Provisional target architecture](target-architecture.md)
- [SCons warm-cache validation](scons-cache-validation.md)
- [Normal publication-path analysis](publication-analysis.md)
- [Resource-efficiency and compute-cost criteria](resource-efficiency.md)

The repository documentation is the source of truth. Issue #55 is only the tracker for progress/discussion.

## Purpose

Migration 005 is a complete architecture reflection and improvement track for the SCAD/Moon integration.

It exists because Migration 004 proved that the execution model can work, but also exposed two problems:

1. the model became too difficult for a normal maintainer to understand from a consumer repository;
2. its performance/resource trade-offs were not good enough to accept the implementation as the final architecture without further review.

The goal is not merely to make `moon.yml` shorter or Docker faster. It is to make the complete lifecycle understandable, correct, efficient and proportionate.

## What Migration 004 handed over

Measured reference points:

| Situation | Feedback time | Heavy hosted work | Interpretation |
| --- | ---: | ---: | --- |
| old parallel Build + Verify | ~37 s relevant | 2 simultaneous heavy jobs | faster feedback, but duplicated VM/image/setup work |
| first one-runner v0.13.0 | ~64–65 s | 1 | too much serialization |
| final v0.13.1 | ~41–45 s | 1 | less duplicated compute, but still slower feedback than old baseline |
| README-only final path | ~4.4–4.8 s | 0 | clear win on both speed and resource use |

On the small clamps reference, the actual Moon/CAD output graph is only around five seconds while SCAD Docker image acquisition is commonly around 15–20 seconds.

Therefore Migration 005 treats **feedback latency and total compute/resource use as different metrics**. Neither “fastest” nor “fewest containers” wins by itself.

## Architecture findings now established

### Moon has two demonstrated uses

1. **Change-impact selection before Docker.** Unrelated changes can avoid the expensive runtime completely.
2. **Complete capability output reuse.** A controlled fresh-runner test showed that a stable documentation task can be restored from Moon cache instead of rerendered.

The original warm-cache failure was caused by our integration: `tools/tool.scad-project/**` included generated Python `__pycache__/*.pyc`, so identical source produced different task hashes on different runners. With bytecode excluded from task identity, Moon kept a stable hash and reported a cached task in about 2 ms.

### SCons is optional and its target-level reuse is now validated

- clamps uses the default direct engine and does not create a SCons object cache;
- HUB75 explicitly selects `build_engine: scons`;
- a controlled exact-source HUB75 rerun restored the ~222 KB normal SCons cache on a fresh hosted VM;
- both presentation-render targets were restored from SCons cache;
- all 26 design-documentation targets were restored from SCons cache;
- presentation Build dropped from about 2.0 s to **0.430 s**;
- design documentation dropped from about 8.07 s to **0.602 s**;
- the complete Moon graph dropped from about 8.805 s to **5.071 s**, with Verification (~4.403 s) becoming the remaining real-work critical path.

The separate Verification SCons cache was not populated or restored. Cache handling must therefore follow the actual configured engine/capability rather than being enabled generically for every repository.

This validates the intended boundary:

```text
Moon
  whole-capability change/reuse decision

SCons, only where configured
  individual target dependency/reuse inside an executing capability
```

See [SCons warm-cache validation](scons-cache-validation.md) for the exact run/job evidence.

### Current consumer Moon configuration exposes too much machinery

Clamps currently exposes seven Moon tasks and HUB75 eight. Maintainers actually need to think in terms of only a few real capabilities:

Clamps:

```text
Design documentation
Verification
```

HUB75:

```text
Presentation renders
Design documentation
Verification
```

Build indexes, current source/tool information, synthetic roots, cache transport and publication staging are shared lifecycle mechanics and should not be hand-authored in every repository.

### Moon can share standard task policy natively

Moon supports inherited workspace task configuration. This makes it plausible for `tool.scad-project` to own the standard SCAD capability policy while a consumer declares only project-specific capability inputs/overrides. A custom Moon YAML generator is not the preferred solution.

## Provisional target architecture

The current target combines two earlier ideas:

- **inherit shared SCAD Moon policy** from pinned shared tooling;
- **make Moon model coarse real capabilities**, not finishing mechanics.

The intended responsibility split is:

```text
GitHub Actions
  exact source/base, hosted lifecycle, credentials
        |
        v
Moon on host
  which SCAD capabilities changed?
  none -> stop before Docker
        |
        v
one SCAD runtime
  Moon -> execute or restore whole capabilities
            |
            +-- tool.scad-project
                    |
                    +-- direct execution, or
                    +-- SCons fine-grained targets when configured
        |
        v
host finishing/publication
  current source/tool/run information + publication policy
```

Source-derived capability output must have stable source-only identity. Current run/ref/PR/publication information is added after execution/restoration and must not invalidate reusable source output.

See [target-architecture.md](target-architecture.md) for the full model.

## Resource-efficiency requirement

Architecture experiments and implementation acceptance must report, where practical:

- wall-clock feedback time;
- total runner-seconds/minutes;
- maximum simultaneous heavy runners;
- container/runtime starts;
- duplicated image/tool downloads;
- productive CAD work;
- work avoided through change selection/cache reuse;
- cache/artifact transfer overhead.

This avoids “winning” by using two VMs merely to hide duplicated setup, while also avoiding excessive serialization simply to reduce runner count.

## Human-understandability acceptance test

Give a maintainer a normal consumer repository plus one linked architecture page.

Without migration history or chat logs, that maintainer must be able to explain:

- which SCAD capabilities the repository has;
- what happens after README-only, CAD-source, Build/docs-only and Verification-only changes;
- why Moon exists;
- when SCons exists and when it does not;
- what is cached and where;
- why current-run information is separate from reusable source output;
- why publication is outside Docker;
- where most CI latency and compute go;
- why the architecture is worth its complexity and resource cost.

If that cannot be answered, the architecture is not finished.

## Current validation phase

Do **not** migrate the HUB75 frame yet.

Completed validation:

- **warm SCons reuse on a real HUB75 SCons capability — passed.** Target-level reuse is measurable and inexpensive to transfer; generic SCons cache handling for non-SCons capabilities is not justified.

Still required before deriving the implementation plan:

1. measure SCAD image size/layer/distribution options;
2. decide normal-CI retained artifact policy;
3. test safe concurrent or combined Build/Verification publication;
4. prototype inherited shared Moon capability tasks from the pinned `tool.scad-project` path;
5. show the resulting consumer configuration for clamps and HUB75 and run the human-understandability test;
6. estimate both feedback latency and total runner/resource use for the resulting lifecycle.

If these validations do not reveal a fundamental flaw, the provisional target becomes the implementation architecture and Migration 005 can be broken into owner-specific implementation steps.
