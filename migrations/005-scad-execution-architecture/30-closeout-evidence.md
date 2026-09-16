# 30 — Final closeout evidence

Migration 005 is complete as of 2026-09-16.

The first closeout was reopened because repository verification found two skipped release/rollout gates. The architecture itself was not reopened. This document records the evidence that closes those corrected gates.

## Final shared tool baseline

`tool.scad-project v0.14.8`

- exact source: `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`;
- main Test: `35096209854` — green;
- Release: `35096353093` — green;
- tagged Test: `35096362420` — green;
- release tag is a lightweight direct commit ref, resolving the cross-repository nested reusable-workflow problem exposed by the first template v0.0.5 attempt.

The selected architecture remains unchanged: one generic affected query, stop before the CAD runtime for unrelated changes, a capability/configuration plan, at most one normal CAD runtime, Moon for whole-capability orchestration/materialization, SCons only where configured/useful, and host-side finishing/publication with exact provenance and durable timing evidence.

## Reference template final gate

`template.scad-project v0.0.5`

- final source: `c718655cd67ff90f2d0ba2cf474c86db69cc8965`;
- exact-main Production: `35097071003` — green;
- Release: `35097219635` — resolve, preflight, Build, Verification, finalize and request cleanup all green;
- release assets: Build ZIP, Verification ZIP, STL ZIP and `SHA256SUMS.txt`;
- `rel/v0.0.5/build` and `rel/v0.0.5/verification` both identify exact source `c718655c...`, `tool.scad-project v0.14.8` and exact tool gitlink `85781a6b...`.

This closes the template release gate that the first Migration-005 closeout had skipped.

## HUB75 frame final gate

`2026-009-01.cad.HUB75-display-frame v0.0.2`

Final tool rollout:

- PR #35 final head: `b4c29dcc7d44aa3b73e739f95e4b489c5ee62df1`;
- PR Production: `35098196082` — green with exact PR-head provenance and durable timing evidence;
- merged v0.14.8 baseline: `a6e884f38ee9a0971361f16c61ca05fd762f4e75`;
- merged-main Production: `35098642458` — green.

Zero-runtime qualification:

- probe PR #36 changed only `README.md`;
- exact probe source: `206cc7adc558f812fd30f6f9766d20407188bb74`;
- Production run `35099086265` — green;
- after exact source/base resolution and the one affected query, host Python, planner installation, execution planning, all caches, runtime pull, Docker execution/materialization, finishing and Build/Verification publication were skipped.

Final release source:

- `18f7900bed31345b8123571ade152af6914e18d6`;
- exact-main Production `35099567639` — green with zero-runtime behaviour for the documentation/release-metadata-only change;
- Release `35099609270` — resolve, preflight, Build, Verification, finalize and request cleanup all green;
- annotated project tag `v0.0.2` points to exact source `18f7900b...`;
- release assets: Build ZIP, Verification ZIP, STL ZIP and `SHA256SUMS.txt`;
- `rel/v0.0.2/build` and `rel/v0.0.2/verification` both identify exact source `18f7900b...`, `tool.scad-project v0.14.8` and exact tool gitlink `85781a6b...`.

## Completion decision

The corrected closeout gates are all satisfied:

- immutable final shared tool release exists and is qualified;
- reference template is qualified and immutably released;
- real HUB75 frame is aligned to the final shared baseline;
- affected production, exact provenance and durable timing evidence are qualified;
- unrelated README-only work proves the zero-runtime path;
- the frame is immutably released with downloadable assets/checksums and browsable Build/Verification release branches.

Migration 005 can therefore close without changing its architecture/performance conclusions. Remaining generic optimisation work, such as unaffected-path latency, remains separate follow-up work and does not reopen this migration.
