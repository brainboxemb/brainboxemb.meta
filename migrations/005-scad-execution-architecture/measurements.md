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

| Phase | Approx. time |
| --- | ---: |
| hosted-runner/action preparation | 1.9 s |
| source/base preparation | 1.9 s |
| Moon change-impact check + retained decision evidence | 4.7 s |
| Moon/SCons cache + range preparation | 1.9 s |
| SCAD Docker image pull | **20.0 s** |
| container bootstrap + validation + output graph | 9.4 s |
| Moon graph reported execution | **5.132 s** |
| validate/stage + workflow-artifact upload | 2.6 s |
| Build + Verification publication | 4.4 s |
| post-job cache/cleanup | ~1.4 s |

The Docker image acquisition is about four times as long as the complete reported Moon output graph on this small library.

The old parallel Build + Verify topology completed the relevant-change critical path in about **37 s**. The final one-host model is about **41–45 s**. The old topology used two simultaneous heavy hosted runners, so Migration 005 treats elapsed feedback time and total compute/resource use as separate metrics.

## 2. Docker runtime acquisition is repeatedly cold

The reusable v0.13.1 workflow explicitly performs:

```text
docker login ghcr.io
docker pull ghcr.io/brainboxemb/scad-toolchain:v0.4.1
docker run ...
```

It restores Moon and SCons cache state but does not restore an OCI image or Docker layer store.

Observed affected runs repeatedly pull all 11 image layers and report:

```text
Status: Downloaded newer image for ghcr.io/brainboxemb/scad-toolchain:v0.4.1
```

Representative image-acquisition times:

- final clamps Migration-004 sample: about 20 s;
- clamps exact-main and controlled reruns: roughly 15–20 s;
- HUB75 exact-main: roughly 19–20 s;
- toolchain repository smoke test after a Buildx push with `load: false`: roughly 23 s.

Runtime distribution is therefore a first-order cost, not a one-off anomaly.

## 3. Moon runtime and change-impact cost

The pinned Moon runtime cache is about **20.9 MB** in observed logs.

A warm clamps measurement shows approximately:

- restore/extract Moon runtime: ~1.2–1.6 s;
- Moon change-impact query: ~1.7–1.9 s;
- compact decision-evidence handling/upload adds additional lifecycle time.

The current pre-container change-impact path is therefore material relative to a 4–5 second README-only workflow, but still far smaller than the SCAD image pull that it avoids.

## 4. Moon change-impact analysis has proven value

Migration 004 isolated input classes in `lib.scad.hub75`:

- Build-only proof `34976316887`: Build directly affected;
- docs-only proof `34976333875`: design documentation directly affected;
- Verify-only proof `34976347095`: Verification directly affected;
- README-only proof `34976305647`: `affected=false`, no SCAD image/container path.

This is concrete evidence for Moon as a cheap repository-level change-impact engine.

## 5. Why the original Moon output-cache qualification appeared ineffective

The Migration-004 qualification runs did not demonstrate warm whole-task reuse. A controlled rerun of exact clamps production run `34972350665` made the problem reproducible:

- attempt 2 restored the Moon cache archive saved by attempt 1 (~259 KB);
- nevertheless docs and Verify executed again;
- task hashes changed between the two attempts despite identical source.

Examples:

| Task | Attempt 1 | Attempt 2 |
| --- | --- | --- |
| docs | `879c5882` | `c764aedd` |
| Verify | `dc7f4445` | `78925029` |
| full root | `51af155f` | `d263a5f9` |

So the cache transport worked but task identity was unstable.

## 6. Root cause: generated Python bytecode polluted Moon task identity

A temporary non-merge diagnostic PR in `lib.scad.clamps` inspected Moon's full task-hash manifests on fresh hosted runners.

Diagnostic source commit:

```text
9029a9e010900029d42e444a2e8792313c72cd27
```

Workflow run `34985150733` executed the same diagnostic twice:

- attempt 1 job `104435229590`;
- attempt 2 job `104435489526`.

Before Moon executes the heavy graph, production runs the Python command:

```text
bash tools/tool.scad-project/scad-project.sh tooling-check
```

That creates:

```text
tools/tool.scad-project/src/scad_project/__pycache__/*.pyc
```

Consumer tasks use a broad input:

```text
tools/tool.scad-project/**
```

Moon's task-hash manifest includes those generated `.pyc` files even though Git ignores them. Their binary hashes differ between fresh runners, while checked-in source/config/tool revisions remain identical.

The same exact diagnostic source therefore produced two different full docs-task hashes:

- attempt 1: `5cdd39337e7445531c8810dcb993519cb9fc59aa04090f0c913cbca3c29528a2`;
- attempt 2: `a4117e6b5ab8d07be33a0d3cac836d89343f7c2c715554949abd03d93a8b1ce8`.

The Moon workspace hash remained stable, localising the instability to task inputs.

**Conclusion:** generated runtime state was accidentally treated as source. This is an integration/configuration defect, not an inherent failure of Moon caching.

## 7. Stable Moon warm-cache experiment succeeds

The diagnostic workflow was then changed so Python does not create bytecode before Moon hashes the source tree (`PYTHONDONTWRITEBYTECODE=1`). It ran docs only, saved Moon's task/output cache, and then reran the exact same job on a fresh hosted VM.

Controlled source:

```text
eb996a8a80ff4fb5dab60f5d30d53c13c6964c27
```

Workflow run:

```text
34985629638
```

Attempt 1 created the docs output and saved a ~146 KB portable Moon cache. The stable `scad.docs` hash was:

