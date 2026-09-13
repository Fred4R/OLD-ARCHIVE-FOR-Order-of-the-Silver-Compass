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
| Preserved Silver Compass baseline, continuity, people, relationships, unresolved boundaries, historical roster snapshots | `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt` | Preserved baseline candidate. Its own `REVIEW_STATUS: REVISED CANDIDATE — user acceptance not established` remains in force. |
| Exact FORCE-1985-V946 source payload | `Sources/Armies/FORCE-1985-V946.txt` | Standalone immutable source artifact. Appendix C remains a preserved embedded copy of the same payload. It is not current legality or fictional chronology. |
| FORCE-1985-V946 repository crosswalk | `Armies/Order-of-the-Silver-Compass/FORCE-1985-V946.yaml` | Maps roster occurrences to project unit IDs, rules IDs, and explicitly scoped project identities. It does not replace the exact source artifact. |
| Exact FORCE-3000 source payload | `Sources/Armies/FORCE-3000.txt` | Standalone immutable source artifact. Appendix B remains the preserved embedded copy. It is not current legality or fictional chronology. |
| FORCE-3000 repository crosswalk | `Armies/Order-of-the-Silver-Compass/FORCE-3000.yaml` | Maps the House Montfort 3,000-point roster to project unit IDs, rules IDs, and explicitly scoped project identities. It does not replace the exact source artifact. |
| Current 11th-edition findings | `Rules/11e/SOURCE_INDEX.md` plus the matching record under `Rules/11e/units/` | Governs only fields actually verified from current official Games Workshop/Warhammer sources. |
| Current official Warhammer lore/rules | Current Games Workshop/Warhammer primary source | Repository records verification and routing; they do not outrank the official source. |
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
2. use the matching rules record;
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

When a conversation supplies or corrects a durable project fact, preserve the fact in the appropriate authoritative home with its evidence class and scope. Do not rely on conversational memory as the only durable record.

## Maintenance

The repository exists to preserve and route meaning, not to create maintenance work for Fred. Routine source routing, cross-reference checking, arithmetic, diffing, provenance checks, and integrity checks should normally be handled by the assistant.


## Validator authority boundary

`scripts/validate_repository.py` enforces repository invariants: hashes, parseability, reference resolution, arithmetic, source routing, and category separation.

Its result is **structural**, not substantive. A passing run does not supersede the Compendium, official Games Workshop sources, original methodology sources, direct user evidence, or unresolved project boundaries. The validator may reject a malformed record; it may not invent the fact that would make the record pass.
