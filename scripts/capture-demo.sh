#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="${1:-assets/demo-terminal.svg}"
CAPT="$(mktemp)"; trap 'rm -f "$CAPT"' EXIT
{
  echo '$ python -m pipeline_doctor --format text fixtures/azure-pipelines/nuget-auth-fail.log'
  python -m pipeline_doctor --format text fixtures/azure-pipelines/nuget-auth-fail.log
  echo
  echo '$ python -m pipeline_doctor --format text fixtures/github-actions/pytest-fail.log'
  python -m pipeline_doctor --format text fixtures/github-actions/pytest-fail.log
} > "$CAPT"
python3 - "$CAPT" "$OUT" << 'PY'
import html, sys
from pathlib import Path
capture = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
out_path = Path(sys.argv[2])

def kind_for(line: str) -> str:
    if line.startswith("$ "): return "prompt"
    if line.startswith("----") or line.startswith("  evidence") or line.startswith("    •") or line.startswith("  remediations"): return "dim"
    if line.startswith("    [") or "human_approval_required=" in line: return "ok"
    if not line.strip(): return "blank"
    return "out"

colors = {"prompt":"#7dd3fc","out":"#e2e8f0","dim":"#94a3b8","ok":"#86efac","blank":"#e2e8f0"}
row_h, pad_top, pad_left, width = 18, 56, 18, 940
height = pad_top + 20 + max(len(capture),1)*row_h + 24
parts = [
 '<?xml version="1.0" encoding="UTF-8"?>',
 f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
 '  <defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#020617"/></linearGradient></defs>',
 f'  <rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/>',
 '  <rect x="0" y="0" width="940" height="36" rx="12" fill="#1e293b"/><rect x="0" y="24" width="940" height="12" fill="#1e293b"/>',
 '  <circle cx="22" cy="18" r="6" fill="#f87171"/><circle cx="42" cy="18" r="6" fill="#fbbf24"/><circle cx="62" cy="18" r="6" fill="#4ade80"/>',
 '  <text x="470" y="22" text-anchor="middle" fill="#cbd5e1" font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">ado-pipeline-doctor · offline fixtures · make demo</text>',
]
y = pad_top
for line in capture:
    k = kind_for(line)
    if k == "blank":
        y += row_h; continue
    text = line if len(line)<=115 else line[:112]+"..."
    parts.append(f'  <text x="{pad_left}" y="{y}" fill="{colors[k]}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12.5" font-weight="{"600" if k=="prompt" else "400"}">{html.escape(text)}</text>')
    y += row_h
parts.append("</svg>")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text("\n".join(parts)+"\n", encoding="utf-8")
print(f"wrote {out_path}")
PY
