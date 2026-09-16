# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened — final generated-output namespace normalization.**

The Migration-005 execution architecture and prior release evidence remain valid. A final naming inconsistency was found while aligning Migration 006: current-generation SCAD workspaces already use compact technical identifiers (`dsg`, `bld`, `vrf`), while persistent generated-output branches were standardized as `build` and `verification`.

The durable portfolio rule is now defined in [`docs/working-model/generated-output.md`](docs/working-model/generated-output.md): human-facing lifecycle names remain readable (**Build**, **Verification**, **Design**, **Documentation**), while stable technical path/branch identifiers use the canonical compact identifiers `bld`, `vrf`, `dsg`, and `docs` where those concepts apply.

Migration 005 must therefore normalize current-generation SCAD publication to `dev/pr-N/{bld,vrf}`, `prod/{bld,vrf}` and `rel/vX.Y.Z/{bld,vrf}`, qualify the shared tool and consumers, and then close again. Historical already-published branches/releases remain historical evidence and are not rewritten.

Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md).

### Migration 006 — simplify the Java execution architecture

**Active design / owner draft, temporarily paused behind the reopened Migration 005 namespace correction.**

Owner implementation has started in `tool.java-project` draft PR #26. Its architecture remains valid, including early affected preflight and selective Windows qualification, but it will not be released or rolled into `template.java-project` / `2026-010-02.java.event-timing-framework` until the shared generated-output namespace is settled by Migration 005.

After 005 closes again, the intended sequence is:

1. finish and qualify `tool.java-project` PR #26 against the canonical technical namespace;
2. release the qualified Java tool revision;
3. `template.java-project` — reference canary for thin-caller, unrelated zero-Java and selective Windows behaviour;
4. decide the normal Windows qualification policy from canary evidence;
5. `2026-010-02.java.event-timing-framework` — real downstream rollout and release qualification.

The Java scope deliberately excludes project-family planning/architecture documentation. The generic project-family and engineering-documentation model remains technology-neutral.

Canonical record: [Migration 006](migrations/006-java-execution-architecture/README.md).

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation.

## Recently completed

- [Migration 004 — SCAD repository execution model](migrations/004-scad-repository-execution-model/README.md) — complete.
- [Migration 003 — SCAD v0.12 rollout](migrations/003-scad-v0.12-rollout/README.md) — complete.
- [Migration 002 — SCAD build-decision audit](migrations/002-scad-build-decision-audit/README.md) — complete.
- [Migration 001 — consolidate public portfolio context](migrations/001-brainboxemb-meta/README.md) — complete.

Migration 005 had reached a complete v0.14.8 rollout, but is intentionally reopened only for the final `bld`/`vrf` namespace correction.

## Parked / follow-up

- Moon as SCAD target engine — issue #51;
- self-contained physical-verification document packages — issue #18;
- one release flow for requested versions across project types — issue #20;
- standardise CHANGELOG format and add a shared template — issue #52;
- `tool.git-project` #17, #22 and #26 remain owner-local follow-ups.
