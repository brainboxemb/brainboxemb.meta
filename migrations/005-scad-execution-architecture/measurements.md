# Migration 005 — measured architecture evidence

Status: **working measurement baseline**

This document keeps measured facts separate from architecture assumptions. It is not a target design.

Related:

- [Migration 005 README](README.md)
- [Current architecture](current-architecture.md)
- [Architecture reflection](architecture-reflection.md)
- [Target variants](target-variants.md)
- [Publication-path analysis](publication-analysis.md)
- [Resource-efficiency criteria](resource-efficiency.md)
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

The old topology also used two simultaneous heavy hosted runners. Migration 005 therefore treats wall-clock latency and total compute/resource use as separate metrics rather than declaring either topology better from elapsed time alone.

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

A controlled rerun of that same exact-main run behaves the same way again: the disposable runner does not have the image and all layers are pulled before production starts.

### HUB75 library

Exact-main run `34976840416` also pulls all 11 layers and reports `Downloaded newer image`; the image acquisition is again roughly 19–20 seconds.

### Toolchain repository itself

`brainboxemb/docker.scad-toolchain` release build run `34459109789` uses Buildx with image push and `load: false`. Its later smoke test cannot find the just-built image in the normal Docker image store and pulls the published image again. That pull is roughly 23 seconds.

This corroborates that runtime distribution is a first-order cost, not a one-off anomaly in a consumer workflow.

## 3. Moon runtime itself also has a transfer cost

The pinned Moon runtime cache is about **20.9 MB** in the observed logs.

When present, restoring/extracting it has been around 1–2 seconds. When absent, the workflow installs/downloads Moon and saves this cache at the end of the run.

The controlled clamps rerun gives a cleaner warm measurement:

- restore pinned Moon runtime: about **1.6 s**;
- Moon affected query itself after restore: about **1.7 s**;
- upload compact pre-check evidence: about **0.8–0.9 s**.

So even with the Moon binary already cached, the current pre-container path is still roughly four seconds once setup/evidence are included.

This is much smaller than the SCAD Docker image pull, but material relative to a 4–5 second unaffected lifecycle.

## 4. Impact detection value is proven

Migration 004 isolated input classes and demonstrated that Moon can distinguish which high-level domain is directly affected.

Examples from `lib.scad.hub75`:

- Build-only proof run `34976316887`: direct source impact on `scad.build`, not direct docs/verify source impact;
- docs-only proof run `34976333875`: direct source impact on `scad.docs`;
- Verify-only proof run `34976347095`: direct source impact on `scad.verify`;
- README-only proof run `34976305647`: `affected=false` and no SCAD image/container path.

This is concrete evidence for Moon's **impact-analysis role**.

## 5. Qualification runs did not demonstrate Moon output-cache benefit

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

### Clamps exact main — original attempt

Run `34972350665`, attempt 1, reports a portable Moon cache miss and both SCons cache misses. It executes:

- Verify: about **2.394 s**, task hash prefix `dc7f4445`;
- docs: about **4.720 s**, task hash prefix `879c5882`;
- complete Moon graph: about **5.453 s**.

It then saves a portable Moon cache of roughly **259 KB** under the run/attempt-specific primary cache key.

At this point the only safe conclusion was that output hydration had not yet been demonstrated.

## 6. Controlled identical production rerun: Moon archive restores, tasks still miss

Migration 005 reran the exact same qualified clamps job instead of changing source.

Controlled case:

- workflow run: `34972350665`;
- original attempt source: exact main `c5732944c8c2ba840a3f0f2f0a0638430a796cfd`;
- rerun: attempt 2 of the same workflow run/event/source;
- attempt-2 job: `104427368493`.

### Cache restore result

The rerun successfully restores the portable Moon cache from attempt 1:

```text
Cache hit for:
tool-git-project-moon-2.5.4-Linux-lib-scad-clamps-production-v1-34972350665-1

Cache Size: ~0 MB (258877 B)
Cache restored successfully
```

This removes the earlier ambiguity around PR/main cache visibility. The archive is definitely available to the rerun.

### But Moon does not hydrate the tasks

Despite the restored archive, Moon executes the real tasks again:

| Task | Attempt 1 hash | Attempt 2 hash | Attempt 2 result |
| --- | --- | --- | --- |
| docs | `879c5882` | `c764aedd` | executes again, ~4.524 s |
| Verify | `dc7f4445` | `78925029` | executes again, ~2.291 s |
| Verification finishing | `46f41c1d` | `6f9222e2` | executes again |
| Build index | `6d7bff36` | `12eef076` | executes again |
| Build finishing | `845cb882` | `bd7ae899` | executes again |
| full root | `51af155f` | `d263a5f9` | completes again |

Attempt-2 graph time is about **5.270 s**, almost the same as the original ~5.453 s.

Therefore the portable cache archive works mechanically, but task identity is unstable.

## 7. Diagnostic proof: generated Python bytecode causes the unstable Moon hash

A temporary non-merge diagnostic PR in `lib.scad.clamps` was used to inspect the full Moon hash manifest on fresh hosted runners.

Diagnostic source commit:

```text
9029a9e010900029d42e444a2e8792313c72cd27
```

Workflow run:

```text
34985150733
```

The same diagnostic job was executed twice against that exact same commit:

