JExec

Pre-Execution Admissibility for governed automation.

JExec defines whether an intended execution is admissible before it mutates state.

It is designed for agents, workflows, scripts, CI jobs, infrastructure actions, and automated systems that can change real environments, production systems, repositories, cloud resources, data, or organizational state.

JExec names the decision boundary between intent and execution.

---

Core Thesis

Modern automation no longer only needs better logs after execution.

It needs a governed decision before execution.

An agent may delete.
A workflow may deploy.
A script may migrate.
A CI job may publish.
An infrastructure action may mutate production.

The critical question is not only whether the action can run.

The critical question is:

Is this execution admissible before it mutates state?

JExec exists to define that question, structure the decision, and produce a record that can be inspected, stored, compared, and integrated into governance workflows.

---

Definition

JExec is a pre-execution admissibility specification for governed automation.

It defines how intended executions should declare:

1. Intent
2. Actor
3. Authority
4. Scope
5. Evidence
6. Risk
7. Decision

before they are allowed to mutate state.

---

What “to JExec” Means

To jexec an intended execution means:

«To test whether an intended execution is admissible before it runs.»

Examples:

- JExec it before deploy.
- This workflow failed JExec.
- Generate a JExec record before production.
- No mutation without admissibility.
- Is this agent action JExec-admissible?

---

The JExec Model

Every JExec decision begins with seven questions.

1. Intent

What is the execution trying to do?

2. Actor

Who or what is requesting execution?

Examples: human user, AI agent, CI job, service account, API token, workflow, script.

3. Authority

Is the actor authorized to perform this execution?

Authority must not be treated as a vague assertion.

A JExec decision should identify the source of authority and whether that authority was verified.

Examples of authority sources:

- role-based access control policy
- manual approval
- service account role
- change request
- signed release approval
- repository permission
- infrastructure policy
- organizational procedure

4. Scope

Where will the execution apply?

Examples: staging, production, repository, database, cloud account, customer-facing system.

5. Evidence

What evidence supports admissibility?

Examples: approval, test results, signed artifact, provenance, policy match, change request, risk assessment.

6. Risk

What can the execution change or damage?

Examples: read-only operation, write operation, deletion, deployment, migration, financial action, customer-facing mutation.

7. Decision

What is the admissibility decision?

Possible outcomes:

- allow
- deny
- warn
- escalate

---

JExec Record

A JExec decision should produce a structured record.

Early draft format:

{
  "jexec_version": "0.1",
  "intent": "deploy service to production",
  "actor": {
    "type": "ci_job",
    "id": "github-actions"
  },
  "authority": {
    "source": "manual_approval",
    "verified": true,
    "verifier": "release-manager",
    "evidence": "approval-123"
  },
  "scope": {
    "environment": "production",
    "system": "customer-facing-service"
  },
  "risk": {
    "class": "state_mutation",
    "impact": "production_deployment"
  },
  "evidence": [
    "tests_passed",
    "approval_present",
    "artifact_signed"
  ],
  "decision": "allow",
  "missing_evidence": [],
  "timestamp": "2026-06-13T00:00:00Z"
}

The JExec Record is intended to make execution decisions inspectable before they become irreversible.

The JExec Record is designed to align structurally with existing attestation and event formats, including in-toto-style attestations and CloudEvents-style envelopes, rather than replace them.

This early record format is not a claim of formal compatibility with those standards. It is a design direction for future alignment.

---

What JExec Is

JExec is:

- a pre-execution admissibility specification
- a decision language
- a record format
- a governance model for intended execution
- a foundation that other systems can use to inform or gate execution

---

What JExec Is Not

JExec is not currently:

- a certification authority
- an enforcement engine
- a security scanner
- a replacement for SLSA
- a replacement for Sigstore
- a replacement for OPA
- a replacement for observability tools
- a claim of industry adoption

JExec does not replace existing systems.

It defines the admissibility decision that existing systems can inform, evaluate, or enforce.

Use SLSA for provenance.
Use Sigstore for signing.
Use OPA for policy.
Use JExec for execution admissibility.

---

Current Status

JExec is in early specification development.

Current focus:

1. Define the category: Pre-Execution Admissibility
2. Define the JExec Protocol
3. Define the JExec Record
4. Build a basic JExec Check
5. Establish governance and claim boundaries

The project will not claim certification, enforcement, adoption, or standard status before the required technical and governance foundation exists.

---

Planned Public Surface

Initial public release will focus on:

- What is JExec?
- JExec Protocol
- JExec Check
- JExec Record
- Governance and claim boundaries

The first release will be intentionally small, governed, and precise.

No mass-generated pages.
No fake standard claims.
No decorative interface.
No unsupported adoption language.

---

Interface Thesis

The JExec interface must embody the thesis.

It should not decorate execution governance.

It should visualize the mutation boundary:

Intent → JExec Boundary → Allowed / Denied / Escalated

Every movement, color, layer, and interaction must explain part of the admissibility system.

The interface must remain:

- accessible
- SEO-safe
- performance-safe
- mobile-safe
- understandable without animation
- serious enough for technical and enterprise readers

---

Governance Principle

JExec is built under a strict claim policy.

Every public claim must be:

- clear
- bounded
- verifiable
- versioned where necessary
- free from inflated authority

The project prioritizes credibility over speed.

---

Foundational Sentence

JExec makes execution answerable before it becomes irreversible.

Technical definition:

JExec defines whether an intended execution is admissible before it mutates state.

---

Version

Initial draft: "v0.1"

Status: specification foundation.
