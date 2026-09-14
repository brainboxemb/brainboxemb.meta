# Migration 002 qualification evidence

Migration 002 implemented and qualified the first post-build SCAD build-decision audit capability in `brainboxemb/tool.scad-project`.

## Owner implementation

- owner repository: `brainboxemb/tool.scad-project`
- owner PR: #49 — `Implement SCAD build-decision audit command`
- final PR head: `d5c8221c550258c872aca3f5aa6cab23b6f989c0`
- merge commit: `d4991b8b4ebf0746e19030d5ca72662976ee3aed`

Implemented owner files include:

- `src/scad_project/build_decision_audit.py`
- `src/scad_project/cli.py` (`scad-project build-audit`)
- `docs/build-decision-audit.md`
- `tests/test_build_decision_audit.py`
- `tests/test_build_audit_cli.py`

## PR qualification

GitHub Actions Test run `34868571369` on final PR head:

- installed CLI smoke: success;
- source launcher smoke: success;
- unit tests: **200 passed**;
- generated unit-test documentation: success;
- unit-test documentation artifact upload: success;
- artifact: `10358002000`.

The earlier failing run found only missing repository-required structured module docstrings in the two new test files. After those documentation requirements were corrected, the full test suite passed.

## Exact-main qualification

GitHub Actions Test run `34868783229` checked out exact main commit `d4991b8b4ebf0746e19030d5ca72662976ee3aed` and completed successfully:

- installed CLI smoke: success;
- source launcher smoke: success;
- unit tests: **200 passed**;
- generated unit-test documentation: success;
- unit-test documentation artifact upload: success;
- artifact: `10358226701`.

## Qualified behaviour

The implemented audit:

- consumes `scad-project.build-decisions` schema version 1;
- accepts explicit changed paths directly or from newline-delimited files;
- uses the existing per-target `sources` evidence rather than creating a second dependency model;
- treats an exact changed-source match as `PROVEN` impact;
- accepts `BUILT` and `CACHE_RESTORED` for proven impact;
- fails `PROVEN + CURRENT`;
- fails target `ERROR`;
- treats `BUILT` without proven impact as a warning rather than a correctness failure;
- writes `scad-project.build-decision-audit` schema version 1 evidence;
- preserves failure evidence before returning exit status 1;
- fails closed for malformed/unsupported source evidence.

## Deliberately deferred

Migration 002 did not add:

- generic Git/GitHub changed-path discovery;
- automatic Build/Verify workflow enforcement;
- another dependency engine or SCons implementation;
- cache artifact-content integrity checks;
- consumer-library rollout.

Those require separate justification. In particular, `lib.scad.clamps` and `lib.scad.hub75` can now be assessed as consumers after deciding how the newly merged `tool.scad-project` capability should be released/versioned.
