# Instructions for AI systems

This is a provenance-controlled Warhammer 40,000 project repository.

Read `AUTHORITY.md`, `README.md`, `STATUS.md`, and `SOURCES.md` before substantive work.

Use `AUTHORITY.md` to determine which record governs the question. Do not assume that a newer file supersedes an older one outside its stated scope.

Use `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt` for continuation-critical baseline continuity that has not been explicitly superseded. Preserve its candidate review status and unresolved boundaries.

For army questions, use the exact source payload under `Sources/Armies/` when one exists, then resolve the corresponding crosswalk under `Armies/`. For current Warhammer 40,000 rules questions, route through `Rules/11e/SOURCE_INDEX.md` and the matching rules record before making current stats, keyword, ability, attachment, points, or legality claims.

Keep distinct:
- authority scope;
- record type;
- canon status;
- evidence class;
- verification status;
- exact source evidence;
- preserved army-list snapshots;
- current official Warhammer lore/rules;
- established project canon/design;
- human evidence;
- inference/interpretation;
- proposal;
- unresolved information.

Never fill `UNRESOLVED` by invention.

Do not infer ownership, biography, relationships, chronology, casualty, reinforcement, rearmament, or institutional authority merely from co-presence in a roster or scene.

A roster occurrence, a datasheet identity, and a project character mapping are different relations. Current rules can update how a datasheet functions without rewriting the historical roster that contained it.

For identification, distinguish behavior, state, trait/disposition, motive/goal, value, skill/ability, self-concept/identity, reputation, narrative identity, and interpretation.

For army teaching, connect:
1. what the unit officially is;
2. what current verified rules permit;
3. what the preserved roster actually contains;
4. what separate project continuity establishes;
5. what that means tactically or in a lived scene.

Explain tactics causally: threat or formation -> choice -> action -> consequence -> changed options.

For storytelling, preserve Fred's agency and character knowledge boundaries.

For repository work, prefer plain portable files and minimal dependencies. Verify writes and repository state before claiming success. If a current official rules source cannot be retrieved, mark the field unresolved or not yet verified rather than substituting an older rule or unsupported secondary claim.


## Repository validation

After changing repository structure, army crosswalks, rules records, authority routing, source artifacts, or checksum coverage, run:

`python scripts/validate_repository.py`

Do not claim the repository is structurally valid until that command passes against the actual committed tree. GitHub Actions runs the same check on pull requests and pushes to `main`.

The validator is a structural guard. It does not promote proposals to canon, resolve `UNRESOLVED`, certify whole-list legality, or replace source review.
