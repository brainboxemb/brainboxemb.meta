# Migration 003 — SCAD v0.12 rollout

Status: **active**

Tracking issue: [#46](https://github.com/brainboxemb/brainboxemb.meta/issues/46)

## Goal

Roll the newly added `tool.scad-project` build-decision audit capability through the current SCAD dependency chain using released, qualified versions and an explicit upstream-to-downstream order.

This is one cross-project migration because the repositories are not independent consumers: the template defines the current reference contract, libraries consume the tool, and the HUB75 frame consumes both the tool and `lib.scad.hub75`.

## Observed starting state

| Repository | Starting dependency state |
| --- | --- |
| `tool.scad-project` | release prep for `v0.12.0` merged; exact-main/release qualification pending |
| `template.scad-project` | `tool.scad-project v0.11.0` |
| `lib.scad.clamps` | tool commit `40694891d3239401cb0ba4bfb35a3812d6584ab7` |
| `lib.scad.hub75` | tool commit `40694891d3239401cb0ba4bfb35a3812d6584ab7` |
| `2026-009-01.cad.HUB75-display-frame` | `tool.scad-project v0.11.0`, `lib.scad.hub75 v0.1.2` |

## Phase A — release `tool.scad-project v0.12.0`

Owner: `brainboxemb/tool.scad-project`

Prerequisites:
- Migration 002 implementation complete;
- release-prep PR #50 merged.

Qualification:
1. exact `main` Test run passes;
2. immutable `v0.12.0` tag is created from that exact verified commit;
3. tag Test run passes.

The released tool version, not an arbitrary main SHA, is the dependency input for later phases.

## Phase B — qualify `template.scad-project`

Owner: `brainboxemb/template.scad-project`

Prerequisite: Phase A complete.

Work:
- update the declared tool ref to `v0.12.0`;
- move the `tools/tool.scad-project` gitlink to the exact release commit;
- synchronize reusable workflow pins to that same commit;
- compare the repository against the current tool contract and repair only actual template drift;
- run the template's normal qualification scenarios.

The template is the reference consumer. Libraries are not updated until this phase is qualified.

## Phase C — update and release the libraries

Owners:
- `brainboxemb/lib.scad.clamps`;
- `brainboxemb/lib.scad.hub75`.

Prerequisite: Phase B complete.

Each library is reassessed independently against the qualified template and the current tool contract. Both currently use the same old loose tool commit, but that does not imply identical migrations.

For each library:
1. identify structural/configuration/workflow drift that matters to current behaviour;
2. update to released `tool.scad-project v0.12.0` and its exact gitlink/workflow commit;
3. preserve library-specific CAD and verification behaviour;
4. qualify PR and exact main;
5. create a new immutable library release;
6. verify the release/tag evidence before downstream consumption.

Cosmetic/template parity that is not required for correctness remains follow-up work rather than a blocker.

## Phase D — align the real HUB75 frame

Owner: `brainboxemb/2026-009-01.cad.HUB75-display-frame`

Prerequisite: the required Phase C library release exists and is qualified.

Work:
- update the tool to released `v0.12.0`;
- update `lib.scad.hub75` to the newly qualified library release;
- synchronize gitlinks and reusable workflow pins;
- compare project infrastructure with the qualified template and repair actual generation drift;
- preserve current project-specific CAD/design/verification decisions;
- run Build and Verify, inspect generated/publication evidence, and qualify exact main.

The frame is the end-to-end proof that the released tool + released HUB75 library work together in a real current project.

## Reassessment rule

Before every phase, re-read the owner repository and re-evaluate scope. Newly discovered work is classified as:

- **migration blocker** — required for the current dependency chain to be correct;
- **follow-up migration** — important cross-project work but not required for this rollout;
- **backlog/improvement** — useful cleanup or parity work.

Only migration blockers extend Migration 003.

## Completion

Migration 003 is complete when:

- `tool.scad-project v0.12.0` is released and tag-qualified;
- `template.scad-project` is qualified against it;
- both SCAD libraries have been individually modernized enough for the current contract and released;
- the HUB75 frame consumes the resulting released versions and passes its Build/Verify/exact-main qualification;
- phase evidence is retained in this migration directory and issue #46.
