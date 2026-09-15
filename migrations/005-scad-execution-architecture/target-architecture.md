# Migration 005 — provisional target architecture

Status: **provisional target — implementation not started**

This is the current preferred architecture after reconstructing the Migration-004 model and measuring its main assumptions. It may still be adjusted by the remaining performance experiments, but those experiments no longer need to keep five structurally equal alternatives open.

Related:

- [Migration 005 README](README.md)
- [Current architecture](current-architecture.md)
- [Architecture reflection](architecture-reflection.md)
- [Measured evidence](measurements.md)
- [Architecture variants](target-variants.md)
- [Resource-efficiency criteria](resource-efficiency.md)

## 1. Human model first

A maintainer of a SCAD repository should normally need to think about only the capabilities the repository actually has.

For `lib.scad.clamps`:

```text
Design documentation
Verification
```

For `lib.scad.hub75`:

```text
Presentation renders
Design documentation
Verification
```

A maintainer should **not** need to understand or hand-maintain separate tasks for:

- writing a Build index;
- writing current source/tool information;
- selecting a source-impact-only graph root;
- selecting a complete publication graph root;
- cache transport mechanics;
- GitHub publication staging.

Those may remain implementation details when they serve a real purpose, but they are shared lifecycle mechanics rather than repository capabilities.

## 2. Preferred responsibility split

```text
GitHub Actions
    |
    |  event, exact source/base, credentials, hosted runner
    v
Moon on the host
    |
    |  cheap question: which SCAD capabilities are affected?
    |  none -> stop before Docker
    v
one SCAD Docker runtime
    |
    |  Moon: coarse capability scheduling + whole-capability output reuse
    |       |
    |       +-- Design documentation
    |       +-- Presentation renders (when configured)
    |       +-- Verification
    |                |
    |                +-- tool.scad-project capability command
    |                        |
    |                        +-- direct execution, or
    |                        +-- SCons fine-grained targets when configured
    v
host finishing/publication
    |
    |  current-run information, staging, retained evidence policy,
    |  generated-output branch publication
    v
published Build / Verification results
```

This deliberately keeps one heavy hosted runner while still allowing independent capability work to overlap inside the single runtime where Moon can schedule it safely.

## 3. Moon's target role

Moon remains because two separate benefits are now demonstrated or well justified.

### 3.1 Change-impact selection before Docker

This is already proven. An unrelated README-only change can finish without downloading or starting the expensive SCAD runtime.

Moon should answer the human-level question:

```text
Which capabilities are affected by this source change?
```

not merely one opaque boolean when the capability list is useful later in the lifecycle.

### 3.2 Whole-capability output reuse

Migration 005 demonstrated that Moon can restore a complete docs result on a fresh hosted VM when the task inputs contain only stable source-derived state.

The current failure was caused by our broad input glob including generated Python bytecode, not by Moon's cache model itself.

Moon therefore remains useful above SCons as a **coarse** reuse layer:

- docs output can be reused as a complete result;
- Verification output can be reused as a complete result;
- presentation Build output can be reused as a complete result;
- unaffected capabilities do not have to execute merely because another capability changed.

The input boundary must be source-only. Generated runtime state such as `__pycache__`, current CI run identifiers or publication context must never define the identity of a source-derived capability.

## 4. Moon configuration ownership

Standard SCAD tasks should be defined once in shared tooling and inherited by consumer repositories.

Moon v2 supports workspace-level task inheritance through `.moon/tasks/**`, and those task files can extend a relative file-system path. Because `tool.scad-project` is already pinned by exact Git submodule revision, the shared Moon policy can be pinned by the same repository/tool revision rather than copied into every consumer.

Conceptually:

```text
tool.scad-project
  shared Moon task policy
      |
      v
consumer .moon/tasks/scad.yml
  extends pinned shared policy
      |
      v
consumer project-specific capability inputs / overrides only
```

The exact file layout is an implementation decision, but the ownership rule is not:

> **Shared lifecycle mechanics are owned by shared tooling; consumer repositories declare only their actual capabilities and project-specific change-impact exceptions.**

The effective task graph must remain inspectable. Moon already exposes task details (`moon task <target>` and JSON output); shared tooling should add a plain-language explanation if that remains too technical for normal maintainers.

## 5. Consumer configuration target

`project.scad.yml` remains the source for SCAD project intent it already knows, including:

- Build output root;
- optional standalone render root;
- Verification commands/output root;
- publication policy;
- selected build engine (`direct` or `scons`).

The Moon-facing consumer configuration should add only source-impact information that cannot be derived safely from that model.

Illustrative clamps intent:

```text
Design documentation
  affected by project CAD/design source

Verification
  affected by CAD/API/test/verification source
```

Illustrative HUB75 intent:

```text
Presentation renders
  affected by panel/render source

Design documentation
  affected by CAD/design source

Verification
  affected by API/fixture/testcase/verification source
```

