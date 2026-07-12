# JExec Decision Log

Append-only. Newest entries at the bottom. Every material decision about the
specification, the site surface, or the governance of the asset is recorded
here before or with the change it authorizes.

---

## 2026-06-13 · D-001 · Category and name

Adopted "Pre-Execution Admissibility" as the category JExec names and defines.
Adopted the verb form ("to JExec an execution") as deliberate category
language. Adopted the foundational sentence: *JExec makes execution answerable
before it becomes irreversible.*

## 2026-06-13 · D-002 · Seven-question model

Fixed the decision model at seven questions (intent, actor, authority, scope,
evidence, risk, decision) and the verdict set at four outcomes (allow, warn,
escalate, deny), both closed sets under versioning.

## 2026-07-12 · D-003 · Execution Admissibility Ontology v0.1

Published the EAO with ten failure classes, EAF-1 through EAF-10, each with a
canonical reference page and a machine-readable entry in /api/eao.json. Class
codes are permanent per VERSIONING.md rule 1.

## 2026-07-12 · D-004 · JAS v0.1 and the unit of assessment

Published the JExec Admissibility Standard with four levels (A0 Ungoverned,
A1 Declared, A2 Verified, A3 Enforced). Decided the unit of assessment is the
**execution path**, never the organization, and that JAS is self-assessment
only: no certificate exists and none may be claimed.

## 2026-07-12 · D-005 · Protocol v0.1 and conservative defaults

Published the verdict rule table. Adopted two doctrine-level defaults:
(1) unclassified risk is treated as irreversible by all evidence rules;
(2) undecidable conditions escalate — they never allow. Adopted the protocol
properties: deterministic, monotone, explainable, complete.

## 2026-07-12 · D-006 · Consistency rule

The protocol table and the JExec Check engine are required to implement
identical rules. Divergence is a governance incident, publicly logged. This is
the asset governing itself by its own thesis.

## 2026-07-12 · D-007 · Site v0.1 surface

Published the reference site under /docs: thesis, ontology (11 pages),
standard, protocol, record, check, governance, review, 404, llms.txt,
robots.txt, sitemap.xml, and /api endpoints (eao.json, standard.json,
record.schema.json). Content policy adopted: no mass-generated pages, no
orphan pages, no dead links; every sitemap entry is a maintained reference
artifact. Canonical host assumed as https://jexec.com — if the live host
differs, canonical URLs, sitemap, robots, llms.txt, and JSON endpoints must be
updated in the same commit (VERSIONING.md rule 4 applies).

## 2026-07-12 · D-008 · Revenue boundary

Activated the Execution Admissibility Review (/review.html) as the first
revenue line. Bound publicly on /governance.html: no payment changes a
definition, level, or verdict rule; no sponsored content inside the reference
layer; sponsorship, if ever accepted, is labeled and confined outside the
specification pages. Declined categories recorded: display ads, sponsored
definitions, certification fees, mass content.

## 2026-07-12 · D-009 · Pre-publication consistency fix (engine ↔ record ↔ schema)

Pre-launch review found that `missing_evidence` existed in the record schema
and the README example but was neither required by the schema nor emitted by
JExec Check — an engine/record inconsistency of the kind VERSIONING.md rule 5
exists to catch. Resolved in both directions before first publication:
`missing_evidence` is now a required record field (empty array when nothing is
missing), the engine emits it (populated from EAF-6 findings), and the
record.html example and field table show it. Also replaced the interim
personal contact address with agent@sohadot.com on review.html,
governance.html, and 404.html. Logged per the consistency rule (D-006):
found, fixed, and recorded — not quietly patched.
