# Migration 005 — architecture reflection

Status: **working architecture assessment — no target selected yet**

This document evaluates the complete current SCAD/Moon integration. It is deliberately broader than a performance investigation. Performance is one test of the architecture, together with correctness, ownership, maintainability and human understandability.

See also:

- [Migration 005 README](README.md)
- [Current architecture in plain language](current-architecture.md)
- [Migration 004 final measured baseline](../004-scad-repository-execution-model/README.md)

## 1. What problem is this architecture trying to solve?

A SCAD repository has several different kinds of work:

- decide whether a change can affect generated CAD/document output;
- render/export/document/verify the design;
- avoid rebuilding individual outputs that are already current;
- reuse generated results across disposable CI runners where safe;
- record exactly which source/tool versions produced published output;
- publish generated Build and Verification trees without giving write credentials to the CAD runtime;
- support releases from one exact source revision.

No single current layer owns all of that.

The present architecture combines:

```text
GitHub Actions
    -> lifecycle, credentials, hosted runner, publication

tool.git-project
    -> generic Moon runtime, affected query, Moon cache, generated-output publication

Moon
    -> repository-level graph, affected propagation, task cache/output hydration

tool.scad-project
    -> SCAD commands, reusable workflow, evidence conventions

SCons
    -> fine-grained SCAD target dependency/rebuild decisions

SCAD Docker image
    -> reproducible OpenSCAD/PythonSCAD/tool runtime

consumer repository
    -> source, project configuration, verification and currently a detailed Moon graph
```

The architecture is therefore solving real problems. The reflection is not based on an assumption that all of these layers are unnecessary.

## 2. Why Moon exists today

`tool.git-project` documents Moon as an optional repository-level orchestrator. Its intended value is to avoid unnecessary domain execution and to reuse task outputs across runs without inventing another scheduler, hash engine, dependency graph or cache implementation.

For SCAD specifically, Moon currently provides two things that SCons does not provide at the same level:

1. **repository-level impact selection before the SCAD runtime starts**;
2. **portable task output caching/hydration across fresh CI runners**.

SCons remains authoritative once a SCAD producer actually runs. It decides whether individual render/export targets need rebuilding.

That is a defensible separation in principle:

```text
Moon:  should this repository-level capability run / can its output be restored?
SCons: within that capability, which concrete SCAD targets must rebuild?
```

The problem is that this simple conceptual split is not what a maintainer sees in a current consumer `moon.yml`.

## 3. What is good in the current architecture?

Several outcomes should be treated as proven value rather than discarded during simplification.

### 3.1 Unrelated changes avoid the expensive runtime

A README-only change can complete in roughly 4–5 seconds and starts no SCAD container. This is a large and measurable improvement over always entering a heavy CAD job.

### 3.2 The impact decision uses the same graph as execution

The host does not maintain a second hand-written changed-path list in GitHub Actions. Moon task inputs and dependencies remain the source for affected analysis.

This reduces the risk that the gate and the real execution graph silently disagree.

### 3.3 Uncertainty fails safe

If the comparison base or affected query cannot be trusted, production runs instead of being silently skipped.

### 3.4 Fine-grained CAD dependency logic remains in SCons

Migration 004 did not try to replace a proven SCAD target engine merely to make Moon own everything.

### 3.5 Credentials have a clear security boundary

The SCAD container does not receive the GitHub write token. Generated-output publication is a host responsibility after the container exits.

### 3.6 Exact source/tool identity is retained

Published output is tied to exact source/tool revisions, which is useful for release reproducibility and physical-verification evidence.

These properties are meaningful architecture requirements, not incidental implementation details.

## 4. Where the architecture has become difficult to justify

### 4.1 The consumer sees orchestration mechanism instead of project intent

`lib.scad.clamps` exposes seven Moon tasks and `lib.scad.hub75` exposes eight.

A project maintainer does not naturally think in terms of:

- `scad.build-index`;
- `scad.build-provenance`;
- `scad.verification-provenance`;
- `scad.production-impact`;
- `scad.ci`.

The maintainer thinks in terms of:

