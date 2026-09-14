# Migration 002 — SCAD build-decision audit

Status: **complete**

Tracking issue: [#19](https://github.com/brainboxemb/brainboxemb.meta/issues/19)

Implementation change request: [change-request.md](change-request.md)

Qualification evidence: [evidence.md](evidence.md)

## What changed

`tool.scad-project` now has an explicit post-build audit for its structured SCons build-decision reports.

The audit receives a build-decision report plus changed paths and checks whether an observed target outcome contradicts impact that can actually be proven from the target's recorded SCAD dependencies.

For example, when a changed path occurs in a target's recorded `sources`, the target may be `BUILT` or `CACHE_RESTORED`, but it must not be reported `CURRENT`.

## Implementation result

The owner implementation added:

- a pure build-decision audit module;
- `scad-project build-audit`;
- explicit changed-path input, including newline-delimited files;
- schema-v1 machine-readable audit evidence;
- exact changed-path-to-target-source matching;
- failure for proven affected targets reported `CURRENT`;
- warnings rather than failures for possible overbuild;
- focused policy/CLI tests and owner documentation.

The implementation deliberately reuses the existing target `sources` evidence. It does not create another dependency model.

## Boundary retained

The first implementation does **not** discover changed repository paths itself.

Generic `git diff` / GitHub-event interpretation does not belong in the SCAD build policy layer. Changed paths are explicit audit input until a separate generic integration is justified.

Also not included:

- SCons reimplementation;
- cache artifact-content integrity checks;
- automatic Build/Verify workflow enforcement;
- physical-verification document packages (#18);
- `lib.scad.clamps` / `lib.scad.hub75` rollout.

## Qualification

Owner PR #49 merged as `d4991b8b4ebf0746e19030d5ca72662976ee3aed`.

Both the final PR qualification and exact-main qualification passed with **200 tests**. See [evidence.md](evidence.md) for exact runs and artifacts.

## Next decision

Migration 002 itself is complete.

Before updating SCAD library consumers, reassess how the new `tool.scad-project` capability should be released/versioned. Consumer updates should not silently depend on an arbitrary unreleased main commit when a normal tool release is the appropriate contract.
