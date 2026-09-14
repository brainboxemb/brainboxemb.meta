# Migration 003 qualification evidence

This page records the repository-owned evidence used to qualify the ordered SCAD v0.12 rollout.

## Phase A — `tool.scad-project v0.12.0`

Release source: `68301267273ea21c4b82ff3b26e1c8a30ff7b065`

- exact-main Test run: `34870452241` — passed;
- release run: `34870689415` — passed;
- tag Test run: `34870705648` — passed;
- immutable released version: `v0.12.0`.

The release includes the Migration-002 `build-audit` capability. Migration 003 does not add generic changed-path discovery or automatic audit enforcement to consumers.

## Phase B — `template.scad-project`

Qualified main: `57ed48879370c5c3b60076ccb5a526d154fa6aa9`

- PR #20 qualification run: `34871385436` — passed;
- exact-main qualification run: `34871575879` — passed;
- build and verification publication both passed.

The first PR run (`34871082562`) exposed one stale template-owned v0.11.0 assertion. The actual Build and Verify geometry already succeeded; the assertion was corrected and the complete qualification rerun passed.

## Phase C — `lib.scad.clamps`

Qualified main/release source: `52048164db5e5da0b9522c758551bc3af65cae45`

- PR #6 Build: `34872213905` — passed;
- PR #6 Verify: `34872213879` — passed;
- exact-main Build: `34872343290` — passed;
- exact-main Verify: `34872343227` — passed;
- release run: `34872490224` — passed;
- released version: `v0.1.2`.

No library API or geometry changes were required. Existing OpenSCAD/PythonSCAD verification remained compatible with the current Build/Verify contract.

## Phase C — `lib.scad.hub75`

Qualified main/release source: `3174d3b0d69f0bc590e6b0e13d2ba976159a5014`

- PR #21 Build: `34872776520` — passed;
- PR #21 Verify: `34872776461` — passed;
- exact-main Build: `34873554237` — passed;
- exact-main Verify: `34873554283` — passed;
- release run: `34873678878` — passed;
- released version: `v0.1.3`.

The panel API and main verification behaviour were preserved.

### Separate physical-verification work

Draft PR #19 is not part of Migration 003. It is a dedicated `lib.scad.hub75` physical-verification step that will be continued after this migration.

The branch was brought forward onto the v0.1.3/v0.12.0 baseline with two-parent merge commit `379a553d86abb48672e763ca84fd966a7ab2f38d` without rewriting its physical-verification history.

- PR #19 Build: `34874033509` — passed;
- PR #19 Verify: `34874033493` — passed, including verification publication;
- the published workbench output still contains separate Dutch and English SQ-01 test cases plus the testcase template under `dev/pr-19/verification`.

PR #19 remains draft because physical SQ-01 work is pending. The project-specific SQ-01 link rewrite remains in place; generic self-contained document packaging stays tracked by `brainboxemb.meta#18`.

## Phase D — `2026-009-01.cad.HUB75-display-frame`

Target dependency state:

- `tool.scad-project v0.12.0` / `68301267273ea21c4b82ff3b26e1c8a30ff7b065`;
- `lib.scad.hub75 v0.1.3` / `3174d3b0d69f0bc590e6b0e13d2ba976159a5014`.

Qualified main: `99ada1ed0f186259c57b4cdb76354adaa4b78cfe`

- PR #30 final-head production run: `34875048610` — passed;
- PR build publication: passed;
- PR verification publication: passed;
- exact-main production run: `34875322954` — passed;
- exact-main build publication: passed;
- exact-main verification publication: passed.

The existing Moon/T6 production graph, geometry, fit/section verification, interactive smoke checks, execution evidence, domain evidence and materialization evidence all remained green. No frame release was created because its current `Unreleased` section also contains independent geometry work.

## Result

Migration 003 is complete. The dependency chain is now based on released and qualified versions from the tool through the template and libraries to the real HUB75 frame consumer.
