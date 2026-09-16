# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened for final rollout/release gates.**

The architecture, shared-tool releases, canary qualification and performance/resource evidence remain valid. The skipped template release gate and the additional semantic release-call blocker have now both been resolved. Only the final real-project frame qualification/release remains.

Completed final-gate evidence:

- `tool.scad-project v0.14.8` / `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4` is released through lightweight semantic tool tags; owner main Test `35096209854`, Release `35096353093` and tagged Test `35096362420` are green;
- `template.scad-project` PR #46 qualified v0.14.8; exact main `c718655cd67ff90f2d0ba2cf474c86db69cc8965` passed Production run `35097071003`;
- template Release run `35097219635` published immutable `v0.0.5`; its annotated project tag points to exact source `c718655c...`, release assets/checksums exist, and `rel/v0.0.5/{build,verification}` both record source `c718655c...` plus tool v0.14.8 / exact gitlink `85781a6b...`;
- `2026-009-01.cad.HUB75-display-frame` PR #35 was repinned to the same final v0.14.8 baseline without CAD changes; exact PR head `b4c29dcc7d44aa3b73e739f95e4b489c5ee62df1` passed Production run `35098196082` with correct provenance and durable timing evidence;
- frame PR #35 is merged as exact main `a6e884f38ee9a0971361f16c61ca05fd762f4e75`.

Current blocking path:

1. require the automatic Production run on frame main `a6e884f3...` to pass;
2. run one README-only frame probe and prove the unrelated-change path performs no planner/CAD/runtime/publication work;
3. prepare the frame `v0.0.2` changelog/release source;
4. publish and fully verify immutable frame release `v0.0.2`, including assets/checksums and `rel/v0.0.2/{build,verification}`;
5. only then close Migration 005.

This remaining work is release completion, **not** a redesign of the selected SCAD execution architecture.

Tracking issue: #55. Status-correction issue: #64. Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md). Durable architecture: [SCAD technical architecture](domains/scad/architecture.md).

## Queued / proposed

These migrations are deliberately recorded on `main` so their current intent is not hidden in planning PRs. They are **inactive** and do not extend Migration 005.

### Migration 006 — simplify the Java execution architecture

**Proposed / inactive.** Current status and preferred direction are recorded in [Migration 006](migrations/006-java-execution-architecture/README.md). Maven remains the intended Java build authority; the leading direction is an early unrelated-change gate, thinner consumers, shared Java lifecycle ownership, deliberate Windows qualification cadence and removal of unnecessary runner/artifact boundaries. Detailed draft research may continue in #65, but `main` is the status authority. Activation waits for Migration 005 to complete.

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive.** Recorded in [Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) and tracked in #66. The leading direction is exact-SHA + readable-version pins for third-party actions, PR-based updates (Dependabot as the primary candidate), `actions-up` as a normalisation/audit candidate, explicit exceptions for released brainboxemb reusable-workflow refs, and no unattended direct workflow mutation. It is intentionally sequenced **after Migration 006** unless priorities are explicitly changed.

Intended sequencing: **005 → 006 → 007**.

## Recently completed

- [Migration 004 — SCAD repository execution model](migrations/004-scad-repository-execution-model/README.md) — complete.
- [Migration 003 — SCAD v0.12 rollout](migrations/003-scad-v0.12-rollout/README.md) — complete.
- [Migration 002 — SCAD build-decision audit](migrations/002-scad-build-decision-audit/README.md) — complete.
- [Migration 001 — consolidate public portfolio context](migrations/001-brainboxemb-meta/README.md) — complete.

## Parked experiment

- **Moon as SCAD target engine** — issue #51.

## Other follow-ups

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52;
- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency;
- `tool.git-project` issue #26 — reduce fixed latency of unaffected Moon preflight after Migration 005.
