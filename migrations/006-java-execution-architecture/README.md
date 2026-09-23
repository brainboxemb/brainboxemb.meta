# Migration 006 — simplify the Java execution architecture

## Why this migration exists

Java repositories had a reproducible Maven/JDK baseline but still duplicated repository-level orchestration for affected selection, setup, Windows coordination, evidence staging and generated-output publication. Migration 006 moved that generic lifecycle into `tool.java-project`, left consumers responsible for impact declarations and product-specific behaviour, and qualified the contract through both the reference template and the real multi-module event-timing framework.

Status: **complete**

Durable model: [Java execution model](../../domains/software/40-01-java-execution.md).
Historical rollout/evidence: [06 — Implementation and qualification plan](06-implementation-plan.md).

## Final architecture

```text
tool.git-project
  generic repository / Moon / affected mechanics
        ↓
tool.java-project
  Maven/JDK execution, selective Windows qualification,
  Java evidence and generated bld finalization/publication
        ↓
consumer repository
  impact declaration, product metadata and product release semantics
```

Maven is Java build/test authority. Moon is consumer-owned impact declaration only.

Consumers use:

```text
java.canonical
java.windows-full
```

with one Windows policy input:

```text
windows-mode: auto | none | smoke | full
```

Final event policy:

```text
unrelated PR                         no Java / no Windows
ordinary affected Java PR           auto -> smoke
build/toolchain/workflow-sensitive  auto -> full
ordinary protected main publication none
explicit/manual stronger check       full when requested
exact release qualification          full
```

`smoke` executes the exact Linux-produced runnable JAR on Windows without a native Windows Maven build. `full` adds an independent native Windows Maven `verify`; that native Windows build can run in parallel with Linux after preflight, while exact-artifact smoke waits for the Linux producer.

## Released owner baseline

`tool.java-project v0.3.2`

- exact source `c0ca2e1365a64bc626ca331a8170d13340ae0b36`;
- exact-main self-test `35190574150` — green;
- release workflow `35190849340` — green;
- tagged self-test `35190862089` — green.

Supporting generic baseline:

- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

## Reference consumer qualification

`template.java-project v0.1.0`

Exact release source:

```text
2406d362f1b93c433bb561bd8d09a9f6cde13774
```

Evidence:

- sensitive/full canary `35190324797` and released-owner qualification `35190926434` — green;
- Java-only canary `35151251145` — `auto -> smoke`, native Windows Maven skipped;
- README-only canary `35151294080` — preflight only, no Java/Windows/publication;
- exact-main run `35192557796` — green, Windows mode `none`, no Windows runner, exact `prod/bld` publication;
- immutable release verification `35192714047` — green, Linux + native full Windows + exact Linux-artifact smoke + `rel/v0.1.0/bld`.

## Real downstream qualification

The released lifecycle first landed in `2026-010-02.java.event-timing-framework` on exact main:

```text
9aff579d824339b191c4d99be22d738f18562ad1
```

The repository retained product-owned Maven/version/release metadata, app/framework artifact names, embedded build identity, logging dependency-boundary assertions and failed-release semantics while removing generic Java orchestration duplication.

Qualification evidence:

- final sensitive/full PR run `35193846536` — green, `auto -> full`;
- isolated Java-only PR #35 / run `35193503922` — `auto -> smoke`, native Windows Maven skipped;
- isolated documentation-only PR #36 / run `35193536122` — preflight only, no Java/Windows/publication;
- exact-main run `35193989780` — green, Windows mode `none`, no Windows runner, exact `prod/bld` publication;
- main timing capture 56 s wall / 51 hosted-runner seconds.

## Immutable downstream product release

After the tooling rollout, the product entered its normal release flow.

The first `v0.2.0` candidate at exact source `e8066c9e33cf2ed77bb7f37ac8a68707933e28e8` passed Linux canonical Maven, independent native Windows Maven, exact Linux-produced app-JAR smoke and `rel/v0.2.0/bld` publication. Final GitHub Release packaging then failed because the product workflow attempted to archive `orchestration/**` from the pre-finalization Actions artifact instead of the finalized release branch.

The repository's fail-safe behaved correctly:

- normal `v0.2.0` was removed;
- the consumed candidate was preserved as `v0.2.0-failed`;
- version `0.2.0` was not reused.

PR #38 fixed only that product-owned release packaging boundary and advanced the release to `0.2.1`.

Final downstream release:

```text
2026-010-02.java.event-timing-framework v0.2.1
exact source 0f9dbc2f5aa0beaec8f63465ada83f2bc2a83709
annotated tag object b6d132c0f383d52975994cfcc12cfa7cc6fab2e3
```

Evidence:

- release-fix PR run `35195850065` — green;
- exact-main `0.2.1` run `35211527836` — green, ordinary main with Windows disabled and `prod/bld` publication;
- exact-tag release run `35211641563` — green;
- Linux canonical Maven — green;
- independent native Windows Maven — green;
- exact Linux-produced app-JAR Windows smoke — green;
- `rel/v0.2.1/bld` publication — green and exact-source;
- `rel/v0.2.1/bld/source-sha.txt` is `0f9dbc2f5aa0beaec8f63465ada83f2bc2a83709`;
- GitHub Release `v0.2.1` published successfully with app JAR, framework JAR, SHA256 checksums and finalized evidence archive;
- release timing capture: 81 s wall / 107 hosted-runner seconds; native Windows qualification consumed 66 s and remained the dominant hosted-compute cost.

The product release provides additional immutable downstream evidence. It does not change the architectural ownership decision: Migration 006 did not need to invent a product version merely to prove generic tooling, but once the product was genuinely released its exact-tag `full` path confirmed the same contract end to end.

## Performance conclusion

The retained evidence shows that affected selection and Maven are not the only relevant costs. Windows setup, checkout/wrapper validation and native Windows Maven can dominate full qualification. The selected optimisation is therefore **selective allocation**, not removal of Windows as a real platform boundary:

- zero Windows for unrelated work;
- exact-artifact smoke for ordinary Java PRs;
- native full Windows for sensitive PRs, deliberate stronger checks and releases;
- no repeated Windows qualification on ordinary protected-main publication.

## Completion

Migration 006 is complete because:

- the generic owner contract is immutably released;
- the reference consumer is immutably released and proves the generic exact-tag release path;
- the real downstream consumes the released shared tooling and proves full, smoke, unrelated and exact-main paths;
- the real downstream now also has immutable `v0.2.1` release evidence for the exact-tag full-Windows path;
- generated Java evidence retains exact source/tool provenance and durable timing evidence;
- Maven remains build/test authority with no duplicate canonical Linux producer;
- project-family/engineering-documentation assembly remains outside Java execution;
- the durable architecture lives in `domains/software/40-01-java-execution.md` rather than this temporary migration folder.

GitHub Actions dependency maintenance remains Migration 007 and is not activated automatically by this closeout.