- attempt 1 job: `104435229590`;
- attempt 2 job: `104435489526`.

### What happens before Moon hashes the task

The production lifecycle runs the Python-based tooling check before executing the Moon aggregate graph:

```text
bash tools/tool.scad-project/scad-project.sh tooling-check
```

On a fresh checkout there is initially no Python bytecode tree. Immediately after `tooling-check`, Git reports the ignored runtime directory:

```text
!! src/scad_project/__pycache__/
```

and multiple files such as:

```text
tools/tool.scad-project/src/scad_project/__pycache__/cli.cpython-312.pyc
tools/tool.scad-project/src/scad_project/__pycache__/docs.cpython-312.pyc
tools/tool.scad-project/src/scad_project/__pycache__/verification.cpython-312.pyc
```

### Moon includes those generated files in the task hash

The consumer `scad.docs` task has this broad input:

```text
tools/tool.scad-project/**
```

Moon's generated task-hash manifest explicitly contains the `.pyc` files under that glob, even though they are ignored by Git.

For example, the attempt-1 manifest includes bytecode hashes such as:

```text
__init__.cpython-312.pyc = 0848357a...
cli.cpython-312.pyc      = 2e01662c...
docs.cpython-312.pyc     = 9c448452...
```

The exact same source on attempt 2 produces different runtime bytecode hashes:

```text
__init__.cpython-312.pyc = e3c26e8c...
cli.cpython-312.pyc      = 4669ea53...
docs.cpython-312.pyc     = 870aab63...
```

All checked-in `.py`, SCAD, project and Moon configuration inputs remain the same.

### Resulting task hashes

The full `scad.docs` task hash changes solely under this otherwise identical fresh-runner setup:

| Diagnostic attempt | Exact source | `scad.docs` task hash |
| --- | --- | --- |
| 1 | `9029a9e...` | `5cdd39337e7445531c8810dcb993519cb9fc59aa04090f0c913cbca3c29528a2` |
| 2 | `9029a9e...` | `a4117e6b5ab8d07be33a0d3cac836d89343f7c2c715554949abd03d93a8b1ce8` |

The workspace-graph hash remains stable (`d3de481f...`), which further localizes the instability to task inputs rather than the Moon workspace definition itself.

### Proven conclusion

The root cause is now established:

> **Generated Python bytecode created before Moon execution is captured by the broad `tools/tool.scad-project/**` task input and makes source-derived Moon task hashes unstable across fresh runners.**

This is an integration/configuration defect, not evidence that Moon is inherently unable to hydrate outputs.

The next experiment must remove this accidental runtime state from task identity—for example by preventing bytecode creation before hashing or by defining a source-only tool input boundary—and then repeat a genuinely warm output-cache run.

## 8. SCons cache value is also not established by these runs

The same exact-main and controlled rerun show normal and verification SCons cache misses. Consequently they do not prove normal cross-run SCons object-cache savings either.

Unlike Moon, SCons has already demonstrated value as the in-run fine-grained target engine: its manifests identify individual render/export targets and current/built/cache-restored states.

Migration 005 should therefore separately measure:

1. SCons as a dependency engine inside one execution;
2. SCons object-cache reuse across hosted runs;
3. Moon whole-task output hydration across hosted runs after task identity is stabilized.

These are three different benefits.

## 9. Publication cost

Representative clamps final run `34971400621` spends roughly 4.4 seconds publishing Build and Verification sequentially after production.

HUB75 exact-main run `34976840416` shows approximately:

- Build generated-branch publication: ~3.0 s;
- Verification publication: ~2.2 s.

They are currently serialized.

Before those publications, the workflow also uploads retained Build and Verification workflow artifacts from the same host job.

The separate [publication analysis](publication-analysis.md) shows that these normal artifacts are not used as a hand-off to the subsequent same-job branch publications. Release has its own separate artifact hand-off lifecycle.

## 10. Current measured conclusions

What is already supported by evidence:

- zero-container unrelated changes are a substantial win in both latency and heavy-compute avoidance;
- Moon impact detection is a real useful capability;
- image acquisition is the dominant single small-repository cost;
- reducing two containers/runners to one reduces duplicated compute but did not improve relevant-change latency;
- the old parallel topology's ~37 s result therefore must be evaluated against its higher total runner/VM use, not treated as a free speed baseline;
- current consumer Moon graphs expose much more than the few domain capabilities maintainers naturally think about;
- the Moon portable archive can restore correctly;
- current whole-task reuse failed because broad task inputs include generated `.pyc` runtime files and produce unstable hashes across fresh runners;
- this hash problem is an integration defect and can now be isolated for a corrected warm-cache experiment;
- current SCons cross-run cache benefit is also not demonstrated by the retained qualification/rerun evidence;
- normal full-tree workflow artifacts are retention policy, not a technical same-job publication hand-off.

What remains to measure before architecture selection:

- stable Moon output hydration after removing generated runtime state from task identity;
- exact image compressed size and per-layer composition;
- download versus unpack/startup contribution to the ~20 s image cost;
- explicit OCI/image-cache restore cost versus GHCR pull cost;
- controlled warm SCons cache behavior;
- necessity of each retained normal workflow artifact;
- safe parallelization or combination of generated-output publication;
- total runner-minutes and heavy-runner concurrency for each architecture candidate, not only wall-clock latency.
