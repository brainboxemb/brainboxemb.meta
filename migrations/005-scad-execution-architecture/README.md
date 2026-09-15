# Migration 005 — understand, document and simplify the SCAD execution architecture

Status: **active — architecture reflection first**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

Working documents:

- [Current architecture in plain language](current-architecture.md)
- [Complete architecture reflection and candidate directions](architecture-reflection.md)

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
8. why generated-output evidence is split into producer, current-run and publication information;
9. why publication is a host responsibility rather than a container responsibility;
10. what a consumer project actually needs to configure versus what should be inherited from shared tooling;
11. where the current CI time really goes;
12. which complexity is essential and which is accidental or historical.

The detailed reconstruction starts in [current-architecture.md](current-architecture.md) and the assessment/candidate improvements are kept in [architecture-reflection.md](architecture-reflection.md).

## Performance baseline inherited from Migration 004

Architecture decisions must use measured performance, but container count is not a proxy for latency.

| Situation | Relevant/unaffected wall-clock | Heavy SCAD containers | Meaning |
| --- | ---: | ---: | --- |
| old parallel Build + Verify | about **37 s** relevant critical path | 2 | More total compute, but expensive setup overlaps. |
| first common v0.13.0 model | about **64–65 s** relevant | 1 | Clear serialization regression. |
| final v0.13.1 model | about **41–45 s** relevant | 1 | Less duplicated compute, but still slower than old relevant baseline. |
| final README-only path | about **4.4–4.8 s** | 0 | Clear win: expensive CAD runtime is never started. |

Representative final `lib.scad.clamps` run `34971400621` shows roughly:

| Phase | Approx. time |
| --- | ---: |
| source/base preparation | 1.9 s |
| Moon impact check + evidence | 4.7 s |
| cache/range preparation | 1.9 s |
| **SCAD Docker image pull** | **20.0 s** |
| container bootstrap + validation + production | 9.4 s |
| of which Moon output graph itself | **5.132 s** |
| staging + workflow-artifact upload | 2.6 s |
| sequential Build + Verification publication | 4.4 s |
| post-job cache/cleanup | ~1.4 s |

The actual output graph is therefore only a small part of the lifecycle. Runtime distribution and orchestration deserve at least as much scrutiny as task-level optimizations.

## Important current finding: Docker image reuse

The current reusable workflow explicitly runs `docker pull ghcr.io/brainboxemb/scad-toolchain:v0.4.1` for an affected change.

The workflow explicitly caches Moon state and SCons object state. It does **not** explicitly cache the Docker/OCI image or Docker layer store. In representative affected evidence Docker downloads the image layers again and reports `Downloaded newer image`.

Migration 005 must measure whether image acquisition can be reduced or reused economically on disposable GitHub-hosted runners. An explicit image cache is not automatically better: cache transfer/storage can itself cost more than pulling from GHCR, so this must be measured rather than assumed.

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
- evidence distinctions are correct but may be shaping too much visible build architecture;
- Moon and SCons both make reuse decisions and need a clearer coarse-versus-fine boundary;
- two synthetic Moon roots encode a real source-impact versus publication-context distinction, but that distinction may not need to be visible in every consumer;
- common inputs/configuration are repeated through many tasks;
- the impact check is highly valuable for unaffected changes but adds several seconds to affected changes;
- Docker image acquisition dominates the small reference build and is not explicitly cached today;
- same-job workflow-artifact upload and sequential publication may contain avoidable overhead.

See [architecture-reflection.md](architecture-reflection.md) for the complete assessment.

## Candidate directions

No target is selected yet. At minimum Migration 005 will compare:

1. **keep Moon but shrink the consumer contract** — standard SCAD Moon policy lives in `tool.scad-project`, consumers declare only project-specific capabilities/inputs;
2. **use coarser Moon capability tasks** — align Moon more closely with complete Build/Verification producers and hide finishing mechanics;
3. **remove Moon from the SCAD consumer surface** — considered as a control, but only acceptable if affected selection/output reuse can be replaced without inventing worse custom orchestration;
4. **retain the current responsibility model but optimize runtime/lifecycle** — useful as a low-risk comparison, though it would not solve consumer complexity by itself.

## Required measurements before selecting a target

- Docker image transfer/layer/unpack/startup costs;
- Moon impact-check sub-costs;
- actual value/hit rate of Moon output hydration versus SCons caching;
- bootstrap/tool-submodule overhead;
- artifact staging/upload overhead;
- Build/Verification publication cost and possible safe overlap;
- configuration complexity for both simple clamps and richer HUB75 examples.

## Human-understandability acceptance test

Give a maintainer a normal consumer repository plus one linked current-architecture page.

Without migration history or chat logs, that maintainer must be able to explain:

- what happens after README-only, CAD-source, Build-only and Verification-only changes;
- why Moon exists;
- what Moon decides versus what SCons decides;
- why each consumer-visible task/capability is separate;
- what is cached and where;
- where generated output and source/tool information come from;
- where most CI time is spent;
- why the chosen architecture is worth its complexity.

If that cannot be answered, the architecture is not finished.

## First phase

Do **not** migrate the HUB75 frame yet.

First:

1. finish the current-architecture reconstruction and performance breakdown;
2. measure Moon cache value and Docker/runtime costs;
3. create concrete simpler configurations for the simple clamps and richer HUB75 cases;
4. compare the candidate architectures on clarity, correctness, latency and total compute;
5. select the target architecture with explicit reasons;
6. only then derive implementation steps and repository owners.

The HUB75 frame remains on its previous qualified `tool.scad-project v0.12.0` / `lib.scad.hub75 v0.1.3` setup until that decision is made.
