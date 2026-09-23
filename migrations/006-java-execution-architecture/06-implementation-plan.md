# Migration 006 — implementation and qualification plan

## Purpose

This document is the historical owner order, qualification gates and evidence record for Migration 006. The durable post-migration model lives in [Java execution model](../../domains/software/40-01_java-execution.md).

Status: **complete**

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

Project-family planning/architecture documentation remained outside the Java execution dependency chain.

## Step 0 — activate and freeze the boundary

Owner: `brainboxemb.meta`

**Status: complete.**

Established Maven as Java build/test authority, `tool.git-project` as generic affected/bootstrap authority, `tool.java-project` as generic Java execution/evidence/publication authority, and consumers as owners of impact declarations plus product-specific behaviour.

## Step 1 — shared Java execution contract

Owner: `tool.java-project`

**Status: complete.**

The owner contract provides:

- exact base/head affected preflight;
- one canonical Linux Maven producer;
- durable execution/provenance/timing evidence;
- `windows-mode: auto|none|smoke|full`;
- exact Linux-artifact Windows smoke;
- independent native Windows Maven qualification for `full`;
- parallel Linux/native-Windows fan-out after preflight;
- generated `bld` finalization without a second Maven build.

## Step 2 — release shared Java owner

Owner: `tool.java-project`

**Status: complete.**

```text
tool.java-project v0.3.2
exact source c0ca2e1365a64bc626ca331a8170d13340ae0b36
```

Evidence:

- exact-main `35190574150` — green;
- release `35190849340` — green;
- tagged self-test `35190862089` — green;
- supporting `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

## Step 3 — reference template canary and release

Owner: `template.java-project`

**Status: complete.**

```text
template.java-project v0.1.0
exact source 2406d362f1b93c433bb561bd8d09a9f6cde13774
```

Evidence:

- normal Java `auto -> smoke`: `35151251145`;
- sensitive `auto -> full`: `35190324797`, `35190926434`;
- README-only zero-Java: `35151294080`;
- exact-main Windows `none`: `35192557796`;
- immutable tagged full release: `35192714047`.

## Step 4 — lock Windows policy

Owners: `brainboxemb.meta` plus released tooling/consumer configuration.

**Status: complete.**

Final policy:

```text
unrelated PR                         no Java / no Windows
ordinary affected Java PR           auto -> smoke
build/toolchain/workflow-sensitive  auto -> full
ordinary protected main publication none
explicit/manual stronger check       full when requested
exact release qualification          full
```

The durable rule is recorded in `domains/software/40-01-java-execution.md`.

## Step 5 — real event-timing framework rollout

Owner: `2026-010-02.java.event-timing-framework`

**Status: complete.**

Initial shared-tooling merge source:

```text
9aff579d824339b191c4d99be22d738f18562ad1
```

Qualification:

1. Java-only PR — #35 / `35193503922`: `auto -> smoke`, native Windows Maven skipped;
2. sensitive PR — #34 / `35193846536`: `auto -> full`, Linux + native Windows Maven + exact Linux-artifact smoke;
3. docs-only PR — #36 / `35193536122`: metadata + preflight only;
4. exact merged main — `35193989780`: Windows `none`, Linux + `prod/bld` only;
5. generated evidence — exact source plus preflight/timing survives publication;
6. product-owned release metadata, artifact naming, embedded build identity, logging boundary and failed-release semantics retained.

Main timing after rollout:

```text
wall to publication capture 56 s
hosted runner time          51 s
started runners              4 (all Linux)
affected decision            3 s
Maven reported              16.532 s
Windows mode                none
```

## Step 6 — immutable downstream release and closeout

Owners: downstream repository + `brainboxemb.meta`

**Status: complete.**

The migration architecture did not require inventing a product version solely for tooling proof. The product subsequently entered its genuine release flow, which provided stronger downstream immutable evidence.

### Failed `v0.2.0` candidate

Exact candidate source:

```text
e8066c9e33cf2ed77bb7f37ac8a68707933e28e8
```

Tag run `35195339776` proved Linux canonical Maven, independent Windows Maven, exact Linux-produced app-JAR smoke and `rel/v0.2.0/bld`. Final GitHub Release packaging then failed because it tried to archive finalized `orchestration/**` evidence from the pre-finalization Actions artifact.

The product fail-safe worked as designed:

- normal `v0.2.0` removed;
- consumed candidate preserved as `v0.2.0-failed`;
- version `0.2.0` not reused.

### Corrected `v0.2.1` release

PR #38 fixed only the product-owned release packaging boundary and advanced the release version.

```text
v0.2.1
exact source 0f9dbc2f5aa0beaec8f63465ada83f2bc2a83709
annotated tag object b6d132c0f383d52975994cfcc12cfa7cc6fab2e3
```

Evidence:

- PR #38 qualification `35195850065` — green;
- exact-main run `35211527836` — green, Windows disabled, Linux + `prod/bld`;
- exact-tag run `35211641563` — green;
- Linux canonical — green;
- native full-Windows Maven — green;
- exact Linux-produced app-JAR smoke — green;
- `rel/v0.2.1/bld` exact-source publication — green;
- GitHub Release published with both JARs, `SHA256SUMS-0.2.1.txt` and finalized evidence archive;
- release timing 81 s wall / 107 hosted-runner seconds, with native Windows qualification at 66 s.

This final product release confirms the same event-sensitive contract end to end without changing the ownership model.

## Final evidence matrix

| Scenario | Preflight | Linux Maven | Windows smoke | Windows Maven | Publication | Exact source |
| --- | --- | --- | --- | --- | --- | --- |
| unrelated PR | yes | no | no | no | no | yes |
| normal Java PR / auto | yes | one canonical | yes | no | PR output | yes |
| sensitive PR / auto | yes | one canonical | yes | yes | PR output | yes |
| ordinary protected main | yes | one canonical | no | no | `prod/bld` | yes |
| immutable reference release | release boundary | fresh exact source | yes | yes | `rel/vX.Y.Z/bld` | yes |
| real downstream `v0.2.1` | release boundary | yes | yes | yes | `rel/v0.2.1/bld` + GitHub Release | yes |

Final invariants:

- Maven remains build/test authority;
- no duplicate canonical Linux producer;
- smoke consumes the exact Linux-produced artifact;
- full Windows is independent native Maven qualification;
- ordinary protected main does not repeat Windows qualification;
- Java-output publication never triggers another Maven build;
- engineering-documentation assembly remains independent from Java execution;
- durable timing/job-selection evidence survives publication;
- semantic released workflow identity and exact committed tool identity remain aligned.

GitHub Actions dependency maintenance remains Migration 007 and is not activated automatically.
