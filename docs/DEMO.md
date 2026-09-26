# Demo — ado-pipeline-doctor

Loom / screen recording script (**60–90 seconds**). Speak calmly; show the terminal, not slides.

## Setup (before record)

```bash
cd ado-pipeline-doctor
python -m venv .venv && source .venv/bin/activate
pip install -e .
# clear scrollback; font size ~16–18pt; dark theme
```

## Exact click / type script

1. Open terminal at repo root. Say: *"This is ado-pipeline-doctor — Failed Azure Pipelines / GitHub Actions logs → structured RCA JSON. Remediations…"*
2. Type `make demo` **or** walk the commands below one by one.
1. Run `python -m pipeline_doctor --help` — wait for JSON / output.
2. Run `python -m pipeline_doctor fixtures/azure-pipelines/nuget-auth-fail.log` — wait for JSON / output.
3. Run `python -m pipeline_doctor fixtures/github-actions/pytest-fail.log -o out/rca.json` — wait for JSON / output.
3. Scroll the JSON briefly. Call out one concrete field (citation path, `human_approval_required`, findings, report path, etc.).
4. Close with: *"Offline fixtures only — clone it, `make demo`, adopt the pattern."* Link the GitHub repo in the Loom description.

## Talking points (pick 2)

- Who it's for: DevOps / platform SAs who triage ADO and GHA failures daily.
- What it is NOT: Not an auto-healer that edits pipelines without approval
- Honest MVP: no fabricated production metrics

## Outro card (last 3s)

`github.com/suhail39ahmed/ado-pipeline-doctor`
