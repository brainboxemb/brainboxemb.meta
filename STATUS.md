# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Active — final library alignment remains.**

The architecture and the completed template/frame release gates remain valid. The closeout was corrected again after verifying that the two current-generation reusable SCAD libraries still declare `tool.scad-project v0.14.3` while the final released shared baseline is `v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`.

Already complete and retained as evidence:

- `tool.scad-project v0.14.8` is released and its semantic reusable-workflow tag resolves cross-repository;
- `template.scad-project v0.0.5` is released from exact source `c718655cd67ff90f2d0ba2cf474c86db69cc8965` through run `35097219635`;
- `2026-009-01.cad.HUB75-display-frame v0.0.2` is released from exact source `18f7900bed31345b8123571ade152af6914e18d6` through run `35099609270`;
- the final frame baseline passed affected Production, merged-main Production and README-only zero-runtime qualification.

Remaining blocking path:

1. upgrade `lib.scad.clamps` from tool v0.14.3 to released v0.14.8 / exact tool source `85781a6b...`, qualify affected and unrelated-change behaviour, and publish the next immutable library release;
2. upgrade `lib.scad.hub75` from tool v0.14.3 to the same v0.14.8 baseline, qualify the focused-runtime/SCons and unrelated-change paths, and publish the next immutable library release;
3. record exact library release/provenance evidence and close Migration 005.

This is a final consumer-baseline consistency pass, **not** an architecture redesign.

Tracking issue: #55. Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md). Durable architecture: [SCAD technical architecture](domains/scad/architecture.md).

## Parallel planning / proposed

Migration 006 may be elaborated in parallel while the library Actions runs are executing, but remains **proposed / inactive** and does not authorize Java owner-repository implementation yet.

### Migration 006 — simplify the Java execution architecture

**Proposed / inactive — next implementation candidate after 005.**

[Migration 006](migrations/006-java-execution-architecture/README.md) records the current Java baseline and working hypotheses. Parallel work may turn these into a concrete target architecture, decisions/open questions and owner-by-owner qualification plan, using current repository state rather than the draft PR as authority.

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation.

Intended implementation sequencing remains **005 complete → 006 → 007**.

## Recently completed

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