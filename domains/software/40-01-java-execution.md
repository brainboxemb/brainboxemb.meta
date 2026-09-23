# Java execution model

This page records the durable cross-repository Java execution model established by Migration 006. Use it when deciding what belongs in a Java consumer, what belongs in shared tooling, when Windows qualification runs, or what generated evidence should survive CI.

## Ownership boundary

The normal Java chain is:

```text
tool.git-project
  generic repository bootstrap, Moon and affected mechanics
        ↓
tool.java-project
  Java/Maven execution, selective Windows qualification,
  Java evidence and generated build-output finalization
        ↓
Java consumer repository
  impact declaration, product metadata and product-specific release behaviour
```

Maven remains Java build/test authority. Moon does not implement the Maven lifecycle; a consumer uses Moon only to declare which repository inputs affect a capability.

A normal consumer declares at least:

```text
java.canonical
  changes that require Java execution

java.windows-full
  narrower build/toolchain/workflow/platform-sensitive changes
  that require native Windows Maven qualification
```

Generic lifecycle execution must not be copied into each consumer merely to make the repository self-contained.

## Execution sequence

The shared production lifecycle is:

```text
exact base → head affected preflight
        ↓
unrelated ───────────────→ stop before JDK/Maven/Windows/publication
        ↓ affected
one canonical Linux Maven producer
        ↓
selected Windows qualification
        ↓
finalize/publish prepared Java output without another Maven build
```

For `full` qualification, the independent native Windows Maven build may start after preflight in parallel with the Linux producer. Only the Windows smoke of the exact Linux-produced runnable artifact depends on Linux completion.

## Windows policy

Consumers use one policy input:

```text
windows-mode: auto | none | smoke | full
```

The portfolio default is event-sensitive rather than a blanket platform matrix:

```text
unrelated PR                         no Java / no Windows
ordinary affected Java PR           auto → smoke
build/toolchain/workflow PR          auto → full
ordinary protected main publication none
explicit reviewer/manual check       explicit, normally full
exact release qualification          full
```

`smoke` means the exact Linux-produced runnable JAR is executed on Windows. It does not run a second Maven build.

`full` means an independent native Windows Maven `verify` is run and, where configured, the exact Linux-produced runnable JAR is also smoked on Windows.

A protected `main` build does not repeat Windows merely because it publishes `prod/bld`; the merged revision was already qualified through its pull request. Release qualification is a separate exact-source boundary and deliberately uses `full`.

The relevant impact families belong in the consumer configuration. Do not encode separate ad-hoc GitHub `paths:` rules for Java versus Windows selection.

## Evidence and generated output

The canonical Linux producer retains Java evidence such as:

```text
evidence/
  executions/java-canonical/
    execution.json
    execution.log
  tests/
  toolchain-build-provenance.txt
```

Current orchestration evidence is retained separately:

```text
orchestration/
  preflight/
    decision.json
    preflight.log
    affected/
  timing.json
  timing.md
```

`decision.json` identifies the exact comparison base/head, selected tasks and resolved Windows mode. `timing.json` / `timing.md` distinguish real Maven/build time from runner, checkout, setup and artifact-transfer overhead.

Generated Java build output uses the shared technical `bld` namespace:

```text
pull request #N -> dev/pr-N/bld
main            -> prod/bld
release tag     -> rel/vX.Y.Z/bld
```

Publication reuses the prepared canonical producer output. Publishing must never trigger another Maven build solely to materialize the generated branch.

## Release boundary

Shared tooling must support exact release qualification, but a cross-project tooling migration does not by itself force an application/framework product release.

The reference consumer may use an immutable release to prove the generic shared release contract. A real product repository keeps its own Maven/version, artifact, embedded-build-identity, release-note and failure/archive semantics. It adopts the released tooling contract and proves its normal PR/main paths immediately; its next real product release exercises the exact-tag `full` path at the product's normal release cadence.

This separation prevents tooling rollout from silently deciding product versioning.

## Proven baseline

Migration 006 qualified this model with:

- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.java-project v0.3.2` / exact `c0ca2e1365a64bc626ca331a8170d13340ae0b36`;
- `template.java-project v0.1.0` / exact `2406d362f1b93c433bb561bd8d09a9f6cde13774`;
- `2026-010-02.java.event-timing-framework` exact adopted main `9aff579d824339b191c4d99be22d738f18562ad1`.

The migration folder retains the detailed rollout/evidence history. This page is the durable model to use after the migration is closed.