```text
d068e1adefa7bd425fe41debef031902248baee77eb9da41ee06fe46055a6633
```

Attempt 2 restored attempt 1's cache on another hosted runner and retained that exact same hash. Moon reported:

```text
consumer:scad.docs (cached, 2ms, d068e1ad)
Tasks: 1 completed (1 cached)
Time: 32ms
```

The `moon-project.sh` wrapper, including Moon startup/materialisation bookkeeping, took about **1.322 s** on the cached attempt. The cold attempt had required roughly **4 s** for the docs task itself and about **5.3 s** through the wrapper.

The render command output visible in the cached Moon log is replayed cached task output; Moon's own result (`cached`, 2 ms, one cached task) confirms that the render commands were not executed again.

### Interpretation

Moon whole-task output reuse is now **demonstrated**, not theoretical.

For this small clamps docs capability it avoids roughly four seconds of actual render work. That is useful compute avoidance, but it is still secondary to the 15–20 second fresh-runner Docker image pull. Because pull-time variance alone can exceed the ~4-second render saving, the end-to-end job stopwatch does not reliably show the cache benefit on this small project.

This is exactly why Migration 005 must measure both:

- work/compute avoided;
- wall-clock feedback latency.

## 8. SCons is not a universal SCAD cache layer

The reusable production workflow currently attempts to restore two SCons cache directories for every affected SCAD repository:

```text
.cache/scad-project/scons
.cache/scad-project/verification-scons
```

Whether they can have value depends on the project's selected execution engine.

### Clamps: direct engine, no SCons cache exists

`lib.scad.clamps` has no `build_engine` configuration. `tool.scad-project` therefore selects its default `direct` engine.

A dedicated diagnostic run `34986143350` executed a complete successful clamps `design-build` directly through `tool.scad-project`. Result:

```text
cache directory absent
```

After the build, `.cache/scad-project/scons` still did not exist. GitHub's cache action consequently reported:

```text
Path Validation Error: Path(s) specified in the action for caching do(es) not exist, hence no cache is being saved.
```

This matches the earlier normal production rerun where both SCons save steps were skipped.

For clamps, generic SCons cache restore/save handling is therefore lifecycle overhead with no functional benefit.

### HUB75: SCons is explicitly configured and its cache is populated

`lib.scad.hub75` explicitly declares:

```yaml
build_engine:
  engine: scons
```

Its exact-main production run `34976840416` completed `Save normal SCons object cache` successfully. The Verification SCons cache save remained skipped because that Verification path does not populate the separate verification cache directory.

So SCons itself is not dead architecture. It is a project/capability-level choice whose cache handling should be activated only where the effective project configuration says it is used.

### Architecture implication

Do not model “Moon cache + normal SCons cache + Verification SCons cache” as three unconditional standard layers.

Instead:

- Moon may cache complete source-derived capabilities;
- SCons may provide fine-grained target reuse **inside capabilities configured to use SCons**;
- direct capabilities should not pay SCons cache restore/save overhead;
- each cache must have one clear scope and measurable reason to exist.

A controlled warm HUB75 SCons reuse measurement is still useful before final architecture selection, but the ownership boundary is already clear.

## 9. Publication cost and artifact retention

Representative clamps final run `34971400621` spends roughly 4.4 s publishing Build and Verification sequentially after production.

HUB75 exact-main `34976840416` shows roughly:

- Build generated-branch publication: ~3 s;
- Verification publication: ~2 s.

The normal workflow also uploads full Build and Verification workflow artifacts before branch publication. Those artifacts are **not** downloaded for the same-job publications. Release uses a separate cross-job artifact lifecycle.

Normal full-tree artifacts are therefore retention/download policy, not a technical data-transfer requirement of current normal CI.

## 10. Resource-efficiency interpretation

The old ~37-second parallel topology and the current ~41–45-second one-runner topology optimize different metrics:

- old: lower wall-clock latency, two simultaneous heavy hosted runners and duplicated image/setup work;
- current: one heavy runner and less duplicated infrastructure, but somewhat slower relevant feedback;
- README-only current path: best on both axes because expensive work is removed entirely.

Migration 005 therefore records total runner-minutes, maximum heavy-runner concurrency, repeated image/setup work and avoidable execution alongside elapsed feedback time.

## 11. Current measured conclusions

Supported by evidence:

- README-only zero-container handling is a substantial latency and resource win;
- Moon change-impact analysis is useful;
- Moon whole-task output hydration **does work** once task identity contains only stable source-derived inputs;
- broad tool globs currently admit generated `.pyc` state and must be corrected;
- on small clamps, Moon avoids about four seconds of docs rendering but Docker image distribution still dominates the lifecycle;
- SCons is meaningful for SCons-enabled capabilities, but clamps uses the direct engine and should not pay generic SCons-cache overhead;
- HUB75 does use SCons and successfully populated the normal SCons cache in qualified production;
- reducing two runners to one reduces duplicated compute but did not improve relevant-change latency;
- normal full-tree workflow artifacts are a retention choice rather than a current same-job hand-off requirement;
- current consumer Moon graphs expose more lifecycle mechanics than maintainers need to author directly.

Remaining measurements before selecting/finalising the target architecture:

- controlled warm HUB75 SCons reuse and its real saving;
- SCAD image compressed/layer composition and realistic image-reuse alternatives;
- necessity/policy for normal retained full-tree artifacts;
- safe overlap or combination of Build/Verification branch publication;
- configuration size and human readability of the leading architecture variants;
- total runner-minutes and concurrency for each candidate, not only wall-clock latency.
