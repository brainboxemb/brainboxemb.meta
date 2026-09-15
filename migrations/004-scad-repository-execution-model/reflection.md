# Migration 004 reflection — is the execution model still understandable?

Status: **reflection gate after Step 6**

This review deliberately looks at the released model as a human maintainer would. It does not treat prior agent/chat reasoning as authority.

## Short answer

The current model is technically coherent and its individual design decisions are documented somewhere, but the model is **not yet documented coherently enough for a maintainer who starts in a consumer repository**.

A maintainer can reconstruct why the graph exists, but currently has to combine:

1. this migration's `change-request.md` for the original architectural choices;
2. `tool.scad-project/docs/production-workflow.md` for the source-impact versus execution-aggregate split and host/container/publication lifecycle;
3. `tool.scad-project/docs/execution-evidence.md` for the producer-versus-finalization/evidence boundary;
4. `tool.scad-project` release history for the explicit decision to keep visible Moon producer boundaries instead of hiding them behind coarse producer wrappers;
5. the consumer's `moon.yml` to infer how those generic decisions map to the repository.

That is too much archaeology for ordinary maintenance.

## What the HUB75 graph actually contains

Released `lib.scad.hub75 v0.1.4` has eight Moon tasks:

| Task | Kind | Human purpose |
| --- | --- | --- |
| `scad.docs` | producer | Generate design documentation and retain docs execution/domain evidence. |
| `scad.build` | producer | Generate configured presentation/build artifacts and retain build execution/domain evidence. |
| `scad.build-index` | build finalization | Create the human-readable build/gallery index after docs and build output exist. |
| `scad.build-provenance` | build finalization | Add current publication/source context to the prepared Build tree. |
| `scad.verify` | producer | Run API/project verification and generate verification fixtures/evidence. |
| `scad.verification-provenance` | verification finalization | Add current publication/source context to the prepared Verification tree. |
| `scad.production-impact` | virtual preflight gate | Answer only: did source/config/tooling changes affect one of the expensive producer domains? |
| `scad.ci` | virtual execution root | Materialize the complete publication-ready Build and Verification trees once production is known to be required. |

The graph is therefore not eight separate CAD phases. It is three producer domains, three output-finalization tasks and two virtual orchestration roots.

Conceptually:

```text
                           source-impact question
                                  |
                                  v
                     scad.production-impact
                       /        |        \
                      v         v         v
               scad.docs   scad.build   scad.verify
                   \          /              |
                    v        v               v
                 scad.build-index   scad.verification-provenance
                         |
                         v
                 scad.build-provenance
                         \             /
                          v           v
                              scad.ci
                         publication-ready
```

The direction above is conceptual: producer tasks feed finalization, while the two virtual roots select different parts of the same graph for two different questions.

## Why two virtual roots exist

This is the least obvious but most important distinction.

`scad.production-impact` is used before pulling the SCAD image. It must depend only on real producer/source inputs. A README-only change should therefore remain unaffected.

`scad.ci` is used after the decision to produce. It must also materialize indexes and publication provenance so both generated branches are complete.

Those finalization tasks consume GitHub context such as event/ref/PR information. Moon correctly treats those environment inputs as changing publication context. If `scad.ci` itself were also used as the preflight target, that context could make an otherwise unrelated change look affected and the expensive SCAD container would start unnecessarily.

The split is therefore intentional, not just naming indirection.

## Why producer and finalization tasks are separate

`tool.scad-project` distinguishes **producer evidence** from **current materialization/publication context**.

Producer evidence belongs to the CAD/docs/verification result that was actually executed and may later be hydrated from cache. It must remain tied to the execution that created it.

Indexes/provenance/materialization describe how that result is being consumed or published now. They may legitimately change even when producer output is reused.

Keeping those responsibilities separate prevents a cache hydration from pretending that old producer evidence was freshly executed for the current revision.

This separation is documented in `tool.scad-project/docs/execution-evidence.md`, but it is not presently obvious from a consumer's `moon.yml`.

## Why three producer domains exist in HUB75

HUB75 differs from the smaller clamps library because it genuinely owns three independently affected output classes:

- standalone presentation renders (`scad.build`);
- generated design documentation (`scad.docs`);
- API plus physical-verification artifacts (`scad.verify`).

