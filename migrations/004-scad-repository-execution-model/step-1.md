# Step 1 — generic Moon affected preflight

Owner: `brainboxemb/tool.git-project`

Status: active

## Goal

Provide a domain-neutral Moon 2.5.4 preflight that determines whether a configured repository task is affected by an explicit VCS base/head range without executing producer commands.

## Required behavior

- explicit base/head selection;
- affected/unaffected result suitable for a GitHub Actions job output;
- diagnostics/evidence showing the revisions/task/query used;
- real Moon 2.5.4 integration coverage;
- Linux and Windows parity;
- no SCAD-specific path rules;
- conservative behavior when impact cannot be established safely.

## Why this step comes first

GitHub Actions job-level containers start before any steps in that job. A reusable host-side affected decision is therefore required before a later SCAD production job can be conditionally created/skipped.
