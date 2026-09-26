# Skill: ado-pipeline-doctor

## Purpose
Turn failed Azure Pipelines / GitHub Actions logs into structured RCA JSON with remediations that **always** require human approval.

## When to use
- A CI job is red and you need a first-pass diagnosis.
- Demo / offline triage using `fixtures/`.

## Inputs
- Path to a log file (`.log` text)

## Outputs
- JSON: `rca`, `remediations[]` each with `human_approval_required: true`, `auto_apply: false`

## Guardrails
- Never apply fixes automatically.
- Never print secrets; logs may already redact them as `***`.
