# ASSET_INTELLIGENCE_FACTORY_PLAN — JExec

Status: active · Owner: JExec stewardship · Version: 1.0 (2026-07-12)

This document governs JExec as a sovereign digital asset being developed into a
**Category Intelligence Factory**: not a website about a topic, but a system that
produces governed intelligence inside a category it names. It follows the
Sovereign Asset System methodology and answers its eleven layers explicitly.

The public artifact this plan governs lives in `/docs` (the site) and is bound by
`/governance` (the constraint). This file is strategy; it is not published on the site.

---

## 1 · Domain thesis

**JExec makes execution answerable before it becomes irreversible.**

Technical form: *JExec defines whether an intended execution is admissible before
it mutates state.*

Why the name is necessary: the industry has post-execution vocabulary in excess
(logs, traces, audits, postmortems) and almost no pre-execution vocabulary. The
verb form — *to JExec an execution* — occupies the empty slot. A category whose
verb you own is a category whose conversations route through you.

## 2 · Category language

The asset owns and defines these terms, all published at canonical URLs:

- **Pre-Execution Admissibility** — the category name itself.
- **The mutation boundary** — the line between intent and state where the decision lives.
- **To JExec** — to test an intended execution for admissibility before it runs.
- **Admissibility failure class (EAF-1 … EAF-10)** — the ontology's citable codes.
- **JExec Record** — the decision artifact. **JAS A0–A3** — the maturity grades.
- **The four verdicts** — allow / warn / escalate / deny as a closed, published set.
- Coined framings with quotation value: *"Capability is not authority."*
  *"Stale evidence is more dangerous than missing evidence because it looks like
  diligence."* *"Unknown risk is worst-case risk."* *"A deny that is kept is the
  cheapest audit finding an organization will ever produce."*

Language discipline: definitions are versioned and never silently rewritten
(see `/governance/VERSIONING.md`), which is what makes the language citable by
researchers, vendors, and AI agents alike.

## 3 · Ontology

**Execution Admissibility Ontology (EAO), v0.1 — ten classes:**

| Code | Class | Model question |
|---|---|---|
| EAF-1 | Unstated Intent | Intent |
| EAF-2 | Unattributed Actor | Actor |
| EAF-3 | Unverified Authority | Authority |
| EAF-4 | Authority–Scope Mismatch | Authority × Scope |
| EAF-5 | Unbounded Scope | Scope |
| EAF-6 | Missing Evidence | Evidence |
| EAF-7 | Stale Evidence | Evidence |
| EAF-8 | Unclassified Risk | Risk |
| EAF-9 | Irreversibility Blindness | Risk |
| EAF-10 | Unrecorded Decision | Decision |

Each class has a deep reference page (definition, signals, agent/CI/human
examples, why it defeats admissibility, remediation, protocol consequence) and a
machine-readable entry in `/api/eao.json`. The ontology closes over the seven-
question model: every question has at least one failure class; every class maps
to record fields. This closure is the intellectual moat — incidents can be
*classified*, not just described.

## 4 · Standard

**JExec Admissibility Standard (JAS), v0.1:** A0 Ungoverned → A1 Declared →
A2 Verified → A3 Enforced. Unit of assessment is the *execution path*, never the
organization — the honesty of that unit is itself a differentiator. No
certification exists or is claimed; JAS is a self-assessment vocabulary, which
makes adoption frictionless and misuse detectable.

## 5 · Protocol

The published verdict rules (protocol.html) map detected classes × two context
facts (production? irreversible?) to consequences, with the overall verdict as
the most severe consequence. Two conservative defaults are named as doctrine:
unknown risk is worst-case risk; undecidable is never allowable. The protocol is
deterministic, monotone, explainable, and complete — properties stated publicly
so independent implementations can be checked against them.

## 6 · Engine / Tool

**JExec Check v0.1** — a client-side, deterministic engine implementing the
protocol table exactly. No backend, no data collection, no AI claims. Output is
a verdict + detected EAF classes (each linking to its reference page) + a
conforming JExec Record. The engine's honesty about its limits ("it evaluates
what you declare") mirrors the category's core insight and builds trust.

Roadmap: v0.2 CLI (`jexec check record.json`) validating records against the
schema; v0.3 CI action annotating pipelines; later a hosted validation endpoint
(the API monetization path).

## 7 · Reference layer

- Stable canonical URLs; descriptive slugs; every page in the sitemap exists.
- JSON-LD on every page (WebSite, DefinedTermSet/DefinedTerm, TechArticle,
  WebApplication, Service).
- Agent-readable layer: `llms.txt`, `/api/eao.json`, `/api/standard.json`,
  `/api/record.schema.json` — versioned with the same discipline as prose.
- Citation format published: "EAF-7 Stale Evidence, EAO v0.1, URL".
- Internal linking is total: model ↔ ontology ↔ standard ↔ protocol ↔ record ↔
  engine, every page ≤ 2 clicks from any other. No orphans, no dead links
  (dead link = governance finding, stated publicly on the 404 page).

