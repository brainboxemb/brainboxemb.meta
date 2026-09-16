# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 006 — simplify the Java execution architecture

**Primary active cross-project migration. Owner implementation is merged and exact-main qualified; release and consumer rollout are now unblocked.**

The shared Java execution lifecycle is merged in `tool.java-project` main as `c7ed36ceaf21874b908a1dd01fa54bc60d420d9c`. Exact-main owner evidence is green for both the affected-policy test and the full Java toolchain self-test.

The qualified owner contract includes:

- one exact base→head generic affected query through released `tool.git-project v0.2.8`;
- unrelated Java impact stopping before JDK/Maven/Windows allocation;
- `windows-mode: auto|none|smoke|full`;
- automatic normal Java impact → Windows artifact smoke;
- automatic build/toolchain-sensitive impact → full native Windows Maven qualification plus artifact smoke;
- exact source identity carried through preflight, Linux canonical execution, full Windows execution and provenance;
- canonical Java generated-output publication under technical `bld` naming;
- engineering-documentation assembly kept outside Java ownership.

Migration 005 has now closed again on the durable `bld` / `vrf` namespace convention, so the next Java sequence is:

1. prepare and release the already-qualified `tool.java-project` owner revision;
2. `template.java-project` — reference canary for thin-caller, unrelated zero-Java and selective Windows behaviour;
3. refine the normal Windows qualification policy only if canary evidence requires it;
4. `2026-010-02.java.event-timing-framework` — real downstream rollout and release qualification.

The Java scope deliberately excludes project-family planning/architecture documentation. The generic project-family and engineering-documentation model remains technology-neutral.

Canonical record: [Migration 006](migrations/006-java-execution-architecture/README.md).

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation.

## Recently completed

### Migration 005 — simplify the SCAD execution architecture

**Complete — final namespace correction released and qualified.**

The durable portfolio rule remains: human-facing lifecycle names are readable (**Build**, **Verification**, **Design**, **Documentation**), while stable technical path/branch identifiers use `bld`, `vrf`, `dsg`, and `docs` where those concepts apply.

Final corrected SCAD baseline:

- `tool.scad-project v0.14.9` / exact `a140b22858ac1899e7f2fa71b679639a70d819c3`;
- `template.scad-project v0.0.6`;
- `lib.scad.clamps v0.1.6`;
- `lib.scad.hub75 v0.1.7`;
- `2026-009-01.cad.HUB75-display-frame v0.0.3`.

All current-generation consumers now qualify `dev/pr-N/{bld,vrf}`, `prod/{bld,vrf}` and immutable `rel/vX.Y.Z/{bld,vrf}` publication. Historical `build` / `verification` branches remain historical evidence and were not rewritten.

Canonical evidence: [Migration 005](migrations/005-scad-execution-architecture/README.md) and [final closeout evidence](migrations/005-scad-execution-architecture/30-closeout-evidence.md).

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
