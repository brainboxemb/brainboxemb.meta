# Migration 004 — SCAD repository execution model

Status: **proposed / inactive**

Tracking issue: [#49](https://github.com/brainboxemb/brainboxemb.meta/issues/49)

## Goal

Decide and document the intended execution model for a current SCAD repository before changing the libraries again.

The immediate question is not whether a library *can* use Moon. The question is whether projects and libraries need different Build/Verify execution models at all, and if so, what concrete library-specific requirement justifies the difference.

`template.scad-project` is the reference project consumer. `lib.scad.clamps` is the practical reference library because it is small enough to expose the library requirements without the additional HUB75 complexity.

## Why this needs a migration

The current repositories expose two different execution models:

- `template.scad-project` and `2026-009-01.cad.HUB75-display-frame` run one SCAD production job and use a repository-level Moon task graph;
- `lib.scad.clamps` and `lib.scad.hub75` call separate reusable Build and Verify workflows, resulting in separate jobs and separate SCAD-toolchain container starts.

A difference may be valid, but it is currently not explained by a documented library requirement. The repositories should therefore not be changed merely for visual consistency, and the existing difference should not be preserved merely because it already exists.

## Before activation

Review the [change request](change-request.md) and answer the architectural questions there.

In particular, activation requires an agreed answer to:

1. what lifecycle behaviour is common to every current SCAD repository;
2. what is genuinely library-specific;
3. whether Moon adds enough value to belong to the common layer;
4. whether Build and Verify should remain logically independent while sharing one CI/container execution;
5. whether the SCAD container can be started later, after cheap repository-level decisions;
6. whether the current template task graph correctly represents the `tool.scad-project` Build/Verify contract;
7. whether a separate `template.scad-lib` is justified or whether `lib.scad.clamps` remains the practical reference library.

## Possible outcomes

This review is allowed to conclude any of the following:

- one common Moon-backed execution model for projects and libraries;
- one common execution shape with a lighter non-Moon library implementation;
- an intentionally different library execution model, with a concrete reason and documented trade-off;
- only corrections to the template/current model, with no library migration;
- creation of `template.scad-lib`, but only if repeated library-specific structure makes a separate template useful rather than decorative.

## Proposed implementation order if activated

The exact implementation steps are intentionally not fixed before the architecture review. If a repository change is justified, use this default order and re-evaluate it before each step:

1. correct or clarify the shared/reference model in `tool.git-project`, `tool.scad-project` and/or `template.scad-project`;
2. prove the library form with `lib.scad.clamps`;
3. apply the proven form to `lib.scad.hub75` only if it still makes sense;
4. requalify `2026-009-01.cad.HUB75-display-frame` only when shared tooling/reference behaviour changed in a way that affects it;
5. document the final project-versus-library decision in the relevant repositories and the SCAD overview.

## Not part of this migration

- physical HUB75 verification such as SQ-01;
- CAD geometry/API changes;
- introducing Moon merely to make repository file trees look alike;
- combining Build and Verify into one semantic domain;
- introducing another dependency/change detector alongside the existing repository orchestration and SCons dependency model.

No implementation work starts until this migration is explicitly activated.