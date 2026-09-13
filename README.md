# Order of the Silver Compass

This repository is the durable home for the Order of the Silver Compass project.

## What matters most

The project exists to support Fred's Warhammer 40,000 experience: armies, lore, characters, relationships, identification, continuity, and immersive fiction.

GitHub is storage and version history. It is not the meaning of the project.

## Start here

For a fresh conversation, begin with `NEW_CONVERSATION.md`.

Use `USING_REPOSITORY.md` for the practical task-routing and conversation workflow. It explains how to retrieve the minimum necessary context without turning the repository itself into the user experience.

1. Read `USING_REPOSITORY.md` for practical task routing and live-conversation use.
2. Read `AUTHORITY.md` to determine which record governs which question and what can supersede what.
3. Read `STATUS.md` before treating any statement as accepted canon.
4. Read `SOURCES.md` to route source questions.
5. Use `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt` as the preserved baseline candidate, with its stated review limits intact.
6. Read `AGENTS.md` for short instructions to future AI systems.
7. Read `CONTINUATION.md` for the experience-first continuation sequence and symbolic-story protocol.
8. Use `Sources/Armies/` for immutable extracted army-list source payloads.
9. Use `Armies/` for durable army-list crosswalks and roster-to-project mappings.
10. Use `Rules/11e/` for current 11th-edition source routing and verified rules findings.
11. Use `Stories/Illustrative/` for immersive A7/PROPOSAL scenes that are explicitly not accepted history merely because they are stored.

## Authority rule

A later repository record supersedes an earlier record only for the field or scope it explicitly controls. Historical evidence is preserved.

Army exports, current rules, and project continuity answer different questions:
- exact roster evidence preserves what was supplied;
- `Armies/` maps roster occurrences into the repository;
- `Rules/11e/` records current official rules only where actually verified;
- the preserved Compendium carries the baseline continuity and project-state record that has not been explicitly superseded.

Roster presence does not itself establish story presence, ownership, biography, casualty, reinforcement, rearmament, or chronology.

Connected army references:
- `Armies/Order-of-the-Silver-Compass/FORCE-1985-V946.yaml`
- `Armies/Order-of-the-Silver-Compass/FORCE-3000.yaml`

Their exact extracted source payloads live under `Sources/Armies/`.

## Current migration state

The preserved MASTER identifies itself as:

**REVISED CANDIDATE — user acceptance not established.**

Repository migration does not convert that candidate status into user acceptance.

The repository should remain simple. Add software, schemas, automation, databases, frameworks, or extra services only when a concrete need demonstrates that plain portable files are inadequate.


## Validate repository integrity

Run:

`python scripts/validate_repository.py`

Install the single validator dependency first with:

`python -m pip install --requirement requirements-validator.txt`

GitHub Actions also runs the same validator automatically on pull requests and on pushes to `main` through `.github/workflows/validate-repository.yml`.

The validator checks repository mechanics: tracked-file SHA-256 coverage, canonical Compendium identity, YAML syntax and duplicate keys, authority/status/evidence separation, army arithmetic, exact source payload hashes, project/rules/source identifiers, roster-occurrence links, and provenance for current-rule claims.

A passing validation is not a lore-truth certificate, user acceptance, current army-legality certificate, or proof that unresolved information has become resolved.
