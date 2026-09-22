# Migration 009 — serialize SCAD production and roll out corrected tooling

Status: **active**

Tracking issue: [#113](https://github.com/brainboxemb/brainboxemb.meta/issues/113)

## Goal

Remove the production-concurrency correctness race from the shared current-generation
SCAD stack and roll the corrected owner release through every current
`tool.scad-project` consumer.

A newer production push must never cancel an earlier production run when that
earlier run may still be materializing or publishing generated Build/Verification
state. Pull-request runs may still supersede stale work for the same PR.

## Trigger

The HUB75 checkpoint exposed the race on 2026-09-22:

- HUB75 main run `35725433627` started after PR #45 merged and reached runtime
  materialization;
- the subsequent checkpoint merge started run `35725610716`;
- shared production concurrency cancelled the first run;
- the second run was green but skipped runtime/materialization/publication because
  its own `before -> head` range contained only the later checkpoint changes;
- `prod/bld` / `prod/vrf` therefore remained older than current `main`.

This is a shared owner problem because the cancellation policy lives in
`tool.scad-project/.github/workflows/project-production.yml`.

## Owner fix

`tool.scad-project` issue/PR #96 owns the correction.

Required contract:

- same-PR runs may use `cancel-in-progress`;
- production/default-branch pushes serialize;
- regression coverage prevents unconditional cancellation from returning;
- release as the next patch version after v0.15.5.

## Rollout scope

Use the canonical repository catalog. Current-generation consumers with
`project_infrastructure.provider: tool.scad-project` are in scope:

- `template.scad-project`;
- `lib.scad.clamps`;
- `lib.scad.hub75`;
- `lib.scad.forge`;
- `lib.scad.util`;
- `lib.scad.mechint`;
- `2026-009-01.cad.HUB75-display-frame`;
- `2026-009-02.cad.hub75-component-lab`;
- `exp.2026-006.scad-library-dependencies`.

Classic SCAD/CAD repositories are explicitly out of scope.

## Rollout sequence

1. qualify and merge `tool.scad-project` PR #96;
2. publish the corrected patch release;
3. qualify the released owner through `template.scad-project`;
4. update every in-scope current-generation consumer through its normal
   repository-update path;
5. for each consumer, verify dependency/workflow alignment and normal CI;
6. require an exact-main production result where the repository publishes
   production output;
7. repair HUB75 production output before completing its v0.0.4 checkpoint;
8. record exact revisions/run IDs here and close the migration only when no
   catalogued current-generation consumer remains on the vulnerable release.

## Completion criteria

Migration 009 is complete only when:

- the corrected `tool.scad-project` patch is immutable/released;
- all in-scope consumers are on that release or a later release containing the fix;
- workflow callers and checked-out tool revisions are aligned;
- representative production evidence proves serialization-safe publication;
- HUB75 `prod/bld` and `prod/vrf` provenance no longer trail the intended
  checkpoint source due to the cancelled-run race.
