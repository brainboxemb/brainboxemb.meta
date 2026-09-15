# Migration 005 — measured architecture evidence

Status: **validation baseline complete; implementation must remeasure final end-to-end results**

## Why this document exists

This is the consolidated measurement baseline behind the Migration-005 architecture decision. Read it when you need the actual timings, byte counts, cache behaviour or comparison points used to justify the selected design. Individual experiments remain in the linked validation documents.

Related:

- [12 — SCons warm-cache validation](12-scons-cache-validation.md)
- [14 — Runtime image validation](14-runtime-image-validation.md)
- [16 — Publication concurrency validation](16-publication-concurrency-validation.md)
- [18 — Moon inheritance validation](18-moon-inheritance-validation.md)
- [20 — Target resource budget](20-target-resource-budget.md)
- [Migration 004 performance evidence](../004-scad-repository-execution-model/performance-evidence.md)

## 1. Migration-004 execution baseline

Representative observations:

| Situation | Feedback / job class | Heavy runtime model |
| --- | ---: | --- |
| old parallel Build + Verify | ~37 s relevant critical path | 2 simultaneous heavy jobs |
| v0.13.0 one-runner | ~64–65 s | 1 heavy job |
| v0.13.1 normal relevant | ~41–45 s typical | 1 heavy job |
| README-only v0.13.1 | ~4.4–4.8 s | zero CAD image/runtime |

The old topology gave lower wall-clock feedback by duplicating runner/image/setup work. Migration 005 therefore never treats wall-clock time alone as the resource metric.

## 2. Image acquisition dominates small affected runs

Current v0.13.1 explicitly cold-pulls `ghcr.io/brainboxemb/scad-toolchain:v0.4.1` on disposable hosted runners.

Observed full-image acquisition is commonly around 15–20 s and has reached roughly 23 s in toolchain smoke testing.

For comparison, the small clamps Moon/CAD output graph is only around five seconds of reported Moon task work in the Migration-004 reference.

Conclusion: runtime distribution is a first-order cost.

## 3. Moon change-impact has proven value

HUB75 isolated proof runs established independent impact classes:

- Build-only `34976316887`;
- docs-only `34976333875`;
- Verify-only `34976347095`;
- README-only `34976305647` -> `affected=false`, zero CAD image/runtime path.

Conclusion: Moon is useful as a repository-level change-impact engine before Docker.

## 4. Moon whole-capability reuse works when identity is stable

A controlled exact-source clamps rerun initially restored a Moon cache archive but still changed task hashes.

Root cause was identified experimentally: the broad task input

```text
tools/tool.scad-project/**
```

included generated `src/scad_project/__pycache__/*.pyc` files. Fresh runners generated different bytecode hashes even though checked-in source was identical.

Controlled stable source `eb996a8a80ff4fb5dab60f5d30d53c13c6964c27`, run `34985629638`, proved the corrected behaviour:

- identical docs task hash across fresh runners;
- Moon reported `consumer:scad.docs (cached, 2ms, d068e1ad)`;
- cached wrapper/materialisation path ~1.322 s;
- cold wrapper path ~5.3 s, with about four seconds of actual docs render work avoided.

Conclusion: Moon whole-capability reuse is real; source identity must exclude generated runtime state.

## 5. SCons is project/capability-specific

### Clamps/direct

`lib.scad.clamps` has no `build_engine` selection and uses the direct engine.

Diagnostic run `34986143350` completed direct design-build with no `.cache/scad-project/scons` directory. Generic SCons cache handling has no value there.

### HUB75/SCons

`lib.scad.hub75` selects:

```yaml
build_engine:
  engine: scons
```

Controlled exact-source warm rerun of `34976840416` restored a ~222 KB normal SCons cache on a fresh VM:

- 2/2 presentation targets restored;
- 26/26 documentation targets restored;
- presentation Build ~2.0 s -> **0.430 s**;
- design docs ~8.07 s -> **0.602 s**;
- complete Moon graph ~8.805 s -> **5.071 s**;
- Verification remained ~4.403 s real work;
- separate Verification SCons cache was not populated.

Conclusion: SCons remains valuable inside SCons-enabled capabilities but must not be a generic cache layer for every repository.

## 6. Runtime image family measurement

Exact candidate source:

```text
eeb40e7eff98e98d754baf8ddb52376a17ecef18
```

Controlled external cold-vs-cold qualification:

- run `34992630534`;
- one hosted Ubuntu 24.04 VM;
- Docker state deliberately cleared between profile pulls for the benchmark only.

| Profile | Compressed OCI bytes | Unpacked bytes | Controlled cold pull |
| --- | ---: | ---: | ---: |
| OpenSCAD-focused | 328,098,501 | 961,779,232 | 13.211 s |
| full/dual | 449,516,893 | 1,313,898,129 | 15.464 s |

