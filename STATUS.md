# Current cross-project changes

This page tracks **temporary/current work that spans repositories**: active migrations, recently completed foundations, deferred follow-ups and proposed next migrations.

It is not the general overview of the brainboxemb repository collection. For that, start with [`README.md`](README.md). For the normal technical working model, use [`docs/`](docs/README.md).

## Active now

### Migration 001 — consolidate coordination into `brainboxemb.meta`

**Status: active — remaining `meta.scad-projects` consolidation.**

The dashboard/catalog and `tech.scad` portions are already migrated. The remaining work is the bounded transfer of useful current coordination responsibility from `meta.scad-projects`.

Current slices:

1. **Readable status and next-migration model** — complete.
2. **Durable technical conventions** — complete; current shared guidance now lives under `docs/`.
3. **Active issue transfer and source redirect** — in progress; relevant old coordination issues are being moved/closed and `meta.scad-projects` will become a historical source.
4. **Consolidation closeout / archival readiness** — next; verify no current responsibility depends on the old meta repositories before archival.

Tracking: issues #11, #25, #31 and #32.

## Recently completed foundations

These are useful context, but they are **not active migrations**:

| Foundation | Status | Meaning |
| --- | --- | --- |
| Repository-build / Moon production transition | **complete** | Generic repository orchestration is in production owners and qualified across Java, engineering docs and SCAD. |
| SCAD structured build-decision telemetry | **complete** | Per-target outcomes `BUILT`, `CACHE_RESTORED`, `CURRENT`, `ERROR` are available as structured evidence. |
| Deterministic real-SCons decision conformance | **complete** | Supported selective-build/cache behaviour is covered by deterministic real-SCons tests. |
| Engineering-document assembly foundation | **complete** | `tool.eng-docs v0.2.0` provides the generic manifest/assembly boundary and has cross-domain consumer qualification. |
| `tech.scad` active catalog role | **superseded** | The current public repository catalog and SCAD landscape overview now live in `brainboxemb.meta`. |

The old phrase **“Step 2.5 core complete” is intentionally not used as current status**. It mixed a completed document-assembly foundation with an optional physical-verification follow-up and obscured what work was actually active.

## Deferred, not blocking

These are valid follow-ups but do not block the current consolidation or the proposed next SCAD tooling migration:

- **Physical-verification document bundles** — issue #18. Improve generic workbench-package assembly for cases such as HUB75 SQ-01; the existing project-local publication path continues to work.
- **Explicit cross-project release request/version preparation** — issue #20.
- **Architecture-view refresh** — issue #21.

## Proposed next migration — inactive

### Migration 002 — SCAD build-decision audit

**Status: proposed / inactive.**

Purpose: add a post-build audit in `tool.scad-project` that checks whether observed target outcomes are compatible with impacts that can actually be proven from changed inputs and structured build evidence.

It does not redesign SCons, implement physical-verification document bundles, introduce a second build engine or broadly migrate consumers.

Migration 002 may only become active after Migration 001 has transferred the required coordination context and the proposed audit is rechecked against the then-current `tool.scad-project` implementation.

See [`migrations/002-scad-build-decision-audit/README.md`](migrations/002-scad-build-decision-audit/README.md) and activation-gate issue #26.

## Historical source repositories

Until Migration 001 finishes:

- `meta.scad-projects` remains a historical/detail evidence source plus a temporary source for not-yet-transferred coordination material;
- `tech.scad` is already superseded as a current owner but remains available for history until archival.

Do not resume an old numbered roadmap mechanically. Start from the normal repository overview/technical guide, and use this page only when you need the current cross-project change status.