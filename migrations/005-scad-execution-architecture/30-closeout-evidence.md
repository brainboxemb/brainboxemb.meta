# 30 — Final closeout evidence

## Why this document exists

Migration 005 changed shared SCAD execution across several owner and consumer repositories. This document records the exact immutable baselines that were actually qualified, so completion does not depend on an old chat, a transient Actions page or an assumption that a rollout was finished.

Use it when checking why Migration 005 is closed, which releases form the final baseline, or whether a later change is a regression versus follow-up work.

Migration 005 is complete as of 2026-09-16.

The execution architecture first closed on the v0.14.8 rollout. It was later reopened for one narrow correctness issue: persistent generated-output branches used `build` / `verification` while current-generation SCAD technical workspace roots already used `bld` / `vrf`. The architecture itself did not need redesign; the technical namespace was normalized, patch-released and requalified across every current-generation consumer.

## Historical architecture baseline retained as evidence

The previously qualified v0.14.8 baseline remains valid historical evidence for the execution architecture:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`;
- `template.scad-project v0.0.5`;
- `lib.scad.clamps v0.1.5`;
- `lib.scad.hub75 v0.1.6`;
- `2026-009-01.cad.HUB75-display-frame v0.0.2`.

Those releases and their historical `build` / `verification` branches are not rewritten. They document the architecture that produced them.

## Final shared tool baseline

`tool.scad-project v0.14.9`

- exact source/tag target: `a140b22858ac1899e7f2fa71b679639a70d819c3`;
- exact-main Test: `35118666631` — green;
- Release: `35119062169` — green;
- tagged Test: `35119081117` — green;
- v0.14.9 is a lightweight tag pointing directly at the exact release commit, preserving cross-repository reusable-workflow resolution;
- semantic Build/Verification kinds remain readable API/configuration concepts, while default persistent technical publication suffixes are `bld` / `vrf`.

Supporting shared releases remain:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

The selected execution architecture remains unchanged: one generic affected query, stop before CAD runtime for unrelated changes, capability/configuration planning, at most one normal CAD runtime, Moon for whole-capability orchestration/materialization, SCons only where configured/useful, and host-side finishing/publication with exact provenance and durable timing evidence.

## Reference template final gate

`template.scad-project v0.0.6`

Namespace rollout and production qualification:

- affected namespace PR Production `35121239377` — green;
- final exact-main production source before releaseprep: `399d28f6ff497efee955a02e781e8166d435b740`;
- exact-main Production `35122146935` — green;
- `prod/bld` and `prod/vrf` both identify that source, `tool.scad-project v0.14.9` and exact tool gitlink `a140b228...`.

Release-only zero-runtime qualification:

- releaseprep PR `35130201114` — green; Python/planner/cache/runtime/materialization/finishing/publication skipped after affected classification;
- release-source exact main `b8a0cc9113084f56c074b7dc61b160105c615b71`;
- release-source exact-main Production `35130279294` — same zero-runtime path, green;
- Release `35130348230` — green.

Immutable release evidence:

- annotated `v0.0.6` tag object points to exact source `b8a0cc9113084f56c074b7dc61b160105c615b71`;
- Build, Verification, STL and `SHA256SUMS.txt` assets are present;
- `rel/v0.0.6/bld/publication-info.txt` and `rel/v0.0.6/vrf/publication-info.txt` both identify exact source `b8a0cc91...`, `tool.scad-project v0.14.9`, exact tool gitlink `a140b228...` and `tool.git-project` gitlink `7c43f37e...`.

## Reusable library alignment

### `lib.scad.clamps v0.1.6`

Final v0.14.9 namespace rollout:

- affected PR Production `35122513993` — green;
- merged-main Production `35122676804` — green;
- exact release source: `021eed7bba76ca77825bd6f6c850e1ebd2916283`;
- Release `35123102064` — green;
- release assets include Build ZIP, Verification ZIP and `SHA256SUMS.txt`;
- `rel/v0.1.6/bld/publication-info.txt` identifies exact source `021eed7b...`, `tool.scad-project v0.14.9`, exact tool gitlink `a140b228...` and `tool.git-project` gitlink `7c43f37e...`;
- the direct-engine contract remains intact: the namespace rollout did not introduce normal or Verification SCons cache transport or change clamp geometry/API behaviour.

### `lib.scad.hub75 v0.1.7`

Final v0.14.9 namespace rollout:

- affected PR Production `35126450152` — green;
- merged-main Production `35126654658` — green;
- exact release source: `1390cd322b31b119779c41743119c85e0e984314`;
- Release `35127144492` — green;
- release assets include Build ZIP, Verification ZIP and `SHA256SUMS.txt`;
- `rel/v0.1.7/bld/publication-info.txt` identifies exact source `1390cd32...`, `tool.scad-project v0.14.9`, exact tool gitlink `a140b228...` and `tool.git-project` gitlink `7c43f37e...`;
- normal SCons restore/save remains active while command-only Verification does not transport a Verification-SCons cache;
- geometry, public API and physical-verification content were unchanged by the namespace rollout.

## Real HUB75 frame final gate

`2026-009-01.cad.HUB75-display-frame v0.0.3`

Namespace rollout:

- affected PR Production `35127778978` — green;
- both normal and Verification SCons restore/save paths qualified;
- merged-main source: `a3f2fd24e21be34417608ae42553b863e25cb1fb`;
- merged-main Production `35128211708` — green;
- `prod/bld` and `prod/vrf` both identify that exact source and v0.14.9 baseline.

Release-only zero-runtime qualification:

- releaseprep PR `35128707436` — green with planner/cache/runtime/materialization/finishing/publication skipped;
- exact release source: `9ff354260276e325d571c82af67bc23e9815744d`;
- exact-main release-source Production `35129225149` — same zero-runtime path, green;
- Release `35129320430` — green.

Immutable release evidence:

- annotated `v0.0.3` tag object `7d6fb7207e1298285d4c1637130e7458fa46b58f` points to exact source `9ff35426...`;
- Build, Verification, STL and `SHA256SUMS.txt` assets are present;
- `rel/v0.0.3/bld` and `rel/v0.0.3/vrf` retain exact source, v0.14.9 / `a140b228...` provenance and the deliberately unchanged HUB75 geometry gitlink `e0432a9533a08a1c0d9e87225c22f3f66b632531`.

## Completion decision

All corrected closeout gates are satisfied:

- the final shared tool v0.14.9 release exists and is qualified;
- the reference template is qualified and immutably released on `rel/v0.0.6/{bld,vrf}`;
- both reusable current-generation SCAD libraries are aligned to v0.14.9 and immutably released on `bld` / `vrf` namespaces;
- the real HUB75 frame is aligned and immutably released on `rel/v0.0.3/{bld,vrf}`;
- affected, merged-main and unrelated zero-runtime paths are qualified across the correction rollout;
- mutable `prod/{bld,vrf}` and immutable `rel/vX.Y.Z/{bld,vrf}` outputs retain exact source/tool provenance;
- downloadable release assets and checksums exist;
- historical `build` / `verification` branches remain historical evidence and are not rewritten.

Migration 005 is therefore closed without changing its execution-architecture or performance conclusions. Generic optimisation such as unaffected-path latency remains separate follow-up work and does not reopen this migration.
