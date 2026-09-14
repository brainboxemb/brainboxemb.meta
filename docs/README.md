# Cross-project architecture and working model

This directory contains durable conventions that apply across multiple public brainboxemb repositories.

It is intentionally smaller than the historical planning trees in `meta.scad-projects`: current rules live here; detailed completed transition evidence remains in historical source repositories until archival.

## Architecture

- [Repository tooling boundaries](architecture/repository-tooling.md) — what `tool.git-project`, domain tools, consumers and `brainboxemb.meta` own.

## Working model

- [Generated output and publication](working-model/generated-output.md) — source/generated separation, Moon/domain execution boundary, publication namespaces and evidence identities.
- [Versioning and releases](working-model/versioning-and-releases.md) — independent versions, released cross-repository interfaces, dependency policy/locks and exact-revision release rule.

## Domain-specific context

SCAD-specific landscape and architecture live under [`../domains/scad/`](../domains/scad/).

Repository membership, lifecycle and current/classic project-infrastructure classification live in [`../repositories/catalog.yml`](../repositories/catalog.yml).

## What does not belong here

Keep these elsewhere:

- project-specific architecture/plans → owning project repository;
- implementation/API details → owning tool/library repository;
- current work/status → [`../STATUS.md`](../STATUS.md);
- repository-spanning migration sequencing/evidence → [`../migrations/`](../migrations/);
- generated/live GitHub status → dashboard/GitHub rather than maintained Markdown;
- completed detailed transition evidence → retained historical source until a later evidence-archive decision requires movement.
