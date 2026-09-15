# Migration 005 — current SCAD execution architecture

This document describes the **current released architecture** before Migration 005 changes it.

The goal is that a maintainer can understand the flow without knowing the migration history or CI-specialist terminology.

## Plain-language glossary

| Plain-language term | Technical term currently used | Meaning |
| --- | --- | --- |
| impact check | preflight / affected check | A cheap check before the SCAD runtime is downloaded. It answers: does this change require CAD-related work? |
| output-making task | producer | A task that actually renders, exports, generates design documentation or runs verification. |
| finishing task | finalization task | A small task that prepares already-generated output for publication, for example an index or source-information file. |
| source-information file | provenance | A file stored with generated output that records which source/tooling produced it. |
| full production graph | aggregate task / `scad.ci` | The Moon entry point that asks for all output needed by normal CI. |
| impact graph | `scad.production-impact` | The Moon entry point used only to decide whether the expensive SCAD runtime is needed. |
| SCAD runtime | Docker image/container | The immutable image containing OpenSCAD, PythonSCAD, SCons and related tooling. |

The architecture may continue to use the technical terms internally, but a project maintainer should not need those terms to understand the normal flow.

## Current normal-CI flow

There are two materially different paths.

### Path A — a change that does not affect CAD output

Example: a root `README.md` edit.

```text
GitHub runner starts
  -> check out the exact changed revision
  -> fetch only the comparison revision
  -> run the impact check
  -> result: no CAD work required
  -> stop

No SCAD image is downloaded.
No SCAD container starts.
No generated Build/Verification output is published.
```

Measured on `lib.scad.clamps`, this path is about **4.4–4.8 seconds**.

This is the clearest successful performance result inherited from Migration 004.

### Path B — a change that affects CAD output

```text
GitHub runner starts
  -> check out exact source + comparison revision
  -> run the impact check
  -> restore Moon/SCons caches
  -> download the SCAD Docker image
  -> start one Docker process
       -> bootstrap repository tool submodules
       -> validate tool versions
       -> run the Moon output graph
            -> create real Build/docs/Verification output
            -> create indexes/source-information files
  -> leave Docker
  -> validate and stage generated trees
  -> upload temporary workflow artifacts
  -> publish Build output
  -> publish Verification output
  -> save orchestration cache / cleanup
```

Representative `lib.scad.clamps` run `34971400621` takes about **41–45 seconds** using the Migration-004 comparison boundary. The full runner log including action setup and cleanup spans about 48 seconds.

## Where relevant-change time currently goes

| Phase | Approx. time | Plain-language purpose |
| --- | ---: | --- |
| source/base preparation | 1.9 s | Get only the two Git revisions required to decide impact. |
| impact check + evidence | 4.7 s | Decide whether CAD work is required and retain that decision. |
| Moon/SCons cache + range preparation | 1.9 s | Restore reusable task/object state. |
| **SCAD Docker image download** | **20.0 s** | Download `ghcr.io/brainboxemb/scad-toolchain:v0.4.1`. |
| container bootstrap + validation + output graph | 9.4 s | Initialize tools and execute all requested work. |
| of which Moon graph execution itself | **5.132 s** | Real output tasks plus small finishing tasks. |
| staging + workflow-artifact upload | 2.6 s | Prepare copies for publication/evidence. |
| Build + Verification publication | 4.4 s | Push the two generated-output branches sequentially. |
| post-job cache/cleanup | ~1.4 s | Save orchestration state and clean up. |

The most important observation is therefore:

> On the small reference library, the actual output graph takes about five seconds while the Docker image download alone takes about twenty seconds.

The architecture must be judged primarily on this critical path, not on the number of Moon tasks or containers in isolation.

## Docker image behaviour today

The current reusable workflow explicitly runs:

```text
docker login ghcr.io
docker pull ghcr.io/brainboxemb/scad-toolchain:v0.4.1
docker run ...
```

The workflow explicitly caches Moon state and SCons object state. It does **not** explicitly cache the Docker/OCI image or Docker layer store.

In representative affected run `34971400621`, Docker reports every image layer being pulled/downloaded and ends with `Downloaded newer image`. The observed pull itself occupies about twenty seconds on the serial critical path.

GitHub-hosted runners are disposable execution environments, so Migration 005 must not assume that a previously run job has left the image available locally. Any proposed image reuse must be measured and designed explicitly.

This is now a first-order architecture/performance question rather than a minor implementation detail.

## What Moon currently exposes in a consumer repository

### `lib.scad.clamps`

The current `moon.yml` exposes seven tasks:

| Task | Plain-language role | Why it exists today |
| --- | --- | --- |
| `scad.docs` | output-making task | Generate design documentation. |
| `scad.build-index` | finishing task | Generate the Build-tree index after docs exist. |
| `scad.build-provenance` | finishing task | Write source/tool information into the Build tree. |
| `scad.verify` | output-making task | Generate/run verification output. |
| `scad.verification-provenance` | finishing task | Write source/tool information into the Verification tree. |
| `scad.production-impact` | impact-only root | Let the host ask whether docs or verification source changed without considering CI-context-only finishing tasks. |
| `scad.ci` | full-execution root | Ask Moon for the complete publishable Build + Verification result. |

### `lib.scad.hub75`

HUB75 has the same structure plus a separate `scad.build` output-making task for standalone presentation renders, so it exposes eight tasks.

This difference is legitimate domain behaviour: HUB75 genuinely has three independent types of generated work (`docs`, standalone `build` renders and `verify`) while clamps has two.

The question for Migration 005 is not whether those domain differences exist. The question is how many of the **finishing/orchestration details** need to remain visible in every consumer `moon.yml`.

## Why two Moon roots exist today

The current model has both `scad.production-impact` and `scad.ci`.

In ordinary language:

- the **impact root** asks only whether source changes require expensive work;
- the **full root** asks for all publishable output, including files whose content depends on the current GitHub event/ref/PR context.

They were separated because event/ref context can change even when CAD source does not. If those context-dependent finishing files participate in the impact decision, an unrelated change can incorrectly look like CAD work and trigger the Docker image.

That is a real correctness/performance concern. It does **not** automatically prove that two visible roots are the simplest possible interface.

## Current architecture boundaries

The current responsibilities are roughly:

| Layer | Current responsibility |
| --- | --- |
| GitHub Actions host | exact source selection, impact check, caches, image pull, Docker start, retained artifacts, publication |
| Moon | repository-level dependency graph and task-level affected/cache behaviour |
| `tool.scad-project` | reusable commands for docs/build/verification/index/source-information and shared workflow |
| SCons | fine-grained SCAD target dependency/rebuild logic inside the domain work |
| consumer repository | declares Moon inputs/outputs/dependencies and project-specific SCAD configuration |

Migration 005 should test whether this division makes consumers express too much mechanism instead of intent.

## Complexity that is clearly justified today

These behaviours have demonstrated value and should not be removed casually:

- unrelated changes can finish without downloading the SCAD image;
- uncertain impact runs safely instead of skipping required work;
- Build and Verification remain independently meaningful;
- exact source/tool versions remain attached to generated output;
- GitHub write credentials remain outside the SCAD runtime;
- SCons retains fine-grained dependency-aware rebuild behaviour.

## Complexity candidates that require challenge

These are not declared wrong yet. They are explicitly open questions for Migration 005.

1. **Docker image distribution dominates the critical path.** The workflow does not explicitly cache the image, and the representative affected run downloads all layers again. Determine image size/layer composition, whether GHCR/network/decompression dominates, and whether an explicit safe reuse strategy is worthwhile.
2. **The impact check costs ~4.7 s.** That is excellent compared with a 20 s image pull when the answer is “unaffected”, but pure overhead when work is affected. Determine whether runtime restore/evidence can be cheaper without weakening conservative behaviour.
3. **Consumer Moon files repeat orchestration detail.** Inputs for project/tool/workflow context recur across several tasks. Determine what can be generated/inherited from shared tooling.
4. **Build finishing is split into index and source-information tasks.** Determine whether that separation has an actual caching/evidence benefit or is historical implementation detail.
5. **Two visible root tasks are conceptually difficult.** Preserve the semantic distinction if needed, but investigate whether the consumer needs to see both.
6. **Temporary workflow artifacts are uploaded before same-job publication.** Determine which uploads are required for retained evidence/release reuse and which are avoidable duplication.
7. **Build and Verification publication is sequential (~4.4 s).** Determine whether safe overlap or one publication primitive can reduce latency.
8. **Repository tool submodules are bootstrapped after the image pull.** Determine whether this work is necessary in its current form or can be reduced without losing exact pinning.
9. **Relevant-change latency regressed.** The old parallel baseline is ~37 s; the current one-host model is ~41–45 s. A successor architecture must explain and justify any remaining regression rather than using “one container” as a proxy for speed.
10. **The HUB75 frame has deliberately not been migrated.** Do not propagate the current architecture until the target is selected.

## Immediate Phase-1 questions

The first architecture work should answer these in this order:

1. Why does acquiring the SCAD runtime cost ~20 s and what part of that is downloadable bytes versus extraction/startup?
2. Can that runtime cost be materially reduced or reused on disposable GitHub-hosted runners without creating a larger cache-transfer cost?
3. After runtime cost, what host orchestration on the critical path can be removed, combined or overlapped?
4. Which Moon tasks represent real independent domain work and which can disappear behind a smaller consumer-facing contract?
5. Which target variants preserve the zero-container unrelated path while meeting or beating the old ~37 s relevant-change baseline?

Only after those questions are measured should Migration 005 choose an implementation architecture.
