# Migration 005 — measured architecture evidence

Status: **complete — baseline and final implementation measurements recorded**

## Why this document exists

This document records both the measurements that selected the Migration-005 architecture and the final implementation evidence used to close the migration.

Related:

- [12 — SCons warm-cache validation](12-scons-cache-validation.md)
- [14 — Runtime image validation](14-runtime-image-validation.md)
- [16 — Publication concurrency validation](16-publication-concurrency-validation.md)
- [18 — Moon inheritance validation](18-moon-inheritance-validation.md)
- [20 — Target resource budget](20-target-resource-budget.md)
- [Migration 004 performance evidence](../004-scad-repository-execution-model/performance-evidence.md)

## 1. Starting point from Migration 004

Representative pre-Migration-005 observations:

| Situation | Feedback / job class | Heavy runtime model |
| --- | ---: | --- |
| old parallel Build + Verify | ~37 s relevant critical path | 2 simultaneous heavy jobs |
| v0.13.0 one-runner | ~64–65 s | 1 heavy job |
| v0.13.1 normal relevant | ~41–45 s typical | 1 heavy job |
| README-only v0.13.1 | ~4.4–4.8 s | zero CAD image/runtime |

The old parallel topology achieved lower wall-clock feedback by duplicating runner/image/setup work. Migration 005 therefore treated wall-clock latency and total resource use as separate acceptance dimensions.

## 2. Architecture-selection measurements

### Runtime image distribution

Controlled external qualification run `34992630534` measured:

| Profile | Compressed OCI bytes | Unpacked bytes | Controlled cold pull |
| --- | ---: | ---: | ---: |
| OpenSCAD-focused | 328,098,501 | 961,779,232 | 13.211 s |
| full/dual | 449,516,893 | 1,313,898,129 | 15.464 s |

The focused image removes **121,418,392 compressed bytes**, about **27.0%**, relative to the full image while retaining the shared OpenSCAD/BOSL2/SCons/docs/watermark contract.

### Moon whole-capability reuse

Stable-source clamps run `34985629638` proved source-derived capability reuse after removing generated Python bytecode from task identity:

- identical docs task hash on fresh runners;
- Moon result `consumer:scad.docs (cached, 2ms, d068e1ad)`;
- cached wrapper/materialization ~1.322 s versus ~5.3 s cold wrapper path.

### SCons warm-target reuse

Controlled HUB75 warm rerun of `34976840416` restored a ~222 KB normal SCons cache:

- presentation Build ~2.0 s -> **0.430 s**;
- design docs ~8.07 s -> **0.602 s**;
- complete Moon graph ~8.805 s -> **5.071 s**;
- Verification remained ~4.403 s real work;
- separate Verification-SCons cache was not populated.

Clamps direct-engine diagnostic `34986143350` produced no normal SCons cache at all, proving that generic SCons transport would be unused overhead there.

### Normal artifact retention

Representative complete normal Build + Verification Actions artifacts were roughly:

- clamps: ~245 KB compressed;
- HUB75: ~695 KB compressed.

No normal downstream workflow used those complete artifacts. Release has a separate exact-source cross-job hand-off. Migration 005 therefore removed duplicate complete normal artifacts by default while retaining compact decision/orchestration evidence.

### Same-runner publication concurrency

Controlled publisher run `34994181268` measured:

- Build: 2.089 s;
- Verification: 2.144 s;
- overlap: 2.089 s;
- concurrent window: 2.144 s versus 4.233 s sequential duration sum.

This validated isolated concurrent publishers on the same runner without adding another hosted VM.

### Shared Moon inheritance

Configuration-only run `34997339916` proved that native Moon inheritance can keep consumer configuration limited to visible capabilities plus project-specific source-family impact rules. No custom config generator was required.

## 3. Final released implementation

Final common baseline at closeout:

```text
docker.scad-toolchain   v0.5.0
tool.git-project        v0.2.8 / 7c43f37e7b07cfb57638a1d1dad2501de09ba7eb
tool.scad-project       v0.14.7 / 3935e5f86fe309b8908a05554f7ada336a6d6886
```

`tool.scad-project v0.14.7` released-tag owner test: `35084470257`.

The final normal production architecture has:

- one hosted job;
- one generic Moon affected query;
- zero planner/image/runtime work when no SCAD capability is affected;
- at most one CAD Docker process when materialization is required;
- runtime profile selected from project configuration;
- normal/Verification SCons transport only when applicable;
- compact retained orchestration evidence rather than duplicate full output artifacts;
- Build/Verification publication allowed to overlap on the same runner;
- durable phase timings and raw-log navigation;
- exact resolved source SHA carried through host publication provenance.

## 4. Final affected-canary measurements

### Clamps — full/dual runtime + direct engine

Canary run: `35026709686`.

Hosted job duration from runner log timestamps: approximately **41.9 s**.

Observed resource behaviour:

- one hosted job;
- one full/dual v0.5.0 runtime;
- direct engine;
- no normal SCons transport;
- no Verification-SCons transport;
- Moon whole-capability reuse available;
- Build/Verification publication succeeds on the same runner;
- compact normal evidence only.

Representative costs in the run included roughly 15.7 s for the full image pull and roughly 6.9 s for planner installation.