Difference:

- **121,418,392 fewer compressed bytes**;
- about **27.0%** lower registry payload;
- about **26.8%** lower unpacked image size.

Both profiles passed the shared OpenSCAD/BOSL2/SCons/docs/watermark contract. The full profile additionally passed PythonSCAD/pybosl2 coverage and retained existing interoperability XFAILs.

A later normal qualification run `34993290359` avoided the broad prune and reused shared layers. After the OpenSCAD profile, the full profile needed only its three extra layers and pulled those in about 5.185 s in that sample.

Conclusion: one multi-stage image family with shared layers is justified; routine CI should reuse layers rather than recreate an artificial cold-vs-cold benchmark.

## 7. Normal artifact retention measurement

Normal production currently uploads complete Build and Verification trees before publishing the same staged output to generated branches.

Representative compressed Actions-artifact sizes:

- clamps Build + Verification: ~245 KB;
- HUB75 Build + Verification: ~695 KB.

Observed upload action time in representative relevant runs:

- clamps rerun `34972350665`: roughly 3 s combined;
- warm HUB75 `34976840416`: roughly 2 s combined.

No normal downstream workflow was found downloading those artifacts. Release has its own exact-source cross-job artifacts and downloads.

Conclusion: complete normal full-tree artifacts are duplicate retention, not a technical publication hand-off. Keep compact evidence; make full normal artifacts opt-in if a future use case requires them.

## 8. Same-runner publication concurrency

Controlled run `34994181268` called the released `tool.git-project` publisher twice concurrently on one Ubuntu runner.

Measured small-tree publication:

- Build: 2.089 s;
- Verification: 2.144 s;
- overlap: 2.089 s;
- concurrent window: 2.144 s;
- sequential duration sum: 4.233 s.

Both temporary branch trees contained the exact source SHA and cleanup removed both branches.

Conclusion: Build/Verification publication is safely isolated and may overlap on the same runner. The measured two-second difference is diagnostic-tree-specific and is not a fixed production saving promise.

## 9. Shared Moon inheritance

Final configuration-only qualification:

- run `34997339916`;
- Moon 2.5.4;
- one Ubuntu runner;
- zero Docker/CAD runtime;
- exact clamps/HUB75 released sources;
- shared task prototype `tool.scad-project@1303ae8c40817a98f9615a58762264b3ef19b6dd`.

Proved effective capabilities:

```text
clamps
  Design documentation
  Verification

HUB75
  Presentation renders
  Design documentation
  Verification
```

Shared commands, stable common tool inputs, standard output boundaries and cache policy were inherited. Consumer configuration contained only capability selection plus project-specific source-impact inputs. A synthetic `.pyc` file did not become a task input.

Conclusion: native Moon inheritance is sufficient; no custom config generator is necessary.

## 10. Representative one-runner step budgets

### Clamps rerun `34972350665` attempt 2

Hosted job about 49 s:

- source/base + preflight/evidence/cache setup: roughly low-teens seconds including action overhead;
- full image pull: ~19 s;
- aggregate CAD/Moon step: ~9 s;
- complete normal full-tree artifact uploads: ~3 s;
- direct project nevertheless paid generic SCons restore actions;
- one runner, one CAD runtime.

### HUB75 run `34976840416` attempt 2

Hosted job about 37 s:

- pre-runtime host setup: ~7 s after runner setup;
- full image pull: ~16 s;
- aggregate CAD/Moon step: ~8 s at Actions granularity / ~5.071 s internal graph;
- useful normal SCons transfer: ~1 s-class action;
- complete normal artifact uploads: ~2 s;
- separate Verification SCons path unused;
- one runner, one CAD runtime.

These samples anchor the target budget but do not remove network variance.

## 11. Final measured conclusions

Architecture selection is supported by evidence that:

- unrelated changes should stop before Docker;
- Moon change-impact is useful;
- Moon whole-capability hydration works with stable source-only identity;
- broad tool globs must be replaced by explicit source-controlled inputs;
- SCons is useful only for configured target engines;
- image distribution dominates small affected runs;
- an OpenSCAD-focused image removes about 27% of full-image compressed distribution;
- normal complete Actions artifacts are duplicate retention in the current same-job publication path;
- Build and Verification publication can overlap safely on one runner;
- native shared Moon task inheritance reduces the consumer model to real capabilities plus source-impact rules.

No architecture measurement remains open before implementation planning.

Implementation must now remeasure the complete lifecycle on the two canaries:

1. clamps — full/dual runtime + direct engine;
2. HUB75 — OpenSCAD-focused runtime + SCons.

Those measurements determine whether the final implementation meets [20 — Target resource budget](20-target-resource-budget.md) and whether any validated assumption needs correction before downstream migration.
