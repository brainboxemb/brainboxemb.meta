# Migration 005 — measured architecture evidence

Status: **working measurement baseline**

This document keeps measured facts separate from architecture assumptions. It is not a target design.

Related:

- [Migration 005 README](README.md)
- [Current architecture](current-architecture.md)
- [Architecture reflection](architecture-reflection.md)
- [Migration 004 performance evidence](../004-scad-repository-execution-model/performance-evidence.md)

## 1. Small-reference critical path — `lib.scad.clamps`

Representative final Migration-004 candidate run: `34971400621`.

Approximate elapsed time:

| Phase | Approx. time |
| --- | ---: |
| hosted-runner/action preparation | 1.9 s |
| source/base preparation | 1.9 s |
| Moon impact check + retained decision evidence | 4.7 s |
| Moon/SCons cache + range preparation | 1.9 s |
| SCAD Docker image pull | **20.0 s** |
| container bootstrap + validation + output graph | 9.4 s |
| Moon graph reported execution | **5.132 s** |
| validate/stage + workflow-artifact upload | 2.6 s |
| Build + Verification publication | 4.4 s |
| post-job cache/cleanup | ~1.4 s |

The important ratio is that the Docker image acquisition is about four times as long as the entire reported Moon output graph on this small library.

The old parallel Build + Verify topology completed the relevant-change critical path in about **37 s**. The final one-host model is about **41–45 s** under the Migration-004 comparison boundary.

## 2. Docker runtime acquisition is repeatedly cold

The reusable v0.13.1 production workflow explicitly runs:

```text
docker login ghcr.io
docker pull ghcr.io/brainboxemb/scad-toolchain:v0.4.1
docker run ...
```

It explicitly restores caches for:

- Moon task hashes/outputs;
- normal SCons object state;
- verification SCons object state.

It does **not** explicitly restore a Docker image, OCI archive or Docker layer store.

### Clamps

Run `34971400621` pulls all 11 image layers and ends with:

```text
Status: Downloaded newer image for ghcr.io/brainboxemb/scad-toolchain:v0.4.1
```

The pull step is about 20 seconds.

Exact-main clamps run `34972350665` behaves the same way: all 11 layers are pulled again and Docker again reports `Downloaded newer image`. The pull occupies roughly 17 seconds between beginning the pull and image availability, with login/registry setup around it.

### HUB75 library

Exact-main run `34976840416` also pulls all 11 layers and reports `Downloaded newer image`; the image acquisition is again roughly 19–20 seconds.

### Toolchain repository itself

`brainboxemb/docker.scad-toolchain` release build run `34459109789` uses Buildx with image push and `load: false`. Its later smoke test cannot find the just-built image in the normal Docker image store and pulls the published image again. That pull is roughly 23 seconds.

This corroborates that runtime distribution is a first-order cost, not a one-off anomaly in a consumer workflow.

## 3. Moon runtime itself also has a transfer cost

The pinned Moon runtime cache is about **20.9 MB** in the observed logs.

When present, restoring/extracting it has been around 1–2 seconds. When absent, the workflow installs/downloads Moon and saves this cache at the end of the run.

This cost is much smaller than the SCAD Docker image pull, but it is material relative to a 4–5 second unaffected path and must be included when evaluating the impact check.

## 4. Impact detection value is proven

Migration 004 isolated input classes and demonstrated that Moon can distinguish which high-level domain is directly affected.

Examples from `lib.scad.hub75`:

- Build-only proof run `34976316887`: direct source impact on `scad.build`, not direct docs/verify source impact;
- docs-only proof run `34976333875`: direct source impact on `scad.docs`;
- Verify-only proof run `34976347095`: direct source impact on `scad.verify`;
- README-only proof run `34976305647`: `affected=false` and no SCAD image/container path.

This is concrete evidence for Moon’s **impact-analysis role**.

## 5. Moon output-cache value is not yet demonstrated by the qualification runs

This must be kept separate from impact detection.

