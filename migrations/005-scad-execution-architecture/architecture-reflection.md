# Migration 005 — architecture reflection

Status: **reflection concluded — provisional target selected**

This document records the architectural conclusions from reconstructing and measuring the complete SCAD/Moon integration. The selected direction is described in [target-architecture.md](target-architecture.md); detailed measurements remain in [measurements.md](measurements.md).

## 1. The current architecture solves real problems

The stack is not complex because every layer is arbitrary. It currently handles several different concerns:

```text
GitHub Actions
  hosted lifecycle, event/source context, credentials, publication

Moon
  repository-level change-impact decisions and complete-output reuse

tool.scad-project
  SCAD-domain commands and policy

SCons
  optional fine-grained target dependency/reuse inside configured capabilities

SCAD Docker image
  reproducible OpenSCAD/PythonSCAD runtime

consumer repository
  project intent and project-specific source
```

The mistake was mainly that too many of those implementation details became part of every consumer repository's visible Moon configuration.

## 2. What is proven worth keeping

### Avoid the expensive runtime when nothing relevant changed

README-only proof finished in roughly 4–5 seconds without starting Docker. This saves both maintainer waiting time and heavy hosted compute.

### Keep uncertainty safe

When the comparison cannot be trusted, required CAD work must run rather than be silently skipped.

### Keep write credentials outside the CAD runtime

Generated-output publication belongs on the host after the SCAD runtime exits.

### Keep exact source/tool identity

Published and released output must remain traceable to exact source/tool revisions.

### Keep Moon as a coarse repository-level layer

Two Moon capabilities are now backed by evidence:

1. it can decide before Docker which repository-level SCAD work is affected;
2. it can restore a complete capability result on a fresh hosted runner when task identity contains only stable source-derived inputs.

The first failed warm-cache experiments were caused by our integration: broad `tools/tool.scad-project/**` inputs included generated Python `__pycache__/*.pyc`, which changed between runners. With bytecode removed from task identity, the same docs task kept one stable hash and was restored as `cached, 2ms` instead of rerendering for roughly four seconds.

### Keep SCons where it is actually selected

SCons is useful as a fine-grained target engine, but it is not a universal layer.

- clamps uses the default direct engine and creates no SCons object cache;
- HUB75 explicitly selects `build_engine: scons` and does populate the normal SCons cache.

The lifecycle should therefore activate SCons cache handling only for capabilities that can actually use it.

## 3. What should change

### Consumer repositories should describe project capabilities, not lifecycle internals

A clamps maintainer should think about:

```text
Design documentation
Verification
```

A HUB75 maintainer should think about:

```text
Presentation renders
Design documentation
Verification
```

They should not hand-maintain separate tasks for Build index generation, current source/tool information, two synthetic graph roots, or generic cache/publication mechanics.

### Shared SCAD Moon policy belongs in `tool.scad-project`

Moon supports native inherited workspace tasks. The standard SCAD task policy can therefore be owned once by the pinned SCAD tooling and inherited by consumers, while consumers provide only project-specific capability/source-impact additions.

This is preferable to inventing a separate YAML generator.

### Moon and SCons need a strict coarse/fine boundary

The intended split is:

```text
Moon
  Does this whole capability need work, or can its complete source-derived output be reused?

SCons, only when configured
  Within a capability that is executing, which individual targets need rebuilding?
```

The two tools should not independently model the same detailed target graph.

### Source-derived output and current-run information must be separate concepts

Current GitHub run/ref/PR information changes per invocation and must not invalidate source-derived cached CAD output.

The architecture should preserve the correctness distinction but hide the mechanics behind shared tooling:

```text
source-derived capability output
    -> execute or restore from cache

current-run/source/tool/publication information
    -> add after capability materialisation
```

A maintainer should not need two synthetic no-op Moon roots merely to express this distinction.

## 4. Performance reflection

Migration 004 produced a mixed result:

