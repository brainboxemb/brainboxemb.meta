# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### PoP — reusable Java CI architecture qualification

**Active — local + build-model/cache-independent qualification complete; cross-run qualification next.**

[PoP/experiment record](experiments/004-java-ci-architecture/README.md) · tracking issue [#69](https://github.com/brainboxemb/brainboxemb.meta/issues/69) · implementation/evidence repository `brainboxemb/exp.2026-004.java-ci-architecture`

The current cross-project work track is a generic Java/software CI **Proof of Principle (PoP)**, not a migration and not an event-timing product task.

The design remains:

```text
Concept / target architecture
        ↓
Proof of Principle
        ↓
Qualification
        ↓
Production migration
```

The PoP repository remains a repeatable qualification/regression environment after adoption. Later migration or production CI problems should preferably be reduced to declarative cases there when the fixture can represent them faithfully.

The local same-worktree Maven Build Cache PoP is now qualified:

- exact experiment main `bc5d1b16da3820b72430611b65969ec7fb0588d0`;
- exact-main workflow run `35250860673` — green across discovery plus all 14 control/cache testcase jobs;
- seven declarative cases cover cold, unchanged warm, docs-only, app code-only, shared-core, code+unit-test and unit-test-only behaviour;
- native Maven `cache-report*.xml` is retained and asserted as the module-level cache oracle;
- JAR archive bytes and semantic payload are measured separately;
- unchanged/docs-only reuse all four modules and rerun no tests;
- app-local changes rebuild only `app` and rerun the two app test classes;
- shared-core changes invalidate the required dependent graph;
- a test-only change invalidates the app module/tests while preserving the production JAR payload.

The target responsibility split remains GitHub Actions for runner/event orchestration, Moon/generic tooling for repository/capability affected selection, and Maven for Java reactor/lifecycle/build/test semantics.

Caching is an **optional optimization capability**, not a correctness dependency. The intended project-level modes are `none | local | shared`, with `none` as the safe initial/default mode and an explicit forced-fresh/cache-bypass path available regardless of the configured mode. Projects should opt into caching when build/test scale makes the extra mechanism worthwhile rather than adopting it merely because the framework supports it.

Build-model/configuration and cache-independent execution are now qualified on exact experiment main `4106f71f09ef98e3a5ce5a1a9b965f27219cf0e7`, exact-main run `35317952373` — green across discovery plus all 22 control/cache testcase jobs. CI-08 through CI-11 prove root/shared versus module-local model invalidation, shared dependency-version invalidation, and correct Maven execution without consuming build-cache results. The next qualification slice is actual toolchain/input identity plus fresh-runner/cross-run shared-cache reuse; fallback and repeated performance qualification follow afterward.

There is currently **no active migration**.

## Proposed / inactive

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation. It remains separate from the active Java CI PoP and must not start automatically.

## Recently completed

### Migration 006 — simplify the Java execution architecture

**Complete.**

The released shared Java baseline is:

- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.java-project v0.3.2` / exact `c0ca2e1365a64bc626ca331a8170d13340ae0b36`;
- owner exact-main self-test `35190574150`, release `35190849340` and tagged self-test `35190862089` — green.

The immutable reference consumer is `template.java-project v0.1.0` at exact source `2406d362f1b93c433bb561bd8d09a9f6cde13774`. Its exact-main run `35192557796` proves ordinary protected-main publication with Windows mode `none`; tagged release verification `35192714047` proves Linux + native full Windows + exact Linux-artifact smoke and immutable `rel/v0.1.0/bld` publication.

The real multi-module consumer `2026-010-02.java.event-timing-framework` first qualified the released lifecycle on exact main `9aff579d824339b191c4d99be22d738f18562ad1`:

- sensitive PR/full: `35193846536` — green;
- isolated Java-only smoke: `35193503922` — green, native Windows Maven skipped;
- isolated documentation-only: `35193536122` — preflight only, no Java/Windows/publication;
- exact main: `35193989780` — green, Windows mode `none`, no Windows runner, exact `prod/bld` publication.

A subsequent normal product release exposed one product-owned packaging defect after the otherwise successful `v0.2.0` tag qualification. The fail-safe correctly archived that consumed candidate as `v0.2.0-failed`; `0.2.0` was not reused.

The corrected immutable downstream baseline is now:

- `2026-010-02.java.event-timing-framework v0.2.1`;
- exact source `0f9dbc2f5aa0beaec8f63465ada83f2bc2a83709`;
- ordinary-main run `35211527836` — green, Windows disabled, Linux canonical + `prod/bld` publication;
- exact-tag release run `35211641563` — green, Linux canonical + native full Windows Maven + exact Linux-artifact Windows smoke + `rel/v0.2.1/bld` + GitHub Release publication;
- annotated tag `v0.2.1` points to exact source `0f9dbc2f...`;
- `rel/v0.2.1/bld/source-sha.txt` identifies the same exact source;
- release timing capture: 81 s wall / 107 hosted-runner seconds, with the 66 s native Windows job the dominant hosted-compute cost;
- release assets include the app JAR, framework JAR, SHA256 checksums and finalized evidence archive.

The architectural point remains unchanged: Migration 006 did not require manufacturing a product release merely for tooling proof. The product was subsequently released through its normal product-owned release flow, and `v0.2.1` now provides additional immutable downstream evidence of the same contract.

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

- [Moon as SCAD target engine](experiments/003-moon-scad-target-engine/README.md) — parked experiment, issue #51;
- self-contained physical-verification document packages — issue #18;
- one release flow for requested versions across project types — issue #20;
- standardise CHANGELOG format and add a shared template — issue #52;
- `tool.git-project` #17, #22 and #26 remain owner-local follow-ups.