## 8 · Governance

Published constraint at /governance.html; repo-side artifacts in `/governance`:
claims policy (what JExec is NOT), versioning rules (append, never rewrite),
append-only decision log. The distinctive rule: **the consistency rule** — the
protocol table and the engine must agree; divergence is a logged governance
incident. A spec about governed execution that governs itself this visibly is
very hard to imitate cheaply.

## 9 · Interface thesis

The interface embodies the mutation boundary; it does not decorate it.

- One motif: a vertical rule dividing intent (dark, unproven) from state
  (panel, material). It appears in the hero and as the left border of every
  record block.
- The only saturated colors are the four verdicts. Color = function.
- Monospace for what machines read (codes, records, fields); sans for what
  humans read. No stock imagery, no 3D, no animation the thesis doesn't need.
- Every page passes: explains something? readable without JS/animation? fast on
  mobile? serious to an enterprise reader? SEO- and accessibility-safe?
- The 404 page renders as a DENY verdict — even the error surface teaches the
  category.

## 10 · Monetization (pre-sale, trust-compatible)

Ordered by activation:

1. **Execution Admissibility Review** (live at /review.html): fixed-scope,
   human-performed review of one execution path; JAS grade + EAO-mapped
   findings + record templates. High-trust, zero-inventory, extends the
   reference instead of diluting it.
2. **Admissibility Readiness Brief**: paid written brief for teams pre-agents
   (template derived from Review deliverables).
3. **Record tooling**: paid CI action / validation endpoint once the free CLI
   exists (free spec, paid convenience).
4. **Taxonomy/standard licensing**: vendors embedding EAO codes or JAS levels
   in their products under attribution license.
5. **Reference sponsorship**: only outside spec pages, always labeled —
   governance page already binds this publicly.

Never: display ads, sponsored definitions, "certification" fees, mass content.

## 11 · Buyer logic

**Who must own this:**
- CI/CD & DevOps platforms (GitHub, GitLab, Harness, CircleCI): admissibility is
  the missing pre-merge/pre-deploy vocabulary their gates already gesture at.
- Agent-infrastructure & AI-safety-adjacent vendors (agent orchestration,
  tool-permission layers): they need exactly this language for "should this
  agent action run" — the category JExec already names and structures.
- Policy/supply-chain security vendors (OPA/Styra ecosystem, Chainguard,
  in-toto-adjacent): JExec is deliberately positioned as the decision layer
  *between* their systems — complement, not competitor, hence acquirable.
- GRC/ITSM platforms (ServiceNow et al.): change management is A1-era JExec;
  agents force the upgrade, and the vocabulary is here.

**Why non-purchase is a loss:** the acquirer's competitor gets (a) the verb of
the category, (b) the citable failure codes that incident reports and agent
frameworks can standardize on, (c) a governed reference whose trust cannot be
replayed quickly — accumulation, versioned history, and restraint cannot be
built in a quarter, which is the moat. A team can clone the idea; it cannot
clone the name that *is* the idea, the language already defined at canonical
URLs, or the record of having governed it credibly over time.

**Acquisition readiness:** clean IP (single steward, one repo, no third-party
content), versioned artifacts, documented decision log, revenue evidence via
Reviews, agent-readable endpoints demonstrating integration paths, and a
category story a corp-dev memo can lift verbatim from this file.

---

## Execution roadmap

- **Phase 1 — Foundation (done in this iteration):** site v0.1 in `/docs`
  (thesis, ontology ×10, standard, protocol, record + schema, engine,
  governance, review, llms.txt, APIs, sitemap); governance files; this plan.
- **Phase 2 — Proof:** deploy to the domain root; submit sitemap to Search
  Console; publish 2–3 deep briefs ("Agent tool calls are executions",
  "The A0→A1 jump", "Stale evidence: the diligence-shaped failure") as
  versioned reference articles; first paid Review to create the revenue
  record — logged as a fact of occurrence per the data boundary, never as an
  amount.
- **Phase 3 — Instrument:** `jexec` CLI + GitHub Action (free) validating
  records; usage becomes the adoption signal buyers price.
- **Phase 4 — Compound:** EAO v0.2 additions via decision log; incident
  write-ups classified in EAF codes; outreach to agent-framework maintainers to
  adopt record fields; maintain the acquisition dossier from this file.

## Standing rules for whoever works on this asset

1. Nothing ships that violates `/governance/CLAIMS_POLICY.md`.
2. Every definition change increments a version and lands in the decision log.
3. Engine and protocol table move in lockstep or not at all.
4. No page enters the sitemap unless it is a maintained reference artifact.
5. Revenue must extend the reference; anything that dilutes it is declined.
6. No number of commercial significance enters this repository or the site —
   prices, fees, revenue, valuations, offers, negotiation positions, client
   identities. Amounts live off-repository only (governance/DATA_BOUNDARY.md).
