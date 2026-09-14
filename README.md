# Order of the Silver Compass

This repository is the durable home for the Order of the Silver Compass project.

## What matters most

The project exists to support Fred's Warhammer 40,000 experience: armies, lore, characters, relationships, identification, continuity, and immersive fiction.

GitHub is storage and version history. It is not the meaning of the project.

## Start here

For a fresh conversation, begin with `CURRENT_STATE.md`.

It is the compact operational continuity kernel. It tells a fresh system where the project is now and routes deeper retrieval without requiring the whole repository to be read first.

`CURRENT_STATE.md` is also the cold-start handoff. Use `USING_REPOSITORY.md` for maintenance and repository workflow.

Retrieve other records only when the task needs them:
- `AUTHORITY.md` and `STATUS.md` for authority, canon/evidence status, conflict and supersession;
- `Story/` for structured current scene staging, durable event chronology, explicit knowledge state, and conversational adoption/writeback rules;
- `Characters/` for extracted durable principal-person continuity, including the bounded `Characters/Fred.md` user-continuity record;
- `Relationships/RELATIONSHIPS.md` for durable interpersonal and functional relation state;
- `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt` for preserved baseline continuity and evidence not yet migrated into a narrower durable home;
- `Sources/Armies/` for immutable army-list source payloads;
- `Armies/` for roster-to-project mappings;
- `Rules/11e/` for current 11th-edition source routing and verified findings;
- `Reference/Secondary/Wahapedia/` for secondary discovery/comparison only, never current authority;
- `Sources/Methodology/` for human-evidence methodology;

## Authority rule

A later repository record supersedes an earlier record only for the field or scope it explicitly controls. Historical evidence is preserved.

`CURRENT_STATE.md` governs the current operational pointer and cold-start live state. It does not replace the evidence underlying those facts.

Army exports, current rules, and project continuity answer different questions:
- exact roster evidence preserves what was supplied;
- `Armies/` maps roster occurrences into the repository;
- `Rules/11e/` records current official rules only where actually verified;
- the preserved Compendium carries baseline continuity and project-state evidence that has not been explicitly superseded or migrated into a narrower authoritative home.

Roster presence does not itself establish story presence, ownership, biography, casualty, reinforcement, rearmament, or chronology.

## Current migration state

The preserved MASTER identifies itself as:

**REVISED CANDIDATE — user acceptance not established.**

Repository migration does not convert that candidate status into user acceptance.

The first operational extraction is now separate in `CURRENT_STATE.md`. The MASTER remains preserved rather than silently rewritten.

The repository should remain simple. Add software, schemas, automation, databases, frameworks, or extra services only when a concrete need demonstrates that plain portable files are inadequate.

## Validate repository integrity

Run:

`python scripts/validate_repository.py`

Install the single validator dependency first with:

`python -m pip install --requirement requirements-validator.txt`

GitHub Actions runs the same validator on pull requests and on pushes to `main`.

The validator checks repository mechanics. A passing validation is not a lore-truth certificate, user acceptance, current army-legality certificate, or proof that unresolved information has become resolved.
