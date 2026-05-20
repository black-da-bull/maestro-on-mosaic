"""CLI for the Maestro Triad Validator.

Usage:
    python -m triad_validator.cli --profile v4_2_3 --triad path/to/triad.json

Exit codes:
    0  — PASS (validator returns verdict=PASS)
    1  — FAIL (one or more checks failed)
    2  — usage / input error (bad file, bad profile)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .profiles import get_profile, PROFILES
from .validator import validate_triad


def _load_triad(path: Path) -> dict[str, str | None]:
    if not path.exists():
        print(f"error: triad file not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        with path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"error: triad file is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict):
        print(
            f"error: triad file must contain a JSON object, got {type(data).__name__}",
            file=sys.stderr,
        )
        sys.exit(2)
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="triad-validator",
        description="Validate a Maestro Triad against a version profile.",
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=sorted(PROFILES.keys()),
        help="Maestro version profile to validate against.",
    )
    parser.add_argument(
        "--triad",
        required=True,
        type=Path,
        help="Path to a JSON file containing the Triad payload.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the audit JSON; defaults to stdout.",
    )
    args = parser.parse_args(argv)

    triad = _load_triad(args.triad)
    profile = get_profile(args.profile)
    result = validate_triad(triad, profile)
    audit = result.to_e2e_json()

    audit_json = json.dumps(audit, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(audit_json + "\n", encoding="utf-8")
    else:
        print(audit_json)

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
