# Migration 005 — normal publication-path analysis

Status: **measured architecture note**

This note examines the final Migration-004 **normal CI** publication path. Release publication is a different lifecycle and should not be conflated with it.

## Current normal path

After the SCAD container exits, the one-host production workflow currently does all of the following:

```text
validate generated Build + Verification trees
  -> copy/stage Build tree
  -> copy/stage Verification tree
  -> add current orchestration evidence to both staged trees
  -> upload Build as a GitHub Actions artifact
  -> upload Verification as a GitHub Actions artifact
  -> publish Build generated-output branch from the staging directory
  -> publish Verification generated-output branch from the staging directory
```

The branch publications use the local staging directories directly. There is no download of the just-uploaded artifacts before normal publication.

## Release path is separate

The release workflow does use workflow artifacts as a real cross-job hand-off:

```text
release Build job
  -> upload release Build artifact

release Verify job
  -> upload release Verification artifact

release Finalize job
  -> download both verified artifacts
  -> package release ZIPs
  -> publish immutable release branches
  -> create annotated tag and GitHub Release
```

Those release artifacts therefore have a clear technical role.

The normal one-host Build/Verification artifacts do **not** serve that release hand-off. Release builds its own exact-source artifacts.

## Measured cost

Representative final clamps run `34971400621` spends roughly **2.6 seconds** on normal validation/staging plus the two workflow-artifact uploads before branch publication.

Build and Verification branch publication then takes roughly **4.4 seconds combined** and is currently sequential.

For HUB75 exact-main run `34976840416`, the branch publication steps are also sequential, roughly around 3 seconds for Build and around 2 seconds for Verification in that sample.

## Normal workflow artifacts are retention policy, not a same-job hand-off

The normal workflow-artifact uploads appear to be **retention/user-download evidence**, not an internal data-transfer requirement of the one-host architecture.

That means the design question should be explicit:

> Do we want downloadable Build and Verification artifacts for every normal CI run strongly enough to pay their upload/storage/retention cost?

Possible answers include:

1. **Keep both artifacts** because retained downloadable CI evidence is a deliberate product requirement.
2. **Keep only compact evidence artifacts** and use generated-output branches for the large generated trees.
3. **Make full normal-run artifacts optional** by repository or event type.
4. **Remove normal full-tree artifacts** if no current user/process consumes them, while keeping the release artifact hand-off unchanged.

This decision is independent of whether Moon is kept or simplified.

## Publication implementations are more independent than the workflow suggests

The generic `tool.git-project/generated-output-publish.sh` does not publish directly from the consumer's main working tree.

For each invocation it:

1. creates a new temporary credential file;
2. creates a new temporary publication repository with `mktemp -d`;
3. initializes/fetches the destination generated-output branch in that isolated repository;
4. copies only the supplied staging tree into that temporary repository;
5. creates the publication commit;
6. rechecks that the exact source revision still matches the requested source;
7. force-pushes only the requested generated-output branch;
8. removes its temporary repository and credentials.

Build and Verification calls also use different source staging directories and different target branch suffixes.

So there is no obvious shared Git worktree whose mutation requires the two publications to be serialized.

This makes **parallel publication a concrete candidate**, not merely a theoretical idea.

It must still be qualified because two concurrent pushes can expose other concerns:

- simultaneous token/auth use;
- clear combined failure reporting;
- GitHub API/network contention;
- ensuring one failed publication cannot hide success/failure of the other.

But the current implementation provides strong evidence that the two calls are structurally isolated enough to justify a real concurrency experiment.

## Potential latency effect

Current sequential publication is roughly the sum of the two independent pushes.

If safe concurrency is confirmed, the critical path should tend toward approximately the slower publication rather than their sum. On the observed small samples this is a possible saving of roughly 1.5–2.5 seconds, not a transformational change.

That is useful, but Migration 005 should not add architectural complexity merely for a tiny saving. The ideal improvement would be simpler **and** faster, for example a shared helper that starts two already-independent publications and reports both outcomes cleanly.

## Current conclusion

The release artifact hand-off is justified by job boundaries.

The normal production artifact uploads are **not required to move data between current normal-CI steps**. They are a policy choice for retained evidence/downloadability and should be justified as such.

The two normal generated-output publications are currently serialized, but the generic publication script gives each invocation isolated temporary repository and credential state. Parallel publication therefore deserves qualification and appears lower risk than the workflow shape initially suggested.

Both changes remain policy/qualification questions rather than automatic deletions:

- decide what normal downloadable artifacts are actually required;
- test publication concurrency and failure semantics before adopting it.
