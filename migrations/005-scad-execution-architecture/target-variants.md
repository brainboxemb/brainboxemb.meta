# Migration 005 — architecture alternatives and decision

Status: **alternatives evaluated — provisional target selected**

The complete target is described in [target-architecture.md](target-architecture.md). This document records which alternatives were considered and why the current direction was selected.

Related:

- [Migration 005 README](README.md)
- [Architecture reflection](architecture-reflection.md)
- [Measured evidence](measurements.md)
- [Resource-efficiency criteria](resource-efficiency.md)

## Starting point

The current consumers expose seven or eight Moon tasks. Several of them are not project capabilities but standard lifecycle mechanics such as writing indexes/source information or selecting one of two synthetic graph roots.

A maintainer naturally thinks about a much smaller model:

`lib.scad.clamps`:

```text
Design documentation
Verification
```

`lib.scad.hub75`:

```text
Presentation renders
Design documentation
Verification
```

The target architecture should expose that intent, while shared tooling owns the mechanics required to make it correct and reproducible.

## Alternative A — inherit the current detailed Moon graph

Standard SCAD Moon tasks move into shared tooling and consumers inherit them instead of copying seven/eight task definitions.

This is low risk and solves much of the duplication, but leaves the internal graph more detailed than the domain really needs.

**Useful part retained:** native Moon task inheritance is the preferred way to share common policy; no custom YAML generator should be introduced unless native inheritance proves insufficient.

## Alternative B — coarse Moon capabilities

Moon models only real source-derived capabilities such as documentation, presentation renders and Verification. Standard finishing mechanics happen behind those capability boundaries.

This aligns Moon with the level at which maintainers reason about repositories and gives a clear split:

```text
Moon  -> whole capability / cross-run reuse
SCons -> individual targets inside a SCons-enabled capability
```

Migration 005 now has direct evidence that this can work:

- Moon change-impact analysis correctly avoids the SCAD runtime for unrelated changes;
- once generated `.pyc` files were removed from task identity, Moon restored a complete documentation capability on a fresh VM with the same stable task hash;
- the cached Moon task completed in about 2 ms, versus roughly four seconds of rendering on the cold attempt.

**Selected as the main structural direction.**

## Alternative C — Moon only for change-impact analysis

Moon would answer which capabilities changed before Docker, then `tool.scad-project`/SCons would execute them without Moon in the heavy runtime.

This became a serious candidate when identical reruns restored a Moon cache archive but still reran everything. The later diagnostic showed why: our broad tool input included generated Python bytecode, so task identity changed between runners.

After correcting that accidental input, Moon whole-output reuse worked. Removing Moon from the execution path would therefore discard a demonstrated coarse reuse capability.

**Retained as fallback, not preferred.** Use it only if the shared coarse Moon model later proves disproportionately complicated or unreliable.

## Alternative D — remove Moon from SCAD

`tool.scad-project` would own both change-impact selection and execution.

This gives the smallest conceptual stack, but would require us to invent and maintain repository-level dependency/change logic that Moon already provides. Moon's change-impact value is proven and its output reuse now also works when inputs are stable.

**Not selected.** Reconsider only if Moon itself becomes the dominant source of complexity or overhead after the consumer contract is simplified.

## Alternative E — keep the current graph and optimize only runtime

This keeps the seven/eight-task consumer model and only attacks Docker/image/publication overhead.

Those runtime optimizations are valuable but do not solve the human-maintainability problem.

**Not sufficient as an architecture on its own.** Its useful optimizations should be applied independently to the selected structure.

## Selected combination: A + B

The provisional target combines the strongest parts of A and B:

1. Moon remains the repository-level capability/change/reuse layer.
2. Moon tasks visible to normal maintainers correspond to real capabilities, not finishing mechanics.
3. Standard task policy is owned by `tool.scad-project` and inherited by consumers using Moon's native task inheritance.
4. Consumers declare only project-specific capabilities and exceptional source-impact inputs that cannot be derived safely.
5. Generated current-run/publication information remains outside source-derived cache identity.
6. SCons remains optional and fine-grained inside capabilities whose effective project configuration selects `build_engine: scons`.
7. GitHub Actions remains a thin host lifecycle and credentials boundary.
8. One heavy hosted runner remains the default; latency should be recovered by removing work and overlapping safe in-runtime work, not by automatically returning to two VMs.

## Why this decision changed after measurement

The architecture decision was deliberately postponed until the cache assumptions were tested.

The important sequence was:

```text
identical production rerun
    -> Moon cache archive restored
    -> task hashes nevertheless changed
    -> docs/Verify reran

hash diagnostic
    -> broad tools/** input included generated __pycache__/*.pyc
    -> those bytecode files differ between fresh runners

stable-input experiment
    -> same task hash on fresh runner
    -> Moon reports cached result
    -> complete docs output restored instead of rendered
```

That evidence removes the strongest argument for “Moon only for the first change check”. The earlier miss was caused by our integration, not by the Moon caching model.

## Resource-use decision

The old two-job Build+Verify model remains an important latency reference (~37 s), but it used two simultaneous heavy hosted runners and duplicated image/runtime setup. The final Migration-004 one-runner model used less total infrastructure but was slower (~41–45 s).

Migration 005 therefore does not select architecture by stopwatch alone. Candidates are evaluated on:

- feedback latency;
- total runner time;
- maximum heavy-runner concurrency;
- duplicated image/tool/setup work;
- unnecessary capability execution;
- cache/artifact transfer cost;
- human/maintenance complexity.

Prefer eliminating work over duplicating runners.

## Remaining validation before implementation

The target is provisional until these checks complete:

1. measure warm SCons reuse on a real SCons-enabled HUB75 capability;
2. measure SCAD image size/layers and realistic image-distribution alternatives;
3. decide normal-CI retained artifact policy;
4. test safe concurrent or combined Build/Verification branch publication;
5. prototype inherited shared Moon capability tasks from the pinned `tool.scad-project` path;
6. show the resulting consumer configuration for clamps and HUB75 and apply the human-understandability test;
7. estimate both latency and total runner/resource use for the resulting lifecycle.

If these checks do not expose a fundamental contradiction, [target-architecture.md](target-architecture.md) becomes the basis for the implementation plan.
