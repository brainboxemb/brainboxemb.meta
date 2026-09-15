# Migration 005 — understand, document and simplify the SCAD execution architecture

Status: **architecture validated — owner-repository implementation plan ready**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Durable working set

- [Current architecture in plain language](current-architecture.md)
- [Architecture reflection](architecture-reflection.md)
- [Measured evidence](measurements.md)
- [Architecture alternatives and decision](target-variants.md)
- [Validated target architecture](target-architecture.md)
- [SCons warm-cache validation](scons-cache-validation.md)
- [Runtime image family](runtime-image-family.md)
- [Runtime image family validation](runtime-image-validation.md)
- [Normal publication-path analysis](publication-analysis.md)
- [Concurrent Build/Verification publication validation](publication-concurrency-validation.md)
- [Normal CI artifact retention policy](normal-ci-artifact-policy.md)
- [Moon shared-capability inheritance validation](moon-inheritance-validation.md)
- [Human-understandability validation](human-understandability-validation.md)
- [Target lifecycle resource and latency budget](target-resource-budget.md)
- [Resource-efficiency and compute-cost criteria](resource-efficiency.md)
- [Owner-specific implementation plan](implementation-plan.md)

The repository documentation is the source of truth. Issue #55 is the tracker for progress/discussion.

## Purpose

Migration 005 is the architecture correction and simplification track for the SCAD/Moon integration.

Migration 004 proved that the execution model can work, but exposed two problems:

1. the model was too difficult for a normal maintainer to understand from a consumer repository;
2. its performance/resource trade-offs were not good enough to accept the implementation as the final architecture without further review.

Migration 005 has now completed that review. The remaining work is owner-repository implementation and qualification of the validated target.

## Migration-004 baseline

Measured reference points:

| Situation | Feedback time | Heavy hosted work | Interpretation |
| --- | ---: | ---: | --- |
| old parallel Build + Verify | ~37 s relevant | 2 simultaneous heavy jobs | faster feedback, but duplicated VM/image/setup work |
| first one-runner v0.13.0 | ~64–65 s | 1 | too much serialization |
| final v0.13.1 | ~41–45 s typical relevant | 1 | less duplicated compute, but still slower feedback than old baseline |
| README-only final path | ~4.4–4.8 s | 0 CAD runtime | clear win on both speed and resource use |

On the small clamps reference, actual Moon/CAD graph work is much smaller than fresh-runner SCAD image acquisition. Migration 005 therefore treats **feedback latency and total compute/resource use as separate metrics**.

## Validated architecture findings

### Moon remains for two measured reasons

1. **Change-impact selection before Docker.** Unrelated changes can avoid the CAD image/runtime completely.
2. **Complete capability output reuse.** A controlled fresh-runner test proved stable documentation output can be hydrated from Moon cache instead of rerendered.

The earlier warm-cache failure was our integration defect: `tools/tool.scad-project/**` included generated Python `__pycache__/*.pyc`, so identical source produced different task hashes. Shared task policy now uses explicit source-controlled tool inputs instead of that broad subtree.

### SCons is optional fine-grained reuse

- clamps uses the direct engine and creates no useful SCons object cache;
- HUB75 explicitly selects `build_engine: scons`;
- controlled HUB75 warm reuse restored both presentation targets and all 26 documentation targets;
- presentation Build dropped from about 2.0 s to 0.430 s;
- design documentation dropped from about 8.07 s to 0.602 s;
- the complete Moon graph dropped from about 8.805 s to 5.071 s.

The boundary is therefore:

```text
Moon
  whole-capability change/reuse

SCons, only where configured
  individual target dependency/reuse inside an executing capability
```

### The runtime image family is validated

The two-profile candidate proved OpenSCAD-only work does not need PythonSCAD-specific runtime layers:

- OpenSCAD profile: **328,098,501 compressed bytes**;
- full profile: **449,516,893 compressed bytes**;
- OpenSCAD-only work avoids **121,418,392 compressed bytes**, about **27.0%** of full-image transfer.

Both profiles passed the shared OpenSCAD contract. The full profile additionally passed PythonSCAD/pybosl2 coverage and retained the documented interoperability XFAIL boundaries.

Runtime selection is capability/configuration-driven, not repository-name-driven.

