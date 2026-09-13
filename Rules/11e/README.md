# Warhammer 40,000 11th-edition rules crosswalk

Read `../../AUTHORITY.md` for repository-wide authority and supersession.

This directory connects Silver Compass roster records to current official Warhammer 40,000 rules sources without rewriting historical roster evidence.

## Authority scope

This directory governs only the current-rules fields that its records explicitly verify from current official Games Workshop/Warhammer sources.

It may narrowly supersede older Compendium rules statements for those verified fields. It does not supersede:
- historical roster payloads or snapshot costs;
- project canon, character identity, relationships, or story chronology;
- unresolved fields;
- the current official Games Workshop source itself.

## Resolution order

When answering an army, unit, tactics, or story-context question:

1. Resolve the roster occurrence, such as `FORCE-1985-V946/F1985-01`.
2. Resolve the stable project unit identifier, such as `UNIT-CANONESS`.
3. Resolve the 11th-edition rules identifier, such as `11E-SOB-CANONESS`.
4. Use only current official data whose source and verification status are recorded.
5. Resolve a project character mapping only when project continuity separately establishes it.

These are different relations. A roster occurrence is not a datasheet; a datasheet is not a character biography; roster presence is not story-scene presence.

## 11th-edition game fields

Current 11th-edition datasheets use model characteristics `M`, `T`, `SV`, `W`, `LD`, and `OC`; weapon profiles use `RANGE`, `A`, `BS` or `WS`, `S`, `AP`, and `D`. Datasheets also carry abilities, keywords, faction keywords, wargear, unit composition, and attachment or transport rules where applicable.

The crosswalk preserves those Games Workshop concepts. It does not invent a parallel rules vocabulary.

## Verification states

- `verified_current` — a current official source was actually inspected.
- `partially_verified_current` — an official source confirms only part of the record.
- `not_yet_verified` — no current official source was successfully retrieved for that field.
- `blocked_current_source` — the authoritative live source was identified but could not be retrieved through the available route.

Historical export points and current points are separate fields. A later rules change does not rewrite an earlier roster snapshot.

## Connected forces

- `FORCE-1985-V946`: exact source `../../Sources/Armies/FORCE-1985-V946.txt`; Appendix C remains the embedded copy.
- `FORCE-3000`: exact source `../../Sources/Armies/FORCE-3000.txt`; Appendix B remains the embedded copy.

The two forces are separate roster snapshots, not automatically sequential moments in fiction.

Current rules records now cover the relevant Adepta Sororitas, Imperial Agents, Imperial Knights, and Adeptus Titanicus unit identities. Missing current fields remain explicitly unverified rather than inferred.