The Step-6 proof PRs demonstrated that each can be affected without the other two being direct source impacts. That is useful information and not merely graph decoration.

## What is documented well

The following architectural decisions are documented with real rationale:

- Moon owns repository/task affected-state while SCons remains the fine-grained SCAD target engine;
- Build and Verify are logical domains, not GitHub-job boundaries;
- README-only/unrelated changes must stop before the SCAD image is pulled;
- the host/container credential boundary keeps publication credentials outside the SCAD runtime;
- source-impact preflight and publication-ready execution are deliberately different queries;
- producer execution evidence is different from current orchestration/materialization/publication evidence.

The strongest current explanation is `tool.scad-project/docs/production-workflow.md` together with `docs/execution-evidence.md`.

## What is not documented well enough

### 1. No consumer-level map of the complete graph

`lib.scad.hub75/README.md` now explains the three producer domains, but it does not explain all eight Moon tasks or show how they fit together.

Opening `moon.yml` therefore looks much more complicated than the conceptual model actually is.

### 2. Important rationale is distributed across repositories

The reason for Moon versus SCons is mainly in meta. The reason for `affected_task` versus `aggregate_task` is mainly in the tool. The reason finalization remains separate from producers is mainly in the execution-evidence document and release history.

There is no single current architectural page that joins those decisions.

### 3. `moon.yml` contains no explanatory comments

The file is machine-readable but not reader-oriented. In particular, the two no-op tasks (`scad.production-impact` and `scad.ci`) are surprising unless the reader already knows the orchestration contract.

### 4. Historical documents contain superseded topology language

The original change request still describes separate lightweight publication jobs in several places. v0.13.1 deliberately collapsed publication into the same host orchestrator job after the performance experiment. The historical decision trail is useful, but it should be clearly distinguished from the current architecture.

### 5. Composite producer commands create an apparent contradiction

`tool.scad-project` exposes `produce-build` and `produce-verification` as stable composite producer actions. At first sight that suggests the Moon graph could be reduced to two coarse producer tasks.

However, the v0.11 execution-evidence contract explicitly chose to keep `scad.docs`, `scad.build` and `scad.verify` visible as separate Moon producer boundaries so their affected-state, cache/evidence and execution identity remain independently observable. That current rationale is not prominent enough next to the composite-command documentation.

## Is the complexity justified?

**Partly.** The graph has more names than the underlying conceptual model, but most boundaries have a concrete reason under the currently qualified invariants.

The strongest justified boundaries are:

- `docs` / `build` / `verify`: real independent producer domains;
- source-impact gate versus publication-ready aggregate: required to keep environment-sensitive publication context from defeating zero-container preflight;
- producer execution versus publication/materialization finalization: required for truthful cached evidence.

The weakest/currently least-proven boundary is the split between `scad.build-index` and `scad.build-provenance`. Both are Build-tree finalization after the two Build-side producers exist. They may be collapsible into one reader-visible `scad.build-finalize` task without weakening the architectural invariants. That should be tested rather than assumed.

Other possible simplifications, such as hiding all Build work behind `produce-build`, would reduce YAML but would also collapse the independently qualified docs/build producer boundaries. That is not automatically an improvement.

## Recommended next action

Do **not** continue to the HUB75-frame rollout yet.

First make the architecture readable before deciding whether to simplify it:

1. add one canonical current-architecture document in `tool.scad-project` containing the complete graph, task-role table and the three ownership layers: Moon, SCAD producer/SCons and publication;
2. make consumer README files link directly to that architecture page and include only their repository-specific producer mapping;
3. add short comments in the reference `moon.yml` explaining the three groups: producers, finalizers and virtual roots;
4. mark historical topology in the Migration 004 change request as superseded where v0.13.1 changed it;
5. evaluate whether `scad.build-index` + `scad.build-provenance` can become one `scad.build-finalize` task without weakening caching, evidence or publication behavior;
6. only after that review decide whether further structural simplification is worth a new tool release.

A useful acceptance test is simple:

> Give a maintainer the current consumer repository and the linked architecture documentation. They should be able to explain every Moon task and predict README-only, Build-only, docs-only and Verify-only impact without reading migration history or chat logs.

Migration 004 should not proceed until that test is credible.
