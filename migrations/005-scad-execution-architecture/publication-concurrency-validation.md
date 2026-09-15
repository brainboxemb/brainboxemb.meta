# Migration 005 — concurrent Build/Verification publication validation

Status: **validated for the target architecture**

This validation answers one normal-publication question:

> After Build and Verification output have both been prepared on one hosted runner, can their generated-output branches be published concurrently without sharing mutable Git state or requiring a second runner?

The answer is **yes** for the released generic publisher.

## Tested publisher

The controlled test executed the exact released `tool.git-project` publisher revision used by Migration 004:

```text
brainboxemb/tool.git-project
6234b7437b0dc0115642468f74d1f4a2c2214bef
```

The test used `generated-output-publish.sh` directly so both invocations could run at the same time inside one shell step.

The publisher already creates, per invocation:

- a separate temporary credential file;
- a separate temporary Git repository;
- a separate orphan publication commit;
- a separate target branch;
- an independent source-revision freshness check before staging and before push.

No caller worktree is used as the publication repository.

## Controlled run

Final successful diagnostic:

- repository: `brainboxemb/brainboxemb.meta`;
- pull request context: PR #59;
- workflow run: `34994181268`;
- job: `104466136935`;
- runner: `ubuntu-24.04`;
- hosted runners used by the diagnostic: **1**;
- Docker/runtime starts: **0**;
- PR-head source revision: `fc541aedb617795ec9dc086fa1eea2016b54c6bf`.

The two run-unique target branches were equivalent to:

```text
dev/pr-59/m005-concurrent-build-34994181268
dev/pr-59/m005-concurrent-verification-34994181268
```

Each tree contained a distinct marker plus the exact PR-head SHA. Both trees were fetched back from GitHub and verified independently before cleanup.

## Timing

Measured around the complete publisher calls:

| Publisher | Duration |
| --- | ---: |
| Build diagnostic tree | 2,089 ms |
| Verification diagnostic tree | 2,144 ms |
| sum if treated sequentially | 4,233 ms |
| concurrent publication window | 2,144 ms |
| measured overlap | 2,089 ms |

The full Build publisher interval overlapped the Verification publisher interval. Both pushes completed successfully within the same ~2.1-second window.

These are intentionally tiny diagnostic trees. The timing therefore demonstrates overlap, not a guaranteed production saving of 2.089 seconds. Real branch size and GitHub network variance can change the absolute gain.

## Isolation and cleanup result

The test verified that:

- both publishers associated output with exactly the same requested source revision;
- Build output appeared only on the Build diagnostic branch;
- Verification output appeared only on the Verification diagnostic branch;
- both publishers could push at the same time;
- neither invocation depended on shared mutable publication-repository state;
- both temporary remote branches were deleted afterwards;
- the cleanup step then confirmed that neither remote branch remained.

An earlier broader diagnostic run also successfully completed and verified the two concurrent valid publications, but then failed in an extra peer-failure test because of the diagnostic harness itself. The final run deliberately removed that unrelated harness experiment and tested only the architecture question above.

## Resource interpretation

The useful form of publication concurrency is **inside the existing one-runner lifecycle**:

```text
one hosted runner
  prepare Build staging tree
  prepare Verification staging tree
        |
        +--> publish Build branch --------+
        |                                  |
        +--> publish Verification branch --+  concurrent
```

It does not justify returning to separate Build and Verification VMs.

The parallel publishers add no extra hosted-runner allocation and no extra CAD runtime. They only overlap two independent Git publication operations that already have to happen.

## Target-architecture consequence

Normal one-runner finishing may publish Build and Verification branches concurrently after both staging trees are complete.

Implementation should:

- start both independent publisher calls from the same host job;
- give each invocation its own output/status file rather than sharing one `GITHUB_OUTPUT` stream;
- wait for both publishers explicitly;
- fail the finishing step if either required publication fails;
- keep the existing stale-source checks in each publisher;
- avoid introducing another hosted job merely to parallelize publication.

The generic publisher itself did not require a code change for this validation. The orchestration change belongs in `tool.scad-project`.

## Result

**Architecture validation: passed.**

Concurrent Build/Verification publication is a safe small latency optimization within the one-heavy-runner target architecture. It is not a reason to add a second runner and should be implemented only after the larger capability/inheritance simplification is settled.