This run occurred while the migration itself changed the tool gitlink, before the later v0.14.4 exact-base-gitlink hardening. The impact decision therefore used conservative migration behaviour. Use this run as the final full/direct resource and affected-latency canary, not as proof of later precise selective impact.

Result: **meets the low/mid-40 s affected budget**.

### HUB75 — focused OpenSCAD runtime + SCons

Canary run: `35026885840`.

Hosted job duration from runner log timestamps: approximately **32.2 s**.

Observed resource behaviour:

- one hosted job;
- one focused OpenSCAD v0.5.0 runtime;
- SCons build engine;
- normal SCons cache restored (~222 KB);
- no Verification-SCons transport for command-only Verification;
- Moon capability cache restored;
- current materialization records for docs/build/verify were millisecond-class whole-capability cache restores;
- Build/Verification publication overlapped on the same runner;
- compact normal evidence only.

The focused image pull was still about 14.3 s in this sample, confirming that image acquisition remains a first-order cost even when capability output is highly reusable.

Like the clamps canary, this migration PR predates exact base-gitlink hardening and therefore used conservative impact classification while changing the tool gitlink. It remains valid warm/cached resource evidence; precise selective impact is proven by the later hardened reference/zero-runtime probes.

Result: **meets the low/mid-30 s warm affected budget**.

## 5. Cold migration-main observations

The first migrated main runs were slower than the warm canaries:

| Repository | Run | Approx. hosted job | Important context |
| --- | --- | ---: | --- |
| clamps | `35065375255` | ~48.1 s | full image, direct engine, cold/migration-conservative path |
| HUB75 | `35065383879` | ~47.1 s | focused image, SCons, cold/migration-conservative path |

These runs are retained as honest cold migration evidence. They should not be presented as steady-state selective-impact timing because they include tool-gitlink migration conditions and cold image/materialization costs that later hardening made more precise.

## 6. Final zero-runtime measurements

All three independent README-only probes prove the same structural path: Moon returns a precise empty affected set and every heavy stage is skipped.

| Consumer | Run | Hosted job wall time | Result |
| --- | --- | ---: | --- |
| `lib.scad.hub75` | `35065524524` | ~7.6 s | `success`, `[]`, zero planner/cache/runtime/Docker/publication |
| `lib.scad.clamps` | `35065514152` | ~9.2 s | `success`, `[]`, zero planner/cache/runtime/Docker/publication |
| `template.scad-project` | `35085786014` | ~9.9 s | `success`, `[]`, `affected=false`, zero planner/cache/runtime/Docker/publication |

The template v0.14.7 log makes the remaining fixed cost particularly visible:

- Actions preparation/downloads occur before the reusable job starts;
- the generic affected action restores a ~20 MB Moon 2.5.4 runtime;
- that runtime-cache restore took about **2.0 s** in run `35085786014`;
- the actual Moon affected query took about **1.2 s**;
- no SCAD planner or CAD runtime was started.

Conclusion: the **zero-CAD architecture goal is fully met**, but the original **4–6 s unrelated-change wall-clock ambition is not fully met**. Current measured range is ~7.6–9.9 s because of generic GitHub Actions/Moon-preflight overhead.

## 7. Final template/reference observability measurement

Final v0.14.7 template qualification run: `35085388134`, exact PR head `78a000603d6a64d2b495f6e054686a128c157877`.

Durable Build `orchestration/timings.json` records:

| Phase | Duration |
| --- | ---: |
| preflight + plan | 8.717 s |
| cache restore | 0.818 s |
| runtime pull | 16.767 s |
| capability materialization | 13.072 s |
| cache save | 0.893 s |
| host finishing | 0.709 s |
| snapshot preparation | 0.007 s |
| **total to prepared snapshot** | **41.059 s** |

This evidence is retained with the generated snapshot rather than relying only on temporary Actions UI timing.

The same run also proves exact provenance consistency: `publication-info.txt`, `orchestration/run-context.json`, Moon materialization records and producer execution records all identify source `78a000603d6a64d2b495f6e054686a128c157877`. Producer owner/tool revision is exact released v0.14.7 source `3935e5f86fe309b8908a05554f7ada336a6d6886`.

## 8. Final conclusions

The implemented architecture proves that:

- unrelated changes stop before SCAD planning/runtime work;
- Moon change-impact remains useful and precise after tool-gitlink hardening;
- Moon whole-capability reuse works with stable source-only identity;
- SCons remains optional and only useful for configured target engines;
- focused runtime distribution materially reduces OpenSCAD-only image bytes;
- normal complete Actions artifacts are unnecessary duplicate retention;
- Build and Verification publishers can overlap safely on the same hosted runner;
- current-generation consumers can inherit shared capability policy instead of copying lifecycle topology;
- exact PR-head provenance survives host finishing/publication;
- durable workflow timing evidence now makes the remaining cost centres visible after Actions logs expire.

Final target interpretation:

- resource architecture: **met**;
- affected canary latency envelopes: **met**;
- zero-CAD unrelated path: **met**;
- 4–6 s unrelated-change wall-clock envelope: **partially met**.

The remaining unrelated-change latency belongs to generic preflight optimisation, not to another SCAD execution-architecture redesign. Migration 005 can close without hiding that miss.
