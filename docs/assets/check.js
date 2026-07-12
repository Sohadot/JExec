/* JExec Check v0.1 — deterministic admissibility engine.
   This file implements, with nothing added and nothing held back,
   the published verdict rules at /protocol.html.
   If this code and that table ever disagree, one of them is wrong
   and the discrepancy is a governance incident. */
(function () {
  "use strict";

  var EAF = {
    "EAF-1":  { name: "Unstated Intent",           url: "/ontology/unstated-intent.html" },
    "EAF-2":  { name: "Unattributed Actor",        url: "/ontology/unattributed-actor.html" },
    "EAF-3":  { name: "Unverified Authority",      url: "/ontology/unverified-authority.html" },
    "EAF-4":  { name: "Authority–Scope Mismatch",  url: "/ontology/authority-scope-mismatch.html" },
    "EAF-5":  { name: "Unbounded Scope",           url: "/ontology/unbounded-scope.html" },
    "EAF-6":  { name: "Missing Evidence",          url: "/ontology/missing-evidence.html" },
    "EAF-7":  { name: "Stale Evidence",            url: "/ontology/stale-evidence.html" },
    "EAF-8":  { name: "Unclassified Risk",         url: "/ontology/unclassified-risk.html" },
    "EAF-9":  { name: "Irreversibility Blindness", url: "/ontology/irreversibility-blindness.html" },
    "EAF-10": { name: "Unrecorded Decision",       url: "/ontology/unrecorded-decision.html" }
  };

  var SEV = { allow: 0, warn: 1, escalate: 2, deny: 3 };

  function evaluate(a) {
    var f = [];
    function add(cls, consequence, because) {
      f.push({ class: cls, name: EAF[cls].name, consequence: consequence,
               url: "https://jexec.com" + EAF[cls].url, because: because });
    }
    var prod = a.env === "production";
    var irrevEff = a.risk === "irreversible" || a.risk === "unclassified";

    if (a.intent === "none") add("EAF-1", "deny", "intent absent");
    else if (a.intent === "vague") add("EAF-1", "warn", "intent too vague to evaluate");

    if (a.actor === "unknown") add("EAF-2", "deny", "actor unknown");
    else if (a.actor === "asserted") add("EAF-2", "escalate", "identity asserted but not authenticated");

    if (a.authority === "none") add("EAF-3", "deny", "no authority source");
    else if (a.authority === "claimed") add("EAF-3", "escalate", "authority source named but not verified");

    if (a.authority !== "none") {
      if (a.coverage === "no") add("EAF-4", "deny", "authority explicitly does not cover the declared scope");
      else if (a.coverage === "unknown") add("EAF-4", "escalate", "authority coverage of scope unknown or partial");
    }

    if (a.bounded === "unbounded") add("EAF-5", prod ? "deny" : "escalate",
      prod ? "unbounded scope in production" : "unbounded scope outside production");
    else if (a.bounded === "partial") add("EAF-5", prod ? "escalate" : "warn",
      prod ? "partially bounded scope in production" : "partially bounded scope");

    if (a.evidence === "missing") add("EAF-6", irrevEff ? "deny" : "escalate",
      irrevEff ? "no evidence behind an irreversible or unclassified mutation" : "no evidence behind a reversible mutation");
    else if (a.evidence === "stale") add("EAF-7", irrevEff ? "escalate" : "warn",
      irrevEff ? "stale evidence behind an irreversible or unclassified mutation" : "stale evidence behind a reversible mutation");

    if (a.risk === "unclassified") add("EAF-8", "escalate", "risk not classified — treated as irreversible by evidence rules");

    if (a.risk === "irreversible" && a.reversal === "none")
      add("EAF-9", "escalate", "irreversible mutation with no declared reversal or review path");

    if (a.record === "none") add("EAF-10", "warn", "no admissibility record will be produced or stored");

    var verdict = "allow";
    f.forEach(function (x) { if (SEV[x.consequence] > SEV[verdict]) verdict = x.consequence; });
    return { verdict: verdict, findings: f };
  }

  function buildRecord(a, r) {
    return {
      jexec_version: "0.1",
      intent: a.intentText || "(intent not declared)",
      actor: {
        type: a.actorType,
        id: a.actorType === "unspecified" ? "(unspecified)" : "(as declared at the boundary)",
        authenticated: a.actor === "authenticated"
      },
      authority: {
        source: a.authority === "none" ? "none" : "(as declared)",
        verified: a.authority === "verified",
        covers_scope: a.authority === "none" ? null : (a.coverage === "covers" ? true : (a.coverage === "no" ? false : null))
      },
      scope: {
        environment: a.env === "production" ? "production" : "non-production",
        bounded: a.bounded === "bounded" ? true : (a.bounded === "partial" ? "partial" : false)
      },
      risk: {
        class: a.risk === "unclassified" ? "unclassified" : "state_mutation",
        irreversible: a.risk === "unclassified" ? null : a.risk === "irreversible",
        reversal_path: a.risk === "irreversible" ? (a.reversal === "exists" ? "(declared)" : null) : "(not applicable)"
      },
      evidence: a.evidence === "missing" ? [] :
        [{ type: "(as declared)", current: a.evidence === "current" }],
      findings: r.findings.map(function (x) {
        return { class: x.class, name: x.name, consequence: x.consequence, url: x.url };
      }),
      decision: r.verdict,
      timestamp: new Date().toISOString()
    };
  }

  function val(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : null;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  var VLABEL = {
    allow: "ALLOW — admissible as declared.",
    warn: "WARN — admissible, with findings that must appear on the record.",
    escalate: "ESCALATE — not decidable at this boundary; suspend until a distinct authority decides.",
    deny: "DENY — inadmissible as declared; the mutation must not proceed."
  };

  document.getElementById("jexec-form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var names = ["intent", "actor", "authority", "coverage", "bounded", "env", "evidence", "risk", "reversal", "record"];
    var a = { intentText: (document.getElementById("intent-text").value || "").trim(),
              actorType: val("actortype") || "unspecified" };
    var missing = [];
    names.forEach(function (n) {
      a[n] = val(n);
      if (a[n] === null) missing.push(n);
    });
    var out = document.getElementById("result");
    if (missing.length) {
      out.innerHTML = '<div class="verdict-panel p-warn"><h2 class="v-warn">INCOMPLETE</h2>' +
        "<p>Answer every question. An admissibility decision over missing declarations would itself be a finding. Unanswered: " +
        esc(missing.join(", ")) + ".</p></div>";
      out.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    var r = evaluate(a);
    var record = buildRecord(a, r);
    var recordJson = JSON.stringify(record, null, 2);

    var findingsHtml = r.findings.length
      ? '<ul class="findings">' + r.findings.map(function (x) {
          return "<li><span class=\"code\">" + x.class + "</span> <strong>" + esc(x.name) + "</strong> " +
            '<span class="badge b-' + x.consequence + '">' + x.consequence.toUpperCase() + "</span><br>" +
            '<span class="muted small">' + esc(x.because) + ".</span> " +
            '<a class="small" href="' + x.url.replace("https://jexec.com", "") + '">Reference →</a></li>';
        }).join("") + "</ul>"
      : '<p class="muted">No admissibility failure class detected. This is what a clean boundary crossing looks like.</p>';

    out.innerHTML =
      '<div class="verdict-panel p-' + r.verdict + '">' +
      '<h2 class="v-' + r.verdict + '">' + r.verdict.toUpperCase() + "</h2>" +
      "<p>" + esc(VLABEL[r.verdict]) + "</p>" + findingsHtml + "</div>" +
      "<h2>JExec Record</h2>" +
      "<p>Produced by this decision, conforming to the <a href=\"/api/record.schema.json\">record schema</a>. Store it append-only — even the allows.</p>" +
      "<pre><code id=\"record-json\">" + esc(recordJson) + "</code></pre>" +
      '<p><button class="ghost" id="copy-record" type="button">Copy record</button></p>';

    document.getElementById("copy-record").addEventListener("click", function () {
      var btn = this;
      navigator.clipboard.writeText(recordJson).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy record"; }, 1600);
      });
    });
    out.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
