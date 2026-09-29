# Migration 013 — adopt interactive engineering documentation and traceability

Status: **complete — full event-timing project adoption cut over and live portal deployed**

Tracking issue: [#169](https://github.com/brainboxemb/brainboxemb.meta/issues/169)

Qualified source experiment:
[Experiment 007](../../experiments/007-requirements-traceability/README.md)

Human review:
[Experiment 007 GitHub Pages](https://brainboxemb.github.io/exp.2026-007.requirements-traceability/)

## Full-project adoption correction

The original closing audit proved the selected technology and a bounded production
canary, but a post-close audit found that the running event-timing project itself
remained only partially migrated. Migration 013 was therefore reopened rather
than accepting a mixed old/new project state.

The correction was developed on the dedicated event-timing integration branch
`migration-013-full-project-adoption` and reviewed as one cut-over in PR #163.
No further partial Migration-013 slices were merged independently to `main`.

Final event-timing main `0924620ad37ccfb30b4dcb16180e7851d370c2df` now
contains every current **promoted stable engineering object** in the production
Needs/graph model:

- 19 system use cases;
- 13 SI-01 requirements;
- 10 IF-03 requirements;
- 10 diagram-linked architecture identities;
- 1 formal verification case (`VC-ST1-001`).

The project deliberately does not manufacture graph objects for ordinary
narrative. IF-11, SI-02, focused SDD candidate material and SVP test profiles
remain narrative where they do not yet own promoted stable engineering IDs.
The full-project coverage validator also detects future legacy-style promoted
IDs, so a newly introduced stable object cannot silently recreate a bounded
canary state.

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
3. native MyST/Sphinx-Needs is the selected authoring form for graph-exposed
   engineering objects; ordinary narrative remains normal Markdown/MyST;
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

Status: **complete as a behaviour canary; source syntax superseded by Step 4 native MyST/Sphinx-Needs adoption**

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

Status: **complete**

Experiment 007 #20/#21 closed the authoring gate. Exact experiment main
`419be32364f6d9c9c80f2ff9e8008ad48282dae2` passed authoring-v2 run
`36462734883`.

The selected production boundary is:

```text
normal Markdown/MyST narrative
        |
        +-- typed Sphinx-Needs engineering objects
        |      +-- stable ID
        |      +-- outgoing relations
        |      +-- typed validation
        |      +-- generated backlinks
        |
        v
    needs.json
        |
        v
optional BrainboxEmb normalization / review / portal / diagram cross-validation
```

Source extraction is owned by Sphinx-Needs. BrainboxEmb tooling does not
maintain a second Markdown/hidden-JSON authoring language. Diagram `object_id`
values reference existing engineering objects from the Needs graph.

Released reusable owner:

- owner PR [tool.eng-docs #47](https://github.com/brainboxemb/tool.eng-docs/pull/47);
- exact merged owner main
  `63af20a033d6295a28c844d12cb87f76165e69a5`;
- immutable `tool.eng-docs v0.4.0` points to that exact revision;
- `eng-docs graph` consumes `needs.json`, normalizes explicitly selected
  outgoing relation fields, derives incoming context and validates diagram
  object references without taking ownership of project semantics.

Retained real-consumer qualification:

- event-timing issue
  [#149](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/issues/149);
- event-timing PR
  [#150](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/150);
- final qualified consumer head
  `a93035a360716820bd280e4aef7a5d79dc92443e`;
- exact PR documentation run `36471704180` — green including publication;
- released consumer dependency pin `tool.eng-docs v0.4.0` with exact gitlink
  `63af20a033d6295a28c844d12cb87f76165e69a5`;
- merged event-timing main
  `a35553d6ddf5126879fa14d3b894a852610c6f4d`;
- current `prod/docs/orchestration/materialization.json` and normalized
  engineering graph both identify that exact main;
- bounded graph remains exactly 17 objects / 34 authored outgoing relations;
- the generated GitHub reader keeps content first, traceability below it and a
  horizontal rule as the closing separator for generated Need blocks;
- the native Sphinx reader uses the consumer-owned `engineering_reader` card
  layout with traceability metadata collapsed by default.

This completes the reusable graph-owner and released real-consumer adoption
gate. Step 5 may now build reader-facing portal views from the same source and
graph evidence.

## Step 5 — event-timing production portal canary

Status: **complete**

The first real production portal canary keeps the existing engineering Book as
a first-class output and derives search/object/workspace views from the same
native MyST/Sphinx-Needs source and normalized graph.

Initial production portal qualification:

- event-timing issue
  [#152](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/issues/152);
- event-timing PR
  [#153](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/153);
- final rebased canary head
  `5b75aa6375b9ceb9ac4ac792906895659541a233`;
- PR documentation run `36527968988` (#647) — green including publication;
- merged main
  `8cb55ff6d6bca47b1f8f79a29f9554481efd7d12`;
- exact-main documentation run `36528108235` (#648) — green;
- Material for MkDocs `9.7.7` provides the derived search/navigation surface;
- all 17 graph objects receive searchable generated object pages;
- the two-pane explorer uses the real generated SI01-01 SVG and its existing
  `data-engineering-id` values directly;
- a real headless Chrome gate exercises selected-object, relation-context and
  authoritative-source navigation;
- portal provenance records exact source/tool revisions and publishes through
  the normal `dev/pr-*/docs` / `prod/docs` lifecycle.

The closing-audit review then found one real production gap: the selected
use-case Needs initially contained only Goal + Primary actor while their richer
authoritative narrative remained immediately outside the directive. That was
closed without adding the project-specific Experiment-007 source parser:

- event-timing issue
  [#156](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/issues/156);
- event-timing PR
  [#157](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/157);
- qualified PR head
  `ee77bf16ae5fd1ced4699d1af65beeebcc628ce2`;
- PR documentation run `36528604011` (#649) — green including publication;
- merged final event-timing main
  `ff41c90a555f2f00fcb5a145f815eb88ba0bffa0`;
- exact-main documentation run `36528778737` (#650) — green;
- the existing closing fences for `UC-001`, `UC-008` and `UC-014` were
  moved only far enough to keep their already-authored narrative inside the
  same Need object; no use-case prose was duplicated or rewritten;
- CI proves richer use-case content reaches `needs.json`, the normalized graph,
  generated GitHub reader, Material object/search views and the real browser
  workspace.

Current `prod/docs` evidence at final main
`ff41c90a555f2f00fcb5a145f815eb88ba0bffa0` records:

- Book `source-sha.txt`: exact final main;
- Moon `software:docs.assemble` materialization: exact final main / success;
- normalized graph: 17 objects / 34 authored outgoing relations / exact final main;
- portal provenance: exact final main, `tool.eng-docs v0.4.0` at
  `63af20a033d6295a28c844d12cb87f76165e69a5`;
- production SVG identities: `TimingNode`, `CommandHandler`, `Conductor`
  and `RemoteApi`;
- full `UC-001` narrative through Preconditions, Main flow and
  Alternative/failure flows before generated traceability metadata.

The portal remains derived output. It does not own requirements, architecture,
use-case or verification meaning.

## Step 6 — initial canary closing audit

Status: **superseded by the full-project adoption correction below**

| Completion criterion | Final evidence | Result |
| --- | --- | --- |
| Reusable owner capabilities are released | `tool.eng-docs v0.4.0` is the immutable released graph owner; exact release/consumer SHA `63af20a033d6295a28c844d12cb87f76165e69a5`. | Pass |
| Event-timing pins released owner revisions | `project.yml` pins `tool.eng-docs v0.4.0`; CI also checks the exact gitlink SHA. | Pass |
| Production SVG exposes real engineering IDs | Final `prod/docs/assets/architecture/layered-architecture.svg` contains `data-engineering-id` for `TimingNode`, `CommandHandler`, `Conductor` and `RemoteApi`. | Pass |
| Initial selected source slice has stable anchors and checked typed relations | Sphinx-Needs requires explicit IDs; the original selected objects retain stable Need IDs, generated reader/native-reader anchors and schema-checked `derived_from`, `satisfies` and `verifies` target types. This criterion was later expanded to full-project stable-object coverage. | Pass |
| Book and portal derive from the same authoritative source | Final Book source SHA, Moon materialization, normalized graph and portal provenance all identify exact event-timing main `ff41c90a555f2f00fcb5a145f815eb88ba0bffa0`. | Pass |
| No hand-maintained inverse matrix or diagram label map is required | Sphinx-Needs generates inverse/backlink fields; repository audit found no authored `derived_from_back` / `satisfies_back` / `verifies_back` relation input and the portal consumes SVG `data-engineering-id` directly. | Pass |
| Exact revision / CI / publication evidence is retained | Steps 1–5 above retain owner releases, consumer heads/merges, exact CI runs and generated publication branches; final production run is #650. | Pass |
| Required versus optional capabilities are explicit | The production contract and optional reader surfaces are classified below. | Pass |
| Experiment 007 remains a regression/reference lab | `exp.2026-007.requirements-traceability` main remains complete and explicitly retained, including its human-review Pages site. | Pass |

### Required production contract

These are the durable Migration-013 invariants for a project that adopts the
engineering-graph model:

- one authoritative project source; derived readers must not become independent
  requirements/architecture/verification authorities;
- native MyST/Sphinx-Needs objects for the graph-exposed slice, with explicit
  stable engineering IDs;
- project-owned typed **outgoing** relations, validated near their owner;
- generated inverse/backlink context rather than authored inverse matrices;
- a released reusable `eng-docs graph` boundary consuming `needs.json` and
  preserving exact source provenance;
- diagram `object_id` / generated `data-engineering-id` identity when a
  diagram participates in engineering navigation, with graph cross-validation;
- normal Book generation remains available as a first-class linear review view;
- exact source/tool/materialization evidence is retained through the normal
  documentation lifecycle.

The production authoring convention is **stable-object scoped, not paragraph scoped**. After the full-project correction, every currently promoted stable engineering object is covered by Needs/graph validation. Ordinary narrative remains Markdown/MyST until it receives a promoted stable engineering ID; any such future ID automatically becomes a coverage obligation.

### Optional / consumer-selected reader capabilities

These are qualified views or conveniences, not additional engineering sources
of truth:

- generated GitHub-reader presentation, including content-first rendering,
  compact traceability metadata and the subtle `— — —` body/metadata separator;
- native Sphinx HTML cards and their collapsed metadata presentation;
- the Material portal itself, including search, generated object pages and the
  two-pane workspace;
- clickable architecture interaction in that portal;
- retained browser screenshots or other visual review evidence beyond the
  underlying CI assertions;
- GitHub Pages or another hosting layer is not part of the reusable graph contract for every future consumer. For the event-timing Migration-013 closeout, however, direct live portal publication became a required consumer criterion and is now deployed from protected `main`.

The Step-5 portal canary was required **evidence for this migration**, but the
portal UI is not elevated into the reusable source/graph contract. A future
consumer may use the core production contract with a different reader surface
without inventing a second engineering authority.

### Stable-source target interpretation

The stable engineering target is the explicit Need ID. Native Sphinx output and
the generated GitHub reader expose that ID as a stable object anchor. Direct
links back to authored source additionally pin the exact repository revision and
source location. This avoids pretending that ordinary Markdown line numbers are
the engineering identity while still giving reviewers an exact source jump.

### Initial closing result

The original canary closing audit passed on event-timing main
`ff41c90a555f2f00fcb5a145f815eb88ba0bffa0`, but the later full-project audit
showed that this was not a sufficient migration completion state. That evidence
is retained as canary qualification history rather than the final cut-over.

## Step 7 — full-project adoption and final cut-over

Status: **complete**

The reopened migration replaced the bounded-canary production state with a
source-driven full-project coverage contract.

Final evidence:

- event-timing cut-over PR
  [#163](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/163);
- exact merged event-timing main
  `0924620ad37ccfb30b4dcb16180e7851d370c2df`;
- exact-main documentation run `36569571453` (#760) — green;
- `prod/docs/source-sha.txt`, normalized graph and portal provenance all identify
  that exact main revision;
- normalized production graph: **53 objects / 42 authored outgoing relations**;
- graph object set: **19 use cases / 13 SI-01 requirements / 10 IF-03
  requirements / 10 architecture objects / 1 verification case**;
- the 10 architecture objects with diagram identity are
  `TimingSystem`, `SystemStatus`, `TimingNode`, `LogBook`, `TimingData`,
  `UpstreamProtocol`, `TimeSource`, `CommandHandler`, `Conductor` and
  `RemoteApi`;
- CI derives expected coverage from current stable source IDs instead of a
  hard-coded object count and rejects missing/unexpected graph objects;
- the IF-03 → SI-01 relation table was removed after those mappings became
  native `derived_from` relations, preserving single-authority outgoing
  relation ownership;
- generated GitHub-reader, native Sphinx reader, Book, normalized graph and
  Material portal all pass on the same exact source revision;
- the portal explorer is browser-exercised against the real generated
  architecture;
- GitHub Pages deployment completed successfully and exposes the live portal at
  https://brainboxemb.github.io/2026-010-01.meta.event-timing-software/;
- Experiment 007 remains the reusable review/regression lab;
- `tool.eng-docs v0.4.0` remains the released reusable graph owner.

This is the final Migration-013 completion state. No global engineering-graph
service or repository-wide conversion of ordinary narrative is introduced.

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
        +--> authoring requalification: native MyST selected
        |
        +--> Step 4: Needs-export graph boundary
        |
        +--> Step 5: event-timing production portal
        |
        v
Step 6: initial canary closing audit — later superseded
        |
        v
Step 7: full-project adoption + live consumer cut-over — complete
```

The migration should stop and reassess if a production owner exposes a concrete
conflict with the qualified experiment assumptions rather than weakening those
assumptions silently.
