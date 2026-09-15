# Migration 005 — understand, document and simplify the SCAD execution architecture

Status: **active — architecture reflection first**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

Working documents:

- [Current architecture in plain language](current-architecture.md)
- [Complete architecture reflection](architecture-reflection.md)
- [Measured architecture evidence](measurements.md)
- [Concrete target-architecture variants](target-variants.md)
- [Normal publication-path analysis](publication-analysis.md)

## Purpose

Migration 005 is a **complete architecture reflection of the SCAD/Moon integration**.

It is not just a Docker-performance exercise and it is not just a cleanup of `moon.yml`.

Migration 004 proved that the current shared model works, but it also showed that a normal maintainer now has to understand too many interacting concepts across:

- GitHub Actions;
- Moon;
- `tool.git-project`;
- `tool.scad-project`;
- SCons;
- the SCAD Docker toolchain;
- generated-output publication;
- repository-local Moon configuration and evidence.

The reasons for those boundaries exist, but they are spread across several repositories and historical decisions. At the same time, the final relevant-change path on the small `lib.scad.clamps` reference is slightly slower than the old parallel model even though it uses less total compute.

The goal is therefore to understand the whole architecture, document it coherently for a human, challenge every visible layer/boundary, and then simplify or improve it where justified.

## Central architecture question

> What role should Moon have in a SCAD repository, which responsibilities belong around it, and how small can the resulting consumer-facing model become while remaining correct, understandable and efficient?

Performance is one acceptance dimension of that question, not the whole question.

## What must be reconstructed before implementation

Migration 005 must explain in ordinary language:

1. why Moon was introduced at all;
2. what Moon does that GitHub Actions and SCons do not already do;
3. what SCons remains responsible for;
4. why the host performs an impact check before starting the SCAD runtime;
5. why current consumers expose separate docs/build/verification/finishing/root Moon tasks;
6. why both `scad.production-impact` and `scad.ci` exist;
7. how Moon caching and SCons caching differ and whether both provide measurable value;
8. why generated-output evidence is split into output-creation, current-run and publication information;
9. why publication is a host responsibility rather than a container responsibility;
10. what a consumer project actually needs to configure versus what should be inherited from shared tooling;
11. where the current CI time really goes;
12. which complexity is essential and which is accidental or historical.

## Performance baseline inherited from Migration 004

Architecture decisions must use measured performance, but container count is not a proxy for latency.

| Situation | Relevant/unaffected wall-clock | Heavy SCAD containers | Meaning |
| --- | ---: | ---: | --- |
| old parallel Build + Verify | about **37 s** relevant critical path | 2 | More total compute, but expensive setup overlaps. |
| first common v0.13.0 model | about **64–65 s** relevant | 1 | Clear serialization regression. |
| final v0.13.1 model | about **41–45 s** relevant | 1 | Less duplicated compute, but still slower than old relevant baseline. |
| final README-only path | about **4.4–4.8 s** | 0 | Clear win: expensive CAD runtime is never started. |

Representative final `lib.scad.clamps` work shows roughly 20 seconds for SCAD Docker image acquisition versus about five seconds for the Moon output graph itself. Runtime distribution and orchestration therefore deserve at least as much scrutiny as task-level optimizations.

## Important finding: Docker image reuse is not currently part of the cache strategy

The current reusable workflow explicitly pulls `ghcr.io/brainboxemb/scad-toolchain:v0.4.1` for an affected change.

It explicitly caches Moon state and SCons object state. It does **not** explicitly cache the Docker/OCI image or Docker layer store. Representative affected runs repeatedly download all image layers again.

Migration 005 must measure whether image acquisition can be reduced or reused economically on disposable GitHub-hosted runners. An image cache is not automatically an improvement if restoring it is as expensive as pulling from GHCR.

## Important finding: Moon impact analysis and Moon output caching are different claims

Migration 004 **proved** that Moon's impact analysis is useful:

- README-only work can stop before Docker;
- isolated HUB75 changes can be classified as Build-, docs- or Verify-related.

Migration 005 has now also run a controlled identical rerun of the exact same clamps source. In that rerun:

- the portable Moon cache archive from the original attempt was successfully restored;
- the exact source revision and workflow inputs were the same;
- Moon nevertheless generated different task hashes for docs and Verify;
- those tasks executed again instead of being restored from cache.

