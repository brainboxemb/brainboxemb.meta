# Migration 013 — adopt interactive engineering documentation and traceability

Status: **active — Step 4**

Tracking issue: [#169](https://github.com/brainboxemb/brainboxemb.meta/issues/169)

Qualified source experiment:
[Experiment 007](../../experiments/007-requirements-traceability/README.md)

Human review:
[Experiment 007 GitHub Pages](https://brainboxemb.github.io/exp.2026-007.requirements-traceability/)

## Why this migration exists

Experiment 007 qualified a documentation model that keeps the existing
engineering book useful while adding machine-checkable traceability and richer
navigation over the same engineering meaning.

The experiment established that the desired production shape is not one new
monolithic documentation tool.

It is a responsibility split:

```text
project Markdown + diagram source
          |
          +-- stable engineering object identity
          +-- compact authored relations
          |
          v
generic extraction / validation / rendering
          |
          +----------------------+----------------------+
          |                      |                      |
          v                      v                      v
engineering book           documentation portal     engineering graph
linear reading             search/navigation        backlinks/context
          |                      |                      |
          +----------------------+----------------------+
                                 |
                          clickable architecture
```

The experiment repository must not become a production dependency. Generic
mechanisms now move to their normal owners and are qualified through a real
event-timing consumer.

## Qualified principles

Migration 013 preserves these Experiment-007 decisions:

1. the engineering **Book** remains a first-class output;
2. normal readable Markdown remains project source;
3. the final project authoring format is an explicit production decision;
   native MyST/Sphinx-Needs and compact adjacent metadata remain candidates until
   the authoring-v2 requalification is reviewed;
4. stable engineering IDs and source targets are explicit;
5. relationships are authored once and inverse backlinks/matrices are generated;
6. a normalized engineering-graph boundary separates source authoring from
   reader views;
7. Sphinx-Needs remains a viable optional relationship/validation engine behind
   that boundary rather than becoming the documentation architecture;
8. Material for MkDocs is a qualified reader-facing portal candidate;
9. diagram source carries engineering identity and generated SVG preserves it;
10. project-specific meaning remains in consuming repositories.

## Scope boundary

Migration 013 is deliberately staged.

Do **not** copy the complete experiment implementation into `tool.eng-docs` in
one change.

Do **not** require every BrainboxEmb repository to adopt the portal/graph model.

The first production canary is the event-timing documentation. Wider adoption is
demand-driven only after the canary proves the released mechanisms.

## Step 1 — reusable diagram engineering identity

Status: **complete**

Owner: `brainboxemb/tool.eng-docs`

Released capability: `v0.3.11` at exact owner main `99a565eedc999a77bb0339a684660b08edbc04dd`.

Add the smallest reusable mechanism proven by Step 06:

- optional opaque `object_id` on diagram nodes;
- schema validation;
- semantic validation where appropriate;
- preserve the same identity in generated SVG as a stable machine-readable
  attribute such as `data-engineering-id`;
- preserve the identity in editable draw.io metadata where practical;
- domain-neutral user example;
- executable SVG/draw.io/schema tests;
- Linux + Windows normal owner qualification.

Constraints:

- no Sphinx-Needs dependency;
- no project-specific graph semantics;
- no event-timing IDs in reusable examples;
- no portal-owned label-to-object mapping.

This was the first migration gate.

Retained qualification evidence:

- owner PR [tool.eng-docs #42](https://github.com/brainboxemb/tool.eng-docs/pull/42);
- exact final PR head `a1f172fa1c4831920436a4122175fffe666ac81d`;
- exact merged owner main `99a565eedc999a77bb0339a684660b08edbc04dd`;
- exact-main Test run `36446180862` — green;
- release lifecycle run `36446445274` — green;
- tagged `v0.3.11` Test run `36446465549` — green;
- released SVG and draw.io output retain `data-engineering-id` without a
  Sphinx-Needs or external-graph dependency.

## Step 2 — event-timing diagram canary

Status: **complete**

Owner: `brainboxemb/2026-010-01.meta.event-timing-software`

After Step 1 is released:

- pin the released `tool.eng-docs`;
- add `object_id` to a small set of real architecture nodes, initially the
  already-qualified `TimingNode`, `CommandHandler`, `Conductor` and
  `RemoteApi`;
- rebuild normal SVG + draw.io output;
- verify exact generated output preserves identity;
- keep the normal architecture diagram visually unchanged except for
  machine-readable metadata;
- do not add a second lookup map.

Retained production-canary evidence:

- event-timing PR [#144](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/144);
- released dependency pin `tool.eng-docs v0.3.11` / exact
  `99a565eedc999a77bb0339a684660b08edbc04dd`;
- canary PR head `8e926b320dd7d5e37f2b72b51df12af2769356ec`,
  documentation run `36447217338` — green;
- merged canary `99599da84039a2827317718205b5ed1ab80c087c`;
- subsequent visual-only Figure SI01-01 refinement merged as
  `24b9dc0338f6e7d49e456e6e8f54ab46431c3cb8`;
- current exact-main documentation run `36448500779` — green;
- current `prod/docs/source-sha.txt` identifies exact source
  `24b9dc0338f6e7d49e456e6e8f54ab46431c3cb8`;
- current generated `layered-architecture.svg` and
  `layered-architecture.drawio` both preserve `TimingNode`,
  `CommandHandler`, `Conductor` and `RemoteApi`.

## Step 3 — stable source anchors and compact relation authoring

Status: **complete as a behaviour canary; authoring syntax under requalification**

Owners:
- project meaning: event-timing coordination repository;
- generic syntax/extraction mechanism: reassess after authoring requalification.

Qualify the smallest production authoring convention using the real first slice:

- `UC-001`, `UC-008`, `UC-014`;
- `SI01-REQ-003/020/021/022/030/031`;
- `IF03-REQ-001/002/004`;
- selected architecture elements;
- `VC-ST1-001`.

Requirements:

- ordinary Markdown remains readable on GitHub;
- every graph-exposed object has a stable source target;
- compact metadata stays adjacent to the owning object;
- inverse traceability is generated rather than authored;
- invalid or unknown relations fail near the owning source.

Do not migrate the complete document set in this step.

Retained production-canary evidence:

- event-timing issue [#147](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/issues/147);
- event-timing PR [#148](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/148);
- final qualified PR head `1098facba9ff05a91e401875b621783b4327b980`;
- PR documentation run `36454777469` — green, including publication;
- merged event-timing main `a855e66f6ecb325ab77139745ef50a5c6b7acc17`;
- exact-main documentation run `36454981276` — green, including publication;
- current `prod/docs/source-sha.txt`, engineering-graph evidence and
  materialization evidence all identify exact main
  `a855e66f6ecb325ab77139745ef50a5c6b7acc17`;
- bounded production graph: 17 engineering objects / 34 authored relations;
- production authoring direction:
  - requirements own upstream `derived_from`;
  - design/architecture owns `satisfies`;
  - verification owns `verifies`;
  - inverse relations are generated rather than authored;
- `prod/docs/evidence/traceability/review.md` exposes the exact hidden authored
  Markdown/YAML input beside normalized outgoing and generated incoming
  relations, while ordinary engineering documents remain readable normally;
- the project-local validator rejects duplicate IDs, unknown relation targets
  and unknown design-relation owners.

The canary intentionally does not establish a stable reusable graph API. It also
does **not** make the anchor + hidden-JSON syntax a final production decision.
Follow-up review found that the current form repeats ID/type/anchor information
and hides the relation input that an engineer maintains.

Experiment 007 issue
[#20](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/issues/20)
and draft PR
[#21](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/pull/21)
therefore requalify native MyST/Sphinx-Needs against the exact 17-object /
34-relation production meaning before Step 4 is released.

## Step 4 — reusable engineering graph boundary

Status: **active — gated by authoring requalification**

Before releasing the reusable owner capability, make an explicit production
authoring decision using Experiment 007 #20/#21. The graph behaviour from Step 3
is retained; only the source-authoring representation is reopened.

After that gate, select the smallest reusable owner
capability needed for:

- object IDs/types;
- source locations;
- typed relations;
- generated backlinks;
- duplicate/unknown-link/type validation;
- bounded focused traversal;
- coverage checks where configured.

`tool.eng-docs` is the likely owner, but this is reassessed from the proven
authoring shape rather than assumed.

The normalized graph contract should remain usable independently of reader
views, but this migration no longer assumes whether source extraction is a
custom Markdown parser or a Sphinx-Needs export boundary. If native MyST is
selected, avoid maintaining a second custom metadata language merely to recreate
the same object/link model.

Release gate:

- do not release `tool.eng-docs v0.4.0` while the authoring choice is open;
- do not merge the event-timing reusable-graph adoption while it depends on the
  unreleased owner;
- record the human authoring decision in Experiment 007 and this migration
  before production rollout resumes.

## Step 5 — event-timing production portal canary

Use released/pinned owner mechanisms to add a real derived portal while keeping
the existing book.

The canary should provide:

- existing engineering book;
- portal search/navigation;
- generated object views;
- focused relation context;
- clickable real architecture;
- richer use-case workspace;
- direct authoritative source navigation;
- exact source/tool provenance through the normal documentation lifecycle.

The portal is derived output. It does not own requirements, architecture or
verification meaning.

## Step 6 — closing audit

Migration 013 completes only when:

- reusable owner capabilities are released;
- the event-timing canary pins released owner revisions;
- production-generated SVG exposes real diagram engineering IDs;
- the selected source slice has stable anchors and checked typed relations;
- book and portal are generated from the same authoritative source;
- no hand-maintained inverse matrices or diagram label maps are required;
- exact revisions/CI/publication evidence are retained here;
- optional versus required capabilities are explicitly documented;
- Experiment 007 remains available as a regression/reference lab.

## Initial owner sequence

```text
Experiment 007 — complete
        |
        v
Migration 013
        |
        +--> Step 1: tool.eng-docs diagram object_id
        |
        +--> Step 2: event-timing diagram canary
        |
        +--> Step 3: traceability behaviour canary
        |
        +--> authoring requalification: compact vs native MyST
        |
        +--> Step 4: reusable graph boundary
        |
        +--> Step 5: event-timing production portal
        |
        v
closing audit
```

The migration should stop and reassess if a production owner exposes a concrete
conflict with the qualified experiment assumptions rather than weakening those
assumptions silently.
