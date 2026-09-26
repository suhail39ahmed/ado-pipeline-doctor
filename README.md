# ado-pipeline-doctor

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-0.1.0%20MVP-green.svg)

**Failed Azure Pipelines / GitHub Actions logs → structured RCA JSON. Remediations always require human approval.**

> Who it's for: DevOps / platform SAs who triage ADO and GHA failures daily.

## Why this exists

Red builds burn SA time. This doctor turns fixture (or real) failure logs into **root-cause hypotheses + remediations** with an explicit `human_approval_required: true` flag — safe to wire into an agent skill without auto-patching production YAML.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Or with pipx (once published to PyPI): `pipx install ado-pipeline-doctor` — until then use editable install from this repo.

## 30-second demo

```bash
python -m pipeline_doctor --help
python -m pipeline_doctor fixtures/azure-pipelines/nuget-auth-fail.log
python -m pipeline_doctor fixtures/github-actions/pytest-fail.log -o out/rca.json
```

Or simply:

```bash
make demo
```

## What it is NOT

- Not an auto-healer that edits pipelines without approval
- Not a replacement for App Insights / proper incident process
- Not a hosted SaaS — offline CLI + skill docs

## Architecture

![Architecture](assets/architecture.svg)

## Roadmap

- [ ] More rule packs (npm cache, NuGet, service connections, OIDC)
- [ ] Optional LLM explain layer behind the same JSON schema
- [ ] ADO REST adapter (read-only) behind a feature flag

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Be kind — [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md). Security reports: [SECURITY.md](./SECURITY.md).

## License

MIT
