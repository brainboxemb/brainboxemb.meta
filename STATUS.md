# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

There is currently **no active cross-project migration** after completion of Migration 006.

Do not automatically start the next proposed migration merely because the previous one closed. Select it deliberately from the proposed/inactive set.

## Proposed / inactive

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation. It was deliberately kept outside Migration 006.

## Recently completed

### Migration 006 — simplify the Java execution architecture

**Complete.**

The released shared Java baseline is:

- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.java-project v0.3.2` / exact `c0ca2e1365a64bc626ca331a8170d13340ae0b36`;
- owner exact-main self-test `35190574150`, release `35190849340` and tagged self-test `35190862089` — green.

The immutable reference consumer is `template.java-project v0.1.0` at exact source `2406d362f1b93c433bb561bd8d09a9f6cde13774`. Its exact-main run `35192557796` proves normal protected-main publication with Windows mode `none`; tagged release verification `35192714047` proves Linux + native full Windows + exact Linux-artifact smoke and immutable `rel/v0.1.0/bld` publication.

The real multi-module consumer `2026-010-02.java.event-timing-framework` now consumes the released baseline on exact main `9aff579d824339b191c4d99be22d738f18562ad1`:

- sensitive PR/full: `35193846536` — green;
- isolated Java-only smoke: `35193503922` — green, native Windows Maven skipped;
- isolated documentation-only: `35193536122` — preflight only, no Java/Windows/publication;
- exact main: `35193989780` — green, Windows mode `none`, no Windows runner, exact `prod/bld` publication.

`prod/bld/source-sha.txt` identifies exact main `9aff579d...`; main timing capture is 56 s wall / 51 hosted-runner seconds with four Linux runners and no Windows runner.

A tooling migration does not force an unrelated product-version release. The generic immutable release path is proven by the tool and template releases; the real product retains its exact-tag/full-Windows release semantics and will exercise them at its next normal product release cadence.

Durable model: [Java execution model](docs/working-model/java-execution.md).
Canonical migration record: [Migration 006](migrations/006-java-execution-architecture/README.md).

### Migration 005 — simplify the SCAD execution architecture

**Complete.**

The SCAD execution/publication architecture and compact technical namespaces are fully qualified. Runtime/publication behaviour was immutably proven on the v0.14.9 consumer rollout using `dsg`, `bld` and `vrf`. The final released-guidance inconsistency was corrected in `tool.scad-project v0.14.10` at exact source `3ad040b2d9c26b8c482853157baeb99a8d9b36db`.

`template.scad-project` pinned the released guidance on main source `637906c49b90308ebba7e4477fa2e5036d9543da`; exact-main Production run `35140381160` is green and resolves `project-production.yml@v0.14.10` to exact `3ad040b2...`.

That final change was guidance-only and did not require a new template release merely to close the migration.

Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md).

Other completed migrations:

- [Migration 004 — SCAD repository execution model](migrations/004-scad-repository-execution-model/README.md) — complete.
- [Migration 003 — SCAD v0.12 rollout](migrations/003-scad-v0.12-rollout/README.md) — complete.
- [Migration 002 — SCAD build-decision audit](migrations/002-scad-build-decision-audit/README.md) — complete.
- [Migration 001 — consolidate public portfolio context](migrations/001-brainboxemb-meta/README.md) — complete.

## Parked / follow-up

- Moon as SCAD target engine — issue #51;
- self-contained physical-verification document packages — issue #18;
- one release flow for requested versions across project types — issue #20;
- standardise CHANGELOG format and add a shared template — issue #52;
- `tool.git-project` #17, #22 and #26 remain owner-local follow-ups.
