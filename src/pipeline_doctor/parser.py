"""Parse Azure Pipelines and GitHub Actions-ish failure logs into structured signals."""
from __future__ import annotations

import re
from pathlib import Path

ADO_ERROR = re.compile(r"##\[error\]\s*(.+)", re.I)
GHA_ERROR = re.compile(r"(?:##\[error\]|Error:|npm error|AssertionError|FAILED)\s*(.+)", re.I)
STEP_ADO = re.compile(r"##\[section\](?:Starting|Finishing):\s*(.+)", re.I)
EXIT_CODE = re.compile(r"exit code(?:\()?['\"]?(\d+)", re.I)


def detect_shape(text: str) -> str:
    if "##[section]" in text or "NuGetCommand" in text or "AzureResourceManager" in text:
        return "azure-pipelines"
    if "##[group]" in text or "Process completed with exit code" in text or "/home/runner/" in text:
        return "github-actions"
    return "unknown"


def parse_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    shape = detect_shape(text)
    errors: list[str] = []
    for rx in (ADO_ERROR, GHA_ERROR):
        for m in rx.finditer(text):
            msg = m.group(1).strip()
            if msg and msg not in errors:
                errors.append(msg)
    steps = [m.group(1).strip() for m in STEP_ADO.finditer(text)]
    exit_codes = [int(m.group(1)) for m in EXIT_CODE.finditer(text)]
    return {
        "source": str(path),
        "shape": shape,
        "failing_steps": steps[-4:] if steps else [],
        "errors": errors[:8],
        "exit_codes": exit_codes[-3:],
        "raw_tail": "\n".join(text.strip().splitlines()[-15:]),
    }
