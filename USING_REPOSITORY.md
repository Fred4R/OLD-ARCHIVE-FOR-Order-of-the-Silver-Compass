# How to Use This Repository

This file explains how an AI or human should use the repository during a live conversation.

It is a workflow guide. It is not a canon source, a Warhammer rules source, or evidence that supersedes the records it routes to.

## Core principle

Use the repository to reduce Fred's burden, not to move repository administration into the conversation.

Retrieve the smallest authoritative record needed for the current task. Do not load, summarize, or narrate the whole repository merely because it exists.

The normal sequence is:

1. identify the task;
2. route to the authoritative record;
3. retrieve only what is needed;
4. distinguish source evidence, current rules, canon, inference, proposal and unresolved information;
5. answer or continue the story;
6. update the repository quietly afterward when the result matters beyond the current exchange.

## Fast routing by task

### Story continuation

Read:
1. `NEW_CONVERSATION.md`;
2. the current-focus section of `CONTINUATION.md`;
3. only the relevant continuation-critical portion of the preserved Compendium;
4. character or rules records only when the scene actually needs them.

Do not begin a story answer with a repository audit.

Do not repeat unchanged room geometry, cast lists or authority summaries unless the listener needs re-orientation.

If current rules enter the scene, verify them first and let them matter because a character has a real problem to solve.

### Current Warhammer 40,000 rules

Start at:
- `Rules/11e/SOURCE_INDEX.md`;
- then the matching record under `Rules/11e/units/`.

Check:
- source identity;
- publication/update date;
- verification status;
- whether the rule is reproduced in a public current source or remains Codex/app-only.

When the repository contains a historical or earlier-current rule, do not assume it is still current. Re-check official Games Workshop material when freshness matters.

### Army roster questions

For what Fred actually supplied:
- read the exact payload under `Sources/Armies/`.

For repository mappings:
- read the matching record under `Armies/`.

For current rules:
- use `Rules/11e/` separately.

Do not rewrite a historical roster merely because current points, keywords or rules changed.

### Canon, continuity and relationships

Read:
- `AUTHORITY.md`;
- `STATUS.md`;
- the relevant Compendium section;
- any later record that explicitly supersedes that field.

A proposal stored in the repository is still a proposal.

An illustrative story is not accepted history merely because Fred enjoyed it or continued chatting afterward.

### Personal identification

Use the methodology sources under `Sources/Methodology/` by function.

Do not turn ordinary conversation into a covert test.

Keep behavior, state, trait, motive, value, skill, self-concept, reputation, narrative identity and interpretation distinct.

### Repository maintenance

For a meaningful durable change:

1. branch from current `main`;
2. make the smallest useful change;
3. update routing and checksums only where necessary;
4. open a pull request;
5. require the repository validator to pass;
6. repair failures rather than weakening the validator;
7. merge the tested tree;
8. re-fetch `main`;
9. require the post-merge validation run to pass before claiming the durable update succeeded.

## Listening-first use

Fred often listens rather than scans.

The repository should therefore improve spoken comprehension rather than encourage report-shaped answers.

For story:
- tell one coherent scene before giving repository notes;
- do not mix tables, source ledgers, status labels or file paths into the scene;
- orient fully on entry or meaningful change, not every few paragraphs;
- let characters pursue their own goals rather than taking turns teaching Fred;
- make a rule part of the causal problem: purpose -> choice -> action -> consequence -> changed options;
- stop before Fred's dialogue or decision when his agency is required;
- allow implication and inference instead of explaining every meaning after the dialogue;
- use names when pronouns would be ambiguous by ear;
- keep individual voices different in method and cadence, not merely in topic.

For explanatory answers intended for listening:
- prefer connected prose over large tables;
- use short conceptual units;
- introduce a rule before its exceptions;
- explain the practical consequence immediately;
- avoid long nested lists unless Fred asks for them.

## Etymology

Use etymology as precision, not decoration.

Prefer the exact word whose history sharpens a distinction. Explain the word origin only when it materially helps the present idea.

Do not interrupt a scene repeatedly for word histories.

Do not use a name's etymology as evidence for personality, motive, destiny, holiness or tactical role.

## Unnamed characters and naming

Naming unresolved characters can improve listening and character differentiation, but names must not be smuggled into canon.

Preferred process:

1. research the naming range of the relevant official faction or culture;
2. propose one or a few names that fit that range;
3. explain uncertain etymology honestly and briefly;
4. introduce at most one or two new names in a scene when the character has a reason to be addressed;
5. treat the name as `PROPOSAL` until Fred explicitly accepts it or later conversation provides adequate adoption evidence;
6. record acceptance separately from the original proposal.

For the current chamber:
- the three Silver Compass Paragon pilots remain unnamed in established canon;
- the Helverin pilot's personal name remains unresolved;
- `Sabine` is Fred's later wording for the Warhound Princeps but formal naming acceptance remains unresolved.

## Current immediate focus

The next conversation should favor experience over architecture.

Current focus:
- Canoness Constantia Serenitas as Warlord;
- Army of Faith;
- Miracle-dice stewardship;
- the real tactical choices produced by Army of Faith;
- gradual differentiation and possible naming of currently unnamed women.

Before giving precise current Army of Faith Stratagem wording, retrieve the current official Codex/app or another authoritative current Games Workshop route when available.

Public official evidence already supports:
- Army of Faith remains a valid Codex Detachment in 11th edition unless separately updated;
- Sacred Rites allows a unit to perform a second Act of Faith in the same phase;
- the current Faction Pack changes Miracle-die generation;
- the current MFM supplies the Detachment Point cost, Force Disposition and current enhancement costs recorded in the Sororitas rules crosswalk.

Do not promote a secondary-source Stratagem list to `verified_current` merely because multiple indexes agree.

## Story failure pattern to avoid

Direct user feedback on 2026-09-13: the prior planning response "sucks to listen to."

The failure was not lack of information. It was poor integration.

Avoid:
- research memo + story pasted together;
- large rules tables before the scene;
- repeated spatial recitation;
- repository vocabulary inside fiction;
- characters functioning mainly as lecturers;
- frequent etymology interruptions;
- narrator explanation after every meaningful line;
- excessive status/provenance caveats during an emotional moment.

Preferred pattern:

`scene problem -> character purpose -> rule becomes necessary -> choice -> consequence -> brief after-scene source/update note`

## What a fresh conversation should feel like

A new chat should not feel like a reset or an audit.

It should recover the relevant state, answer Fred's immediate request, and continue.

The repository is successful when Fred can speak naturally and the system does the retrieval, verification, continuity work and maintenance underneath the experience.
