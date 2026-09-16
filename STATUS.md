# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 006 — simplify the Java execution architecture

**Active — owner implementation has started in `tool.java-project`.**

Migration 005 is now complete, including final v0.14.8 alignment and immutable releases of both reusable SCAD libraries. Migration 006 is therefore the primary active cross-project migration.

Current implementation sequence:

1. `tool.java-project` — implement and qualify the shared Java execution/preflight contract; current work item is draft PR #26;
2. release the qualified Java tool revision;
3. `template.java-project` — reference canary for thin-caller, unrelated zero-Java and selective Windows behaviour;
4. decide the normal Windows qualification policy from canary evidence;
5. `2026-010-02.java.event-timing-framework` — real downstream rollout and release qualification.

The Java scope deliberately excludes project-family planning/architecture documentation. The generic project-family and engineering-documentation model remains technology-neutral: meta/coordination owns cross-repository engineering meaning, `tool.eng-docs` owns reusable document mechanisms/assembly, and Java owns only Java-derived producers/evidence.

Windows qualification is being split into explicit `none`, `smoke` and `full` execution levels. Normal callers use `windows-mode: auto`: an affected normal Java change selects the cheap exact-Linux-JAR Windows smoke; Windows-sensitive build/toolchain impact selects the full independent Windows Maven qualification. Explicit modes remain available as an escape hatch.

Canonical record: [Migration 006](migrations/006-java-execution-architecture/README.md).

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation.

## Recently completed

- [Migration 005 — simplify the SCAD execution architecture](migrations/005-scad-execution-architecture/README.md) — complete after final `lib.scad.clamps v0.1.5` and `lib.scad.hub75 v0.1.6` alignment/release on `tool.scad-project v0.14.8`.
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
