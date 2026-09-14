# Current cross-project changes

This page tracks **temporary/current work that spans repositories**: active migrations, recently completed foundations, deferred follow-ups and proposed next migrations.

It is not the general overview of the brainboxemb repository collection. For that, start with [`README.md`](README.md). For the normal technical working model, use [`docs/`](docs/README.md).

## Active now

There is currently **no active cross-project migration**.

### Migration 001 — public portfolio consolidation

**Status: complete.**

Migration 001 established `brainboxemb.meta` as the public landing page, technical guide, canonical public repository catalog, domain overview, migration/evidence location and dashboard host.

Final qualification evidence:

- exact main commit: `e0104cb4e558c0fc10d7c20f6f4140a71f32cde8`;
- Deploy run: `34863909122`;
- 28 dashboard tests: success;
- runtime config: `27 repositories in 6 groups`;
- dashboard generation: 27 repositories;
- Pages artifact upload: success;
- Pages deployment: success.

The two superseded source repositories, `tech.scad` and `meta.scad-projects`, are both private and archived and are no longer part of the public catalog.

See [`migrations/001-brainboxemb-meta/`](migrations/001-brainboxemb-meta/) for retained migration evidence.

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

These remain valid follow-ups and are not active migrations:

- **Physical-verification document bundles** — issue #18.
- **Explicit cross-project release request/version preparation** — issue #20.
- **Architecture-view refresh** — issue #21.

## Proposed next migration — inactive

### Migration 002 — SCAD build-decision audit

**Status: proposed / inactive.**

Purpose: add a post-build audit in `tool.scad-project` that checks whether observed target outcomes are compatible with impacts that can actually be proven from changed inputs and structured build evidence.

It does not redesign SCons, implement physical-verification document bundles, introduce a second build engine or broadly migrate consumers.

Migration 002 requires an explicit activation decision. Before activation, its assumptions must be rechecked against the current `tool.scad-project` implementation.

See [`migrations/002-scad-build-decision-audit/README.md`](migrations/002-scad-build-decision-audit/README.md) and activation-gate issue #26.
