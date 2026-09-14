# Migration 002 — SCAD build-decision audit

Status: **active**

Tracking issue: [#19](https://github.com/brainboxemb/brainboxemb.meta/issues/19)

Implementation change request: [change-request.md](change-request.md)

## Goal

Add a conservative post-build audit to `tool.scad-project`.

The audit checks whether the structured build outcome for a target contradicts impact that can actually be proven from changed inputs and the target's recorded SCAD dependency list.

Example: when the build report proves a target depends on a changed SCAD file, `BUILT` or `CACHE_RESTORED` can be valid, but `CURRENT` is a correctness contradiction.

## Reassessment before activation

Migration 002 was rechecked against current `tool.scad-project` main before activation.

The current implementation already provides the foundations the audit needs:

- schema-v1 machine-readable target outcomes: `BUILT`, `CACHE_RESTORED`, `CURRENT`, `ERROR`;
- each target report contains its resolved `sources` / OpenSCAD dependencies;
- deterministic real-SCons conformance tests already cover private/shared dependency changes and cache behaviour.

The main correction to the earlier high-level plan is that the first implementation does **not** need another dependency model and must not implement generic Git change discovery.

Instead, the first slice takes an explicit list of changed paths and evaluates those paths against the existing target `sources` evidence.

## Owner

Implementation owner: [`brainboxemb/tool.scad-project`](https://github.com/brainboxemb/tool.scad-project).

`brainboxemb.meta` owns only the change request, migration scope, ordering and retained qualification evidence.

## First implementation slice

The active first slice is defined in [change-request.md](change-request.md).

In summary it adds:

- a pure build-decision audit module;
- an explicit `scad-project build-audit` command;
- schema-v1 machine-readable audit output;
- exact changed-path-to-target-source matching;
- failure for proven affected targets reported `CURRENT`;
- warnings, not failures, for possible overbuild;
- focused unit and CLI tests.

The audit is **not automatically called by `scad-project build` in this first slice** because generic changed-path discovery is not currently owned by the SCAD build command.

## Not part of this migration slice

- generic `git diff` / GitHub-event interpretation;
- SCons reimplementation;
- artifact-content integrity checks;
- automatic workflow enforcement;
- physical-verification document packages (#18);
- broad `lib.scad.clamps` / `lib.scad.hub75` rollout.

The libraries can be updated after this audit capability is implemented and qualified; consumer rollout is a separate decision.

## Qualification

Migration 002 is complete when:

1. the owner implementation satisfies the change-request acceptance criteria;
2. owner unit/CLI tests are green;
3. structured audit output and failure/warning behaviour are documented in `tool.scad-project`;
4. the agreed qualification evidence is recorded here;
5. no extra Git/change-discovery or consumer-migration scope was pulled into the implementation.
