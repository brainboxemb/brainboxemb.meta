# Migration 004 qualification evidence

Status: **active**

Tracking: meta issue #49.

## Step 1 — generic Moon affected preflight

Status: **complete**

Owner: `brainboxemb/tool.git-project`.

Released capability: `tool.git-project v0.2.5`.

Exact released source commit:

```text
ce7c81c39ebc70933b4150028aa74d928a53c2ba
```

Owner work:

- issue/PR #21 — `Add generic Moon affected preflight`;
- reusable action: `moon/affected`;
- Linux wrapper: `moon-affected.sh`;
- Windows wrapper: `moon-affected.ps1`;
- retained query/decision evidence under `.moon/preflight`.

Qualified behavior with real Moon 2.5.4 and real Git commits:

- README-only change outside task inputs => `affected=false`;
- configured task-input change => `affected=true`;
- missing base revision => conservative `affected=true`;
- explicit base/head ranges are used;
- preflight queries do not execute the producer;
- Linux and native Windows behavior match;
- reusable composite action itself is exercised in CI.

PR-head qualification on `6ec28d7bd77e789a8867e8c8326d81a9c2d066ed`:

- Moon production orchestration run `34886865162` — Linux and Windows green;
- Self-test Git project tooling `34886865079` — green;
- generic release lifecycle `34886865532` — green;
- generated output publication `34886865453` — green;
- PR preview cleanup `34886865539` — green;
- execution evidence schema `34886865072` — green.

Exact-main qualification ran successfully for the merge commit before release.

Release:

- tag `v0.2.5` is an annotated tag pointing to exact main `ce7c81c39ebc70933b4150028aa74d928a53c2ba`;
- release run `34887174233` completed successfully, including tagged verification and GitHub Release creation.

A duplicate release run (`34887175316`) started for the same request and failed only because the successful run had already created the exact tag. This is not a Migration 004 blocker; generic release idempotency is tracked separately as `tool.git-project` issue #22.

## Step 2 — reference task-graph correction

Status: **next; not yet implemented**

Owner: `brainboxemb/template.scad-project`.

Before changing the graph, re-check whether the current template verification producer actually consumes normal Build output. Remove `scad.verify -> scad.build` only if current repository behavior confirms the dependency is stale rather than required.
