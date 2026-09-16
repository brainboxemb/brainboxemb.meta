# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened for one final released owner-guidance correction.**

The v0.14.9 runtime/default/test namespace correction is qualified across the template, both reusable libraries and the HUB75 display frame, including immutable `rel/.../{bld,vrf}` releases. During final durable-documentation review, however, the released `tool.scad-project v0.14.9` `AGENTS.md` was found to still instruct agents to use legacy `dev/pr-N/{build,verification}` and `prod/{build,verification}` branches.

That is a release blocker because current-generation consumers explicitly tell agents to read the **pinned** `tools/tool.scad-project/AGENTS.md`. A main-only documentation fix would therefore leave released/pinned consumer guidance wrong.

Shortest safe closeout path:

1. fix owner guidance to `bld` / `vrf` without changing execution semantics;
2. patch-release `tool.scad-project`;
3. update current-generation consumer tool pins so their pinned guidance is correct;
4. qualify the minimal required consumer path and immutable release evidence;
5. then close Migration 005 again.

The durable namespace rule remains unchanged in [`docs/working-model/generated-output.md`](docs/working-model/generated-output.md).

Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md).

### Migration 006 — simplify the Java execution architecture

**Owner implementation merged and exact-main qualified; owner release remains temporarily gated only by the final Migration-005 guidance patch.**

The shared Java execution lifecycle is merged in `tool.java-project` main as `c7ed36ceaf21874b908a1dd01fa54bc60d420d9c`. Exact-main owner evidence is green for both the affected-policy test and the full Java toolchain self-test.

The qualified owner contract includes one exact generic affected query, unrelated stop before JDK/Maven/Windows, `windows-mode: auto|none|smoke|full`, selective Windows smoke/full qualification, exact source identity through execution/provenance, canonical `bld` publication and engineering-documentation assembly outside Java ownership.

Owner implementation may remain merged and qualified. Do not release the Java owner contract or begin Java consumer rollout until the final released SCAD guidance baseline is corrected and Migration 005 closes again.

Canonical record: [Migration 006](migrations/006-java-execution-architecture/README.md).

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation.

## Recently completed architecture evidence

The v0.14.9 SCAD namespace execution rollout itself is fully qualified:

- `tool.scad-project v0.14.9` / exact `a140b22858ac1899e7f2fa71b679639a70d819c3`;
- `template.scad-project v0.0.6`;
- `lib.scad.clamps v0.1.6`;
- `lib.scad.hub75 v0.1.7`;
- `2026-009-01.cad.HUB75-display-frame v0.0.3`.

Those releases prove the runtime/publication behavior. Migration 005 remains open only because the released owner guidance embedded in v0.14.9 is inconsistent with that proven behavior.

Other completed migrations:

- [Migration 004 — SCAD repository execution model](migrations/004-scad-repository-execution-model/README.md) — complete.
- [Migration 003 — SCAD v0.12 rollout](migrations/003-scad-v0.12-rollout/README.md) — complete.
- [Migration 002 — SCAD build-decision audit](migrations/002-scad-build-decision-audit/README.md) — complete.
- [Migration 001 — consolidate public portfolio context](migrations/001-brainboxemb-meta/README.md) — complete.

## Parked / follow-up

- Moon as SCAD target engine — issue #51;
- self-contained physical-verification document packages — issue #18;
- one release flow for requested versions across project types — issue #20;
- standardise CHANGELOG format and add a shared template — issue #52;
- `tool.git-project` #17, #22 and #26 remain owner-local follow-ups.
