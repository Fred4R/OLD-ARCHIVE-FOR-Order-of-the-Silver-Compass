# Status and Provenance

Read `AUTHORITY.md` for which record governs a question.

Do not collapse authority, record type, canon status, evidence class, or verification status into one field.

## Canon status

Use these distinctions for project standing when they apply:

- `ESTABLISHED_PROJECT_CANON`
- `INTERPRETATION`
- `PROPOSAL`
- `UNRESOLVED`
- `REJECTED`

A statement's presence in a candidate document does not by itself make it accepted canon.

## Record type

Record type describes what a record is, not whether it is canon.

Examples include:
- source snapshot;
- roster crosswalk;
- rules finding;
- continuity record;
- relation record;
- interpretation;
- proposal;
- workflow record.

`SOURCE_SNAPSHOT` is therefore a record type, not a canon status.

## Evidence class

Preserve the Compendium's evidence distinctions:

- `A1` — available direct user statement in the relevant audit/conversation;
- `A1-REPORTED` — predecessor summary or embedded quotation of an earlier user statement;
- `A2` — exact embedded source artifact;
- `A3` — inherited accepted-baseline claim whose original source was not independently seen;
- `A4` — candidate-lineage claim;
- `A5` — official source actually inspected;
- `A6` — interpretation or inference;
- `A7` — proposal;
- `A8` — unresolved or unavailable evidence.

These are categories, not a universal ranking.

An evidence class such as `A1` is not a canon status.

Repeated transmission through one lineage is not independent corroboration.

## Verification status

Time-sensitive or external claims may also need a verification state.

Current rules records use states such as:
- `verified_current`;
- `partially_verified_current`;
- `not_yet_verified`;
- `blocked_current_source`.

Verification status answers whether a current/external claim was checked. It does not make a project claim canon.

## Provenance safeguards

A checksum proves byte identity, not authorship, acceptance, truth, or current rules legality.

A retrieval failure means only that the attempted route failed. It is not proof that the source does not exist.

A later correction overrides only the scope it actually addresses.

## Unresolved information

Do not resolve uncertainty by invention.

Do not invent departures, casualties, names, biographies, motives, relationships, chronology, institutional mergers, or other facts merely to make records agree.

Partial evidence may narrow an unresolved question without resolving it.

## Claim discipline

Do not call something accepted, current/legal, complete, ready, cold-start tested, committed, uploaded, merged, or verified unless the relevant condition has actually been checked.


## Validation is not status

The repository validator may confirm that status, evidence class, verification state, sources, and references are stored consistently. It does not assign `ESTABLISHED_PROJECT_CANON`, convert `UNRESOLVED` into resolved fact, or certify current Warhammer legality merely because the repository passes validation.
