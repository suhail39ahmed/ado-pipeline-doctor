from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .parser import parse_log
from .rca import diagnose


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pipeline-doctor", description="Failed log → RCA JSON")
    p.add_argument("log_path", type=Path, help="Path to fixture or real log file")
    p.add_argument("-o", "--output", type=Path, help="Write JSON to file")
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
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
