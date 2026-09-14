# Moon as SCAD target engine

Status: **parked**

Tracking issue: [#51](https://github.com/brainboxemb/brainboxemb.meta/issues/51)

Implementation owner: `tool.scad-project`

Related migration: Migration 004 — SCAD repository execution model

## Question

Can Moon replace all or part of the current SCons target-execution layer in `tool.scad-project` while preserving the fine-grained dependency, selective rebuild and cache behaviour that is already qualified?

## Why this is parked

Migration 004 is already changing the higher-level execution model around:

- one understandable SCAD production lifecycle;
- Build/Verify aggregation;
- affected/preflight decisions before expensive SCAD execution;
- container startup;
- publication placement;
- justified differences between projects and libraries.

Replacing the fine-grained target engine at the same time would make the migration too broad and would make performance/correctness evidence hard to attribute.

For Migration 004, SCons therefore remains the qualified target engine.

## Current baseline

`tool.scad-project` already has an engine-independent OpenSCAD dependency scanner. It discovers recursive `use`/`include` dependencies and static imported assets, then the SCons driver registers those dependencies per configured PNG/STL target.

That provides selective invalidation at target level. A coarse Moon task with a repository-wide `**/*.scad` input is not equivalent.

## Experiment candidates

When this experiment is activated, compare at least:

1. Moon for repository orchestration with SCons for SCAD targets;
2. coarse Moon tasks for Build/Verify domains;
3. fine-grained Moon tasks generated from `tool.scad-project` target configuration and the existing OpenSCAD dependency scanner.

## Evidence required

The experiment must cover cold, unchanged and selective-change scenarios, including:

- one target entrypoint changed;
- a transitive include used by only one target changed;
- a shared include changed;
- an imported asset changed;
- an unrelated documentation change;
- verification-only changes;
- cache/hydration restoration;
- understandable Build/Verify decision evidence.

## Decision supported

SCons should only be replaced if the Moon-based model is at least as correct and selective while materially simplifying the stack or improving execution, caching or evidence.

## Reactivation trigger

Revisit after Migration 004 has settled the repository-level execution model, unless Migration 004 finds a concrete blocker that specifically requires reconsidering the target-engine boundary.
