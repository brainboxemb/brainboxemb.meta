# Current cross-project changes

This page tracks **temporary/current work that spans repositories**: active migrations, recently completed foundations, deferred follow-ups and proposed next migrations.

It is not the general overview of the brainboxemb repository collection. For that, start with [`README.md`](README.md). For the normal technical working model, use [`docs/`](docs/README.md).

## Active now

### Migration 001 — consolidate public portfolio context into `brainboxemb.meta`

**Status: final qualification pending.**

The substantive consolidation is complete:

- the dashboard is a sub-capability of `brainboxemb.meta`;
- `repositories/catalog.yml` is the canonical public repository catalog;
- durable SCAD landscape knowledge formerly owned by `tech.scad` lives under `domains/scad/`;
- durable cross-project project/tooling conventions formerly coordinated through `meta.scad-projects` live under `docs/` and the migration records here;
- relevant open work was completed, transferred or explicitly deferred;
- `tech.scad` and `meta.scad-projects` are now both **private and archived**;
- both private repositories have been removed from the public-only catalog in the current closeout change.

The only remaining Migration-001 gate is to qualify the dashboard/Pages output against the resulting **27-public-repository** catalog and record that exact-main evidence.

Tracking: issues #11, #25 and #32.

## Recently completed foundations

These are useful context, but they are **not active migrations**:

| Foundation | Status | Meaning |
| --- | --- | --- |
| Repository-build / Moon production transition | **complete** | Generic repository orchestration is in production owners and qualified across Java, engineering docs and SCAD. |
| SCAD structured build-decision telemetry | **complete** | Per-target outcomes `BUILT`, `CACHE_RESTORED`, `CURRENT`, `ERROR` are available as structured evidence. |
| Deterministic real-SCons decision conformance | **complete** | Supported selective-build/cache behaviour is covered by deterministic real-SCons tests. |
| Engineering-document assembly foundation | **complete** | `tool.eng-docs v0.2.0` provides the generic manifest/assembly boundary and has cross-domain consumer qualification. |
| `tech.scad` catalog/knowledge role | **retired** | Current public catalog and SCAD portfolio knowledge live in `brainboxemb.meta`; the old repository is private/archived. |
| `meta.scad-projects` coordination role | **retired** | Current guidance and cross-project planning live in `brainboxemb.meta`; the old repository is private/archived. |

The old phrase **“Step 2.5 core complete” is intentionally not used as current status**. It mixed a completed document-assembly foundation with an optional physical-verification follow-up and obscured what work was actually active.

## Deferred, not blocking

These remain valid follow-ups and are independent from Migration 001:

- **Physical-verification document bundles** — issue #18.
- **Explicit cross-project release request/version preparation** — issue #20.
- **Architecture-view refresh** — issue #21.

## Proposed next migration — inactive

### Migration 002 — SCAD build-decision audit

**Status: proposed / inactive.**

Purpose: add a post-build audit in `tool.scad-project` that checks whether observed target outcomes are compatible with impacts that can actually be proven from changed inputs and structured build evidence.

It does not redesign SCons, implement physical-verification document bundles, introduce a second build engine or broadly migrate consumers.

Migration 002 does **not** activate automatically when Migration 001 closes. Its assumptions must first be rechecked against the then-current `tool.scad-project` implementation and it requires an explicit activation decision.

See [`migrations/002-scad-build-decision-audit/README.md`](migrations/002-scad-build-decision-audit/README.md) and activation-gate issue #26.
