# Migration 003 — SCAD v0.12 rollout

Status: **complete**

Tracking issue: [#46](https://github.com/brainboxemb/brainboxemb.meta/issues/46)

## Goal

Move the current SCAD dependency chain onto released `tool.scad-project v0.12.0` in a controlled upstream-to-downstream order, and prove the resulting combination in the real HUB75 frame project.

## Completed rollout

1. `tool.scad-project v0.12.0` was released and tag-qualified from exact verified main.
2. `template.scad-project` was updated and qualified first as the reference consumer.
3. `lib.scad.clamps` was updated and released as `v0.1.2`.
4. `lib.scad.hub75` was updated and released as `v0.1.3`.
5. `2026-009-01.cad.HUB75-display-frame` was updated to the released tool and library versions and passed PR plus exact-main production/publication qualification.

The migration did not redesign Moon/SCons, change consumer geometry, or add automatic Git changed-path discovery for `build-audit`.

## Related work that is not part of this migration

`lib.scad.hub75` draft PR #19 remains a separate physical-verification step. Its Dutch and English SQ-01 workbench testcases remain published on `dev/pr-19/verification` and were digitally requalified on the v0.12.0/v0.1.3 baseline.

Generic self-contained physical-verification document packages remain tracked separately in issue #18.

## Evidence

See [qualification evidence](evidence.md) for the exact commits, releases and workflow runs used for every phase.
