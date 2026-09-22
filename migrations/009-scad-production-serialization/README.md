# Migration 009 — serialize SCAD production and roll out corrected tooling

Status: **complete**

Activation PR: [#113](https://github.com/brainboxemb/brainboxemb.meta/pull/113)  
Completion PR: [#114](https://github.com/brainboxemb/brainboxemb.meta/pull/114)

## Goal

Remove the production-concurrency correctness race from the shared
current-generation SCAD stack and roll the corrected owner release through every
current `tool.scad-project` consumer.

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

The cancellation policy was owned by
`tool.scad-project/.github/workflows/project-production.yml`, so the fix
belonged in the shared owner rather than in HUB75.

## Owner correction

`tool.scad-project` PR #96 changed production concurrency so:

- same-PR runs may supersede stale work;
- production/default-branch pushes serialize instead of cancelling an in-progress
  predecessor;
- regression coverage rejects a return to unconditional cancellation.

That correction first shipped in v0.15.6.

Migration qualification then exposed an older normal-entrypoint defect:
`update-repo status` in the SCAD consumer wrapper performed an update instead
of forwarding a read-only status operation. Experiment 006 DEP-06 caught the
problem. `tool.scad-project` PR #98 restored the contract and added regression
coverage.

The final Migration 009 owner baseline is therefore:

- `tool.scad-project v0.15.7`;
- exact commit `bfaac9f6916c09bc6525abddf64c87238fe59103`;
- immutable tag `v0.15.7` points to that exact commit;
- release run `35735174529` is green.

## Qualification

The retained `exp.2026-006.scad-library-dependencies` lab requalified the
released v0.15.7 stack before the final portfolio rollout.

Merged-main source:
`c4f4690c6850fbe44395017ef81f43a0a7121629`.

All nine workflows are green on that source, including:

- DEP-06 status and safe update: run `35735859277`;
- normal dependency entrypoints: run `35735859241`;
- SCAD production: run `35735860077`;
- DEP-01 through DEP-05 and DEP-07 also green on the same source.

This proves both the production-serialization correction and the restored
read-only status/update contract against the retained Migration-008 dependency
acceptance boundary.

## Final rollout

Every catalogued current-generation consumer now declares
`tool.scad-project v0.15.7`, carries exact gitlink
`bfaac9f6916c09bc6525abddf64c87238fe59103`, and uses the canonical executable
`update-repo.sh` wrapper.

| Consumer | Final main | Evidence |
| --- | --- | --- |
| `template.scad-project` | `dc32a7c505930f254ee501706caaeac2e567c916` | exact-main production `35737063392`; `prod/bld` and `prod/vrf` on v0.15.7 |
| `lib.scad.clamps` | `2f800e0ec5f92e52cdbb1ebca1e314ed3bb9926d` | exact-main production `35737075983`; both production families on v0.15.7 |
| `lib.scad.hub75` | `9b73887d6cb7cdff6588c7830b30577b15d9e265` | exact-main production `35737089079`; both production families on v0.15.7 |
| `lib.scad.forge` | `21f22ac8435a919283bae36634f776fe03d65f2a` | exact-main production `35737100121`; both production families on v0.15.7 |
| `lib.scad.util` | `6bcafb8dddff76c2c3383053091c7ab2f63887ea` | exact-main production `35737110140`; both production families on v0.15.7 |
| `lib.scad.mechint` | `c7376baddae1c094a19f611b2577c9cbb0ae55de` | exact-main production `35737160277`; both production families on v0.15.7 |
| `2026-009-01.cad.HUB75-display-frame` | `9fec18b4f925f41f292201784de2608ccd0b21c4` | exact-main production `35736506128`; `prod/bld` and `prod/vrf` repaired to the same source on v0.15.7 |
| `2026-009-02.cad.hub75-component-lab` | `3f7aa5b49dd5d92e0190708380b4fd48596b0d50` | PR lab-build `35736977132` green; repository intentionally has no push-to-main build trigger |
| `exp.2026-006.scad-library-dependencies` | `c4f4690c6850fbe44395017ef81f43a0a7121629` | nine-workflow regression matrix green; production `35735860077` |

Classic SCAD/CAD repositories remained out of scope.

## HUB75 recovery

The original production gap is closed.

HUB75 exact-main production run `35736506128` completed successfully on
`9fec18b4f925f41f292201784de2608ccd0b21c4`. Both
`prod/bld/publication-info.txt` and `prod/vrf/publication-info.txt` identify:

- source `main`;
- commit `9fec18b4f925f41f292201784de2608ccd0b21c4`;
- `tool.scad-project v0.15.7`;
- exact root tool gitlink `bfaac9f6916c09bc6525abddf64c87238fe59103`;
- workflow run `35736506128`.

The stale-publication condition caused by the cancelled predecessor run no
longer exists.

## Completion

Migration 009 is complete because:

- the corrected shared owner is immutable and released;
- Experiment 006 qualifies both the concurrency and normal status/update
  contracts on the released owner;
- every in-scope current-generation consumer is aligned to v0.15.7 and the same
  exact tool gitlink;
- exact-main production evidence is green wherever the repository has a normal
  main-production lifecycle;
- HUB75 Build/Verification provenance is current again.

Further HUB75 mechanical work, including the detachable tube-mount/coupler WIP,
is project work and is not part of this completed migration.
