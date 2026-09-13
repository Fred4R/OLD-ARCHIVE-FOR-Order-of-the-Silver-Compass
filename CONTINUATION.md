# Continuation and Symbolic-Story Plan

This file defines how the project should continue without allowing infrastructure to displace the experience it exists to support.

The governing priority is:

1. help Fred understand and enjoy the armies, characters, choices and setting;
2. use current official Warhammer 40,000 evidence where rules or lore require it;
3. preserve continuity, provenance and uncertainty durably;
4. add repository machinery only when it materially protects or enables the first three goals.

## Experience-first rule

Repository work is infrastructure, not the main event.

When a task can be completed faithfully without adding new structure, do not add new structure merely because it is possible.

Prefer:
- clear army explanation over schema discussion;
- causal tactical teaching over rules transcription;
- faithful continuation over meta-commentary;
- durable plain-text/YAML records over extra software;
- useful progress over process narration.

Fred should not be made to supervise routine repository QA, source-routing, diffing, arithmetic, cross-reference checks or validation.

## Near-term continuation sequence

### 1. Build the 11th-edition system-rules layer

Add only the system records that connect multiple armies and multiple future questions:

- `Rules/11e/system/ARMY_CONSTRUCTION.yaml`
- `Rules/11e/system/MISSIONS.yaml`
- `Rules/11e/system/TERRAIN_AND_OBJECTIVES.yaml`
- `Rules/11e/system/SOURCE_AND_UPDATE_ROUTING.yaml`

These records should use current official Games Workshop sources and preserve dates, versions and scope.

They should explain permissions and consequences, not merely repeat rule text.

The preferred causal teaching chain is:

`mission -> battlefield condition -> available formation -> choice -> action -> consequence -> changed options`

### 2. Connect both army snapshots to system rules

Keep `FORCE-1985-V946` and `FORCE-3000` as separate historical roster snapshots.

Add references from their crosswalks to relevant system concepts such as:
- Force Disposition;
- Detachment Point budget;
- Leader/Support structure;
- objective role;
- terrain dependence;
- reserve/deployment function;
- Stratagem/Command Point interaction;
- play context.

Do not convert those references into fictional chronology.

### 3. Improve current datasheet coverage only where useful

Prioritize fields that materially affect:
- tactical choices;
- army legality;
- formation behavior;
- story-grounded explanation.

Do not fill every null merely to make records look complete.

Where a current Codex/app-only field cannot be verified from an available official source, preserve that distinction explicitly.

### 4. Use the live story as the experiential integration layer

Continue from the current House Montfort working-and-receiving chamber aboard the `True Meridian`.

The immediate social focus remains Fred's interest in understanding Justina and the conversation around Stratagem stewardship.

When rules learning naturally enters the scene, connect it to:
- who holds authority;
- what information is actually known;
- what choice is available;
- what resource or opportunity the choice consumes;
- what becomes possible or impossible afterward.

Do not turn the scene into a lecture or a disguised user test.

### 5. Maintain repository integrity as a quiet background function

After meaningful repository changes:
- run `python scripts/validate_repository.py`;
- use the GitHub Actions result as an independent structural check;
- repair failures rather than weakening checks;
- update source-routing and checksums when required.

Do not announce “complete,” “verified,” “current,” “legal,” “accepted,” or “ready” unless the relevant condition was actually checked.

## Symbolic-story protocol

Repository actions may inspire symbolic echoes in illustrative or later accepted fiction, but the software action and the fictional event are never the same thing.

The symbol should express the **function** of the action, not its literal technology.

### Preferred symbolic correspondences

