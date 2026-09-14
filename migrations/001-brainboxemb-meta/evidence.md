# Migration 001 evidence

Migration 001 is complete. This file keeps the qualification points that are useful for reconstructing what was proven without repeating the normal reader documentation.

## Phase 1 — Meta foundation

- PR #12
- merge `62df26489e84dedc9cbd11c7cdf7186e0b78261d`
- Deploy run `34853241040`: dashboard tests, generation and Pages deployment succeeded

## Phase 2 — Public repository catalog

- PR #14
- merge `7a8ad3974bf9b3e43ce0744825d124595ae894e2`
- Deploy run `34855023365`
- 28 tests passed
- runtime preparation: `29 repositories in 6 groups`
- dashboard generation: 29 repositories
- Pages deployment succeeded

This established one machine-readable public repository list for the dashboard.

## Phase 3 — Dashboard subproject

- PR #15
- merge `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`
- Deploy run `34856871791`
- 28 relocated tests passed
- dashboard generated from the new `dashboard/` paths
- Pages deployment succeeded

## Phase 4 — SCAD landscape consolidation

- meta PR #16 merge `7ca593b76a26ac05861b86604fcb6f25baeac5fa`
- `tech.scad` PR #2 merge `b04e539a2215efa3b38fe1aa5a4d657fe4a89ae1`
- meta closeout PR #17 merge `70526bf2c3cf903e0f72bada788eb83924509159`
- Deploy run `34858288823`: success including Pages
- `tech.scad` archive/private-ready PR #3 merge `26a2ef228231bdad9b8ebfb884a54506a7a01c6d`

Useful SCAD portfolio knowledge was moved into `domains/scad/`; the old static catalog role was retired.

## Phase 5 — meta.scad-projects coordination transfer

Key results:

- completed old roadmap work was not recreated as active work;
- current/deferred work was reclassified in `brainboxemb.meta`;
- reader-facing project/tooling guidance was moved under `docs/`;
- `meta.scad-projects` PR #44 redirected current work before archival, merge `6071b21c247359e5fd40b610020494d82b5699ab`;
- public SCAD documentation was made independent of the old repositories in meta PR #39, merge `4a14762f83156f260cf3ce5cbc90cc00c9248c94`.

GitHub was then verified to report both:

```text
brainboxemb/tech.scad             private + archived
brainboxemb/meta.scad-projects    private + archived
```

## Final public-catalog qualification

PR #40 removed the two private archived repositories from the public catalog.

- merge commit: `e0104cb4e558c0fc10d7c20f6f4140a71f32cde8`
- exact-main Deploy run: `34863909122`
- 28 tests passed
- runtime config: `27 repositories in 6 groups`
- generated dashboard: 27 repositories
- Pages artifact upload: success
- Pages deployment: success

## Final documentation review

Before final closeout, the public documentation was reviewed from a reader's perspective. Two gaps were found:

1. agent/architecture wording had been repeated across several reader-facing pages;
2. the old human-readable SCAD indexes for projects, libraries and tooling had been compressed too far into the YAML catalog.

The closeout documentation change therefore:

- shortened root and dashboard agent guidance;
- simplified the root/technical landing pages;
- restored reader-facing `domains/scad/projects.md`, `libraries.md` and `tooling.md`;
- retained detailed technical material only behind clearly named follow-up pages.

## Deferred work

The following are separate work and do not block Migration 001:

- physical-verification document bundle improvements;
- explicit cross-project release/version preparation;
- architecture-view refresh;
- proposed Migration 002 (SCAD build-decision audit), which remains inactive until explicitly activated.
