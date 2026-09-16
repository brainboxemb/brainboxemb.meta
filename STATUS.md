# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

**No cross-project migration is currently active.**

Migration 005 is complete. Migration 006 is the next intended candidate, but remains **proposed / inactive** until it is explicitly activated after a fresh repository-state revalidation. Migration 007 remains proposed/inactive behind Migration 006.

## Queued / proposed

### Migration 006 — simplify the Java execution architecture

**Proposed / inactive — next intended candidate.**

[Migration 006](migrations/006-java-execution-architecture/README.md) records the current status and preferred direction for simplifying Java repository execution. Maven remains the intended Java build/test authority. The leading hypotheses are an early unrelated-change gate, thinner consumers, shared Java lifecycle ownership, deliberate Windows qualification cadence, fewer unnecessary runner/artifact boundaries, and durable timing/provenance evidence.

Migration 005 is now complete, so it is no longer an activation blocker. Migration 006 still does **not** activate automatically: before implementation, revalidate the current Java repositories and turn the working hypotheses into a concrete target architecture, owner sequence and qualification plan. Draft research in #65 remains input; `main` remains the status authority.

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive — intentionally after Migration 006.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the current direction: exact-SHA + readable-version pins for third-party actions, PR-based updates with Dependabot as the primary candidate, `actions-up` as a normalisation/audit candidate, explicit exceptions for released brainboxemb reusable-workflow refs, and no unattended direct workflow mutation.

Migration 007 is deliberately sequenced after Migration 006 unless cross-project priorities are explicitly changed.

Intended sequencing remains **005 complete → 006 next candidate → 007 later**.

## Recently completed

### Migration 005 — simplify the SCAD execution architecture

**Complete.**

Final shared baseline:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`.

Final release gates are closed:

- `template.scad-project v0.0.5` from exact source `c718655cd67ff90f2d0ba2cf474c86db69cc8965`, Release run `35097219635`;
- `2026-009-01.cad.HUB75-display-frame v0.0.2` from exact source `18f7900bed31345b8123571ade152af6914e18d6`, Release run `35099609270`;
- frame affected Production `35098196082`, merged-main Production `35098642458`, and README-only zero-runtime probe `35099086265` are green;
- both final project releases have Build/Verification/STL/checksum assets and immutable `rel/<version>/{build,verification}` provenance on the exact released source.

The corrected closeout is recorded in [Migration 005](migrations/005-scad-execution-architecture/README.md) and [final closeout evidence](migrations/005-scad-execution-architecture/30-closeout-evidence.md). Tracking issue #55 is closed completed.

### Migration 004 — SCAD repository execution model

**Complete.** Qualified the common conditional-SCAD execution model through the template and both reusable SCAD libraries and handed architecture simplification to Migration 005.

### Migration 003 — SCAD v0.12 rollout

**Complete.** Rolled the released tool through the template, both SCAD libraries and the real HUB75 frame.

### Migration 002 — SCAD build-decision audit

**Complete.** Added and qualified the explicit post-build decision audit.

### Migration 001 — consolidate public portfolio context

**Complete.** Consolidated repository/catalog/dashboard/documentation context into `brainboxemb.meta`.

## Parked experiment

- **Moon as SCAD target engine** — issue #51.

## Other follow-ups

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52;
- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency;
- `tool.git-project` issue #26 — reduce fixed latency of unaffected Moon preflight after Migration 005.