So the current state is stronger than “cache benefit has not yet been observed”:

> **the current portable Moon cache integration does not provide stable task reuse for an identical rerun.**

The root cause is not yet known. The next diagnostic step is to compare Moon hash manifests and identify exactly which hashed input changes between attempts.

Until that is understood, whole-task output caching is not a valid justification for keeping Moon in the heavy execution path. Moon's demonstrated impact-analysis role remains separate and valuable.

Detailed timings and task hashes are in [measurements.md](measurements.md).

## Architecture properties worth preserving unless evidence says otherwise

- an unrelated change should not start the expensive SCAD runtime;
- uncertainty must run safely rather than incorrectly skip required work;
- Build and Verification remain independently meaningful capabilities;
- SCons remains dependency-aware for fine-grained SCAD targets unless a replacement is demonstrably better;
- published output identifies exact source/tooling;
- GitHub write credentials stay outside the SCAD runtime;
- a release can be reproduced from one exact source revision.

These are outcomes. Their current implementation is open to change.

## First architecture findings

The complete reflection currently identifies several issues worth challenging:

- consumer `moon.yml` files expose seven/eight tasks even though maintainers naturally think in terms of only a few domain capabilities;
- `tool.scad-project` already has complete `produce-build` / `produce-verification` commands while Moon consumers separately expose finishing tasks, so the stable boundary is ambiguous;
- evidence distinctions are useful but may be shaping too much visible build architecture;
- Moon and SCons both make reuse decisions and need a clearer coarse-versus-fine boundary;
- two synthetic Moon roots encode a real source-impact versus publication-context distinction, but that distinction may not need to be visible in every consumer;
- common inputs/configuration are repeated through many tasks;
- Moon itself supports workspace-level task inheritance, so duplicated consumer task definitions may be avoidable without custom generation;
- the impact check is highly valuable for unaffected changes but adds several seconds to affected changes;
- Docker image acquisition dominates the small reference build and is not explicitly cached today;
- the current Moon output-cache integration restores its archive but does not yield stable task hashes on an identical rerun;
- normal full-tree workflow artifacts are not required as a hand-off to same-job publication;
- Build and Verification branch publication appears structurally independent enough to justify a concurrency experiment.

## Candidate directions

No target is selected yet. The concrete comparison is in [target-variants.md](target-variants.md). The important current alternatives are:

1. **keep Moon and inherit standard SCAD policy** — consumers declare only project-specific capabilities/impact additions;
2. **use coarser Moon capability tasks** — Moon models complete Build/Verification-style capabilities rather than internal finishing mechanics;
3. **use Moon only for impact analysis** — retain the demonstrated pre-Docker benefit and let `tool.scad-project`/SCons execute only affected capabilities;
4. **remove Moon entirely from SCAD** — control option, acceptable only if replacement impact logic is genuinely simpler and equally safe;
5. **optimize lifecycle/runtime independently** — image distribution, normal artifact retention and publication concurrency can improve whichever structural variant wins.

## Human-understandability acceptance test

Give a maintainer a normal consumer repository plus one linked current-architecture page.

Without migration history or chat logs, that maintainer must be able to explain:

- what happens after README-only, CAD-source, Build-only and Verification-only changes;
- why Moon exists;
- what Moon decides versus what SCons decides;
- why each consumer-visible capability is separate;
- what is cached and where;
- where generated output and source/tool information come from;
- where most CI time is spent;
- why the chosen architecture is worth its complexity.

If that cannot be answered, the architecture is not finished.

## Current phase

Do **not** migrate the HUB75 frame yet.

Next:

1. diagnose the unstable Moon task hashes by comparing hash manifests from identical runs;
2. then measure whether stable Moon output hydration provides material value;
3. measure warm SCons reuse separately;
4. measure Docker image transfer/layer/startup costs and realistic reuse options;
5. qualify publication simplifications;
6. compare the concrete architecture variants on clarity, correctness, latency and total compute;
7. select the target architecture with explicit reasons;
8. only then derive implementation steps and repository owners.

The HUB75 frame remains on its previous qualified `tool.scad-project v0.12.0` / `lib.scad.hub75 v0.1.3` setup until that decision is made.
