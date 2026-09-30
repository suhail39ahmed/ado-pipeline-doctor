from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .parser import parse_log
from .rca import diagnose


def _print_text(result: dict, log_path: Path) -> None:
    """Screenshot-friendly RCA summary (fixtures only — no fake metrics)."""
    rca = result.get("rca") or {}
    rems = result.get("remediations") or []
    print("ado-pipeline-doctor · RCA (offline fixtures)")
    print("-" * 56)
    print(f"  source:   {log_path}")
    print(f"  shape:    {rca.get('shape', '?')}")
    print(f"  category: {rca.get('category', '?')}")
    print(f"  summary:  {rca.get('summary', '')}")
    rules = ", ".join(rca.get("rule_ids") or []) or "(none)"
    print(f"  rules:    {rules}")
    steps = ", ".join(rca.get("failing_steps") or []) or "(unknown)"
    print(f"  steps:    {steps}")
    print("  evidence:")
    for e in (rca.get("evidence") or [])[:4]:
        line = e if len(e) <= 90 else e[:87] + "..."
        print(f"    • {line}")
    print("  remediations (human approval required):")
    for r in rems:
        action = r.get("action", "")
        flag = "✓" if r.get("human_approval_required") else "?"
        print(f"    [{flag}] {action}")
    print("-" * 56)
    print(
        f"human_approval_required={result.get('human_approval_required')}  "
        f"auto_apply={result.get('auto_apply')}"
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pipeline-doctor", description="Failed log → RCA JSON")
    p.add_argument("log_path", type=Path, help="Path to fixture or real log file")
    p.add_argument("-o", "--output", type=Path, help="Write JSON to file")
    p.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="json (default) or text (screenshot-friendly)",
    )
    args = p.parse_args(argv)

    if not args.log_path.exists():
        print(f"File not found: {args.log_path}", file=sys.stderr)
        return 2

    parsed = parse_log(args.log_path)
    result = diagnose(parsed)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {args.output}")
    elif args.format == "text":
        _print_text(result, args.log_path)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
