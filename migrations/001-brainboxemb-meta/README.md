# Migration 001 — Consolidate public portfolio context

Status: **complete**

Migration 001 turned the former dashboard repository into `brainboxemb.meta` and brought the useful public overview from `tech.scad` and `meta.scad-projects` into one place.

The migration is finished. This page is the short historical summary; detailed qualification is kept in [evidence.md](evidence.md).

## Result

`brainboxemb.meta` now provides:

- the public repository overview and machine-readable catalog;
- the dashboard;
- reader-facing guidance about projects and shared tooling;
- domain guides such as [SCAD and CAD](../../domains/scad/README.md);
- cross-project migration plans and retained evidence when needed.

Project, library and tool implementation remains in the repository that owns it.

The older `tech.scad` and `meta.scad-projects` repositories are now private archives and are no longer part of the public catalog.

## Phases

| Phase | Result | Main evidence |
| --- | --- | --- |
| 1 — Meta foundation | Established the new repository identity and migration structure. | PR #12, merge `62df2648…`, run `34853241040` |
| 2 — Public repository catalog | Introduced one public catalog used by the dashboard. | PR #14, merge `7a8ad397…`, run `34855023365` |
| 3 — Dashboard subproject | Moved dashboard implementation under `dashboard/`. | PR #15, merge `fa1a2157…`, run `34856871791` |
| 4 — SCAD landscape | Moved useful `tech.scad` knowledge into `domains/scad/`. | PRs #16/#17 and `tech.scad` PR #2 |
| 5 — Coordination transfer | Moved durable cross-project guidance/status from `meta.scad-projects`, classified remaining work, and prepared both old repositories for private archival. | PRs #35–#40 and old-meta PR #44 |
| Final qualification | Qualified the post-archive 27-repository dashboard on exact main. | commit `e0104cb4…`, run `34863909122` |

## Final dashboard evidence

Run `34863909122` on exact main commit `e0104cb4e558c0fc10d7c20f6f4140a71f32cde8` showed:

- 28 tests passed;
- runtime configuration contained **27 repositories in 6 groups**;
- dashboard generation completed for 27 repositories;
- Pages artifact upload succeeded;
- Pages deployment succeeded.

## Documentation correction before closeout

During final review, the consolidated documentation was found to be too agent/architecture-oriented and the old human-readable SCAD indexes had been over-compressed into the YAML catalog.

Before closing the migration, the public documentation was therefore simplified and the readable SCAD entry points for **projects**, **libraries** and **tooling/templates** were restored under `domains/scad/`.

This is intentionally separate from the machine-readable catalog: the catalog drives tooling, while the Markdown pages help people understand the repository collection.

## Work not activated by this migration

Migration 002 — [SCAD build-decision audit](../002-scad-build-decision-audit/README.md) remains **proposed / inactive**.

Deferred items such as physical-verification document bundles remain separate follow-up work. Completing Migration 001 does not activate them.
