# Migration 004 qualification evidence

Status: **active**

Tracking: meta issue #49.

## Step 1 — generic Moon affected preflight

Owner: `brainboxemb/tool.git-project`.

Goal: provide a domain-neutral Moon 2.5.4 preflight that can determine whether a configured repository task is affected by an explicit VCS base/head range without executing producer commands.

Required evidence:

- real Moon 2.5.4 integration coverage;
- Linux and Windows wrapper parity;
- unaffected documentation-only change returns `affected=false`;
- affected configured input returns `affected=true`;
- uncertainty/error fails conservative for CI consumers;
- no domain-specific SCAD path logic in the generic owner.

Evidence will be filled after owner PR/release qualification.