### HUB75 Build-only proof

Run `34976316887` correctly identifies Build as the direct changed domain before Docker starts.

However, the portable Moon cache is a miss. Once the aggregate `scad.ci` graph runs, docs and Verify are executed as well because no reusable Moon output is available for them.

### HUB75 docs-only proof

Run `34976333875` correctly identifies docs as the direct changed domain.

Again the portable Moon output cache is a miss. The aggregate graph therefore also executes Build and the full physical/API verification path.

### HUB75 exact main

Run `34976840416` again reports no portable Moon cache entry and no SCons cache entries for the relevant namespaces. It executes all three real domains:

- `scad.build`: about 2.0 s;
- `scad.verify`: about 5.15 s;
- `scad.docs`: about 8.07 s;
- total Moon graph: about 8.805 s because work overlaps inside the graph.

It then saves a portable Moon task/output cache of roughly **730 KB**.

### Clamps exact main

Run `34972350665` also reports a portable Moon cache miss and both SCons cache misses. It re-executes:

- Verify: about 2.4 s;
- docs: about 4.7 s;
- complete Moon graph: about 5.45 s.

It then saves a portable Moon cache of roughly **259 KB**.

### Interpretation

The qualification evidence therefore proves:

- Moon affected analysis can avoid the whole expensive runtime when nothing relevant changed;
- Moon can identify the directly affected domain.

It does **not yet prove**, from these observed runs, that Moon output hydration materially reduces a later affected run.

That does not establish that Moon caching is ineffective. The proof PRs ran close together and GitHub Actions cache availability/scope can prevent a just-created cache from being usable by another concurrent/PR/main context. Exact-main also crossed PR/main cache context boundaries.

The correct status for Migration 005 is therefore:

> **Moon output-cache benefit is currently unproven in retained Migration-004 evidence and must be measured separately.**

The architecture must not cite output hydration as a practical benefit until a controlled warm-cache experiment demonstrates it and quantifies the gain.

## 6. SCons cache value is also not established by these cold qualification runs

The same observed exact-main runs show SCons cache misses. Consequently they do not prove normal cross-run SCons cache savings either.

Unlike Moon, SCons has already demonstrated value as the in-run fine-grained target engine: its manifests identify individual render/export targets and current/built/cache-restored states.

Migration 005 should therefore separately measure:

1. SCons as a dependency engine inside one execution;
2. SCons object-cache reuse across hosted runs;
3. Moon whole-task output hydration across hosted runs.

These are three different benefits.

## 7. Publication cost

Representative clamps final run `34971400621` spends roughly 4.4 seconds publishing Build and Verification sequentially after production.

HUB75 exact-main run `34976840416` shows approximately:

- Build generated-branch publication: ~3.0 s;
- Verification publication: ~2.2 s;

They are currently serialized.

Before those publications, the workflow also uploads retained Build and Verification workflow artifacts from the same host job.

Migration 005 must identify which of these transfers are required for user/release evidence and which exist only because of an earlier multi-job design.

## 8. Current measured conclusions

What is already supported by evidence:

- zero-container unrelated changes are a substantial win;
- impact detection is a real useful capability;
- image acquisition is the dominant single small-repository cost;
- reducing two containers to one reduces duplicated compute but did not improve relevant-change latency;
- current consumer Moon graphs expose much more than the few domain capabilities maintainers naturally think about;
- current qualification evidence does not demonstrate warm Moon output hydration or warm SCons cross-run reuse.

What remains to measure before architecture selection:

- exact image compressed size and per-layer composition;
- download versus unpack/startup contribution to the ~20 s image cost;
- explicit OCI/image-cache restore cost versus GHCR pull cost;
- controlled warm Moon output-cache behavior and resulting producer skips;
- controlled warm SCons cache behavior;
- Moon impact-check sub-costs with warm and cold Moon runtime;
- necessity of each retained workflow artifact;
- safe parallelization or combination of generated-output publication.
