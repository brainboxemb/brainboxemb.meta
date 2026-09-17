# Migration 006 — simplify the Java execution architecture

## Why this migration exists

Java repositories already had a reproducible Maven/JDK baseline, but still duplicated repository-level orchestration for affected selection, checkout/setup, Windows coordination, evidence staging and generated-output publication. That duplicated implementation spent hosted compute on unrelated work and obscured ownership.

Migration 006 moved the generic Java execution lifecycle into `tool.java-project`, left consumers responsible for impact declarations and product-specific behaviour, and qualified the contract through both the reference template and the real multi-module event-timing framework.

Status: **complete — released shared tooling, immutable reference-consumer release and real downstream main qualification agree on the same execution model**

Durable model: [Java execution model](../../docs/working-model/java-execution.md).
Detailed rollout/evidence: [06 — Implementation and qualification plan](06-implementation-plan.md).

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

and one Windows policy input:

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

`smoke` executes the exact Linux-produced runnable JAR on Windows without a native Windows Maven build.

`full` adds an independent native Windows Maven `verify`. That native Windows build can start after preflight in parallel with Linux; only exact Linux-artifact smoke waits for Linux completion.

## Released owner baseline

`tool.java-project v0.3.2`

- exact source: `c0ca2e1365a64bc626ca331a8170d13340ae0b36`;
- exact-main self-test: `35190574150` — green;
- release workflow: `35190849340` — green;
- tagged self-test: `35190862089` — green;
- reusable workflow identity resolves to the exact released source;
- durable preflight/timing evidence is retained in generated `bld` output;
- full native Windows qualification can run in parallel with Linux canonical work;
- Maven cache inputs cover multi-module POM/wrapper inputs rather than only one root POM.

Supporting generic baseline:

- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

## Reference consumer qualification

`template.java-project v0.1.0`

Exact release/main source:

```text
2406d362f1b93c433bb561bd8d09a9f6cde13774
```

Evidence:

- sensitive PR/full canary on owner-head: `35190324797` — green, `auto -> full`, Linux and native Windows parallel, exact Linux-artifact smoke green;
- released-owner PR qualification: `35190926434` — green;
- Java-only canary: `35151251145` — native Windows Maven skipped, exact Linux artifact smoke green;
- README-only canary: `35151294080` — preflight only, no Java/Windows/publication;
- exact-main production run: `35192557796` — green, Windows mode `none`, no Windows runner, exact `prod/bld` publication;
- immutable release verification: `35192714047` — green, exact tag source, Linux + full Windows + exact Linux-artifact smoke and `rel/v0.1.0/bld` publication.

The template immutable release proves the generic exact-tag release path independently of any product release cadence.

## Real downstream qualification

`2026-010-02.java.event-timing-framework` now consumes the released baseline on exact main:

```text
9aff579d824339b191c4d99be22d738f18562ad1
```

The real repository retained its product-owned Maven/version/release metadata, two product JAR names, embedded build identity, logging dependency-boundary assertions and failed-release semantics while removing generic Java orchestration duplication.

Evidence:

- final workflow/tooling-sensitive PR run `35193846536` — green, `auto -> full`, Linux canonical and native Windows Maven parallel, exact Linux-artifact smoke green;
- final PR generated output identifies exact source `3cc8521f6533ffffba39ab2a6cb3fe3592f56f8d`; timing capture is 58 s wall / 82 hosted-runner seconds, affected decision 3 s, Maven-reported 6.912 s;
- isolated Java-only PR #35, run `35193503922` — `auto -> smoke`, native Windows Maven skipped, exact Linux-produced app JAR smoke green;
- isolated documentation-only PR #36, run `35193536122` — metadata + affected preflight only; Java, Windows and publication skipped;
- exact-main run `35193989780` — green, Windows mode `none`, no Windows runner, Linux canonical + `prod/bld` publication only;
- `prod/bld/source-sha.txt` identifies exact main `9aff579d824339b191c4d99be22d738f18562ad1`;
- main timing capture is 56 s wall / 51 hosted-runner seconds with four Linux runners, 3 s affected decision and Maven-reported 16.532 s;
- `prod/bld/artifacts` contains both `event-timing-app-0.2.0-SNAPSHOT.jar` and `event-timing-framework-0.2.0-SNAPSHOT.jar`.

## Closeout decision on product releases

The original rollout plan required a new immutable downstream product release purely as a Migration-006 closeout gate. Real rollout evidence showed that this couples shared-tooling qualification to unrelated product version cadence without adding a new generic execution proof.

That requirement is therefore corrected:

- the immutable generic release contract is proven by `tool.java-project v0.3.2` and `template.java-project v0.1.0`;
- the real downstream proves the released shared tooling on PR and exact protected-main paths;
- the real product keeps its existing release/tag/failure semantics and will exercise the exact-tag `full` path at its next normal product release;
- Migration 006 does not change `0.2.0-SNAPSHOT` merely to manufacture a tooling evidence tag.

This preserves the ownership boundary: tooling migrations define tooling behaviour; product repositories decide product versions and release timing.

## Performance conclusion

The retained timing evidence makes the cost split visible instead of treating total workflow wall time as build time. Across the qualified runs, the affected/Moon decision is only a few seconds and Maven itself is also a minority of some full paths; Windows runner setup, checkout/wrapper validation and native Windows Maven work can dominate.

The optimisation decision is therefore selective allocation, not removal of Windows as a real platform boundary:

- zero Windows for unrelated changes;
- cheap exact-artifact smoke for ordinary Java PRs;
- full native Windows only for sensitive PRs, explicit stronger qualification and releases;
- no repeated Windows qualification on ordinary protected-main publication.

## Completion

Migration 006 is complete because:

- the generic owner contract is immutably released;
- the reference consumer is immutably released and proves the exact release path;
- the real downstream consumes the released shared tooling and is qualified on full, smoke, unrelated and exact-main paths;
- generated Java evidence keeps exact source/tool provenance and durable preflight/timing evidence;
- Maven remains Java build/test authority with no duplicate canonical Linux producer;
- project-family/engineering-documentation assembly remains outside the Java lifecycle;
- the durable architecture now lives in `docs/working-model/java-execution.md` rather than depending on this temporary migration folder.

GitHub Actions dependency maintenance remains Migration 007. Product-local performance tuning or the next real event-timing release does not reopen Migration 006.
