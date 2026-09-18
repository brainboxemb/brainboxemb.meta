# Detachable SCAD clip interface PoP

Status: **active — upstream reference work complete; reduced receiver + snap under refinement**

Tracking issue: [#79](https://github.com/brainboxemb/brainboxemb.meta/issues/79)

Production driver:
`brainboxemb/2026-009-01.cad.HUB75-display-frame`

Implementation/evidence repository:
[`brainboxemb/exp.2026-005.scad-detachable-clip-interface`](https://github.com/brainboxemb/exp.2026-005.scad-detachable-clip-interface)

## Question

Can a compact printed fixed-side interface accept a removable clip part with
repeatable insertion/removal and useful retention, while remaining printable,
serviceable and unobtrusive when no clip is installed?

The first production use under consideration is the horizontal aluminium-tube
clip in the HUB75 display frame, but the PoP deliberately starts with neutral
coupons rather than production coupler geometry.

## Why a separate PoP

The current HUB75 core couplers are digitally accepted, but physical coupler
acceptance is downstream of unfinished physical verification of the HUB75 panel
model itself.

That blocks freezing the production panel-facing interface. It does not block
learning whether a detachable clip mechanism works.

Keeping the experiment separate allows these two tracks to proceed independently:

```text
physical panel/core acceptance
        -> production interface freeze

detachable attachment PoP
        -> qualified interface contract

both complete
        -> production integration
```

## Repository roles

### External-source fork

A selected third-party OpenGrid/OpenSCAD implementation is retained as a fork so
upstream history, licence and exact provenance remain visible.

Generic naming:

```text
fork.<upstream-owner>.<upstream-repository>
```

normalized to lowercase.

Selected fork:

```text
brainboxemb/fork.andylevesque.quackworks
```

GitHub confirms that repository as a real fork of `AndyLevesque/QuackWorks`.
Its `main` is currently the exact inspected source
`e0c1cb7ec78dd9e9a8476ed739bd3402074354f3`.

The fork is an external-source boundary, not the place for HUB75-specific
fixtures or design decisions.

### Experiment repository

Established:

```text
brainboxemb/exp.2026-005.scad-detachable-clip-interface
```

The **Upstream Full reference** and **Full versus Lite comparison** are complete
in experiment PRs #1 and #2. The repository pins the fork below
`dsg/openscad/ext/quackworks` at exact
`e0c1cb7ec78dd9e9a8476ed739bd3402074354f3`.

The Full/Lite comparison adds separate Full/Lite receiver and snap profile PNGs
and 1.0 mm profile-slice STLs. The upstream dimensions are:

```text
                         Full       Lite
receiver height          6.8 mm     4.0 mm
snap height              6.8 mm     3.4 mm
snap footprint          24.8 mm    24.8 mm
```

Lite is selected as the primary starting reference for the reduced receiver + snap design.

It owns:

- neutral fixed-side and removable-side coupons;
- source/mechanism analysis;
- adapters needed only by the experiment;
- candidate attachment concepts when comparison is genuinely necessary;
- detachable tube-clip prototype;
- reproducible digital and physical testcases;
- retained qualification evidence.

### Production project

The HUB75 project consumes only the resulting qualified interface contract after
its own core panel-facing interface is physically accepted and frozen.

## OpenGrid source survey

### Primary candidate — QuackWorks

Repository:

```text
AndyLevesque/QuackWorks
```

Exact inspected main:

```text
e0c1cb7ec78dd9e9a8476ed739bd3402074354f3
```

Relevant files:

```text
openGrid/openGrid.scad
openGrid/opengrid-snap.scad
```

The important architecture is already close to the PoP question:

- the OpenGrid cell/board is the fixed receiver;
- `openGridSnap()` is a separate removable approximately 24.8 mm square part;
- small perimeter nubs provide retention;
- long click-hole regions make the surrounding snap material compliant;
- `directional=true` changes retention behaviour while retaining the same basic
  receiver;
- the snap is intended to print as a standalone part;
- recent upstream history contains explicit fixes for snap mesh/print
  connectivity.

This makes QuackWorks a stronger first mechanism reference than a tile-to-tile
connector implementation.

### Comparison — jp-embedded/opengrid

`jp-embedded/opengrid` remains useful because it contains alternative
snap/socket and lock implementations, including BOSL2 clip/rabbit-style
mechanisms. It is a comparison source, not currently the preferred fixed
receiver/removable insert reference.

### Application reference — openGrid Snap Mount Generator

`nnarain/opengrid-snap-mount-generator` demonstrates almost exactly the
application pattern behind this PoP: it takes the QuackWorks-style
`openGridSnap()` and fuses one or more snaps to an otherwise ordinary mounting
plate with user-defined holes.

It is useful as evidence that "removable OpenGrid snap + arbitrary functional
part" is a practical decomposition. It currently carries a copied snap
implementation rather than establishing a cleaner upstream source/licence
boundary, and its copy predates recent QuackWorks snap-connectivity fixes, so it
is a design/application reference rather than the preferred source dependency.

### Verification reference — connector-foundry

`dnnsmnstrr/connector-foundry` vendors/wraps the QuackWorks OpenGrid board and
snap as externally sourced parts and adds systematic reference-shape and
assembled-fit verification. Its approach is useful evidence for how the PoP can
separate upstream geometry confidence from experiment-owned adapters and tests.

### Official OpenGrid reference

`openGrid-3D/openGrid-openSCAD` and the official OpenGrid documentation remain
important for ecosystem intent and terminology even though the currently
inspected OpenSCAD repository is less directly useful for this particular
removable-snap PoP.

## Licence/provenance constraint

QuackWorks declares CC BY-NC-SA 4.0 at repository level. The
`opengrid-snap.scad` header additionally credits the OpenGrid design to David D
and the OpenSCAD snap implementation to metasyntactic, with wording that should
be treated as needing explicit provenance/licence review.

Therefore the initial PoP should:

1. retain the exact upstream source separately;
2. document the mechanism in engineering terms;
3. use upstream geometry only inside the clearly attributed experimental
   boundary when required;
4. avoid assuming that a production reimplementation may copy upstream geometry
   merely because the PoP can render it;
5. make a deliberate licensing/design decision before production reuse.

This record is not legal advice; it is an engineering provenance boundary.

## Design-first target concept

The intended functional decomposition is:

```text
fixed coupler-side feature
        +
removable attachment feature
        +
tube-clamping profile
```

The first PoP should establish the attachment pair without the tube. Only after
insertion, retention, printability and tolerances are understood should the real
horizontal tube profile be added.

Early experiment steps should treat **PNG and STL as complementary evidence**:
PNG assemblies/sections explain the mechanism and mating geometry, while
separate STL exports make the same fixed/removable parts available for physical
handling and print-fit checks.

The fixed feature should preferably remain compact and useful as a common
interface when no clip is installed.

## Assumptions requiring evidence

The PoP should answer at least:

- can the removable part insert and release without damaging the fixed side;
- which material region must flex and in which direction;
- what geometry locates versus retains the part;
- what printer/material/tolerance range still produces a usable fit;
- what loads are carried in pull, shear and rotation;
- whether directional retention is useful for the tube application;
- whether a 28 mm / 24.8 mm OpenGrid-scale mechanism can be reduced or reshaped
  without losing its useful behaviour;
- whether the interface remains simple enough to add to several coupler families;
- whether the eventual tube clip can be printed in a favourable orientation
  independently of the production coupler.

## Experiment sequence

Keep the implementation/evidence sequence small and descriptive:

1. **Upstream Full reference**
   - reproduce the selected QuackWorks fixed receiver + removable snap at the
     pinned revision;
   - generate assembled, exploded and section PNG evidence;
   - export the fixed receiver and removable snap as STL;
2. **Full versus Lite comparison**
   - compare the upstream low-profile Lite relationship with the Full reference;
   - retain Full as the control when the purpose of a removed feature is unclear;
3. **Reduced receiver + snap**
   - isolate the minimum attachment pair from the full OpenGrid context;
   - keep the fixed/removable geometry neutral and reusable;
4. **Retention and flex geometry**
   - make compliant regions, lead-ins and locking/contact surfaces measurable;
5. **Tolerance qualification**
   - vary only the critical clearance/interference dimensions;
6. **Tube-clip carrier**
   - add the horizontal-tube clamp only after the attachment principle is
     understood.

Do not manufacture extra candidate mechanisms unless an earlier case exposes a
concrete unresolved design decision.

## Upstream Full reference retained result

The upstream Full reference established the source decomposition without adapting it:

- fixed side: OpenGrid cell/receiver;
- removable side: separate approximately 24.8 mm `openGridSnap()`;
- full receiver and full snap share the nominal 6.8 mm Z envelope;
- retention is local around the snap perimeter;
- long side openings leave compliant material beside the retention features.

The experiment explicitly does not infer insertion force, pull-out force,
fatigue, material choice or printer-tolerance robustness from those renders.
Those remain later PoP questions.

The later Full/Lite comparison retained this as the control reference.

## Full versus Lite comparison retained result

The Lite receiver is derived from the upper part of the Full receiver. The Lite
snap keeps the same footprint but removes the lower Full-height stage and moves
the retention/compliance geometry into the shallower body.

The receiver is 4.0 mm high and the basic Lite snap is 3.4 mm high. The accepted
reference does not convert that arithmetic 0.6 mm difference into a seated
offset; receiver and snap use the upstream CENTER anchoring.

The active **Reduced receiver + snap** work reduces the Lite relationship first,
keeping Full as a control when the purpose of a removed feature is uncertain.
Current geometry/evidence refinement is tracked in experiment PR #7.

## Qualification boundary

The PoP may qualify an attachment principle and interface contract.

It does not:

- accept the real HUB75 panel geometry;
- accept the current production couplers physically;
- freeze the production coupler interface;
- authorize direct copying of third-party geometry into the production project.

Production integration starts only when the HUB75 project has both a frozen core
interface and a qualified detachable-interface result.

## Reuse

If later clip/coupler work exposes an attachment failure that can be reproduced
on the neutral fixture, retain it as a regression case in the PoP repository
rather than solving it only inside the product assembly.
