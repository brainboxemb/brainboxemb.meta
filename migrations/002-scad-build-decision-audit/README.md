# Migration 002 — SCAD build-decision audit

Status: **proposed / inactive**

Tracking issue: [#19](https://github.com/brainboxemb/brainboxemb.meta/issues/19)

## What problem would this solve?

`tool.scad-project` already records what happened to each build target, for example whether it was built, restored from cache or left current.

The proposed audit adds one extra check after a normal SCons build: if the available dependency information proves that a target was affected by a changed input, the reported result must make sense for that impact.

A simple example is a target that definitely depends on a changed SCAD file. It may be rebuilt or restored from a valid cache, but it should not be reported unchanged.

## What would be added?

The first version should stay conservative:

- use existing structured build/dependency evidence;
- distinguish proven impact from possible or unproven impact;
- accept `BUILT` and valid `CACHE_RESTORED` for a proven affected target;
- report a proven affected target as an error when it is incorrectly marked `CURRENT`;
- treat unnecessary rebuilds as observations/warnings at first rather than correctness failures;
- keep uncertainty visible instead of guessing.

Implementation belongs in [`tool.scad-project`](https://github.com/brainboxemb/tool.scad-project). This repository only keeps the cross-project migration plan and qualification record.

## What is deliberately not part of it?

Migration 002 does not:

- replace or reimplement SCons dependency handling;
- prove artifact integrity merely because a cache restore occurred;
- introduce another generic build engine;
- redesign physical-verification documentation;
- require a broad migration of SCAD projects.

The physical-verification document follow-up in issue #18 remains independent.

## Before activating it

The migration is not active merely because this plan exists. Before implementation starts:

1. reread the current `tool.scad-project` main branch, tests and build-decision report format;
2. confirm that this audit still solves a real current problem;
3. confirm that a post-build audit is still the smallest useful next step;
4. recheck which inputs can genuinely prove target impact;
5. simplify or change this plan if the implementation has evolved;
6. keep unrelated follow-ups outside the migration.

Activation means explicitly changing this migration to **active** and recording the reassessment in issue #19. There is no separate activation-gate issue.

## Expected qualification

When activated, tests should at least cover:

- proven dependency impact + `BUILT` → pass;
- proven dependency impact + valid `CACHE_RESTORED` → pass;
- proven dependency impact + `CURRENT` → fail;
- missing/invalid target outcome → fail;
- no proven impact + `CURRENT` → pass;
- no proven impact + `BUILT` → observation/warning;
- possible impact without enough evidence → report uncertainty rather than a false failure.

## When is the migration complete?

Migration 002 is complete only when the owner implementation, deterministic owner tests and agreed qualification evidence are green, and `tool.scad-project` documents the resulting audit behaviour.
