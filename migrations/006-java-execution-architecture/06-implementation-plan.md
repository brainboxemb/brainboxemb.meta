# Migration 006 — implementation and qualification plan

## Purpose

This document is the historical owner order, qualification gates and evidence record for Migration 006. The durable post-migration model lives in [Java execution model](../../docs/working-model/java-execution.md).

Status: **complete**

Target architecture history: [05 — Target architecture](05-target-architecture.md).

## Working chain

```text
tool.git-project
      ↓
tool.java-project
      ↓
template.java-project
      ↓
2026-010-02.java.event-timing-framework
```

Project-family planning/architecture documentation remained a parallel generic capability owned by the meta repository plus `tool.eng-docs`; it was never made a Java execution dependency.

## Step 0 — activate and freeze the boundary

Owner: `brainboxemb.meta`

**Status: complete.**

The migration established:

- Maven as Java build/test authority;
- `tool.git-project` as generic affected/bootstrap authority;
- `tool.java-project` as generic Java execution/evidence/publication authority;
- consumer-owned impact declarations and product-specific behaviour;
- engineering-documentation assembly outside Java execution ownership.

## Step 1 — shared Java execution contract

Owner: `tool.java-project`

**Status: complete.**

The owner now provides:

- exact base/head affected preflight;
- one canonical Linux Maven producer;
- durable producer/test/provenance evidence;
- durable `orchestration/preflight/**` and timing evidence;
- `windows-mode: auto|none|smoke|full`;
- exact Linux-artifact Windows smoke;
- independent native Windows Maven qualification for `full`;
- full-path fan-out so native Windows Maven can run in parallel with Linux after preflight;
- generated `bld` finalization/publication without another Maven build;
- multi-module Maven cache inputs.

Owner correction PR #31 was externally canaried before release.

## Step 2 — release the shared Java owner revision

Owner: `tool.java-project`

**Status: complete.**

Released baseline:

```text
tool.java-project v0.3.2
exact source c0ca2e1365a64bc626ca331a8170d13340ae0b36
```

Evidence:

