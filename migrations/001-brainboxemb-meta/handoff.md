# Migration 001 handoff

Use this message to continue the consolidation in a new ChatGPT/work session.

```text
Work from brainboxemb/brainboxemb.meta as the cross-project coordination source.

First read:
- README.md
- AGENTS.md
- migrations/001-brainboxemb-meta/README.md
- migrations/001-brainboxemb-meta/handoff.md

Then reconstruct the current state from GitHub rather than old chat history:
- migration issue #11 and any linked PRs;
- current main branch and CI/Pages results in brainboxemb.meta;
- current relevant state of brainboxemb/tech.scad;
- current relevant state of brainboxemb/meta.scad-projects;
- current dashboard output/configuration when the active phase touches it.

Before taking the next phase, re-evaluate whether it is still the right step:
- is the goal still necessary;
- is the owner/ownership boundary correct;
- are prerequisites met;
- has later work already implemented part of it;
- do tests/evidence cover the real risk;
- can the phase be smaller or more reversible.

Keep the blocking path small. Classify discoveries as:
- migration blocker;
- follow-up migration;
- backlog / improvement.

Only blockers extend the current migration phase.

Implementation detail belongs in the repository that owns the behavior. Keep cross-project plan/status/evidence in brainboxemb.meta.

Do not start a later phase merely because it is listed in the plan.
```
