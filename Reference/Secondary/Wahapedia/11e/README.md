# Wahapedia 11th-edition reference export

This directory is a secondary reference snapshot, not an authoritative Warhammer 40,000 rules source.

Snapshot timestamp from `Last_update.csv`: `2026-09-13 03:43:55`.

## Intended use

Use these files for discovery, cross-checking, structured lookup, source-location discovery, and change detection. A Wahapedia row can identify a candidate rule or source, but it cannot by itself make a repository claim `verified_current`.

Current official Games Workshop / Warhammer sources remain authoritative for current rules.

## Data model

The export is relational:

- `Datasheets.csv` is the datasheet anchor; its `id` is referenced as `datasheet_id` by the `Datasheets_*` tables.
- `Datasheets_abilities.csv` links datasheets to `Abilities.csv` through `ability_id`.
- `Datasheets_detachment_abilities.csv` links datasheets to `Detachment_abilities.csv`.
- `Datasheets_enhancements.csv` links datasheets to `Enhancements.csv`.
- `Datasheets_keywords.csv`, `Datasheets_models.csv`, `Datasheets_models_cost.csv`, `Datasheets_options.csv`, `Datasheets_unit_composition.csv`, and `Datasheets_wargear.csv` add keyword, model, cost, option, composition, and weapon data keyed by `datasheet_id`.
- `Datasheets_leader.csv` maps leader datasheet IDs to attachable datasheet IDs.
- `Detachments.csv` is keyed by Detachment `id`; `Detachment_abilities.csv`, `Enhancements.csv`, and `Detachments_chapter_dp.csv` link through Detachment IDs.
- `Factions.csv` maps faction IDs to names and Wahapedia routes.
- `Source.csv` maps source IDs to source metadata and, where supplied, official locators.
- `Last_update.csv` timestamps the exported snapshot.
- `Export Data Specs.xlsx` is the provider's binary specification workbook; prefer the CSV files for repository retrieval.

## Safety boundaries

- Do not infer that every row in `Source.csv` is current; it includes historical, prior-edition, Legends, and incomplete source records.
- Do not use this export to overwrite preserved roster evidence.
- Do not use a secondary-source disagreement to silently rewrite an official Games Workshop rule.
- When a current claim matters, route from this corpus to the controlling official source and record any unresolved discrepancy rather than choosing whichever wording is easier to retrieve.