- exact-main self-test `35190574150` — green;
- release workflow `35190849340` — green;
- tagged self-test `35190862089` — green;
- supporting generic affected baseline `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

Consumers end on the immutable release, not owner main or a feature branch.

## Step 3 — reference template canary and immutable release

Owner: `template.java-project`

**Status: complete.**

The template owns only `java.canonical` / `java.windows-full` impact declarations plus its artifact inputs and trigger policy.

Qualified scenarios:

### Normal affected Java

- isolated Java-only canary `35151251145`;
- `auto -> smoke`;
- one Linux canonical producer;
- exact Linux-produced JAR smoke on Windows;
- native Windows Maven skipped.

### Windows-sensitive affected PR

- owner-head external canary `35190324797` and released-owner PR qualification `35190926434`;
- `auto -> full`;
- Linux canonical and native Windows Maven run after preflight, with native Windows eligible in parallel;
- exact Linux-artifact smoke green.

### Unrelated/README-only

- run `35151294080`;
- preflight only;
- no JDK, Maven, Windows or build publication.

### Merged main

- exact main `2406d362f1b93c433bb561bd8d09a9f6cde13774`;
- run `35192557796` — green;
- Windows mode `none`;
- no Windows runner;
- exact `prod/bld` publication.

### Immutable release

- `template.java-project v0.1.0` points to exact `2406d362f1b93c433bb561bd8d09a9f6cde13774`;
- tagged release verification `35192714047` — green;
- Linux + native full Windows Maven + exact Linux-artifact smoke;
- `rel/v0.1.0/bld` exact-source publication.

A manual `workflow_dispatch` full control is exposed. The connector used during this migration could not fire that UI trigger directly; the same `full` execution semantics were independently qualified through sensitive PRs and the immutable tag release.

## Step 4 — lock the Windows impact policy

Owners: `brainboxemb.meta`, implemented by released `tool.java-project` plus consumer configuration.

**Status: complete.**

Final policy based on measured runner cost and failure coverage:

```text
unrelated PR                         no Java / no Windows
ordinary affected Java PR           auto -> smoke
build/toolchain/workflow-sensitive  auto -> full
ordinary protected main publication none
explicit/manual stronger check       full when requested
exact release qualification          full
```

Normal main intentionally does not repeat Windows qualification already performed on the protected PR. This rule is now durable in `docs/working-model/java-execution.md`.

## Step 5 — real event-timing framework rollout

Owner: `2026-010-02.java.event-timing-framework`

**Status: complete for tooling rollout and normal-product qualification.**

Merged exact main:

```text
9aff579d824339b191c4d99be22d738f18562ad1
```

The real repository retains product-owned:

- Maven/version/release metadata;
- app/framework artifact naming;
- embedded build identity;
- logging dependency-boundary assertions;
- product release/tag failure/archive semantics;
- domain-specific smoke output.

Generic Java orchestration now uses released `tool.java-project v0.3.2`.

Qualified scenarios:

1. Java-only PR — PR #35 / run `35193503922`: `auto -> smoke`, Linux + exact Linux-artifact Windows smoke, native Windows Maven skipped;
2. sensitive multi-module/workflow PR — final PR #34 run `35193846536`: `auto -> full`, Linux + native Windows Maven + exact Linux-artifact smoke green;
3. documentation-only PR — PR #36 / run `35193536122`: metadata + preflight only; Java/Windows/publication skipped;
4. explicit full override — control is present; identical full execution semantics are qualified by scenario 2 and the reference release, but the manual UI event itself was not separately fired;
5. exact merged main — run `35193989780`: green, Windows mode `none`, no Windows runner, Linux + publication only;
6. exact release contract — statically preserved in the product workflow; generic immutable release mechanics are dynamically proven by `template.java-project v0.1.0`; the next real product release will exercise this path at normal product cadence;
7. exact Linux-produced app smoke — green in smoke and full PR paths;
8. generated Java evidence/provenance — `prod/bld/source-sha.txt` is exact main and `orchestration/preflight/**` plus timing survive publication;
9. failure semantics — existing product failed-tag/archive checks remain repository-owned and are still run by the cheap metadata job;
10. meta/engineering-documentation boundary — remains independent from Java execution; no Java dependency was introduced into documentation assembly.

Final main timing capture:

```text
wall to publication capture 56 s
hosted runner time          51 s
started runners              4 (all Linux)
affected decision            3 s
Maven reported              16.532 s
Windows mode                none
```

Both product JARs are present in `prod/bld/artifacts`.

## Step 6 — durable model and closeout

Owners: `brainboxemb.meta` plus downstream repository.

**Status: complete.**

### Closeout correction

The original plan required a fresh immutable downstream product release as a tooling-migration gate. Rollout evidence showed that this would couple tooling qualification to unrelated product-version cadence without adding a new generic execution proof.

The corrected boundary is:

- shared tooling must be immutably released — satisfied by `tool.java-project v0.3.2`;
- the generic release path must be immutably proven — satisfied by `template.java-project v0.1.0`;
- the real downstream must consume the released tooling and prove its PR/main/product-specific contract — satisfied on exact main `9aff579d...`;
- the next real product release exercises the preserved exact-tag `full` path at the product's normal release cadence and is not manufactured solely to close this migration.

This is an ownership correction, not a relaxation of release correctness. Tooling decides tooling semantics; the product owner decides when a product version is released.

The durable model has been moved to [Java execution model](../../docs/working-model/java-execution.md). Migration 006 can therefore close without changing the event-timing product version from `0.2.0-SNAPSHOT`.

## Final evidence matrix

| Scenario | Preflight | Linux Maven | Windows smoke | Windows Maven | Publication | Exact source |
| --- | --- | --- | --- | --- | --- | --- |
| unrelated PR | yes | no | no | no | no | yes |
| normal Java PR / auto | yes | one canonical | yes | no | PR output | yes |
| sensitive PR / auto | yes | one canonical | yes | yes | PR output | yes |
| ordinary protected main | yes | one canonical | no | no | `prod/bld` | yes |
| immutable reference release | release boundary | fresh exact source | yes | yes | `rel/vX.Y.Z/bld` | yes |
| next real product release | product release boundary | required | required | required | immutable | required |

Final invariants:

- Maven remains build/test authority;
- no duplicate canonical Linux producer;
- smoke consumes the exact Linux-produced artifact;
- full Windows is independent native Maven qualification;
- Java-output publication never triggers another Maven build;
- generic engineering-documentation assembly does not require Java execution;
- durable timing/job-selection evidence survives publication;
- semantic released workflow identity and exact committed tool identity stay aligned.

GitHub Actions dependency maintenance remains Migration 007. Later product release work or owner-local performance tuning does not reopen Migration 006 unless it reveals an actual regression in this contract.