- make Build output;
- make Verification output;
- perhaps make standalone renders/documentation independently;
- do not run CAD when an unrelated file changed.

The current consumer graph therefore exposes too much implementation policy.

### 4.2 There are two competing definitions of a “complete producer”

`tool.scad-project` already exposes:

- `produce-build` — design docs + configured build + index + source/publication information;
- `produce-verification` — verification + source/publication information.

At the same time, current Moon consumers deliberately split those operations into separate tasks so Moon can see producer and finishing boundaries.

This creates an architectural ambiguity:

> Is the stable domain contract “produce a complete Build/Verification result”, or is the stable contract “expose every internal finishing step to Moon”?

Both models currently exist. Migration 005 should choose one primary contract rather than document both indefinitely.

### 4.3 Evidence requirements are shaping the task graph

The evidence model correctly distinguishes:

- the execution that originally produced an artifact;
- the current run that reused/materialized it;
- the publication context in which it was published.

That distinction is technically sound.

However, the current graph risks turning that evidence distinction into visible build architecture. A human should not need several Moon tasks merely because evidence is stored in several files.

The architecture should ask whether the evidence model can remain correct while its mechanics move behind a smaller interface.

### 4.4 Two dependency/cache engines require a very clear boundary

Moon and SCons both make “do I need to do work?” decisions, but at different levels.

That can be valid, but only if the boundary is obvious:

- Moon should make coarse repository-capability decisions and reuse complete capability outputs;
- SCons should make fine-grained target decisions inside an executing capability.

If Moon inputs become as detailed as individual SCAD sources and generated subtrees while SCons independently models the same dependencies, the architecture starts paying configuration and cognitive cost twice.

Migration 005 must verify that Moon is actually operating at a meaningfully coarser level rather than duplicating SCons semantics.

### 4.5 The two visible root tasks are a workaround for publication context

`scad.production-impact` exists because context-sensitive finishing tasks contain environment inputs. If the full `scad.ci` root were used for the initial impact check, event/ref context could make an unrelated source change appear affected.

The semantic distinction is real:

- “does source require expensive work?”
- “make the complete result for this CI publication context”.

But exposing two synthetic no-op Moon tasks in every consumer is a poor human interface. The distinction may belong in shared tooling even if it must remain internally.

### 4.6 Repeated inputs make consumer configuration fragile

Project/tool/config/workflow paths occur repeatedly across tasks. That makes the graph verbose and increases the chance that one task is updated while another is forgotten.

A consumer should ideally declare domain intent once and inherit common tooling/config inputs from a shared contract.

### 4.7 The impact check is both valuable and overhead

The Moon impact check is highly valuable when it returns “no CAD work”: it saves a roughly 20-second image pull plus the rest of production.

When the change is affected, its roughly 4.7-second path is pure additional latency before the real runtime can start.

That does not mean the gate should be removed. It means its cost and implementation must be proportional to the benefit. Restoring a ~20 MB Moon runtime plus retaining several evidence files deserves scrutiny for such a simple yes/no question.

### 4.8 Docker/image acquisition dominates small builds

In representative final `lib.scad.clamps` run `34971400621`:

- Docker image pull: about **20 seconds**;
- entire Moon producer/finalization graph: about **5.1 seconds**.

The reusable workflow explicitly caches Moon state and SCons object state, but does not explicitly cache the Docker image/layer store. The affected run reports all image layers being downloaded and `Downloaded newer image`.

This means the architecture currently optimizes small task-level details while the dominant cost is runtime distribution.

Migration 005 must measure image size, layer sizes, network transfer, extraction time and container startup separately before deciding where optimization effort belongs.

### 4.9 One container reduced compute but serialized the critical path

The old Build and Verify jobs each paid image/startup overhead, but in parallel. The final model pays the heavy setup once but serializes most lifecycle work.

Measured `lib.scad.clamps` relevant-change latency therefore moved from roughly **37 seconds** to **41–45 seconds**.

This is an important architecture lesson:

> container count is a resource metric, not a latency metric.

Both must remain explicit.

### 4.10 Publication may contain avoidable hand-offs