| Repository action | Story symbol | Meaning carried |
| --- | --- | --- |
| retrieve an exact source | sealed dispatch, original warrant, witnessed ledger entry | recover what was actually said or supplied |
| checksum / byte verification | matched seal, serial mark, paired impression | identity of the artifact, not truth of its contents |
| authority routing | steward's ledger, jurisdictional seal, assigned lectern | who may answer which question |
| crosswalk / identifier linkage | compass bearing, waymark, indexed chart | one thing can be found from another without becoming identical to it |
| validation | inspection rite, cogitator green-mark, muster check | the chain is structurally intact |
| unresolved information | blank docket, open seal-space, unspent token | uncertainty is preserved rather than filled |
| current-rules update | newly dated order, amended tactical slate | present instruction changes without rewriting past action |
| preserved historical snapshot | archived battle slate, sealed muster roll | evidence of an earlier configuration |
| pull-request review | provisional course reviewed before commitment | a proposed change is examined before adoption |
| accepted merge to main | ratified record or confirmed chart revision | a repository change has become the current durable record, not fictional institutional merger |
| validation failure | rejected seal, misaligned tally, broken chain of references | something must be repaired before reliance |
| source-route failure | blocked archive door or failed signal path | one route failed; the source is not thereby proven absent |

Avoid using “merger” as a fictional symbol for repository merging when institutions or chains of command are involved. In this project, cooperation does not imply institutional fusion.

## Symbolism quality rules

Symbolism should be:
- perceptible but not explained to death;
- grounded in the current scene and characters;
- subordinate to character purpose;
- intelligible when heard aloud;
- precise enough to reward recognition without requiring repository knowledge.

Symbolism should not:
- make characters aware of GitHub, files, validators or AI tooling;
- give a character knowledge they have not received;
- manufacture Fred's dialogue, conclusion, attraction, consent or decision;
- turn a technical success into fictional canon;
- force every repository action into the next scene.

Use symbolism when it sharpens the lived experience. Omit it when it would feel contrived.

## Character-fit for symbolic functions

Use established character functions rather than arbitrary metaphors.

- Justina is especially suited to symbols of discernment, jurisdiction, evidence and the separation of observation from inference.
- Aurelia is especially suited to stewardship, household accounting, custody, negotiated authority and preservation of options.
- Constantia is especially suited to command, commitment, reserve, risk and the cost of spending limited resources.
- Eulalia is especially suited to interpretation, wording, precision and the relation between a statement and what it actually warrants.

These are narrative-use proposals constrained by established characterization. They do not create new biographies or relationships.

## Etymological diction for listening

Use etymology only where it clarifies a real distinction.

Preferred project distinctions include:

- **discern** — from Latin `discernere`, to separate or distinguish: useful for evidence versus inference.
- **authority** — from Latin `auctoritas`, connected with authorship, warrant and standing: useful for who is entitled to settle a question.
- **provenance** — from Latin/French roots meaning origin or coming-forth: useful for where a claim or artifact comes from.
- **mission** — from Latin `missio`, a sending: what the force is sent to accomplish.
- **strategy** — from Greek `strategia`, generalship: how the whole force intends to achieve the mission.
- **tactic** — from Greek `taktike`, the art of ordering or arrangement: the local action or arrangement used now.
- **disposition** — from Latin `disponere`, to arrange or set in order: useful for Force Disposition, not personality disposition.
- **valid** — from Latin `validus`, strong: something able to bear the weight placed upon it.
- **option** — from Latin `optare`, to choose: useful when explaining how spending a resource destroys one future choice to strengthen another present choice.

Do not use word origins as evidence about a person, faction or fictional motive.

## Story-and-repository rhythm

A good recurring rhythm is:

1. research or retrieve what is needed;
2. update the durable record if the result matters beyond the current answer;
3. validate the repository;
4. return to the experiential question;
5. when natural, let the next scene contain a symbolic echo of the function just performed.

This keeps the repository beneath the story rather than on top of it.

## Acceptance boundary

Illustrative symbolism stored under `Stories/Illustrative/` remains `PROPOSAL / A7`.

If Fred accepts an event, relationship development, name, institutional fact or other durable fictional consequence, record that accepted development separately in the appropriate continuity home. Do not infer acceptance from enjoyment, continuation, repository storage or symbolic resonance.
