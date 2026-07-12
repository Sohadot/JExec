# JExec Versioning Rules

Version 1.0

## Versioned artifacts

| Artifact | Current | Canonical |
|---|---|---|
| Execution Admissibility Ontology (EAO) | v0.1 draft | /ontology/ · /api/eao.json |
| JExec Admissibility Standard (JAS) | v0.1 draft | /standard.html · /api/standard.json |
| JExec Protocol (verdict rules) | v0.1 draft | /protocol.html |
| JExec Record format | v0.1 draft | /record.html · /api/record.schema.json |
| JExec Check (engine) | v0.1 | /check.html · /assets/check.js |

## Rules

1. **Append, never rewrite.** A class code (EAF-n) or level id (An) permanently
   denotes what it denoted. Deprecation is explicit and visible; silent
   redefinition is forbidden.
2. **Every material change increments a version** and lands as an entry in
   `DECISION_LOG.md` before or with the change.
3. **Records outlive versions.** `jexec_version` in every record keeps old
   verdicts interpretable under the rules that produced them.
4. **Prose and JSON move together.** `/api/*.json` carries the same version as
   the pages it mirrors; a release that updates one without the other is
   incomplete.
5. **The consistency rule.** The protocol table (protocol.html) and the engine
   (check.js) implement the same rules. Divergence is a governance incident:
   logged, fixed, and noted — not quietly patched.
6. **URLs are forever.** A published canonical URL is never allowed to 404.
   Superseded content is marked superseded in place or redirected.
