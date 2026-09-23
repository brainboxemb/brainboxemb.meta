# Meta specification

## Why this repository exists

BrainboxEmb projects, libraries, tools, templates and experiments live in
separate repositories with independent implementation and release lifecycles.

`brainboxemb.meta` provides the durable public coordination layer above them:

- a map of what exists;
- shared portfolio-wide engineering conventions;
- domain-level shared guidance;
- cross-repository coordination;
- current migration/experiment status and retained evidence.

A normal project does not require meta in order to build or run.

## Typical users

Typical users are:

- maintainers coordinating changes across repositories;
- contributors looking for the correct implementation owner;
- people browsing the public repository collection;
- automation/agents reconstructing current state and working rules;
- domain maintainers publishing shared SCAD/software guidance.

## Why use meta

Use meta when a question spans repositories or when one shared convention should
not be owned by a single implementation repository.

Examples include:

- which tool owns generic bootstrap behavior;
- which repositories are current-generation versus classic;
- which migration is active;
- what release/pinning rules apply across project families;
- where a cross-project decision should be documented.

## Non-goals

Meta does not:

- implement domain build/runtime behavior;
- contain product-specific source;
- replace owner repository documentation;
- force every domain to have equal maturity;
- turn completed experiments into production dependencies;
- act as a runtime dependency of normal projects.

## Compatibility intent

Current portfolio guidance may evolve, but an older consumer must be able to
reconstruct exact dependency behavior from its pinned owner revision rather than
depending on current moving meta guidance.
