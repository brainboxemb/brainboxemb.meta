# 30 — Final closeout evidence

## Why this document exists

Migration 005 changed shared SCAD execution across several owner and consumer repositories. This document records the exact immutable baselines that were actually qualified, so completion does not depend on an old chat, a transient Actions page or an assumption that a rollout was finished.

Use it when checking why Migration 005 is closed, which releases form the final baseline, or whether a later change is a regression versus follow-up work.

Migration 005 is complete as of 2026-09-16.

The closeout was reopened twice when repository verification exposed skipped rollout/release gates. The architecture itself did not need redesign; the missing consumer gates were completed and requalified.

## Final shared tool baseline

`tool.scad-project v0.14.8`

- exact source: `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`;
- main Test: `35096209854` — green;
- Release: `35096353093` — green;
- tagged Test: `35096362420` — green;
- reusable-workflow release tag is a lightweight direct commit ref, resolving the cross-repository nested reusable-workflow problem exposed during template qualification.

Supporting shared releases:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

The selected architecture remains: one generic affected query, stop before CAD runtime for unrelated changes, capability/configuration planning, at most one normal CAD runtime, Moon for whole-capability orchestration/materialization, SCons only where configured/useful, and host-side finishing/publication with exact provenance and durable timing evidence.

## Reference template final gate

`template.scad-project v0.0.5`

- exact source: `c718655cd67ff90f2d0ba2cf474c86db69cc8965`;
- exact-main Production: `35097071003` — green;
- Release: `35097219635` — green;
- Build, Verification, STL and checksum assets present;
- `rel/v0.0.5/{build,verification}` identify the exact source, `tool.scad-project v0.14.8` and exact tool gitlink `85781a6b...`.

## Real HUB75 frame final gate

`2026-009-01.cad.HUB75-display-frame v0.0.2`

- affected PR Production `35098196082` — green;
- merged-main Production `35098642458` — green;
- README-only zero-runtime probe `35099086265` — green;
- exact release source: `18f7900bed31345b8123571ade152af6914e18d6`;
- exact-main release-source Production `35099567639` — green;
- Release `35099609270` — green;
- annotated `v0.0.2` tag points to exact release source;
- Build, Verification, STL and checksum assets present;
- `rel/v0.0.2/{build,verification}` retain exact source and final shared-tool provenance.

## Final reusable-library alignment

### `lib.scad.clamps v0.1.5`

Final v0.14.8 rollout:

- affected PR Production `35101169850` — green;
- merged-main Production `35101626924` — green;
- README-only zero-runtime probe `35101816174` — green;
- exact release source: `11f804c5087c2b5ec06af11603af4508d5c1db43`;
- Release `35103156647` — green;
- annotated tag object `19e7b0fb1494f1e9b21720cfcbcfca28f8f0c3bb` points to exact source `11f804c5...`;
- release assets include Build ZIP, Verification ZIP and `SHA256SUMS.txt`;
- `rel/v0.1.5/build/publication-info.txt` and `rel/v0.1.5/verification/publication-info.txt` both identify exact source `11f804c5...`, `tool.scad-project v0.14.8`, exact tool gitlink `85781a6b...` and `tool.git-project` gitlink `7c43f37e...`;
- direct-engine behaviour remains intact; the rollout did not introduce SCons cache transport or change clamp geometry/API behaviour.

### `lib.scad.hub75 v0.1.6`

Final v0.14.8 rollout:

- affected PR Production `35101188447` — green;
- merged-main Production `35101638473` — green;
- README-only zero-runtime probe `35101927430` — green;
- exact release source: `4dd285d5bced43657392d9fd6d245005f12e53eb`;
- Release `35103198893` — green;
- annotated tag object `2b031039c45f1bcfce005758b685ffed3051f010` points to exact source `4dd285d5...`;
- release assets include Build ZIP, Verification ZIP and `SHA256SUMS.txt`;
- `rel/v0.1.6/build/publication-info.txt` and `rel/v0.1.6/verification/publication-info.txt` both identify exact source `4dd285d5...`, `tool.scad-project v0.14.8`, exact tool gitlink `85781a6b...` and `tool.git-project` gitlink `7c43f37e...`;
- the focused OpenSCAD runtime and configured SCons policy remain intact; geometry/API/physical-verification content was not changed by the tooling rollout.

## Completion decision

All corrected closeout gates are satisfied:

- the final shared tool release exists and is qualified;
- the reference template is qualified and immutably released;
- the real HUB75 frame is aligned and immutably released;
- both reusable current-generation SCAD libraries are aligned to the same final v0.14.8 baseline and immutably released;
- affected, merged-main and unrelated zero-runtime paths are qualified across the rollout;
- immutable Build/Verification release branches retain exact source/tool provenance;
- downloadable release assets and checksums exist.

Migration 005 can therefore close without changing its architecture/performance conclusions. Generic optimisation such as unaffected-path latency remains separate follow-up work and does not reopen this migration.
