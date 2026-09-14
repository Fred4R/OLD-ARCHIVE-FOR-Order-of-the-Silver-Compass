# Repository Authority and Supersession

This file defines which repository record governs which kind of question.

Authority, evidence, and status are separate.

- **Authority** identifies the record that governs a defined scope.
- **Evidence** identifies what supports a claim and how it was obtained.
- **Status** identifies the claim's project standing.

There is no universal ranking for every question. Identify the question type first, then use the authoritative home for that scope.

## Current authoritative homes

| Question | Authoritative home | Scope and limit |
| --- | --- | --- |
| Repository routing and supersession | `AUTHORITY.md` | Controls repository routing only. It does not create fictional canon or game rules. |
| Canon/evidence terminology | `STATUS.md` together with preserved Compendium Section 0C | Canon status and evidence class remain separate. |
| Source routing | `SOURCES.md` | Points to source families; it does not replace them. |
| Current operational continuity and cold-start live state | `CURRENT_STATE.md` | Governs the current scene pointer, immediate focus and continuation-critical operational state. It is a derived routing/continuity kernel, not independent evidence; underlying factual claims remain controlled by their cited source records. |
| Structured current scene staging | `Story/CURRENT_SCENE.yaml` | Derived companion for current location, participant-count safeguards, immediate lived beat and explicitly unresolved spatial state. `CURRENT_STATE.md` remains the controlling operational pointer. |
| Durable story event and waymark index | `Story/EVENTS.yaml` | Governs only the event chronology explicitly extracted there. It preserves underlying evidence class and does not upgrade inherited acceptance. |
| Explicit story knowledge state | `Story/KNOWLEDGE.yaml` | Governs only who-knows-what claims explicitly extracted there. Absence from this registry is not proof that a person lacks knowledge. |
| Conversational adoption and durable writeback | `Story/ACCEPTANCE.md` | Controls how user-authored statements/actions may adopt or correct assistant-proposed story facts before repository writeback. It does not create acceptance by itself. |
| Fred user continuity and agency boundary | `Characters/Fred.md` | Narrow durable home for project-relevant user-authored role, knowledge, stated goals and agency limits. It is not a personality profile and cannot replace Fred's current direct statements. |
| Principal character continuity | `Characters/*` continuity records listed in `Characters/README.md` | Narrow derived homes for extracted durable person facts and unresolved boundaries. They do not upgrade the preserved evidence. `Characters/Constantia-Serenitas.md` remains a separate A6 simulation guide rather than a continuity authority. |
| Durable relationship state | `Relationships/RELATIONSHIPS.md` | Governs extracted interpersonal, knowledge, functional and institutional relations explicitly recorded there. It does not create private motives, attraction, consent or history not supported by the underlying evidence. |
| Preserved Silver Compass baseline evidence, inherited continuity, unresolved boundaries and historical roster snapshots | `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt` | Preserved baseline candidate and underlying evidence reservoir. Its own `REVIEW_STATUS: REVISED CANDIDATE — user acceptance not established` remains in force. Extracted character and relationship records may become narrower retrieval homes without upgrading this evidence. |
| Constantia lore-grounded simulation guidance | `Characters/Constantia-Serenitas.md` | `INTERPRETATION / A6` portrayal guide. It combines established Constantia facts, preserved roster structure and verified official lore/rules to guide simulation; it does not create biography, relationships, miracle causation or accepted canon. |
| Exact FORCE-1985-V946 source payload | `Sources/Armies/FORCE-1985-V946.txt` | Standalone immutable source artifact. Appendix C remains a preserved embedded copy of the same payload. It is not current legality or fictional chronology. |
| FORCE-1985-V946 repository crosswalk | `Armies/Order-of-the-Silver-Compass/FORCE-1985-V946.yaml` | Maps roster occurrences to project unit IDs, rules IDs, explicitly scoped project identities, and bounded current-system references. System links support current interpretation; they do not replace the exact source artifact or certify whole-list legality. |
| Exact FORCE-3000 source payload | `Sources/Armies/FORCE-3000.txt` | Standalone immutable source artifact. Appendix B remains the preserved embedded copy. It is not current legality or fictional chronology. |
| FORCE-3000 repository crosswalk | `Armies/Order-of-the-Silver-Compass/FORCE-3000.yaml` | Maps the House Montfort 3,000-point roster to project unit IDs, rules IDs, explicitly scoped project identities, and bounded current-system references. System links do not certify a current 3,000-point construction row, whole-list legality, or fictional chronology. |
| Current 11th-edition findings | `Rules/11e/SOURCE_INDEX.md` plus the matching record under `Rules/11e/system/`, `Rules/11e/units/`, or `Rules/11e/detachments/` | Governs only fields actually verified from current official Games Workshop/Warhammer sources. System records govern shared construction and source-routing fields; unit records govern datasheet-specific fields; Detachment records govern Detachment-specific fields such as Detachment Points, Force Disposition, Enhancements, Stratagems and Detachment rules. |
| Current official Warhammer lore/rules | Current Games Workshop/Warhammer primary source | Repository records verification and routing; they do not outrank the official source. |
| Secondary Warhammer discovery reference | `Reference/Secondary/Wahapedia/README.md` and its `11e/` dataset | Discovery, comparison, indexing and coverage checks only. It cannot establish `verified_current`, supersede Games Workshop/Warhammer, or create project continuity. |
| Human-evidence methodology | Original PDFs under `Sources/Methodology/` | These sources govern the scientific constructs and limits they actually support. `Sources/Methodology/REVIEW_STATUS.md` governs only the later review-completion state. |
| Repository structural integrity | `scripts/validate_repository.py` plus `.github/workflows/validate-repository.yml` | Checks repository invariants and provenance wiring. A pass does not establish truth, canon acceptance, or current game legality. |
| Workflow state | GitHub issues, pull requests, commits, and branches | Workflow only; not Silver Compass canon merely because it exists or is merged. |