### Normal CI does not need duplicate full-tree Actions artifacts

Normal production currently uploads complete Build and Verification trees and then publishes the same staged trees directly to generated-output branches. No normal downstream consumer was found downloading those artifacts. Release uses its own exact-source cross-job artifacts.

Target policy:

- keep compact decision/orchestration evidence;
- do not upload complete normal Build/Verification Actions artifacts by default;
- retain release artifacts as a separate required hand-off;
- future full normal artifacts, if needed, must be explicit opt-in policy.

### Build and Verification publication may overlap on one runner

Controlled run `34994181268` executed two released publisher instances at the same time on one Ubuntu runner:

- Build: 2.089 s;
- Verification: 2.144 s;
- overlap: 2.089 s;
- concurrent window: 2.144 s versus 4.233 s sequential sum.

Both branch trees contained the exact source SHA and cleanup removed both temporary branches. This is a safety/isolation proof, not a promise that every production publication saves exactly two seconds.

### Shared Moon capability inheritance is validated

Final inheritance run `34997339916` used:

- clamps exact source `f0dbb82b477201646fc3e2173ccba96d70fb8920`;
- HUB75 exact source `2eaaa540e3658bd3821eb6ec0f2d0352cbefff48`;
- shared task prototype `tool.scad-project@1303ae8c40817a98f9615a58762264b3ef19b6dd`;
- released Moon 2.5.4 owner `tool.git-project@6234b7437b0dc0115642468f74d1f4a2c2214bef`.

It proved native Moon inheritance is sufficient. The consumer can contain only:

1. the visible capability list;
2. project-specific source-impact patterns.

Shared `tool.scad-project` policy owns the commands, stable common tool inputs, standard output boundaries and Moon cache policy.

No custom Moon-YAML generator is needed.

### The maintainer-facing model passes the understandability test

The resulting visible capabilities are:

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

A maintainer no longer authors tasks for indexes, publication information, synthetic roots, cache transport or publication staging.

`project.scad.yml` explains runtime/build intent; reduced `moon.yml` explains which capabilities exist and what project sources affect them. Shared validation must reject contradictions between those two views.

## Validated target architecture

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
one capability-appropriate SCAD runtime
  Moon -> execute or restore only affected whole capabilities
            |
            +-- tool.scad-project
                    |
                    +-- direct execution, or
                    +-- SCons targets when configured
        |
        v
host finishing/publication
  current source/tool/run information
  compact retained evidence
  concurrent isolated Build/Verification publication when useful
```

Important invariants:

- source-derived capability identity contains source/tool/config only;
- current run/ref/PR/publication context is added after execution/restoration;
- one heavy hosted runner is the default;
- one CAD runtime is the default;
- runtime image is selected from effective capabilities;
- SCons transport exists only where a configured capability can use it;
- complete normal output artifacts are not retained redundantly by default.

## Resource/latency acceptance

The target resource budget is documented in [target-resource-budget.md](target-resource-budget.md).

Key acceptance points:

- unrelated change: remain roughly in the existing 4–6 s host-only class and start zero CAD runtime;
- clamps remains a full/dual image case, so its main wins are less unused/duplicated work and stable Moon reuse rather than image slimming;
- HUB75 can use the OpenSCAD-focused image and should recover much of the old parallel topology's latency without reintroducing a second heavy runner;
- implementation must report wall-clock time **and** runner/resource use.

## Implementation consequence

The released generic Moon affected implementation already computes `affected-tasks.json`, but exposes only a single boolean to the workflow. The target needs the actual affected coarse capability IDs from that same query so one Docker invocation can receive only the required capabilities.

This is an implementation/API refinement, not an unresolved architecture question.

See [implementation-plan.md](implementation-plan.md) for the owner order.

## Current phase

Architecture validation is complete.

Do **not** migrate `2026-009-01.cad.HUB75-display-frame` yet.

The first implementation step is to finalise and release the already-qualified two-profile runtime image family and its external test contract. Later tool changes must pin released immutable dependencies, then clamps and HUB75 act as the two canaries before downstream consumers move.

If implementation evidence contradicts an assumption, correct the architecture explicitly in this repository rather than silently working around it in a consumer.
