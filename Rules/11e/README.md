# Warhammer 40,000 11th-edition rules crosswalk

Read `../../AUTHORITY.md` for repository-wide authority and supersession.

This directory provides the current universal 11th-edition system layer and connects Silver Compass roster records to current official Warhammer 40,000 rules sources without rewriting historical roster evidence.

## Authority scope

This directory governs only the current-rules fields that its records explicitly verify from current official Games Workshop/Warhammer sources.

It may narrowly supersede older Compendium rules statements for those verified fields. It does not supersede:
- historical roster payloads or snapshot costs;
- project canon, character identity, relationships, or story chronology;
- unresolved fields;
- the current official Games Workshop source itself.

## Universal 2,000-point entry point

For a question about the rules or structure shared by any standard current 2,000-point game, start with `system/STRIKE_FORCE_2000.yaml`.

That record is deliberately faction-neutral. It routes universal Strike Force construction, mission, terrain/objective and current-Core-Rules questions without importing Sororitas rules, another faction's rules, a roster, or project-character assumptions. Faction and datasheet records are consulted only after the universal layer when the question actually requires them.

## Resolution order

When answering an army, unit, tactics, or story-context question:

1. Resolve the roster occurrence, such as `FORCE-1985-V946/F1985-01`.
2. Resolve the stable project unit identifier, such as `UNIT-CANONESS`.
3. Resolve the 11th-edition unit rules identifier, such as `11E-SOB-CANONESS`, when the question concerns a datasheet.
4. Resolve the matching record under `detachments/` when the question concerns a Detachment, Enhancement, Stratagem, Detachment Point cost or Force Disposition.
5. Use only current official data whose source and verification status are recorded.
6. Resolve a project character mapping only when project continuity separately establishes it.

These are different relations. A roster occurrence is not a datasheet; a datasheet is not a character biography; roster presence is not story-scene presence.

## 11th-edition game fields

Current 11th-edition datasheets use model characteristics `M`, `T`, `SV`, `W`, `LD`, and `OC`; weapon profiles use `RANGE`, `A`, `BS` or `WS`, `S`, `AP`, and `D`. Datasheets also carry abilities, keywords, faction keywords, wargear, unit composition, and attachment or transport rules where applicable.

The crosswalk preserves those Games Workshop concepts. It does not invent a parallel rules vocabulary.

## Secondary discovery reference

`../../Reference/Secondary/Wahapedia/11e/` is available as a secondary, non-authoritative discovery and comparison corpus. Its governing note is `../../Reference/Secondary/Wahapedia/README.md`.

Use it to locate candidate fields, compare coverage, or identify questions that require official verification. Do not use it by itself to set `verified_current`, fill `not_yet_verified` or `blocked_current_source`, supersede Games Workshop/Warhammer, or create project continuity.

The normal rules route remains official-source first: resolve the exact field through `SOURCE_INDEX.md` and the matching system, unit, or Detachment record, then consult the controlling current official source when needed.

## Verification states

- `verified_current` — a current official source was actually inspected.
- `partially_verified_current` — an official source confirms only part of the record.
- `not_yet_verified` — no current official source was successfully retrieved for that field.
- `blocked_current_source` — the authoritative live source was identified but could not be retrieved through the available route.

Historical export points and current points are separate fields. A later rules change does not rewrite an earlier roster snapshot.

## Detachment records

Detachment-specific current rules live under `detachments/`. They preserve Codex origin, current-edition carry-forward, current amendments, construction values and verification boundaries without duplicating those fields inside character or unit records.

Current connected record:
- `detachments/Adepta-Sororitas/Army-of-Faith.yaml`

## Connected forces

- `FORCE-1985-V946`: exact source `../../Sources/Armies/FORCE-1985-V946.txt`; Appendix C remains the embedded copy.
- `FORCE-3000`: exact source `../../Sources/Armies/FORCE-3000.txt`; Appendix B remains the embedded copy.

The two forces are separate roster snapshots, not automatically sequential moments in fiction.

Current rules records now cover the relevant Adepta Sororitas, Imperial Agents, Imperial Knights, and Adeptus Titanicus unit identities. Missing current fields remain explicitly unverified rather than inferred.


## System-rules layer

Shared current rules concepts live under `system/`.

Current records:
- `system/STRIKE_FORCE_2000.yaml` — faction-neutral entry point for universal current 2,000-point Strike Force questions;
- `system/ARMY_CONSTRUCTION.yaml` — current verified army-construction structure;
- `system/BATTLE_SEQUENCE.yaml` — battle rounds, player turns, phases and Command-phase/Core-CP sequence;
- `system/BATTLE_SHOCK_AND_ACTIONS.yaml` — leadership, battle-shock and verified action/OC/Stratagem consequences;
- `system/MOVEMENT_AND_RESERVES.yaml` — Movement-phase structure, move-type routing and high-level ingress/reserve structure;
- `system/SHOOTING.yaml` — Shooting-phase structure and verified shooting-type/normal-shooting fields;
- `system/COMBAT.yaml` — Engagement Range, charge timing and high-level Fight-phase structure;
- `system/MISSIONS.yaml` — current shared mission generation, event/casual distinctions and scoring boundaries;
- `system/TERRAIN_AND_OBJECTIVES.yaml` — current terrain/objective interaction with explicit time-sensitive layout boundaries;
- `system/SOURCE_AND_UPDATE_ROUTING.yaml` — current official-source routing and update discipline.

Both preserved army crosswalks already link to shared system records where applicable. Those links support current interpretation without rewriting historical roster evidence or certifying whole-list legality.

System records must use current official Games Workshop evidence. They connect rules structure across armies without turning rules structure into fictional chronology.

The universal Core Rules extraction is intentionally incomplete where the exact current 2026 text was not successfully inspected. In particular, the complete Making Attacks procedure, full Transport procedure, exact Core Stratagem list and full common-ability catalogue remain gated to the current official Core Rules. Do not backfill those fields from 10th-edition quick-start material or model memory.
