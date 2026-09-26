"""Rule-based RCA + remediations. Always flags human_approval_required=true."""
from __future__ import annotations

RULES = [
    {
        "id": "nuget-401",
        "match": ["401", "nuget", "service index", "NU1301"],
        "category": "auth",
        "summary": "NuGet feed authentication failed (401).",
        "remediations": [
            "Verify pipeline NuGet service connection / PAT scopes (Packaging Read).",
            "Renew expired ADO packaging credentials; do not embed PATs in YAML.",
            "Confirm feed permissions for the build service identity.",
        ],
    },
    {
        "id": "aad-secret-expired",
        "match": ["AADSTS7000222", "client secret", "expired", "invalid_client"],
        "category": "auth",
        "summary": "Azure service connection client secret expired.",
        "remediations": [
            "Rotate the app registration secret and update the service connection.",
            "Prefer federated / workload identity federation over long-lived secrets.",
            "Add secret expiry monitoring (Advisor / Key Vault + alert).",
        ],
    },
    {
        "id": "npm-401",
        "match": ["npm error", "npm.pkg.github.com"],
        "category": "auth",
        "summary": "GitHub Packages npm auth missing or invalid.",
        "remediations": [
            "Ensure NODE_AUTH_TOKEN / GITHUB_TOKEN has packages:read.",
            "Check .npmrc registry mapping for @org scope.",
            "Confirm package visibility and actor permissions.",
        ],
    },
    {
        "id": "pytest-assert",
        "match": ["AssertionError", "FAILED tests/", "short test summary"],
        "category": "test",
        "summary": "Unit/integration tests failed assertions.",
        "remediations": [
            "Inspect failing test diffs; confirm fixture data vs code change.",
            "Re-run locally with the same Python version as CI.",
            "Do not skip tests to go green without review.",
        ],
    },
]


def diagnose(parsed: dict) -> dict:
    blob = " ".join(parsed.get("errors", []) + [parsed.get("raw_tail", "")]).lower()
    matched = []
    for rule in RULES:
        hits = sum(1 for m in rule["match"] if m.lower() in blob)
        need = 1 if len(rule["match"]) == 1 else min(2, len(rule["match"]))
        if hits >= need:
            matched.append(rule)
    seen: set[str] = set()
    rules = []
    for rule in matched:
        if rule["id"] not in seen:
            seen.add(rule["id"])
            rules.append(rule)
    if not rules:
        rules = [
            {
                "id": "generic-failure",
                "category": "unknown",
                "summary": "Unrecognized failure pattern — manual triage required.",
                "remediations": [
                    "Capture failing step name, exit code, and first ERROR line.",
                    "Diff against last green commit.",
                    "Re-run with debug logging enabled.",
                ],
            }
        ]
    primary = rules[0]
    return {
        "rca": {
            "category": primary["category"],
            "summary": primary["summary"],
            "rule_ids": [r["id"] for r in rules],
            "evidence": parsed.get("errors", [])[:5],
            "shape": parsed.get("shape"),
            "source": parsed.get("source"),
            "failing_steps": parsed.get("failing_steps", []),
            "exit_codes": parsed.get("exit_codes", []),
        },
        "remediations": [
            {"action": a, "human_approval_required": True} for r in rules for a in r["remediations"]
        ],
        "human_approval_required": True,
        "auto_apply": False,
    }
