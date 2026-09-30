# Demo — ado-pipeline-doctor

Honest, fixture-only demos. Remediations always carry `human_approval_required: true`. No fabricated metrics.

## Static preview (README)

![30-second demo](../assets/demo-terminal.svg)

```bash
pip install -e .
make demo-assets   # regenerates assets/demo-terminal.svg from fixtures
```

---

## Timed Loom script (60–90 seconds)

| Time | On screen | Say |
|------|-----------|-----|
| 0:00–0:10 | Repo root | "ado-pipeline-doctor — failed Azure Pipelines or GitHub Actions logs into structured RCA JSON. Remediations never auto-apply." |
| 0:10–0:40 | `--format text` on `fixtures/azure-pipelines/nuget-auth-fail.log` | "Fixture NuGet 401. Category auth, rule nuget-401, evidence lines from the log, three remediations each flagged human approval required." |
| 0:40–1:05 | GHA pytest fixture | "Same shape for GitHub Actions. Offline fixtures — safe to wire into an agent skill without patching production YAML." |
| 1:05–1:20 | Optional: open JSON briefly | "Default output is JSON for agents; `--format text` for screenshots." |
| 1:20–1:30 | Outro | "`make demo`. Clone and try your own sanitized log." |

### Exact commands

```bash
cd ado-pipeline-doctor
python -m venv .venv && source .venv/bin/activate
pip install -e .
# font ~16–18pt; dark theme; no real secrets on screen

python -m pipeline_doctor --format text fixtures/azure-pipelines/nuget-auth-fail.log
python -m pipeline_doctor --format text fixtures/github-actions/pytest-fail.log
make demo
```

### Talking points (pick 2)

- Who it's for: DevOps / platform SAs who triage ADO and GHA failures daily.
- What it is NOT: not an auto-healer; not App Insights; not SaaS.
- Safety: `human_approval_required: true` / `auto_apply: false` on every remediation.

### Outro card

`github.com/suhail39ahmed/ado-pipeline-doctor`

---

## GIF / screenshot crop tips

- Crop to terminal only; pause on the remediations block (the approval flags are the punchline).
- Still frames: (1) NuGet 401 summary, (2) remediations with `[✓]`, (3) GHA pytest category line.
- Optional later: `assets/demo.gif` via Kap / Peek / asciinema+agg.

---

## LinkedIn caption draft (manual — do not auto-post)

Red builds burn SA time. I open-sourced **ado-pipeline-doctor**:

Failed ADO / GHA logs → structured RCA JSON  
Remediations always require human approval (`auto_apply: false`)  
`make demo` on offline fixtures — no cloud needed  

Not an auto-healer. A safe pattern for agent skills that *propose* fixes.

→ https://github.com/suhail39ahmed/ado-pipeline-doctor  

#AzureDevOps #GitHubActions #DevOps #SRE #OpenSource

---

## Shot list (3 frames)

1. NuGet auth fail — category + summary  
2. Remediations block with `human_approval_required`  
3. GHA pytest fixture summary  

---

## CI workflow (install once)

OAuth tokens without `workflow` scope cannot push `.github/workflows/*`. YAML: [`docs/ci/demo.yml`](./ci/demo.yml).

```bash
mkdir -p .github/workflows && cp docs/ci/demo.yml .github/workflows/demo.yml
git add .github/workflows/demo.yml && git commit -m "ci: enable make demo workflow" && git push
```
