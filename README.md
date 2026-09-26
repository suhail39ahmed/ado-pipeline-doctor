# ado-pipeline-doctor

CLI + skill: parse failed **Azure Pipelines** / **GitHub Actions** logs → **RCA JSON** + suggested remediations. Every remediation is flagged `human_approval_required: true`.

## What it is
- Offline rule-based doctor over fixture logs
- Supports ADO and GHA log shapes (2 fixtures each)

## What it is not
- Not an auto-healer that patches pipelines without approval
- Not a replacement for proper observability / incident process

## Architecture

```
  log file --> parser (shape detect) --> RCA rules --> JSON
                                              |
                                              +--> human_approval_required: true
```

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m pipeline_doctor.cli fixtures/azure-pipelines/nuget-auth-fail.log
python -m pipeline_doctor.cli fixtures/github-actions/pytest-fail.log -o out/rca.json
```

## Demo assets checklist
- [ ] `assets/demo.gif`
- [ ] `assets/architecture.png`
- [ ] `docs/DEMO.md`

## License
MIT
