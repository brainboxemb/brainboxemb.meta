# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

There is currently **no active repository-spanning migration or PoP**.

The OpenGrid-inspired detachable clip PoP has been closed. The removable HUB75
tube clip is intended to print on its side, which makes the compliant snap/flex
geometry a poor fit for the desired part orientation and layer direction.

The next removable-connection direction is a simple dovetail developed directly
inside `brainboxemb/2026-009-01.cad.HUB75-display-frame`. It is normal product
design work and does not require a new experiment track.

There is currently **no active migration**.

## Proposed / inactive

### Migration 007 — standardise GitHub Actions dependency maintenance

**Proposed / inactive.**

[Migration 007](migrations/007-github-actions-dependency-maintenance/README.md) records the intended exact-SHA/PR-based action-maintenance work, including Dependabot and `actions-up` evaluation. It remains separate from the completed Java CI PoP and must not start automatically.

## Recently stopped

### Experiment 005 — detachable SCAD clip interface

**Stopped early — experiment not completed; OpenGrid snap mechanism not selected for production.**

[Experiment record](experiments/005-detachable-scad-clip-interface/README.md)
· implementation/evidence repository
`brainboxemb/exp.2026-005.scad-detachable-clip-interface`
· external-source fork
`brainboxemb/fork.andylevesque.quackworks`

The experiment completed the upstream Full and Full/Lite reference work in PRs
#1 and #2 and retained the source/mechanism evidence. The experiment itself was
then stopped early: reduced receiver work in draft PR #7 was not completed and
was closed without merge.

The deciding product constraint is print orientation: the actual removable tube
clip should print on its side, while the investigated mechanism depends on
compliant snap/flex regions. Rather than qualify a mechanism that is already a
poor fit for the intended part, the work returns to the HUB75 product design
with a simpler dovetail direction.

No detachable-interface contract was qualified and no production integration is
authorized by this experiment result.


### PoP — reusable Java CI architecture qualification

**Complete — initial Java CI PoP/qualification closed; retained as reusable regression lab.**

[PoP/experiment record](experiments/004-java-ci-architecture/README.md) · tracking issue [#69](https://github.com/brainboxemb/brainboxemb.meta/issues/69) · implementation/evidence repository `brainboxemb/exp.2026-004.java-ci-architecture`

This completed cross-project track is a generic Java/software CI **Proof of Principle (PoP)**, not a migration and not an event-timing product task.

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

Build-model/configuration and cache-independent execution are qualified on exact experiment main `4106f71f09ef98e3a5ce5a1a9b965f27219cf0e7`, exact-main run `35317952373`.

Runtime identity and fresh-runner cache transport are now qualified on exact experiment main `7bdf9017d543a81d48557968a232b39890b9b642`, exact-main run `35320255528` — all 28 jobs green. CI-12 proves a real Maven JDK 8 → 17 change selects a separate runtime cache namespace and rebuilds rather than consuming prior runtime state. CI-13 proves a separate hosted runner can start with zero module outputs, restore Maven's transported local build cache, reuse all four modules and recover all five Surefire reports. CI-14 proves an explicit transport miss falls back to the normal Maven build.

The PoP also established two required design constraints: cache storage is partitioned by runtime identity, and Surefire reports are retained as attached cache outputs.

Cross-workflow persistence is now qualified by CI-15 on exact experiment main `681ce7b9d56973b5540cb314c8e45e25618915a0`. Producer run `35323272710` built all four modules and saved 12 Maven build-cache files. A later, separate `workflow_run` consumer `35323361468` restored the exact cache on the same source, started with zero module outputs, reused all four modules as Maven-native `LOCAL`, and restored all four JARs plus five Surefire reports. The retained evidence/capability update is on experiment main `0d59eb6af11eff0db311650fd9b1a6aa30f8eb4f`; PR regression run `35324923371` was 28/28 green.

Representative end-to-end production value is now qualified against exact real-consumer source `brainboxemb/2026-010-02.java.event-timing-framework@0f9dbc2f5aa0beaec8f63465ada83f2bc2a83709`.

Two independent exact-main benchmark pairs were retained:
- experiment `2d9ac9af9006725576009b5c453590800a1a7337` — producer `35335319664`, consumer `35335436917`;
- experiment `d47d10ae0cb2be7828310331a8fed8121e10d0fd` — producer `35335827417`, consumer `35335932166`.

Across six matched samples, every shared consumer was faster than its paired control: savings `16, 14, 4, 3, 9, 2 s`, median **6.5 s / 28.8%**. Total producer+consumer hosted compute is not structurally qualified as a saving: paired deltas were `10, 10, -1, 0, 9, -2 s`. The second run retained ~153 kB of Maven build-cache state with ~1 s median save and restore steps. Final owner evidence is on experiment main `5c3aabe2e38a7607eb3401445ee707cd244d5161`.

CI-16 then exposed and corrected a product-provenance correctness gap on the real consumer. Baseline run `35336851477` restored both `framework` and `app` as `LOCAL` for a different Git commit with the identical source tree, leaving the producer revision embedded in the app JAR. The qualified product-scoped correction declares `../.git/HEAD` as an additional Maven Build Cache input only for the app module. Run `35337342442` then proves `framework=LOCAL`, `app=BUILD` and exact current embedded revision. The retained correction/evidence is on experiment main `e30c71c2f7404a49900c301c6dceac064abd8e5d`; final PR regression run `35358585970` was 30/30 green.

Release/canonical-artifact policy is now closed on experiment main `2353b18ccfd90c25c9cc7fab65e1a2a8f2b73da9`, PR regression run `35359099065` — 30/30 green. Normal canonical PR/main execution may use project-selected `none | local | shared` when all material inputs participate in cache validity. Exact-tag release remains a separate trust boundary: fresh/empty module output, no Maven build-output cache read/write, dependency cache allowed, ordinary Maven lifecycle, and publication reusing prepared canonical output without rebuilding. Existing real release run `35211641563` already proves that operational shape, so no redundant CI-17 was added.

The initial Java CI PoP is therefore **complete**. It supports a later production adoption decision but does not itself activate a migration. The experiment repository remains the reusable qualification/regression lab for future Java CI architecture changes.


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