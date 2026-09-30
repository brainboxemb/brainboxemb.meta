# Migration 014 — adopt reusable roadmap rendering

Status: **active — refined owner released; first consumer PR qualified; exact-main cut-over pending**

Tracking issue: [#181](https://github.com/brainboxemb/brainboxemb.meta/issues/181)

Reusable-owner issues:
[tool.eng-docs #59](https://github.com/brainboxemb/tool.eng-docs/issues/59),
[tool.eng-docs #61](https://github.com/brainboxemb/tool.eng-docs/issues/61),
[tool.eng-docs #63](https://github.com/brainboxemb/tool.eng-docs/issues/63) and
[tool.eng-docs #65](https://github.com/brainboxemb/tool.eng-docs/issues/65)

First production consumer:
[`2026-010-01.meta.event-timing-software`](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software)

## Why this migration exists

The event-timing documentation currently contains a project-local
manager-roadmap renderer. It reads the authoritative SIP directly and rejects
normal planning changes when titles, Result bullets or Demo bullets do not fit
fixed card geometry.

That makes a presentation concern part of the source-document contract. During
the Step-4 planning update this caused repeated CI-only failures for unrelated
layout constraints, including content from later steps that was not being
changed functionally.

The intended reusable boundary is:

```text
authoritative project planning
        |
        | consumer-owned meaning
        v
consumer roadmap adapter / view data
        |
        | generic presentation contract
        v
tool.eng-docs RoadmapView
        |
        +--> SVG
        +--> printable PDF
```

The roadmap is a view of planning. It is not the authority for planning meaning.

## Ownership boundary

### `brainboxemb.meta`

Owns migration sequencing, cross-repository gates and retained qualification
evidence. It does not own renderer implementation.

### `brainboxemb/tool.eng-docs`

Owns reusable mechanisms only:

- a domain-neutral roadmap presentation model;
- schema/semantic validation of that presentation model;
- generic layout, pagination and rendering;
- SVG output;
- printable PDF output when required by the first consumer cut-over;
- useful overflow handling;
- CLI/user documentation;
- domain-neutral examples and tests.

It must not know about SIP, TimingNodes, event timing, Step-4 semantics or
project-specific document identifiers.

### Event-timing consumer

Owns:

- the authoritative SIP and planning prose;
- mapping project planning semantics to the reusable presentation model;
- any deliberately compact roadmap wording;
- estimates, project status and project-specific labels;
- generated-output integration and publication.

## Reusable presentation contract

The first reusable contract is a **RoadmapView**, not a planning-domain model.

Illustrative input:

```yaml
roadmap:
  title: Engineering roadmap
  subtitle: optional context
  items:
    - id: "4"
      title: First registration-system slice
      state:
        label: ACTIVE
        tone: active
      meta:
        - "~3d"
        - "forecast 19 Oct"
      sections:
        - heading: RESULT
          bullets:
            - Location/open-close rules are explicit.
            - Direct registration produces TimingData.
        - heading: DEMO
          bullets:
            - Set location and open registration.
            - Inject and inspect one registration.
      badges:
        - label: SSSD
          tone: mature
```

Names are illustrative; owner implementation may refine spelling while
preserving the boundary.

Required properties:

- item identity is opaque to the renderer;
- section headings are consumer data, not hard-coded Result/Demo semantics;
- state labels/tone are presentation data, not project workflow semantics;
- badges are generic chips, not hard-coded engineering-document types;
- authoritative planning prose is not part of the renderer input contract.

## Overflow and layout behaviour

A reusable renderer must not make authoritative project text shorter merely to
fit a card.

For RoadmapView presentation data it must:

1. wrap text predictably;
2. never silently clip or ellipsize semantic content;
3. prefer layout adaptation/pagination over failure;
4. report an actionable error only when the presentation model is structurally
   invalid or no supported layout can represent it;
5. allow the consumer to supply intentionally compact roadmap wording without
   modifying authoritative planning source.

The first implementation may use bounded layout choices rather than solve
arbitrary typography, but those bounds belong to RoadmapView presentation data,
not to the project's SIP.

## CLI direction

The first owner slice should provide an explicit local command, conceptually:

```text
eng-docs roadmap --source <roadmap-view.yaml> --out <directory>
```

The same validation/rendering path must run locally and in CI. CI must not be
the first place normal layout errors are discovered.

## Migration steps

### Step 1 — specification and contract

Status: **done**

Gate:

- this ownership boundary is accepted;
- RoadmapView is presentation data, not source planning authority;
- no event-timing-specific semantics are required in the reusable API.

### Step 2 — reusable owner implementation

Status: **done**

Owner: `brainboxemb/tool.eng-docs`

Implement under issue #59 using the normal issue → feature branch → draft PR
flow.

Minimum qualification:

- schema/validation for the generic presentation model;
- local CLI;
- deterministic SVG rendering;
- printable PDF output if required by the consumer cut-over;
- domain-neutral example;
- tests for wrapping/overflow and invalid input;
- Linux and Windows owner CI green;
- user-facing documentation updated.

Do not copy the event-timing renderer unchanged.

### Step 3 — owner release

Status: **done**

Release the qualified `tool.eng-docs` capability before production consumer
cut-over. Record exact tag, owner revision and green release evidence here.

### Step 4 — event-timing consumer cut-over

Status: **active — v0.6.0 PR qualification green; exact-main qualification pending**

First-consumer review triggered owner issue #61 / PR #62 to refine the generic
visual hierarchy without changing the ownership boundary. Variable-height
wrapping/pagination remains generic, while the consumer owns which ordered
metadata value represents its end date/forecast and which heading names its
document-status badge group. That refinement was released as v0.5.1. A denser three-column grid followed in
v0.5.2, and the reusable print-friendly BoardView/detail-board renderer is now
released as v0.6.0. Event-timing has been repinned and requalified on v0.6.0.

Owner: `brainboxemb/2026-010-01.meta.event-timing-software`

After the owner release:

- pin the released `tool.eng-docs`;
- add a small consumer-owned adapter/view producer from SIP/project planning to
  RoadmapView;
- restore complete SIP wording where it was shortened only for old card geometry;
- replace the project-local generic manager-roadmap renderer;
- keep project-specific planning extraction/mapping in the consumer;
- prove local roadmap generation before CI;
- qualify exact PR and exact main documentation builds.

The current Step-4 feature PR should not remain a CI-driven layout-debug loop.

## Qualification evidence

### Reusable owner

- `tool.eng-docs` PR
  [#60](https://github.com/brainboxemb/tool.eng-docs/pull/60) merged the generic
  RoadmapView implementation to main as
  `f9607fedee988c96d6e7dfccf50594eb3d8c36c9`.
- Exact-main Test run
  [36736031799](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36736031799)
  passed Linux, Windows, conformance-document generation and generated-output
  publication.
- Release `v0.5.0` was created from that exact main revision.
- Tagged verification run
  [36736466247](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36736466247)
  passed Linux, Windows, conformance generation and publication.
- Release workflow
  [36736447736](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36736447736)
  completed successfully and published the Python package assets.
- Owner issue
  [#59](https://github.com/brainboxemb/tool.eng-docs/issues/59) is closed as
  completed.

#### Visual refinement

- First-consumer visual review is captured in owner issue
  [#61](https://github.com/brainboxemb/tool.eng-docs/issues/61), closed by
  [PR #62](https://github.com/brainboxemb/tool.eng-docs/pull/62).
- PR #62 merged to owner main as
  `6815a2f003150ad803f1162b1eed0e6b96e2636d`.
- Exact-main Test run
  [36741834973](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36741834973)
  passed Linux, Windows, conformance generation and publication.
- Release `v0.5.1` was created from that exact main revision.
- Tagged verification run
  [36742112482](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36742112482)
  passed the same owner qualification at the immutable tag.
- Release workflow
  [36742092047](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36742092047)
  completed successfully and published the package assets.
- The refinement adds a compact visible marker, stable state/primary-meta
  placement, named badge groups and quieter section/card styling while retaining
  adaptive height and pagination.

#### Three-column density refinement

- Owner issue [#63](https://github.com/brainboxemb/tool.eng-docs/issues/63)
  was closed by [PR #64](https://github.com/brainboxemb/tool.eng-docs/pull/64).
- PR #64 merged to owner main as
  `92ff73115455c23f19529ce6b376998086842d9c`.
- Exact-main Test run
  [36744597776](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36744597776)
  passed.
- Tagged verification run
  [36744805179](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36744805179)
  and Release run
  [36744784655](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36744784655)
  qualified released `v0.5.2`.
- The default A4-landscape grid now uses smaller outer margins, gaps and card
  inset so the first consumer returns to three columns without shrinking text
  or reintroducing content limits.

#### Reusable detail-board rendering

- Owner issue [#65](https://github.com/brainboxemb/tool.eng-docs/issues/65)
  was closed by [PR #66](https://github.com/brainboxemb/tool.eng-docs/pull/66).
- PR #66 merged to owner main as
  `86deb06231a8d4fce64ffe877f82edaa7ba803bb`.
- Exact-main Test run
  [36745831458](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36745831458)
  passed Linux, Windows, roadmap and BoardView conformance generation/publication.
- Tagged verification run
  [36746026784](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36746026784)
  passed at immutable tag `v0.6.0`.
- Release workflow
  [36746008771](https://github.com/brainboxemb/tool.eng-docs/actions/runs/36746008771)
  completed successfully and published package assets.
- RoadmapView and BoardView now share print-friendly presentation primitives:
  white cards, neutral borders/rules and compact color accents rather than large
  colored backgrounds.

### First production consumer

Event-timing PR
[#214](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/pull/214)
currently qualifies the refined cut-over at head
`7cf82d5cd9bc891c850551b63fea1151571c02d9`:

- `project.yml` and the `tools/tool.eng-docs` gitlink pin released
  `v0.6.0` / `86deb06231a8d4fce64ffe877f82edaa7ba803bb`;
- the project-local manager-roadmap file is now a consumer adapter that reuses
  the existing project-owned `parse_sip()` semantics and emits RoadmapView;
- generic card layout, wrapping, pagination, SVG and PDF rendering are owned by
  `eng-docs roadmap`;
- existing publication filenames are retained so document assembly did not need
  an unrelated migration;
- Step 4 was restored to four Result bullets and seven Demo bullets, proving the
  authoritative SIP is no longer forced into the former 1..3-bullet / fixed-line
  card contract;
- the earlier v0.5.0 run
  [36737383063](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/actions/runs/36737383063)
  established the structural cut-over;
- exact-head v0.5.1 documentation run
  [36742717634](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/actions/runs/36742717634)
  passed planning generation, traceability, portal verification, generated
  reader verification, retained producer-evidence checks and preview
  publication at `7b456adc34eb179831d9246e3600d8daa7774d24`;
- the consumer maps the visible marker to the step number, shows end/forecast
  before effort, keeps the title free of redundant `Step N` text, and groups
  document badges under `DOCUMENT STATUS`;
- overall plan/cadence data is now shown once in the first `PLAN / TERMS`
  overview card instead of being repeated in every page header;
- the released v0.5.2 grid renders the production roadmap with three columns
  and reduced double whitespace at the page/card edges;
- project-owned step/lane/activity/document semantics are mapped into BoardView;
  the previous local `render_step_svg()` implementation has been removed;
- exact-head v0.6.0 documentation run
  [36746582605](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/actions/runs/36746582605)
  passed planning generation, BoardView detail boards, traceability,
  portal/reader verification and preview publication at
  `7cf82d5cd9bc891c850551b63fea1151571c02d9`;
- preview inspection also exposed and removed one duplicated Step-5 SIP heading
  before retaining the final qualification evidence.

The structural v0.5.0 evidence remains part of the migration history. The
first-consumer visual refinement has now also been released and qualified through
event-timing #214. The only remaining gate is deliberate: after #214 is merged,
run and retain the same documentation qualification on the exact event-timing
`main` commit. Only then may Migration 014 be marked complete.

## Detail-board presentation follow-up

First-consumer review also exposed a second duplicated presentation mechanism:
the event-timing portrait step/detail boards were still rendered locally. That
follow-up was completed through `tool.eng-docs` issue #65 / PR #66 and released
as v0.6.0.

The same ownership boundary applies:

- `tool.eng-docs` owns generic print-friendly BoardView layout/rendering;
- event-timing owns lane, activity, document and planning-change semantics;
- the consumer adapter maps those concepts into BoardView;
- roadmap and detail boards should share one presentation style rather than
  maintain separate color/layout implementations.

This follow-up remains part of Migration 014 because it is another
cross-repository extraction triggered by the same planning-publication cut-over.
It does not expand `tool.eng-docs` into a planning-domain model. Event-timing
now emits BoardView and receives SVG/PDF from `eng-docs board`.

## Completion criteria

Migration 014 is complete only when:

- released `tool.eng-docs` owns the reusable RoadmapView and BoardView rendering contracts;
- reusable schemas/examples contain no event-timing/SIP semantics;
- event-timing consumes the released capability through a project-owned adapter;
- authoritative SIP prose is no longer constrained by roadmap card geometry;
- the duplicated generic roadmap/detail-board renderers are removed from the event-timing consumer;
- the same roadmap validation/rendering command runs locally and in CI;
- exact owner and exact consumer CI evidence is retained here.

## Non-goals

This migration does not redesign event-timing planning semantics, force roadmap
adoption elsewhere, turn `tool.eng-docs` into a planning workflow engine, or
activate another inactive migration.