The current one-host workflow stages generated trees, uploads two workflow artifacts, then publishes Build and Verification sequentially from the same host job.

Some of that may be required for retained CI evidence or release use, but same-job artifact upload is no longer automatically justified as a data-transfer mechanism.

The architecture should distinguish:

- artifacts retained because a human/release process needs them;
- artifacts used only as an internal hand-off;
- branch publication that could potentially overlap safely.

## 5. Human-understandability assessment

The current architecture does **not** yet pass the intended human-maintainability test.

A new maintainer can reconstruct the rationale, but must combine information from:

- the consumer `moon.yml`;
- `tool.git-project` Moon documentation;
- `tool.scad-project` production-workflow documentation;
- execution-evidence documentation;
- Migration 004 decisions/history.

The architecture is therefore documented in the sense that the facts exist, but not documented as one coherent operational model.

Terms such as “producer”, “provenance”, “materialization” and “preflight” also appear before the simpler concepts they represent are established.

Migration 005 should use ordinary terms first and technical terms second.

## 6. Ownership reflection

The existing top-level three-layer split remains sound:

```text
generic repository tooling
    -> tool.git-project

domain-specific SCAD tooling
    -> tool.scad-project

project/library intent and source
    -> consumer repository
```

The problem is mostly **where the detailed Moon graph lives**.

The current consumer owns details that are largely generic SCAD orchestration policy: finishing tasks, publication metadata dependencies, two synthetic roots and repeated tool/config inputs.

A likely improvement direction is therefore not to move SCAD knowledge into `tool.git-project`, but to move more **SCAD Moon policy from each consumer into `tool.scad-project`**.

The consumer should primarily state what project-specific capabilities and source areas exist.

## 7. Candidate target directions

No direction is selected yet. All must be tested against correctness, clarity and measured performance.

### Variant A — keep Moon, drastically shrink the consumer contract

Concept:

- keep Moon as repository-level affected/cache engine;
- keep SCons as fine-grained SCAD engine;
- move standard SCAD Moon task generation/defaults into `tool.scad-project`;
- consumer declares only project-specific capabilities and exceptional inputs;
- internal finishing/root tasks can still exist but do not need to be hand-authored or prominently documented in each consumer.

Potential consumer mental model:

```text
Build
Verification
(optional) standalone render/docs capability
```

Advantages:

- preserves Moon-native affected analysis and output hydration;
- preserves current safety properties;
- removes repeated orchestration YAML from consumers;
- likely lowest-risk evolutionary change.

Questions:

- can Moon configuration be generated/composed cleanly enough without creating an opaque hidden graph?
- how should a maintainer inspect the generated/effective graph?
- can source-impact and publication-context differences be internalized safely?

### Variant B — keep Moon only for coarse capability tasks

Concept:

- use `produce-build` and `produce-verification` as the principal Moon tasks;
- let each task produce a complete domain result;
- reduce or eliminate separate Moon index/source-information tasks;
- retain an internal/source-only way to determine whether Build or Verification is affected before Docker startup.

Potential visible graph:

```text
scad.build
scad.verify
scad.ci  -> build + verify
```

Advantages:

- aligns Moon with coarse capability boundaries;
- aligns with stable combined commands already present in `tool.scad-project`;
- much easier to explain.

Risks/questions:

- context-sensitive index/publication files must not poison source-impact checks;
- a coarse cached Build result may combine output whose refresh rules differ;
- producer evidence must remain truthful when output is hydrated;
- HUB75 has real docs/build distinctions that may require three capabilities rather than two.

### Variant C — remove Moon from the normal SCAD consumer surface

Concept:

- `tool.scad-project` owns the host impact decision using SCAD project configuration;
- SCons remains the only build dependency/cache engine visible to the SCAD domain;
- GitHub Actions calls one high-level SCAD lifecycle;
- Moon may disappear entirely from SCAD consumers, even if retained for other domains.

Advantages:

- simplest possible consumer mental model;
- avoids two dependency engines in SCAD repositories;
- potentially removes Moon runtime/preflight overhead.

Risks/questions:

