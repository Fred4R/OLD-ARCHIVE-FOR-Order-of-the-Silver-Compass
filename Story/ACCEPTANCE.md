---
record_id: "STORY-ACCEPTANCE-01"
record_type: "conversation_adoption_policy"
as_of: "2026-09-13"
authority_scope: "how live conversation can establish durable project story facts for repository writeback"
does_not_supersede:
  - "direct user meaning or later correction"
  - "STATUS.md canon/evidence definitions"
  - "underlying source evidence"
  - "character agency, consent, private motive, or unresolved information"
---

# Conversational adoption and durable writeback

This policy answers a narrow question: when a live story exchange contains both user-authored material and assistant narration, what may be preserved afterward as a durable project fact?

It is intentionally conservative. The purpose is to preserve continuity without allowing the assistant to canonize its own improvisation.

## Direct user evidence

A clear, non-hypothetical user statement about the project can be direct `A1` evidence for the scope actually stated.

A user-authored action can establish that the user character performed that action and the minimum observable circumstances the action necessarily relies on, provided those circumstances are already present in the live exchange and are not contradicted by stronger evidence.

Do not expand a user statement or action into unstated motive, attraction, consent, expertise, biography, theology, or future commitment.

## Explicit acceptance and correction

Explicit user acceptance can adopt an assistant-proposed fact, but only the fact actually accepted.

An explicit user correction controls over conflicting assistant narration within the corrected scope. Preserve the earlier narration only as superseded workflow or proposal history when useful; do not keep it as competing canon.

## Minimal presupposition adoption

If the user materially acts on an assistant-introduced observable fact, the interaction may establish the minimum premise required to make the user's action intelligible.

Example principle: if the assistant introduces an object on a table and the user says they pick up that object, the object's presence can become an adopted scene fact. Its hidden origin, symbolism, owner, age, motive for placement, or future importance do not become established merely because the user interacted with it.

This is evidence of adoption of the minimum observable premise, not retroactive proof that every surrounding assistant detail was true.

If the user's wording can be understood without adopting the assistant-introduced premise, or if the user is speaking hypothetically, conditionally, or about a possible future action, preserve the premise as unresolved or proposed rather than upgrading it.

## What does not count as acceptance

The following do not, by themselves, establish durable canon:

- silence or failure to object;
- a generic request to continue;
- enjoyment of the scene;
- the assistant repeating its own earlier narration;
- later assistant summaries derived only from assistant-authored material;
- a repository commit or merged pull request;
- model presence in a roster or co-presence in a scene;
- narrative tone, sensuality, implication, or dramatic emphasis.

## Names and identity

A user repeating an assistant-proposed name can establish reported usage when the context supports that reading. It does not automatically establish formal naming acceptance, surname, title, biography, institutional identity, or etymological meaning.

When acceptance is ambiguous, preserve the weaker state rather than forcing a formal identity.

## Other people's private states

Fred's action or interpretation cannot by itself establish another person's attraction, consent, desire, motive, faith interpretation, agreement, loyalty, or private conclusion.

Observable behavior may be recorded as behavior. A private-state claim requires separate evidence appropriate to that person.

## Evidence capture

For a durable change, preserve enough provenance to explain why the fact was written back. Prefer a short exact user phrase when it is necessary and appropriate, or a concise labeled paraphrase when exact quotation adds no value.

Do not archive whole conversations by default. Store only the minimum evidence needed for the durable project fact, its date or conversation context, and its evidence class.

A later correction may narrow or supersede that fact without deleting the older evidence.

## Writeback sequence

Before repository writeback:

1. identify the smallest durable fact actually established;
2. identify its proper authoritative home;
3. preserve evidence class and unresolved limits;
4. update derived story registries only if their scope changed;
5. update `CURRENT_STATE.md` last if the operational present changed;
6. use the repository PR and validation workflow for meaningful durable changes.

Assistant narration cannot self-certify acceptance.
