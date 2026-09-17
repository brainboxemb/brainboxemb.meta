# Moon as SCAD target engine

Status: **parked**

Tracking issue: [#51](https://github.com/brainboxemb/brainboxemb.meta/issues/51)

Implementation owner when adopted: `tool.scad-project`

Related migration history: Migration 004 — SCAD repository execution model

## Question

Can Moon replace all or part of the current SCons target-execution layer in `tool.scad-project` while preserving the fine-grained dependency, selective rebuild and cache behaviour that is already qualified?

## Why this is parked

Migration 004 deliberately kept SCons as the qualified fine-grained target engine while the repository-level execution model was being changed. Replacing the target engine at the same time would have made performance and correctness evidence hard to attribute.

## Current baseline

`tool.scad-project` has an engine-independent OpenSCAD dependency scanner. It discovers recursive `use`/`include` dependencies and static imported assets, after which the current target engine registers dependencies per configured PNG/STL target.

That provides selective invalidation at target level. A coarse Moon task with a repository-wide `**/*.scad` input is not equivalent.

## Experiment candidates

When this experiment is reactivated, compare at least:

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

Revisit when SCAD target-engine simplification is deliberately selected as active experiment work. Do not reactivate it merely because another experiment or migration completes.
