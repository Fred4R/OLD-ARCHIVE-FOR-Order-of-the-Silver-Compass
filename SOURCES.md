# Source Routing

Use sources by function rather than treating any one source as universally authoritative.

For precedence and supersession, read `AUTHORITY.md`.

## Silver Compass project material

The preserved baseline candidate is:

- `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt`
- SHA-256: `5d112c261a9726e6a67afc19d509a0353cedfec5a624f3a72a5ea951c06ea37a`
- Internal review status: `REVISED CANDIDATE — user acceptance not established`

Use that preserved Compendium for baseline project continuity, relationships, roster snapshots, provenance, unresolved boundaries, and migration state unless a newer repository record explicitly supersedes the exact field in question.

Exact army-list source payloads live under `Sources/Armies/` when extracted. Army crosswalk records live under `Armies/`. They map preserved roster evidence into repository identifiers but do not replace the exact roster payload.

Current extracted army sources:
- `Sources/Armies/FORCE-1985-V946.txt`
  - SHA-256: `f0f1772c4547b24d95e236a65b2fbaed5dc1e78bf6824ab41f4d52713000a0a6`
  - Embedded duplicate: Appendix C of `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt`
- `Sources/Armies/FORCE-3000.txt`
  - SHA-256: `ce28c1e3d3a99fb0765af0b141adcb88ca6373474df2a2f1a909597aca0c2ac9`
  - Embedded duplicate: Appendix B of `Order_of_the_Silver_Compass_MASTER_v4.3.41.txt`

## Human-evidence methodology

- Kyllonen & Zu (2025): constructs, measurement, validity, reliability, method effects, and related measurement safeguards.
  - Repository file: `Sources/Methodology/Kyllonen_Zu_2025_Educational_Measurement_Ch19.pdf`
  - Artifact hash: `65252c9f09ebc6f4be60f6e4bafc5fac572cafb0285247170ba3b2b4af197b50`

- Connelly & McAbee (2024): self/other differences, reputation, person perception, context, consensus, and accuracy.
  - Repository file: `Sources/Methodology/Connelly_McAbee_2024_Reputations_at_Work.pdf`
  - Artifact hash: `b1e7739c84f63747ae9b9fa133bff67caf23c5c88753f57eb9c66123e8db39f9`

- Roberts & Yoon (2022): traits, motives/goals, skills/abilities, narrative identity, development, and person-situation interaction.
  - Repository file: `Sources/Methodology/Roberts_Yoon_2022_Personality_Psychology.pdf`
  - Artifact hash: `d8d5dfa8ab160d90730aa13e4e0fa6f1e064852bbd72f8563bbf80960651f7f2`

These academic sources govern only the scientific constructs and limits they actually support. `Sources/Methodology/REVIEW_STATUS.md` records the later full-review state and narrowly supersedes the older Compendium audit only on that review-completion question. The papers improve inference; they do not create project canon or dictate fiction.

## Relevant official Adepta Sororitas lore anchors

These sources are used to test compatibility and sharpen portrayal. They do not create project biography, motive, relationship or private belief by themselves.

- Games Workshop / Warhammer Community, "New animation Adepta Sororitas: Penitence arrives on Warhammer+ along with a host of special content", 2026.
  - The Order of the Sacred Rose is one of the six Orders Majoris.
  - Its Matriarch is Saint Arabella, remembered as level-headed and serene and as a liberator of the oppressed.
  - Sacred Rose Sisters are described as intoning prayers of fortitude and strength rather than bloodlust and vengeance.
  - Project use: this supports compatibility with Constantia's already-established Sacred Rose inheritance and her calm, liberation-oriented theology. It does not transfer Arabella's biography or make serenity a rule-determined personality.
  - Locator: https://www.warhammer-community.com/en-gb/articles/mb5z0ebi/new-animation-adepta-sororitas-penitence-arrives-on-warhammer-along-with-a-host-of-special-content/

- Games Workshop / Warhammer Community, "Starting an Adepta Sororitas Army in Warhammer 40,000 – Everything You Need To Know, From Painting to Lore", 2024.
  - The Adepta Sororitas are a martial sisterhood whose devotion is presented as integral to how they fight.
  - Their historical institutional role includes defending holy sites and waging wars of faith against heretics.
  - Project use: broad faction context only; it does not define Constantia's personal history.
  - Locator: https://www.warhammer-community.com/en-gb/articles/PFyXcQCJ/starting-an-adepta-sororitas-army-in-warhammer-40000-everything-you-need-to-know-from-painting-to-lore/

## Warhammer 40,000 lore and rules

Current official Games Workshop/Warhammer sources govern current lore and rules.

For 11th-edition rules questions:
- start with `Rules/11e/SOURCE_INDEX.md`;
- resolve the relevant rules record under `Rules/11e/units/`;
- use a roster under `Armies/` for snapshot composition and snapshot costs only.

The repository's rules records govern only the fields they explicitly verify and date. They do not outrank the current official Games Workshop source.

If the current official source could not be retrieved, mark the field `not_yet_verified` or `blocked_current_source` rather than silently substituting an older rule.

Historical project snapshots remain historical evidence and should not be silently presented as current.
