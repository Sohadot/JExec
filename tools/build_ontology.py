#!/usr/bin/env python3
"""Build the Execution Admissibility Ontology (EAO) pages + machine layer.

Single source of truth: CLASSES below. Emits:
  docs/ontology/<slug>.html   (10 class reference pages)
  docs/api/eao.json           (agent-readable ontology)
"""
import json, html, pathlib

BASE = "https://jexec.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent / "docs"
VERSION = "0.1"

CLASSES = [
dict(
  code="EAF-1", slug="unstated-intent", name="Unstated Intent",
  gist="The execution never declares what it is trying to do, so admissibility cannot even be evaluated.",
  consequence=[("deny","intent absent"),("warn","intent declared but too vague to evaluate")],
  fields=["intent"],
  definition=[
    "An execution reaches the mutation boundary without a declared, inspectable statement of what it intends to change. This is not a judgment that the intent is bad. The intent is absent, or so vague that no admissibility question can be asked of it.",
    "Unstated Intent is the first-order failure class. Every other admissibility question is evaluated relative to intent: authority is authority to do <em>what</em>, scope is the reach of <em>what</em>, evidence supports <em>what</em>, risk is the damage <em>what</em> can cause. When intent is unstated, the evaluation has no object.",
  ],
  signals=[
    "Scripts that run because they have always run, with no statement of what they change.",
    "CI steps named after their mechanism (<code>deploy.sh</code>, <code>sync</code>, <code>cleanup</code>) instead of their intended change.",
    "Agent tool calls whose goal exists only inside a prompt context that is never recorded.",
    "Change tickets that authorize “maintenance” without saying what will be different afterward.",
  ],
  examples=dict(
    agent="An autonomous agent issues a destructive API call as an instrumental sub-step of a vague goal such as “clean up the workspace.” The mutating step itself carries no declared intent, so the boundary sees an unexplained deletion.",
    ci="A nightly job mutates a database schema. Its only self-description is the word “sync.” Nobody can say, before it runs, which tables it intends to alter.",
    human="An operator runs an ad-hoc production command from a runbook that documents <em>how</em> to run it but not <em>what this particular run is for</em>.",
  ),
  why="Admissibility is a relation between an intended change and its justification. When the intended change is unstated, authority cannot be matched to it, scope cannot be checked against it, and evidence cannot support it. Any verdict issued over an unstated intent is a verdict about nothing, which is why the protocol denies rather than guesses.",
  remediation=[
    "Require a declared <code>intent</code> field before execution: operation, object, and target, in one sentence a reviewer could dispute.",
    "Reject mechanism-grade intents (“run script”, “maintenance”) at the boundary; they name the actor’s activity, not the state change.",
    "For agents, materialize the goal chain: the mutating step must carry the intent it serves, not merely inherit an ambient prompt.",
  ],
  related=["EAF-5","EAF-8","EAF-10"],
),
dict(
  code="EAF-2", slug="unattributed-actor", name="Unattributed Actor",
  gist="There is no verified answer to the question: who or what is executing this?",
  consequence=[("deny","actor unknown"),("escalate","identity asserted but not authenticated")],
  fields=["actor"],
  definition=[
    "The entity requesting execution cannot be attributed: it is unauthenticated, shared, or ambient. Shared credentials, org-wide tokens, and agent processes that act under a platform identity rather than an identity of their own all produce executions with no accountable actor.",
    "Attribution is not a logging nicety. Authority is a property of an actor; if the actor is unattributed, no authority can attach to the execution at all.",
  ],
  signals=[
    "One service token used by many pipelines, so any mutation could have come from any of them.",
    "Cron jobs and daemons running as <code>admin</code> or a team account.",
    "Agent frameworks where every agent acts as the platform, with no per-agent identity and no link to the initiating human.",
    "Production access through a bastion under a shared login.",
  ],
  examples=dict(
    agent="Several autonomous agents share one API key. When one of them deletes a resource, the mutation cannot be attributed to a specific agent, a specific task, or the human who initiated it.",
    ci="A runner authenticates with an organization-wide personal access token. Every repository’s pipeline mutates state as the same anonymous super-actor.",
    human="An on-call engineer makes an emergency change through a team login. Three weeks later, nobody can say who acted.",
  ),
  why="Every downstream admissibility question presumes a subject. “Is the actor authorized?” is unanswerable when the actor is a crowd or a ghost. Unattributed executions also destroy accountability after the fact: an incident review over shared credentials ends at the credential, not at a decision-maker.",
  remediation=[
    "Give every executing entity its own identity — including per-agent identities distinct from the operator who launched them.",
    "Authenticate identity at the boundary and record <code>actor.type</code> and <code>actor.id</code> in the JExec Record.",
    "Forbid shared credentials for any execution classed as a mutation.",
  ],
  related=["EAF-3","EAF-10"],
),
dict(
  code="EAF-3", slug="unverified-authority", name="Unverified Authority",
  gist="Authority is claimed, but never verified against an identifiable source.",
  consequence=[("deny","no authority source at all"),("escalate","source named but not verified")],
  fields=["authority"],
  definition=[
    "The execution asserts that it is permitted — “approved”, “authorized”, “routine” — without an identifiable, checkable source of that permission: no policy, no approval reference, no role grant, no change request.",
    "The most common form is silent: authority is inferred from capability. The token works, therefore the action must be allowed. JExec treats this inference as the central confusion of automated systems. Credentials prove that the system <em>will</em> obey; they say nothing about whether it <em>should</em>.",
  ],
  signals=[
    "“Approved in chat” with no durable reference.",
    "The requesting actor approving its own execution.",
    "Pipelines that deploy because the secrets are present, not because a deploy was authorized.",
    "Agents assuming the full standing authority of their operator for every sub-action, indefinitely.",
  ],
  examples=dict(
    agent="An agent holds a repository-admin token and force-pushes to a protected branch. Nothing authorized the force-push; the token’s capability was silently treated as permission.",
    ci="A release pipeline promotes an artifact to production whenever it reaches the final stage. The “authority” is the pipeline’s structure itself — unverifiable and unowned.",
    human="An engineer with production database access corrects live data by hand. Access existed; authority for this change was never established.",
  ),
  why="An admissibility decision must be able to point at the source of the authority it relied on, and at who or what verified it. Otherwise the verdict reduces to “the actor was able to,” which is precisely the condition JExec exists to interrogate. Capability without verified authority is how automation scales mistakes into incidents.",
  remediation=[
    "Name the authority source in the record: policy, role, manual approval, change request, signed release — with a reference.",
    "Record verification: <code>authority.verified</code>, the verifier, and the evidence pointer.",
    "Keep the requesting actor and the verifying authority distinct; self-approval is absence of approval.",
  ],
  related=["EAF-2","EAF-4"],
),
dict(
  code="EAF-4", slug="authority-scope-mismatch", name="Authority–Scope Mismatch",
  gist="Verified authority exists — for a different scope than the one this execution mutates.",
  consequence=[("deny","authority explicitly does not cover the declared scope"),("escalate","coverage partial or unknown")],
  fields=["authority","scope"],
  definition=[
    "The execution carries real, verified authority — but that authority covers a different environment, system, or object set than the one about to be mutated. A staging approval reused for production. A change request for service A cited while mutating service B.",
    "This class is the most dangerous in systems that check authorization as a boolean. “Is the actor authorized?” returns true; “is the actor authorized <em>for this scope</em>?” was never asked.",
  ],
  signals=[
    "Approvals with no scope written into them, reused across environments.",
    "Wildcard roles (“admin on the account”) treated as intent-specific permission.",
    "Change requests cited by executions that touch systems the request never mentions.",
    "Agents granted write-capable tools when their authorized task only requires reading.",
  ],
  examples=dict(
    agent="An agent is authorized to triage issues in one repository. Its tool grant, however, spans the whole organization, and it “helpfully” edits a workflow file in another repo. Authority existed; coverage did not.",
    ci="A pipeline approved to deploy to staging is re-pointed at production during an incident. The approval it carries is real and verified — for staging.",
    human="A DBA authorized to migrate the analytics database runs the same migration on the transactional database “while at it.”",
  ),
  why="Authority that is not bound to a scope is ambient power, and ambient power expands silently. The admissibility question is comparative: does the coverage of the verified authority contain the declared scope of this execution? A boundary that skips the comparison converts every broad role into a standing production permission.",
  remediation=[
    "Bind every approval and role to an explicit scope, and write that scope into the record.",
    "Compare authority coverage against declared scope at the boundary — as data, not as judgment.",
    "Expire scope bindings; grant agents least-scope tools per task, not per platform.",
  ],
  related=["EAF-3","EAF-5"],
),
dict(
  code="EAF-5", slug="unbounded-scope", name="Unbounded Scope",
  gist="The execution cannot state its blast radius before it runs.",
  consequence=[("deny","unbounded scope in production"),("escalate","unbounded elsewhere, or partially bounded in production"),("warn","partially bounded outside production")],
  fields=["scope"],
  definition=[
    "The execution has no declared limit to where it applies: which environment, which systems, which objects. It will touch “whatever matches,” and what matches is discovered during execution rather than declared before it.",
    "Unbounded scope is the shape of most mass incidents: the recursive delete, the migration without a WHERE clause, the cleanup script that iterates over “all” resources under an account root.",
  ],
  signals=[
    "Destructive statements whose selection criteria are computed at runtime and never reviewed as data.",
    "Scripts that enumerate resources dynamically with no cap and no dry-run count.",
    "Agent tools accepting arbitrary paths, arbitrary queries, or account-level handles.",
    "Infrastructure actions executed at organization or account root “for convenience.”",
  ],
  examples=dict(
    agent="An agent asked to remove stale branches is handed a tool that can delete any ref in any repository. The task was bounded; the tool’s reach was not, and the boundary only sees the tool.",
    ci="A cleanup job deletes cloud resources by tag query. A tagging error widens the match set from 12 resources to 4,000. Nothing before execution stated an expected count.",
    human="An operator runs a recursive permission fix from one directory too high.",
  ),
  why="Risk and evidence are functions of scope. If scope is unbounded, risk is unclassifiable and no finite set of evidence can be sufficient — there is no stated claim for the evidence to support. The protocol therefore refuses unbounded scope in production outright: an execution that cannot state its blast radius has not finished asking to run.",
  remediation=[
    "Declare environment, system, and object set (or expected object count) in the record before execution.",
    "Require dry-run counts for match-based mutations; treat count drift as a new execution needing a new decision.",
    "Scope credentials and agent tools to the declared set; deny wildcard scopes at the production boundary.",
  ],
  related=["EAF-4","EAF-8","EAF-9"],
),
dict(
  code="EAF-6", slug="missing-evidence", name="Missing Evidence",
  gist="Nothing supports that this execution should happen — no tests, no approval reference, no provenance, no policy match.",
  consequence=[("deny","evidence missing for an irreversible or unclassified mutation"),("escalate","evidence missing for a reversible mutation")],
  fields=["evidence"],
  definition=[
    "The execution arrives at the boundary with an empty evidence set for its risk class: no passing tests, no approval pointer, no signed artifact, no policy match, no risk assessment. It may still be the right thing to run. Nothing on the record supports that.",
    "Evidence is what converts “we believe this is admissible” into a decision that can be inspected, compared, and challenged. Without it, the verdict is faith — and faith does not survive incident review.",
  ],
  signals=[
    "Deploy paths where test stages are skippable and skipped.",
    "“Hotfix” lanes that bypass every check and leave no compensating record.",
    "Agent actions justified only by the model’s own output, with no external verification attached.",
    "Records whose <code>evidence</code> array is structurally present and always empty.",
  ],
  examples=dict(
    agent="An agent concludes a config value is wrong and rewrites it in production. The only support is the agent’s own reasoning — no test, no approval, no policy reference travels with the mutation.",
    ci="A release job publishes an artifact whose test stage was cancelled to save time. The publish step neither knows nor cares.",
    human="A schema migration is applied because “it worked locally.”",
  ),
  why="Admissibility without evidence is assertion. The requirement is proportional, not absolute: a read-only job needs almost nothing; an irreversible production mutation needs approval, provenance, and verification. The protocol’s asymmetry — deny when irreversible, escalate when reversible — encodes that proportionality.",
  remediation=[
    "Define evidence requirements per risk class once, in the Standard, instead of per pipeline forever.",
    "Block irreversible mutations with empty evidence sets; there is no legitimate case for them.",
    "Make bypass lanes produce escalation records rather than silence — an emergency is a reason to record more, not less.",
  ],
  related=["EAF-7","EAF-8"],
),
dict(
  code="EAF-7", slug="stale-evidence", name="Stale Evidence",
  gist="Evidence exists — but it describes a system, artifact, or moment that no longer exists.",
  consequence=[("escalate","stale evidence behind an irreversible mutation"),("warn","stale evidence behind a reversible mutation")],
  fields=["evidence"],
  definition=[
    "The execution carries evidence that was valid once and is treated as valid forever: last week’s approval for today’s changed diff, test results from a different artifact hash, a review of a plan that has since been revised.",
    "Stale evidence is more dangerous than missing evidence because it looks like diligence. The record is populated; every field passes a presence check; and none of it describes the execution that is about to run.",
  ],
  signals=[
    "Approvals granted before subsequent commits landed on the same branch.",
    "Test results bound to no artifact hash, reused across rebuilds.",
    "Re-running an old “approved” pipeline against an environment that has drifted for months.",
    "Agent plans approved once by a human, then executed repeatedly as conditions change.",
  ],
  examples=dict(
    agent="A human approves an agent’s five-step plan. By step four, earlier steps have changed the environment; the approval now describes a world that no longer exists, and step five mutates the new one.",
    ci="A deployment reuses the green test run from build 4112 while shipping build 4127.",
    human="A change board approves a migration for Saturday; it runs the following Thursday against a database three schema versions later.",
  ),
  why="An admissibility decision is about a specific execution at a specific time. Evidence decays as the diff, the artifact, or the environment changes — and it decays silently, because nothing in most systems invalidates it. The boundary must therefore ask not “is evidence present?” but “does this evidence still describe this execution?”",
  remediation=[
    "Bind evidence to content: artifact hashes, commit ranges, environment versions.",
    "Expire approvals; re-evaluate admissibility on any change to intent, scope, or artifact.",
    "For irreversible classes, one approval authorizes one execution — never a family of them.",
  ],
  related=["EAF-6","EAF-10"],
),
dict(
  code="EAF-8", slug="unclassified-risk", name="Unclassified Risk",
  gist="Nobody has said what this execution can change or damage.",
  consequence=[("escalate","risk unclassified — and treated as irreversible by every evidence rule until classified")],
  fields=["risk"],
  definition=[
    "The execution carries no risk classification: is it read-only, a write, a deletion, a migration, a customer-facing mutation, a financial action? The failure is not that risk is high — high risk with strong evidence can be admissible. The failure is that risk is unknown.",
    "Every proportionality rule in admissibility keys off the risk class: how much evidence is enough, which authority suffices, whether a reversal path must exist. Unclassified risk disables proportionality itself.",
  ],
  signals=[
    "Pipelines that gate a production deploy and a docs publish identically.",
    "Agent tool catalogs with no mutation flags — read and delete presented as interchangeable capabilities.",
    "“Run script” tickets with no impact statement.",
    "Risk fields that exist in the schema and are populated with <code>unknown</code> in every record.",
  ],
  examples=dict(
    agent="A framework exposes forty tools to an agent with uniform metadata. The boundary cannot distinguish the tool that reads a file from the tool that rotates production credentials.",
    ci="One reusable workflow handles linting, packaging, and production deployment. Its callers inherit a single, undifferentiated gate.",
    human="A ticket says “run the attached script on prod.” No one states what the script can touch.",
  ),
  why="A boundary that cannot grade risk must either overreact to everything or underreact to everything — and under real delivery pressure, it underreacts. JExec’s conservative default makes ignorance expensive in the right direction: an unclassified execution is treated as irreversible until someone says otherwise, which makes classification the cheap path.",
  remediation=[
    "Make <code>risk.class</code> mandatory at the boundary; absence is itself a finding, not a default.",
    "Classify tools and actions once at registration time, not per-run under pressure.",
    "Adopt the conservative default: unclassified is handled as irreversible until classified.",
  ],
  related=["EAF-5","EAF-6","EAF-9"],
),
dict(
  code="EAF-9", slug="irreversibility-blindness", name="Irreversibility Blindness",
  gist="An irreversible mutation is handled with the same casualness as a reversible one.",
  consequence=[("escalate","irreversible mutation with no declared reversal or review path")],
  fields=["risk"],
  definition=[
    "The execution will destroy information or commit external effects — a deletion, a dropped column, a sent email, a financial transfer, a published artifact — and the decision path treats it like an ordinary write: same checks, same speed, no reversal path declared, no distinct review.",
    "The failure is not the irreversibility itself. Some executions must be irreversible. The failure is blindness: the boundary never registered that this one is different.",
  ],
  signals=[
    "Deletes gated identically to updates in the same pipeline.",
    "“We have backups” asserted as a reversal path and never tested as one.",
    "External side effects — messages, payments, releases — triggered inside loops or retries.",
    "Agents granted destructive tools alongside read tools with equal standing and equal friction.",
  ],
  examples=dict(
    agent="A retry wrapper around an agent’s “send notification” tool re-fires on timeout. The timeouts were delivery delays. Four thousand customers receive the message three times; no reversal path exists because none was ever declared.",
    ci="A cleanup stage permanently deletes storage buckets on the same approval that reorders a config map.",
    human="An engineer drops a “deprecated” table during a routine change window. The backup that would have made this reversible expired quietly months earlier.",
  ),
  why="Reversible errors are an engineering cost; irreversible errors are permanent state. A boundary that prices them identically prices catastrophe and inconvenience the same, and will eventually pay the difference. Admissibility for irreversible classes must be asymmetric: stronger evidence, distinct authority, and a declared reversal path — or a declared, deliberate acceptance that there is none.",
  remediation=[
    "Declare a reversal path — or an explicit review acknowledging its absence — for every irreversible class.",
    "Gate asymmetrically: irreversible mutations require stronger evidence and a distinct authority source.",
    "Stage external effects behind holds; never place irreversible calls inside automatic retry loops.",
  ],
  related=["EAF-5","EAF-8"],
),
dict(
  code="EAF-10", slug="unrecorded-decision", name="Unrecorded Decision",
  gist="The execution may even be admissible — but no durable record of that decision will exist.",
  consequence=[("warn","no admissibility record produced or stored")],
  fields=["decision","timestamp"],
  definition=[
    "No durable, inspectable record of the admissibility decision is produced or stored. The mutation happens; the decision evaporates. Whatever gate logic ran leaves nothing that can be inspected, compared across time, or cited in review.",
    "This class closes the ontology because it attacks the system itself: a boundary whose decisions leave no records cannot be shown to exist. Six months later, an unrecorded allow and no decision at all are indistinguishable.",
  ],
  signals=[
    "Approvals living in chat scrollback and meeting memory.",
    "Gate logic embedded in scripts that emit only an exit code.",
    "Agent deliberation discarded with the context window at the end of the session.",
    "Audit trails reconstructed after incidents instead of read during them.",
  ],
  examples=dict(
    agent="An agent framework checks permissions internally before each tool call, then throws the check away. After an incident, the operator can prove what the agent did — never what was decided about it.",
    ci="A deployment gate evaluates six conditions and returns a boolean. Which condition nearly failed last Tuesday is unknowable.",
    human="A production change is approved verbally on a bridge call during an outage. Everyone remembers it differently.",
  ),
  why="Records are what make the boundary exist over time rather than per-run. They allow decisions to be compared (“why was this allowed in March and denied in May?”), audited without archaeology, and improved deliberately. Denials are the cheapest audit findings an organization will ever produce — but only if they are kept.",
  remediation=[
    "Emit a JExec Record for every boundary decision — including allows, which are the majority and the baseline.",
    "Store records append-only, outside the executing system’s own write path.",
    "Reference record identifiers from deploy logs and change systems; retain denials indefinitely.",
  ],
  related=["EAF-1","EAF-7"],
),
]

