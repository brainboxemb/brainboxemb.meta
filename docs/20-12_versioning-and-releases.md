# Versioning and releases

## Independent repository versions

Each repository is independently versioned.

Matching version numbers across repositories do not imply a coordinated release set. A branch name, development artifact or moving `main` commit is not an official release unless the owning repository publishes the corresponding immutable version/tag according to its release process.

## Released cross-repository interfaces

Reusable tooling consumed by another repository is a production interface.

Normal production adoption follows this sequence:

1. implement and test in the owner repository;
2. merge the qualified implementation;
3. verify the exact owner `main` commit;
4. create the immutable versioned tag/release;
5. deliberately upgrade consumers to that released interface.

Consumers therefore remain on their accepted pin until an explicit update is reviewed.

## Policy versus lock

Current-generation consumers separate dependency intent from the exact checked-in lock:

```text
project.yml ref
    update policy / intended interface

Git submodule gitlink
    exact resolved commit used by normal clone/bootstrap/build
```

An intentional update resolves the configured policy and leaves changed gitlinks for review. Normal bootstrap restores the committed lock and must not silently advance it.

## Stable release refs

For reusable production tooling, prefer immutable release refs such as:

```yaml
ref: vX.Y.Z
```

A deliberate branch ref can be useful for integration work against unreleased development, but normal production consumers should not depend on a moving owner `main` without an explicit reason.

Reusable GitHub workflow/action refs should follow the same released interface contract where they are part of that dependency.

## Exact-revision release rule

Release qualification is tied to one exact revision.

Conceptually:

```text
qualified owner main commit
        ↓
exact verification
        ↓
annotated/tagged release revision
        ↓
release assets/publication
```

Do not tag one revision while relying on evidence produced from another merely because their source happens to look equivalent.

## Development version preparation

Some domains need repository-specific version preparation before tagging, for example Maven projects that move from a development/SNAPSHOT version to a release version.

The cross-project ownership boundary is:

```text
tool.git-project
    generic release request / exact-commit / tag lifecycle

domain tooling
    domain-specific version preparation and validation

consumer repository
    product-specific release metadata/assets where needed
```

A fuller explicit release-request/version-preparation workflow remains a deferred follow-up tracked in `brainboxemb.meta` issue #20. The existence of that follow-up does not invalidate the stable exact-revision rules above.

## Compatibility evidence

Compatibility is evidence-based, not inferred from equal version numbers.

Useful evidence includes:

- consumer dependency policy;
- exact committed gitlinks;
- runtime/toolchain refs;
- exact owner release commits;
- reference-consumer qualification;
- exact-main and tagged CI evidence where required.

## Where volatile versions belong

Stable architecture documents should avoid copying current pins unless a specific release/evidence statement needs them.

Exact SHAs, versions and run IDs belong primarily in:

- owner release/change documentation;
- migration qualification evidence;
- consumer configuration/gitlinks;
- generated repository status/output.
