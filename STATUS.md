# Current cross-project status

This page is the short human-readable answer to: **what is finished, what is still open, and what should happen next?**

Detailed historical step numbering remains in source repositories and retained evidence, but it is deliberately not the primary status language here.

## Active now

### Migration 001 — consolidate coordination into `brainboxemb.meta`

**Status: active — Phase 5B durable coordination conventions.**

The dashboard/catalog and `tech.scad` portions are already migrated. The remaining work is the bounded transfer of current coordination responsibility from `meta.scad-projects`.

Current Phase-5 slices:

1. **5A — readable current status** — **complete**; `STATUS.md` and the proposed/inactive Migration 002 now make finished/deferred/next work explicit.
2. **5B — durable SCAD coordination conventions** — **active now**; move only still-current cross-project architecture/working rules, not historical plans wholesale.
3. **5C — active issue transfer and source redirect** — finish moving relevant issues, then make `meta.scad-projects` point to the new owner.
4. **5D — consolidation closeout / archival readiness** — close Migration 001 and archive superseded coordination sources when safe.

Tracking: issues #11, #25, #30, #31 and #32.

## Finished foundations

These are complete and should not be treated as current blocking migrations:

| Foundation | Status | Meaning |
| --- | --- | --- |
| Repository-build / Moon production transition | **complete** | Generic repository orchestration is in production owners and qualified across Java, engineering docs and SCAD. |
| SCAD structured build-decision telemetry | **complete** | Per-target outcomes `BUILT`, `CACHE_RESTORED`, `CURRENT`, `ERROR` are available as structured evidence. |
| Deterministic real-SCons decision conformance | **complete** | Supported selective-build/cache behaviour is covered by deterministic real-SCons tests. |
| Engineering-document assembly foundation | **complete** | `tool.eng-docs v0.2.0` provides the generic manifest/assembly boundary and has cross-domain consumer qualification. |
| `tech.scad` active catalog role | **superseded** | The current public repository catalog and SCAD landscape overview now live in `brainboxemb.meta`. |

The phrase **“Step 2.5 core complete” is intentionally retired from current-status wording**. It mixed a completed document-assembly foundation with one optional physical-verification follow-up and made the actual next work unclear.

## Current durable guidance

The cross-project rules being consolidated now live under [`docs/`](docs/):

- repository/tool/domain ownership boundaries;
- `tool.git-project` generic bootstrap/dependency/orchestration role;
- current versus classic project-infrastructure classification;
- generated-output namespaces such as `dev/pr-N/*`, `prod/*`, `rel/vX.Y.Z/*`;
- producer versus materialization/publication evidence;
- independent repository versions and exact-revision release rules.

SCAD-specific landscape details remain under [`domains/scad/`](domains/scad/).

## Deferred, not blocking

These are useful follow-ups, but none blocks Migration 001 or the proposed next SCAD tooling migration:

- **Physical-verification document bundles** — issue #18. Improve generic workbench-package assembly for cases such as HUB75 SQ-01; current project-local publication continues to work.
- **Explicit cross-project release request/version preparation** — issue #20.
- **Architecture-view refresh** — issue #21.

## Proposed next migration — inactive

### Migration 002 — SCAD build-decision audit

**Status: proposed / inactive.**

Purpose: add a post-build audit in `tool.scad-project` that checks whether observed target outcomes are compatible with impacts that can actually be proven from changed inputs and structured build evidence.

It does **not** redesign SCons, implement physical-verification document bundles, introduce a second build engine or broadly migrate consumers.

Migration 002 may only become active after Migration 001 has transferred the required coordination context and the proposed audit is rechecked against the then-current `tool.scad-project` implementation.

See [`migrations/002-scad-build-decision-audit/README.md`](migrations/002-scad-build-decision-audit/README.md) and activation-gate issue #26.

## Historical source repositories

Until Migration 001 finishes:

- `meta.scad-projects` remains historical/detail evidence plus a temporary source for not-yet-transferred coordination material;
- `tech.scad` is already superseded as a current owner but remains available for history until archival.

Do not resume an old numbered roadmap mechanically. Start from this status, then open the active or explicitly activated migration plan.