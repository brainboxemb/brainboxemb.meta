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

## Architecture interpretation

The normal workflow-artifact uploads appear to be **retention/user-download evidence**, not an internal data-transfer requirement of the one-host architecture.

That means the design question should be explicit:

> Do we want downloadable Build and Verification artifacts for every normal CI run strongly enough to pay their upload/storage/retention cost?

Possible answers include:

1. **Keep both artifacts** because retained downloadable CI evidence is a deliberate product requirement.
2. **Keep only compact evidence artifacts** and use generated-output branches for the large generated trees.
3. **Make full normal-run artifacts optional** by repository or event type.
4. **Remove normal full-tree artifacts** if no current user/process consumes them, while keeping the release artifact hand-off unchanged.

This decision is independent of whether Moon is kept or simplified.

## Publication concurrency

Build and Verification generated-output branches are independent namespaces. The current host workflow publishes them one after the other.

Migration 005 should test whether the two publication operations can overlap safely while preserving:

- exact source revision checks;
- independent branch histories;
- clear failure reporting;
- no shared temporary Git worktree/config collision.

The current generic publish action appears to create a temporary publication branch/worktree state, so concurrency must be tested rather than assumed safe in the same working directory.

An alternative is a shared publication primitive that can publish both trees in one operation while keeping branch outputs independent.

## Current conclusion

The release artifact hand-off is justified by job boundaries.

The normal production artifact uploads are **not required to move data between current normal-CI steps**. They are a policy choice for retained evidence/downloadability and should be justified as such.

This makes normal artifact retention and sequential publication legitimate Migration-005 simplification/performance candidates, but neither should be removed until its actual consumers and failure semantics are checked.