The final syntax is not selected here. The important point is that a consumer no longer declares seven/eight lifecycle steps.

## 6. `tool.scad-project` role

`tool.scad-project` owns complete capability commands and SCAD-domain policy.

It should present commands at the same level as the human model, for example conceptually:

```text
build documentation
build presentation renders
run verification
```

Existing commands such as `produce-build` / `produce-verification` are useful evidence that this coarse boundary already partly exists, but their exact current composition must not dictate the new API if Build renders and Build documentation need to remain independently affected capabilities.

Index generation and source/tool information belong to the capability/lifecycle implementation, not to consumer-authored Moon topology.

## 7. SCons role

SCons remains the fine-grained dependency engine **only where the project selects it**.

Evidence already distinguishes two cases:

- `lib.scad.clamps` uses the default direct engine; no `.cache/scad-project/scons` is created, so generic SCons cache restore/save is wasted work;
- `lib.scad.hub75` explicitly selects `build_engine: scons`; its qualified exact-main run populated the normal SCons cache.

Therefore:

```text
Moon
  decides/reuses a whole capability

SCons (optional)
  decides/reuses individual targets inside an executing capability
```

The workflow should restore/save an SCons cache only if the effective project/capability configuration can actually use it.

A separate Verification SCons cache should exist only if Verification really has a SCons-backed target engine. The current generic empty cache slot is not itself an architectural requirement.

## 8. Current-run information must be outside source-derived cache identity

The current architecture had a real reason for separating source-impact tasks from finishing tasks: publication information includes values that change per CI invocation.

The target architecture preserves the **distinction**, but not necessarily the visible task count.

Source-derived cached capability output must not depend on values such as:

```text
GitHub run id
PR number
current ref/publication context
```

After Moon has executed or restored the source-derived capability outputs, shared lifecycle code writes the current source/tool/run information required for truthful publication.

That gives both:

- stable reusable source output;
- truthful current publication information.

## 9. GitHub Actions role

GitHub Actions should remain a thin lifecycle shell around shared tooling:

1. resolve exact source and comparison base;
2. check which SCAD capabilities changed;
3. stop immediately when none changed;
4. acquire one SCAD runtime when needed;
5. restore only caches applicable to the configured project/capabilities;
6. execute/materialise the coarse capability graph in one Docker process;
7. validate output;
8. add current-run information;
9. publish/retain output according to explicit policy.

The reusable workflow should not contain repository-specific CAD logic.

## 10. Resource and latency objective

The target retains the one-heavy-runner principle from Migration 004 because two independent hosted VMs duplicate image download, checkout and runtime setup.

However, “one runner” is not sufficient success by itself.

The target should recover latency by:

- removing work rather than creating a second VM;
- hydrating unchanged capabilities from Moon cache;
- using SCons target reuse only where configured;
- allowing independent capability work to overlap within one runtime when safe;
- avoiding cache restore/save operations for unused engines;
- reducing SCAD image distribution cost;
- removing or making optional retained normal-CI artifacts nobody consumes;
- overlapping or combining independent publication work when safe.

Every performance comparison must report both wall-clock feedback and total hosted compute/resource use.

## 11. What this target deliberately rejects

### Current seven/eight-task consumer graph

Rejected as a long-term consumer contract. Too much generic lifecycle detail is repeated in each repository.

### Moon only for the host impact check

No longer the preferred design. Once task identity was fixed, Moon whole-output reuse demonstrably worked and avoided real render work. Removing that capability would discard a useful coarse-grained reuse layer, especially for richer repositories with independently affected Build/docs/Verification domains.

It remains a fallback if later experiments show the shared coarse Moon model introduces disproportionate complexity.

### Remove Moon entirely

Not preferred. The impact-analysis value is proven and replacing it would require us to invent and maintain equivalent dependency/affected logic.

### Return to two heavy hosted jobs merely for latency

Not preferred. The old ~37-second result came partly from overlapping two expensive VM/container initialisations. Migration 005 should first remove the dominant single-runner overhead and exploit in-runtime concurrency before paying for duplicated hosted infrastructure again.

## 12. Remaining validation before implementation plan

This target is provisional until the following are completed:

1. measure warm SCons reuse on a real SCons-enabled HUB75 capability;
2. measure SCAD image size/layers and compare realistic image-distribution improvements;
3. decide normal-CI artifact retention policy explicitly;
4. test safe concurrent/combined Build + Verification branch publication;
5. prototype Moon inherited shared tasks from the pinned `tool.scad-project` path;
6. sketch the resulting consumer configuration for both clamps and HUB75 and apply the human-understandability test;
7. estimate latency and total runner time for the resulting lifecycle.

If those checks do not expose a fundamental contradiction, this document becomes the basis for the Migration-005 implementation steps.
