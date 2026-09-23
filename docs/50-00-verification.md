# Meta verification

## Purpose

Meta mostly owns documentation, catalog state and cross-repository coordination.
Verification therefore focuses on consistency and evidence rather than on a
single executable product.

## What must stay coherent

- root README/AGENTS route to valid current authorities;
- numbered general documentation has one authority per durable rule;
- domain guidance does not contradict portfolio-wide ownership rules;
- `repositories/catalog.yml` matches the intended public repository inventory;
- dashboard/configuration automation consumes that catalog correctly;
- STATUS identifies the actual active cross-project track;
- migration/experiment completion claims are backed by retained owner evidence.

## Evidence

Use the strongest practical evidence for the type of change:

- link/path review for documentation moves;
- exact owner repository state for current technical claims;
- workflow runs for dashboard/repository-configuration behavior;
- exact PR/main CI for implementation owners;
- immutable release/tag evidence for reusable interfaces;
- migration/experiment records for historical qualification.

A documentation edit alone does not prove an implementation claim.

## Documentation-structure changes

When moving or renumbering source documentation:

1. create the new authority;
2. update repository-local links;
3. preserve historical migration/experiment records unless a current link is
   genuinely broken;
4. remove the superseded current authority only after navigation is coherent;
5. verify root README/AGENTS and domain entrypoints.

A future generated `bld/docs/99-book.md` may provide an additional assembly
check, but it is not the source authority.