- old parallel Build+Verify: ~37 s relevant feedback, but two simultaneous heavy hosted runners;
- v0.13.0 one-runner attempt: ~64–65 s, clear regression;
- v0.13.1: ~41–45 s, one heavy runner, less duplicated compute but still slower than the old feedback path;
- README-only: ~4–5 s and no Docker, clear win on both latency and resource use.

On the small clamps reference, the actual Moon/CAD graph is only around five seconds while Docker image acquisition is commonly around 15–20 seconds.

This means the architecture must not spend most of its complexity optimizing five seconds of CAD while repeatedly paying a much larger runtime-distribution cost.

## 5. Compute/resource reflection

Wall-clock latency is not the same as efficiency.

The old two-job topology got a shorter stopwatch partly by running two heavy hosted VMs at the same time, each doing image/runtime setup. For an open-source project that may not appear as a direct invoice, but it still represents runner capacity, network transfer and energy use.

Migration 005 therefore evaluates both:

- how long the maintainer waits;
- how much total hosted compute and duplicated work was needed.

A design should prefer eliminating work over parallelising duplicate setup. Two VMs remain acceptable only when the feedback gain is important enough to justify the resource increase and cannot be achieved with one runtime through cache reuse or safe internal concurrency.

## 6. Runtime/lifecycle complexity still matters independently

The structural simplification does not solve all measured overhead.

Open areas that remain legitimate optimization work are:

- repeated cold SCAD image acquisition;
- restoring/saving cache mechanisms that a repository cannot use;
- full normal-CI artifact uploads whose purpose is retention rather than technical hand-off;
- sequential Build/Verification branch publication;
- several seconds of Moon runtime/change-impact/evidence setup on affected changes.

These are lifecycle optimizations that can be applied to the selected architecture rather than treated as competing architecture variants.

## 7. Resulting ownership model

The preferred ownership boundary is now:

```text
tool.git-project
  generic Moon runtime and generic repository primitives

 tool.scad-project
  standard SCAD capability policy, inherited Moon task definitions,
  capability commands and SCAD-specific lifecycle behavior

consumer repository
  project configuration, project source and only project-specific
  capability/change-impact exceptions
```

`tool.git-project` should not learn SCAD domain rules, and consumer repositories should not copy generic SCAD orchestration policy.

## 8. Provisional architecture decision

The reflection selects a combination of the earlier A and B alternatives:

- **inherit shared policy** rather than hand-copying it in consumers;
- **model coarse real capabilities** rather than exposing finishing mechanics as the consumer contract.

Moon remains because both its change-impact and complete-output reuse value are now demonstrated. SCons remains optional inside capabilities that select it.

Moon-only-change-impact remains a fallback. Removing Moon entirely is not justified by current evidence. Keeping the existing seven/eight-task consumer graph is not accepted as the long-term human interface.

See [target-architecture.md](target-architecture.md) for the resulting model and [target-variants.md](target-variants.md) for the decision record.

## 9. Human acceptance test

The architecture is ready for rollout only when a maintainer can take a normal consumer repository plus one linked architecture page and explain, without migration history or chat logs:

- which human-level SCAD capabilities exist;
- what happens for README-only, CAD-source, Build-only/docs-only and Verification-only changes;
- why Moon exists;
- when SCons exists and when it does not;
- what gets cached and why;
- why current-run information does not invalidate source-derived cache results;
- why publication remains outside Docker;
- where most CI time and compute go;
- why the architecture is worth its complexity.

## 10. Remaining validation gate

Do **not** migrate the HUB75 frame yet.

Before converting this provisional target into an implementation plan, complete these checks:

1. warm SCons reuse on a real SCons-enabled HUB75 capability;
2. Docker image distribution/layer/reuse options;
3. normal-CI artifact retention policy;
4. safe concurrent or combined Build/Verification publication;
5. a real prototype of inherited shared Moon capability tasks;
6. concrete resulting consumer configuration for clamps and HUB75;
7. latency and total-runner/resource estimate for that resulting lifecycle.

Those validations may refine the target, but a major change in direction now requires new evidence rather than reopening all alternatives by default.