- would require another trustworthy repository-level affected model;
- risks duplicating source-pattern knowledge outside the real build graph;
- loses Moon output hydration unless replaced;
- could turn `tool.scad-project` into a custom scheduler/cache system, which is specifically what Moon was introduced to avoid.

This variant must therefore be considered, not assumed desirable.

### Variant D — retain current responsibilities but optimize only runtime/lifecycle

Concept:

- keep the current Moon graph structure;
- improve Docker image distribution, impact-check cost and publication concurrency;
- improve documentation without changing task boundaries.

Advantages:

- lowest implementation risk;
- directly attacks measured critical-path overhead.

Disadvantages:

- leaves the seven/eight-task consumer model and duplicated configuration largely intact;
- documentation would explain complexity rather than reduce it.

This is a useful control variant: if structural simplification gives little benefit or creates correctness risk, lifecycle optimization may still be worthwhile.

## 8. Initial architectural preference

The evidence currently points most strongly toward evaluating **Variant A and Variant B first**.

Why:

- the generic/domain/project ownership split is still sensible;
- Moon has demonstrated useful repository-level affected behavior;
- SCons has demonstrated useful fine-grained SCAD behavior;
- the largest maintainability problem is that too much orchestration detail is exposed in consumers;
- `tool.scad-project` already contains high-level producer commands, suggesting that a coarser SCAD contract is technically plausible.

This is not yet a target decision. Docker/runtime measurements and cache/evidence behavior must be tested before choosing.

## 9. Required measurements before target selection

### Runtime/image

Measure for the exact pinned toolchain image:

- compressed transfer size;
- per-layer sizes;
- `docker pull` network/download duration;
- extraction/unpack duration where observable;
- `docker run` startup excluding repository bootstrap;
- whether GitHub-hosted images ever arrive warm in comparable runs;
- cost of any explicit OCI/image caching alternative, including cache upload/download time.

An image cache is useful only if restoring it is materially cheaper and reliable enough compared with pulling from GHCR.

### Moon impact path

Break the ~4.7-second affected path into:

- cache lookup/download of pinned Moon runtime;
- extraction;
- Moon invocation itself;
- affected graph calculation;
- evidence generation;
- evidence artifact upload.

Then decide which parts are necessary before Docker starts.

### Moon cache value

Measure how often the portable Moon output cache actually prevents producer execution on representative SCAD repositories, separately from SCons cache hits.

If Moon rarely hydrates complete useful output in this domain, its cache value may be lower than assumed even if its affected analysis remains valuable.

### Publication path

Measure:

- staging/copy time;
- retained artifact upload time;
- Build branch publication;
- Verification branch publication;
- whether Build/Verification publication can overlap safely;
- which workflow artifacts are genuinely consumed later.

## 10. Decision criteria

A target architecture should be selected only if it can explain, in ordinary language:

1. why Moon exists in the SCAD stack;
2. what Moon decides that SCons does not;
3. why each consumer-visible task/capability must exist;
4. what happens for README-only, Build-only and Verification-only changes;
5. what is cached at Moon level versus SCons level;
6. where exact source/tool evidence comes from;
7. why GitHub credentials remain outside the runtime;
8. where the dominant CI time goes;
9. why the chosen architecture is worth its complexity.

And it should be measured against at least:

- unaffected-change latency: current ~4.4–4.8 s;
- relevant-change latency: old parallel baseline ~37 s, current final model ~41–45 s;
- total runner/compute consumption;
- number of concepts/tasks a consumer maintainer must understand;
- amount of repository-local orchestration configuration.

## 11. Immediate next work

Before changing any consumer implementation:

1. finish the runtime/image and Moon-precheck timing breakdown;
2. quantify Moon output-cache benefit versus SCons cache benefit;
3. produce concrete configuration sketches for Variants A and B using both `lib.scad.clamps` and `lib.scad.hub75`;
4. test whether the two-root source-impact/publication distinction can be hidden inside shared SCAD tooling;
5. compare the variants on clarity, correctness, latency and runner usage;
6. select the target architecture and only then derive implementation steps and repository owners.
