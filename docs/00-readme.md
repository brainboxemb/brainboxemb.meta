# BrainboxEmb meta documentation

This is the front page of the durable documentation for `brainboxemb.meta`.

The repository is the public portfolio/coordination map. It explains which
repositories exist, how shared engineering work is organised, where durable
cross-repository conventions live and which repository owns a change.

## Typical readers

- maintainers working across multiple BrainboxEmb repositories;
- contributors trying to find the correct owner for a change;
- agents reconstructing current portfolio state from repositories rather than
  chat history;
- readers trying to understand a technical domain such as SCAD or software.

## Reading order

| Family | Start here | Purpose |
| --- | --- | --- |
| 10 Plan | [10-plan.md](10-plan.md) | current meta-repository work |
| 20 Manuals | [20-manuals.md](20-manuals.md) | how to work with and maintain the portfolio |
| 30 Specification | [30-specification.md](30-specification.md) | why meta exists and for whom |
| 40 Design | [40-design.md](40-design.md) | how portfolio coordination is organised |
| 50 Verification | [50-verification.md](50-verification.md) | how current claims stay trustworthy |

For current repository-spanning work, use [STATUS.md](../STATUS.md). It is an
operational register, not a chapter copied into this documentation set.

## Domain views

Technology-specific shared guidance stays in [domains/](../domains/README.md):

- [SCAD / CAD](../domains/scad/README.md);
- [Software](../domains/software/README.md).

## Operational registers

These remain separate because they are live/history registers rather than
chapters of the general engineering book:

- [repository catalog](../repositories/README.md);
- [migrations](../migrations/README.md);
- [experiments / PoPs](../experiments/README.md);
- [dashboard](../dashboard/README.md).

Implementation authority for an individual project, tool or library remains in
that owning repository.