## Preserved Compendium and later repository records

The v4.3.41 Compendium is a preserved baseline candidate. Do not silently rewrite it to make later repository work appear contemporaneous with its audit.

Newer repository records may supplement it or narrowly supersede it.

A later record supersedes an earlier record only for the field or question it explicitly controls. Preserve older immutable evidence.

Examples:
- a current rules record can supersede an older rules statement for one named rule, keyword, points value, or legality field;
- an army crosswalk can add a repository mapping without changing historical roster bytes;
- a later correction can supersede an earlier project claim only within the scope actually corrected.

A newer repository record does not automatically supersede unrelated continuity, relationship state, historical source snapshots, institutional authority, fictional chronology, or a source artifact's exact wording.

## Supersession contract

When a durable record changes an earlier answer, record these elements where relevant:

- `record_id` — stable identity;
- `record_type` — source snapshot, crosswalk, rules finding, continuity record, interpretation, or another defined type;
- `canon_status` — project standing when a project-canon claim is made;
- `evidence_class` — A1, A1-REPORTED, A2, A3, A4, A5, A6, A7, or A8 when applicable;
- `verification_status` — whether an external or current claim was actually checked;
- `as_of` — date or temporal scope for time-sensitive claims;
- `supersedes_for` — exact field or question the newer record controls;
- `does_not_supersede` — boundaries that remain unchanged.

Do not place an evidence class such as `A1` in a canon-status field. Do not use a record type such as `SOURCE_SNAPSHOT` as though it were a canon status.

## Conflict procedure

When records disagree:

1. determine whether they answer the same question;
2. identify each record's authority scope, evidence class, date, and status;
3. apply an explicit scoped correction or supersession if one exists;
4. preserve older immutable evidence;
5. if the conflict remains, mark it `UNRESOLVED`;
6. do not invent an event, relationship, motive, chronology, ownership change, casualty, departure, arrival, rearmament, or rules result merely to make records agree.

## Current-rules procedure

For a current Warhammer 40,000 question:

1. start at `Rules/11e/SOURCE_INDEX.md`;
2. use the matching unit record under `Rules/11e/units/` for datasheet questions or the matching Detachment record under `Rules/11e/detachments/` for Detachment-specific questions;
3. inspect source and verification status;
4. if a field is missing, `not_yet_verified`, or `blocked_current_source`, retrieve the current official source if possible;
5. do not substitute a historical roster value or inherited rules claim and call it current.

## Army-list procedure

For an army-list question:

1. identify the exact force snapshot;
2. use its immutable source payload under `Sources/Armies/` for what was supplied; if no standalone artifact exists yet, use the preserved exact appendix identified by the crosswalk;
3. use the `Armies/` record for normalized repository mappings;
4. use `Rules/11e/` for current rules only where separately verified;
5. use project continuity for fictional identities and relationships only where separately established.

Roster presence is not story presence. Roster difference is not fictional chronology.

## Durable conversational changes

A chat statement does not become durable project canon merely because it appeared in conversation.

Use `Story/ACCEPTANCE.md` to determine whether user-authored material explicitly accepts, minimally adopts, corrects, or leaves assistant narration unresolved. Silence, a generic request to continue, and a repository merge do not by themselves establish fictional canon.

When a conversation supplies or corrects a durable project fact, preserve the smallest fact actually established in the appropriate authoritative home with its evidence class and scope. Update derived story registries only where their scope changes, and update `CURRENT_STATE.md` last when the operational pointer changes. Do not rely on conversational memory as the only durable record.

## Maintenance

The repository exists to preserve and route meaning, not to create maintenance work for Fred. Routine source routing, cross-reference checking, arithmetic, diffing, provenance checks, and integrity checks should normally be handled by the assistant.


## Validator authority boundary

`scripts/validate_repository.py` enforces repository invariants: hashes, parseability, reference resolution, arithmetic, source routing, and category separation.

Its result is **structural**, not substantive. A passing run does not supersede the Compendium, official Games Workshop sources, original methodology sources, direct user evidence, or unresolved project boundaries. The validator may reject a malformed record; it may not invent the fact that would make the record pass.

