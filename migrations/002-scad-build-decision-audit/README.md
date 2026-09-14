# Migration 002 — SCAD build-decision audit

Status: **proposed / inactive**

Tracking issue: [#19](https://github.com/brainboxemb/brainboxemb.meta/issues/19)

Activation gate: [#26](https://github.com/brainboxemb/brainboxemb.meta/issues/26)

## What this migration would do

Add one additional assurance layer to the current SCAD build system: after a real build, compare the structured target decisions with impact that can actually be proven from changed inputs.

Example:

```text
changed SCAD dependency
        ↓
current target/dependency manifest proves target A depends on it
        ↓
SCons runs normally
        ↓
structured report says what happened to target A
        ↓
audit checks that the outcome is compatible with the proven impact
```

The purpose is to detect correctness contradictions such as a target that is definitely affected but is reported `CURRENT`.

## Why it is separate

The foundations already exist:

- structured target outcomes are implemented;
- deterministic real-SCons decision tests are implemented;
- repository-build/Moon orchestration migration is complete.

This audit is therefore a new, bounded capability. It is not unfinished work from the repository-build migration and it does not need the deferred physical-verification document-bundle work.

## Owner

Implementation owner: `brainboxemb/tool.scad-project`.

`brainboxemb.meta` owns only:

- migration scope and activation decision;
- cross-project contract/ordering;
- qualification evidence and closeout.

## Proposed initial scope

The first version should be conservative.

### Proven impact

Treat impact as proven only when current structured evidence directly links a changed input to a target, for example:

```text
changed path ∈ target.sources
```

A future independently stored baseline may prove additional causes such as changed target-spec/backend signatures, but the first implementation must not invent certainty from a current digest alone.

### Allowed outcomes

For a proven affected target, both can be legitimate depending on cache context:

```text
BUILT
CACHE_RESTORED
```

`CURRENT` for a proven affected existing target is a correctness contradiction.

`ERROR` remains an error.

For targets with no proven impact, an unnecessary `BUILT` is initially an overbuild warning/observation rather than a correctness failure.

## Important boundaries

This migration must not:

- reimplement or second-guess SCons dependency resolution;
- infer artifact integrity from `CACHE_RESTORED`;
- turn GitHub Actions cache metadata into a second per-target oracle;
- introduce a generic build engine;
- redesign documentation/physical verification;
- force broad consumer migration merely to qualify the audit.

## Reassessment before activation

Before changing status to `active`:

1. verify Migration 001 has transferred the required coordination context;
2. inspect current `tool.scad-project` main, tests and build-decision report schema;
3. confirm a post-build audit is still the smallest useful next assurance layer;
4. revalidate the exact input/evidence matrix and command/API shape;
5. simplify the plan if current implementation has made part of it obsolete;
6. keep physical-verification bundle work separate unless new evidence creates a real dependency.

## Proposed evidence

When activated, qualification should include deterministic cases for at least:

- proven dependency impact + `BUILT` → pass;
- proven dependency impact + valid `CACHE_RESTORED` → pass;
- proven dependency impact + `CURRENT` → fail;
- invalid/missing target outcome → fail;
- no proven impact + `CURRENT` → pass;
- no proven impact + `BUILT` → warning/observation initially;
- possible impact without independent baseline → report uncertainty, do not claim correctness failure;
- cache provenance remains explanatory rather than an independent artifact-integrity guarantee.

## Completion condition

Migration 002 is complete only when the owner implementation, deterministic owner tests and agreed cross-project qualification evidence are green, and the resulting audit contract is documented in `tool.scad-project`.

## Activation

This directory being present does **not** activate the migration.

Activation is an explicit coordination decision: change this status to `active`, close activation-gate issue #26 as completed, record the reassessment, and only then start owner implementation.