NAV = """<header class="site-head"><div class="wrap">
<a class="brand" href="/">JExec</a>
<nav class="site-nav" aria-label="Site">
<a href="/">Thesis</a>
<a href="/ontology/" aria-current="page">Ontology</a>
<a href="/standard.html">Standard</a>
<a href="/protocol.html">Protocol</a>
<a href="/record.html">Record</a>
<a href="/check.html">Check</a>
<a href="/governance.html">Governance</a>
</nav></div></header>"""

FOOT = """<footer class="site-foot"><div class="wrap">
<span>JExec · Pre-Execution Admissibility · spec draft v0.1</span>
<a href="/governance.html">Claims policy</a>
<a href="/api/eao.json">eao.json</a>
<a href="/llms.txt">llms.txt</a>
</div></footer>"""

BADGE = {"deny":"b-deny","escalate":"b-escalate","warn":"b-warn","allow":"b-allow"}

def class_page(i, c):
    prev_c = CLASSES[i-1] if i > 0 else None
    next_c = CLASSES[i+1] if i < len(CLASSES)-1 else None
    url = f"{BASE}/ontology/{c['slug']}.html"
    badges = " ".join(
        f'<span class="badge {BADGE[v]}">{v.upper()}</span> <span class="muted small">{html.escape(when)}</span><br>'
        for v, when in c["consequence"])
    signals = "\n".join(f"<li>{s}</li>" for s in c["signals"])
    remediation = "\n".join(f"<li>{r}</li>" for r in c["remediation"])
    related = " · ".join(
        f'<a href="/ontology/{r["slug"]}.html">{r["code"]} {html.escape(r["name"])}</a>'
        for r in CLASSES if r["code"] in c["related"])
    fields = ", ".join(f"<code>{f}</code>" for f in c["fields"])
    definition = "\n".join(f"<p>{p}</p>" for p in c["definition"])
    jsonld = json.dumps({
      "@context":"https://schema.org","@type":"DefinedTerm",
      "name": f'{c["code"]} — {c["name"]}',
      "termCode": c["code"],
      "description": c["gist"],
      "url": url,
      "inDefinedTermSet": {"@type":"DefinedTermSet",
        "name":"Execution Admissibility Ontology (EAO)",
        "url": f"{BASE}/ontology/"}
    }, ensure_ascii=False)
    prevnext = '<nav class="prevnext" aria-label="Ontology order">'
    prevnext += (f'<a href="/ontology/{prev_c["slug"]}.html">← {prev_c["code"]} {html.escape(prev_c["name"])}</a>' if prev_c else '<a href="/ontology/">← Ontology index</a>')
    prevnext += (f'<a href="/ontology/{next_c["slug"]}.html">{next_c["code"]} {html.escape(next_c["name"])} →</a>' if next_c else '<a href="/protocol.html">Protocol →</a>')
    prevnext += '</nav>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{c['code']} {html.escape(c['name'])} — Execution Admissibility Ontology — JExec</title>
