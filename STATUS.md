# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 006 — simplify the Java execution architecture

**Active — released owner and reference-template canary are qualified; the real event-timing framework is next.**

The shared Java lifecycle is released as `tool.java-project v0.3.1` at exact source `4969c1316ca7dd3e2648e4098eccf2d5e7dd37d9`. Tagged owner self-test `35145830189` is green and `rel/v0.3.1/bld` exists.

`template.java-project` now consumes that release through a thin production caller. PR #9 merged as exact main source `f1b2a36349c6eb6d0b2806426c8b9ad6e99e5016`; exact-main run `35151495208` is green and `prod/bld/source-sha.txt` identifies that exact source.

The template canary also proves the selective execution policy:

- full/sensitive path: run `35151167342` — Linux canonical Maven, native Windows Maven, exact Linux-artifact Windows smoke and publication all green;
- ordinary Java path: run `35151251145` — Linux canonical plus Windows artifact smoke green, native Windows Maven explicitly skipped;
- README-only path: run `35151294080` — preflight only, Java execution and publication skipped, no Windows runner allocated.

The observed template policy therefore remains `auto -> smoke` for normal Java impact and `auto -> full` for build/toolchain/workflow-sensitive impact. A deliberate `workflow_dispatch` `full` input remains exposed; the full execution path itself is qualified by the runs above.

Next owner: `2026-010-02.java.event-timing-framework`. Keep project-specific release/version behaviour there while moving generic Java orchestration onto the released shared lifecycle.

Canonical record: [Migration 006](migrations/006-java-execution-architecture/README.md).

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation.

## Recently completed

### Migration 005 — simplify the SCAD execution architecture

**Complete.**

The SCAD execution/publication architecture and compact technical namespaces are fully qualified. Runtime/publication behaviour was immutably proven on the v0.14.9 consumer rollout using `dsg`, `bld` and `vrf`. The final released-guidance inconsistency was then corrected in `tool.scad-project v0.14.10` at exact source `3ad040b2d9c26b8c482853157baeb99a8d9b36db`.

`template.scad-project` pinned the released guidance on main source `637906c49b90308ebba7e4477fa2e5036d9543da`; exact-main Production run `35140381160` is green and resolves `project-production.yml@v0.14.10` to exact `3ad040b2...`.

That final change was guidance-only. It did not change the already-qualified runtime/publication architecture and does not require inventing a later template patch release merely to close the migration. Existing immutable consumer releases remain the runtime evidence; the exact-main template run proves the corrected released/pinned guidance.

Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md).

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
