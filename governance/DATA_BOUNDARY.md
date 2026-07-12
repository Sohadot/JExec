# JExec Data Boundary

Version 1.0 · Adopted 2026-07-12 (D-010, D-011)

This repository is public and the site it publishes is the reference layer of
the asset. Two boundaries protect that layer. They apply to every file, every
commit, and every future contributor — including automated ones.

## 1 · Public API boundary (D-010)

Public API files (`docs/api/*`, `docs/llms.txt`) may contain **only stable
reference material**: definitions, schemas, standards, and ontology data.

They must never contain: private reviews or their findings, customer data,
credentials, negotiations, or internal strategy. The machine-readable layer is
a mirror of the public specification — nothing else ever enters it.

## 2 · Commercial numbers boundary (D-011)

**No number of commercial significance ever enters this repository or the
published site.** That includes, without limitation:

- prices, fees, and rate structures for Reviews or any other service
- revenue figures, income totals, and client counts
- valuations, asking prices, offers, and negotiation floors or positions
- client identities and any engagement detail that could identify one

The decision log records revenue evidence as **facts of occurrence** — date
and type of engagement only, never amount, never client, unless the client
consents in writing (and even then, never the amount).

Amounts, terms, and negotiation materials live off-repository, in private
storage, full stop. A fee is stated to a client in private correspondence;
it has no other legitimate location.

## Why this is strict

This repository's history is public and permanent; anything committed here is
disclosed forever, to every future counterparty. In a negotiation, the side
whose numbers are known negotiates against itself. The reference gains
authority by being fully public; the commercial position gains strength by
never being public. Confusing the two layers weakens both.

## Enforcement

A violation is a governance incident: the entry is corrected, the correction
is logged in `DECISION_LOG.md`, and — because git history does not forget —
the incident response assumes the disclosed information is permanently public
and adjusts the commercial position accordingly rather than pretending the
leak can be undone.
