# Migration 001 handoff

Use this message to continue the consolidation in a new ChatGPT/work session.

```text
Work from brainboxemb/brainboxemb.meta as the cross-project coordination source.

First read:
- STATUS.md
- README.md
- AGENTS.md
- migrations/001-brainboxemb-meta/README.md
- migrations/001-brainboxemb-meta/handoff.md

Treat STATUS.md as the primary current-position summary. Historical step numbers
from meta.scad-projects are supporting context, not an instruction to resume the
highest numbered old step.

Then reconstruct the current state from GitHub rather than old chat history:
- Migration 001 issue #11;
- Phase-5 umbrella issue #25 and the current Phase-5 slice named in STATUS.md;
- current main branch and CI/Pages results in brainboxemb.meta;
- current relevant state of brainboxemb/meta.scad-projects;
- current dashboard/catalog only when the active slice touches it.

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

A migration marked proposed / inactive must not be implemented. In particular,
Migration 002 remains inactive until its activation gate is deliberately closed
after reassessment.

Implementation detail belongs in the repository that owns the behavior. Keep
cross-project plan/status/evidence in brainboxemb.meta.
```