<meta name="description" content="{html.escape(c['gist'])} {c['code']} is an admissibility failure class in the JExec Execution Admissibility Ontology.">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="/assets/jexec.css">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
{NAV}
<main><div class="wrap">
<p class="crumbs"><a href="/">JExec</a> / <a href="/ontology/">Execution Admissibility Ontology</a> / {c['code']}</p>
<p class="kicker">Admissibility failure class</p>
<h1>{c['code']} — {html.escape(c['name'])}</h1>
<p class="lede">{html.escape(c['gist'])}</p>
<p>{badges}</p>

<h2>Definition</h2>
{definition}

<h2>How it appears</h2>
<ul>
{signals}
</ul>

<h2>Across actors</h2>
<h3>Agent</h3>
<p>{c['examples']['agent']}</p>
<h3>CI / pipeline</h3>
<p>{c['examples']['ci']}</p>
<h3>Human operator</h3>
<p>{c['examples']['human']}</p>

<h2>Why it defeats admissibility</h2>
<p>{c['why']}</p>

<h2>Remediation</h2>
<ul>
{remediation}
</ul>

<h2>In the JExec Record</h2>
<p>Primarily affects: {fields}. The <a href="/protocol.html">JExec Protocol</a> maps {c['code']} to the consequences above; <a href="/check.html">JExec Check</a> detects it deterministically and links back to this page.</p>

