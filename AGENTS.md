For a fresh conversation, read `NEW_CONVERSATION.md` first. It is a routing handoff, not a canon source.

Read `USING_REPOSITORY.md` next. It defines the practical retrieval workflow and how to keep repository mechanics beneath the user experience.

# Instructions for AI systems

This is a provenance-controlled Warhammer 40,000 project repository.

Read `AUTHORITY.md`, `README.md`, `STATUS.md`, and `SOURCES.md` before substantive work.

Use `AUTHORITY.md` to determine which record governs the question. Do not assume that a newer file supersedes an older one outside its stated scope.

Use `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt` for continuation-critical baseline continuity that has not been explicitly superseded. Preserve its candidate review status and unresolved boundaries.

For army questions, use the exact source payload under `Sources/Armies/` when one exists, then resolve the corresponding crosswalk under `Armies/`. For current Warhammer 40,000 rules questions, route through `Rules/11e/SOURCE_INDEX.md`, then use the matching unit record under `Rules/11e/units/` or Detachment record under `Rules/11e/detachments/` before making current stats, keyword, ability, attachment, Detachment, Enhancement, Stratagem, points, or legality claims.

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

For storytelling, preserve Fred's agency and character knowledge boundaries. Illustrative fiction stored under `Stories/Illustrative/` must remain `PROPOSAL` / `A7` unless later accepted through the proper continuity process.

For repository work, prefer plain portable files and minimal dependencies. Verify writes and repository state before claiming success. If a current official rules source cannot be retrieved, mark the field unresolved or not yet verified rather than substituting an older rule or unsupported secondary claim.

For meaningful repository changes, follow the merge contract in `USING_REPOSITORY.md`: one coherent task, current-`main` baseline, explicit scope and evidence, smallest useful diff, pull request, structural validation, semantic diff review, exact-head merge, and post-merge verification. Normally squash-merge one conceptual task. Never use a Git merge to resolve an evidential uncertainty.


## Repository validation

After changing repository structure, army crosswalks, rules records, authority routing, source artifacts, or checksum coverage, run:

`python scripts/validate_repository.py`

Do not claim the repository is structurally valid until that command passes against the actual committed tree. GitHub Actions runs the same check on pull requests and pushes to `main`.

The validator is a structural guard. It does not promote proposals to canon, resolve `UNRESOLVED`, certify whole-list legality, or replace source review.


## Continuation planning

For substantial continuation, read `CONTINUATION.md`. It keeps story and army understanding ahead of infrastructure and defines how repository work may be echoed symbolically without becoming canon.

## Listening-first response discipline

Fred often listens rather than scans. When the request is story-oriented, do not answer with a research memo followed by fiction.

Use the repository internally, then tell one coherent scene. Keep tables, file paths, provenance labels and repository operations outside the scene. Re-orient only when something changes. Let characters pursue their own purposes. Make rules necessary to a choice and consequence. Use etymology sparingly. Do not explain every implication after the dialogue has already conveyed it.

Direct feedback on 2026-09-13 identified the opposite pattern as unpleasant to listen to. Treat this as an interface correction and regression safeguard.

When proposing names for unresolved characters, use official faction naming range and accurate etymology, but do not infer personality from a name and do not promote a proposed name to canon without acceptance evidence.
