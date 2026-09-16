# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened — final generated-output namespace normalization and release qualification.**

The Migration-005 execution architecture and prior release evidence remain valid. A final naming inconsistency was found while aligning Migration 006: current-generation SCAD workspaces already use compact technical identifiers (`dsg`, `bld`, `vrf`), while persistent generated-output branches were standardized as `build` and `verification`.

The durable portfolio rule is defined in [`docs/working-model/generated-output.md`](docs/working-model/generated-output.md): human-facing lifecycle names remain readable (**Build**, **Verification**, **Design**, **Documentation**), while stable technical path/branch identifiers use the canonical compact identifiers `bld`, `vrf`, `dsg`, and `docs` where those concepts apply.

Migration 005 must normalize current-generation SCAD publication to `dev/pr-N/{bld,vrf}`, `prod/{bld,vrf}` and `rel/vX.Y.Z/{bld,vrf}`, qualify the shared tool and consumers, and then close again. Historical already-published branches/releases remain historical evidence and are not rewritten.

`tool.scad-project v0.14.9` is released from exact main commit `a140b22858ac1899e7f2fa71b679639a70d819c3`. The reference template is on v0.14.9 and its final production-namespace configuration canary is being qualified before the library and project consumers roll forward.

Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md).

### Migration 006 — simplify the Java execution architecture

**Owner implementation merged and exact-main qualified in parallel with Migration 005; release/consumer rollout remains gated.**

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

The parallelism rule remains:

1. 005 continues through SCAD consumer qualification/release and closeout;
2. 006 owner implementation may remain merged and qualified on `tool.java-project/main`;
3. do **not** release the new Java owner contract or modify Java consumers until 005 closes again;
4. discoveries that affect the shared cross-domain contract must be resolved in meta before either migration invents a local variant.

After the 005 gate, the intended Java sequence is:

1. prepare and release the already-qualified `tool.java-project` owner revision;
2. `template.java-project` — reference canary for thin-caller, unrelated zero-Java and selective Windows behaviour;
3. decide/refine the normal Windows qualification policy from canary evidence if needed;
4. `2026-010-02.java.event-timing-framework` — real downstream rollout and release qualification.

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