<h2>Related classes</h2>
<p>{related}</p>
{prevnext}
</div></main>
{FOOT}
</body>
</html>
"""

def eao_json():
    return json.dumps({
      "name": "Execution Admissibility Ontology (EAO)",
      "shortName": "EAO",
      "version": VERSION,
      "status": "draft",
      "publisher": "JExec — Pre-Execution Admissibility",
      "canonical": f"{BASE}/ontology/",
      "license": "Text © JExec. Cite with attribution and a link to the canonical URL.",
      "definition": "A classification of the ways an intended execution fails to be admissible before it mutates state.",
      "verdicts": ["allow","warn","escalate","deny"],
      "classes": [
        {
          "code": c["code"],
          "name": c["name"],
          "url": f"{BASE}/ontology/{c['slug']}.html",
          "summary": c["gist"],
          "recordFields": c["fields"],
          "defaultConsequences": [{"verdict": v, "condition": w} for v, w in c["consequence"]],
          "related": c["related"],
        } for c in CLASSES
      ]
    }, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    for i, c in enumerate(CLASSES):
        p = ROOT / "ontology" / f"{c['slug']}.html"
        p.write_text(class_page(i, c), encoding="utf-8")
        print("wrote", p)
    (ROOT / "api" / "eao.json").write_text(eao_json() + "\n", encoding="utf-8")
    print("wrote", ROOT / "api" / "eao.json")
