# New chat / work-session handoff

Use this instruction to continue cross-project work in a new ChatGPT conversation.
The repositories and current GitHub evidence, not old chat history, determine the
active work track, next valid step, owner and required evidence.

## Copy/paste start instruction

```text
Werk vanuit brainboxemb/brainboxemb.meta als cross-project coordination source.

Bepaal zelf vanuit de actuele repository welke cross-project work track momenteel
primair actief is en welke eerstvolgende geldige stap daarin aan de beurt is.
Een work track kan bijvoorbeeld een migration, een experiment of een Proof of
Principle (PoP) zijn. Vraag mij niet om een migration-, experiment-, PoP- of
stepnummer als dat uit de repository kan worden afgeleid.

Gebruik oude chatgeschiedenis niet als source of truth. Controleer eerst de
actuele repositorydocumentatie en daarna de relevante owner repositories,
issues/pull requests, CI/evidence en gegenereerde output.

Lees eerst:
- README.md;
- AGENTS.md;
- STATUS.md;
- docs/README.md;
- migrations/README.md;
- experiments/README.md.

Bepaal daarna zelf:
1. welke actieve cross-project work track volgens STATUS.md primair is;
2. welk type work track dit is en welk record/index daarbij authority heeft;
3. welke eerstvolgende niet-afgeronde stap of prerequisite werkelijk aan de
   beurt is;
4. welke owner repository bij die stap hoort;
5. welke prerequisites, supporting documents en evidence werkelijk relevant zijn.

Als de actieve track een migration is, lees vervolgens de migration-README en
alleen de relevante supporting files, zoals change-request.md, decision.md,
evidence.md, activation.md of stepbestanden wanneer die aanwezig zijn.

Als de actieve track een experiment/PoP is, lees vervolgens het record onder
experiments/ en de tracking issue. Gebruik daarna de dedicated experiment/PoP
repository als implementatie/evidence-owner wanneer die bestaat. Houd fixtures,
testcases, harnesses, adapters en qualification results daar; brainboxemb.meta
houdt de cross-project vraag, target concept, status, evidenceconclusie en
productiebeslissing bij.

Gebruik voor een PoP een design-first aanpak wanneer het concept uit bestaande
engineeringkennis en actuele architectuur kan worden ontworpen:
- ontwerp eerst het target concept en de verantwoordelijkheden;
- splits design decisions van aannames die runtime evidence nodig hebben;
- gebruik de PoP alleen om die onzekerheden reproduceerbaar te bewijzen;
- implementeer niet automatisch alle mogelijke kandidaattools alleen om ze te
  vergelijken;
- voeg alternatieven toe wanneer het target concept een principe niet haalt of
  een concrete ontwerpbeslissing zonder vergelijking onopgelost blijft.

Een geldige PoP-failure is nuttige evidence. Pas het concept/assumption aan in
plaats van de testcase zwakker te maken zodat de PoP groen wordt.

Behandel een PoP-repository bij voorkeur als herbruikbaar, niet disposable.
Wanneer een latere migration of production owner een probleem laat zien dat de
fixture betrouwbaar kan reproduceren:
- leg eerst een reproduceerbare testcase vast;
- bewijs de failure;
- kwalificeer de correctie in de PoP-repository;
- pas daarna de echte owner aan via zijn normale issue/PR/migration flow;
- behoud de testcase als regression coverage.

Als een experiment/PoP-record een nog ontbrekende repository als prerequisite
noemt, behandel het aanmaken daarvan als de eerstvolgende stap. Implementeer de
proef niet tijdelijk in een productie-owner alleen om verder te kunnen.

Als meta-documentatie en actuele owner-repository evidence elkaar tegenspreken,
onderzoek dan eerst de discrepantie. Corrigeer brainboxemb.meta wanneer de
cross-project status, sequencing of evidence daar achterloopt. Een verouderde
status mag niet bepalen welke stap wordt uitgevoerd.

Herverifieer vóór implementatie de stap inhoudelijk. Controleer expliciet:
- is het doel, target concept of de onderzoeksvraag nog steeds het juiste doel;
- klopt de owner en ownership-boundary nog;
- kloppen prerequisites en volgorde nog;
- zijn de aannames nog geldig tegen de huidige implementatie;
- dekken de geplande tests/scenario's/evidence de echte risico's voldoende af;
- kan de stap eenvoudiger, scherper of robuuster worden gemaakt op basis van
  eerdere resultaten;
- als documentatie/evidence/publicatie geraakt wordt: zijn eerst de actuele
  repository-use-cases bekeken en is de gekozen oplossing daarop gebaseerd.

Als die herbeoordeling een beter plan of een nieuwe prerequisite oplevert, werk
waar nodig eerst brainboxemb.meta bij en voer daarna de gecorrigeerde stap uit.
Een migrationplan of experiment/PoP-opzet is een gecontroleerde werkhypothese,
geen opdracht om oude tekst mechanisch te volgen.

Gebruik voor implementatie de repository die de geselecteerde stap als owner
heeft. Pak geen latere stap op behalve wanneer de huidige stap een noodzakelijke
plancorrectie of prerequisite blootlegt.

Houd de blocking path klein. Classificeer nieuw ontdekt werk passend bij het
actieve tracktype, bijvoorbeeld als:
- blocker voor de huidige stap;
- aanvullende PoP/qualification testcase;
- afzonderlijk experiment;
- follow-up migration;
- backlog / improvement.

Alleen echte blockers verlengen de actuele stap.

Voor experiments/PoPs geldt aanvullend:
- geef de voorkeur aan reproduceerbare fixtures en declaratieve/executable
  testcases boven handmatige probing;
- laat CI de testcases en assertions waar praktisch mogelijk zelf orkestreren;
- trek geen productieconclusie uit één losse probe als dezelfde vraag als
  herhaalbare testcase kan worden vastgelegd;
- onderscheid control baseline, PoP-evidence en latere qualification-evidence;
- een afgeronde PoP/experiment activeert niet automatisch een migration.

Na implementatie of PoP/experimentuitvoering:
- controleer de tests/evidence die bij de stap horen;
- beoordeel wat de resultaten betekenen voor concept en latere stappen;
- werk cross-project status/evidence en relevante plan- of experimentverbeteringen
  in brainboxemb.meta bij waar dat nuttig is;
- houd implementatiedetails in de repository die eigenaar is van de stap.

Gebruik brainboxemb/meta.scad-projects alleen als historische bron wanneer dat
expliciet nodig is. Die repository is gearchiveerd en is niet meer de actuele
cross-project authority.
```

## Resolution rule

A new session should normally be able to answer these questions from GitHub before
implementation starts:

```text
Which cross-project work track is primary now?
Is it a migration, experiment, PoP or another explicit track?
Which step or prerequisite is next?
Who owns it?
What evidence proves its prerequisites?
```

`STATUS.md` is the current-position entrypoint. Migration and experiment/PoP
indexes then point to the authoritative cross-project record. Owner repositories
remain authoritative for implementation state and local evidence.
