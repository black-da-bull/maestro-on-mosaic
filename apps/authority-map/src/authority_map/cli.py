"""Authority Map command-line interface.

Subcommands:

  am list                     # one-line summary of every row
  am show <claim_substring>   # full row(s) matching the substring
  am validate                 # exit non-zero on any structural error
  am scope <plane>            # rows filtered by scope plane

The default seed file is resolved relative to the package, but can be
overridden with --seed or the AUTHORITY_MAP_SEED env var.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

from authority_map.loader import AuthorityMapLoadError, load_authority_map
from authority_map.schema import AuthorityMap, ScopePlane
from authority_map.validator import validate_authority_map


# Default seed location: apps/authority-map/seed/authority_map_v0.1_seed.yaml
# relative to this file's parent directories.
def _default_seed_path() -> Path:
    here = Path(__file__).resolve()
    # __file__       = apps/authority-map/src/authority_map/cli.py
    # parents[0]     = .../src/authority_map/
    # parents[1]     = .../src/
    # parents[2]     = apps/authority-map/   <-- package root
    return here.parents[2] / "seed" / "authority_map_v0.1_seed.yaml"


def _resolve_seed(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    env = os.environ.get("AUTHORITY_MAP_SEED")
    if env:
        return Path(env)
    return _default_seed_path()


def _row_dict(row) -> dict:
    """Serialize a row dataclass for JSON output."""
    return {
        "claim_or_artifact": row.claim_or_artifact,
        "scope_plane": row.scope_plane.value,
        "source_class": row.source_class_label(),
        "authority_tier": row.authority_tier.value,
        "current_status": row.current_status,
        "promotion_requirement": row.promotion_requirement,
        "blocking_reason": row.blocking_reason,
        "downstream_risk_if_promoted_early": (
            row.downstream_risk_if_promoted_early
        ),
        "recommended_next_action": row.recommended_next_action,
    }


def cmd_list(args: argparse.Namespace, amap: AuthorityMap) -> int:
    if args.json:
        print(json.dumps([_row_dict(r) for r in amap.rows], indent=2))
        return 0
    print(
        f"Authority Map v{amap.version} ({amap.generated_at}) "
        f"— {len(amap.rows)} rows"
    )
    for i, row in enumerate(amap.rows):
        print(
            f"  [{i:2d}] {row.scope_plane.value:30s} "
            f"{row.source_class_label():15s} "
            f"{row.authority_tier.value:22s} "
            f"{row.claim_or_artifact}"
        )
    return 0


def cmd_show(args: argparse.Namespace, amap: AuthorityMap) -> int:
    matches = amap.find(args.claim)
    if not matches:
        print(f"no rows match {args.claim!r}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps([_row_dict(r) for r in matches], indent=2))
        return 0
    for row in matches:
        print(f"\n=== {row.claim_or_artifact} ===")
        print(f"  scope_plane    : {row.scope_plane.value}")
        print(f"  source_class   : {row.source_class_label()}")
        print(f"  authority_tier : {row.authority_tier.value}")
        print(f"  current_status : {row.current_status}")
        print(f"  promotion_req  : {row.promotion_requirement}")
        print(f"  blocking_reason: {row.blocking_reason}")
        print(f"  downstream_risk: {row.downstream_risk_if_promoted_early}")
        print(f"  next_action    : {row.recommended_next_action}")
    return 0


def cmd_scope(args: argparse.Namespace, amap: AuthorityMap) -> int:
    try:
        plane = ScopePlane(args.plane)
    except ValueError:
        valid = ", ".join(p.value for p in ScopePlane)
        print(f"unknown scope plane {args.plane!r}; expected one of: {valid}",
              file=sys.stderr)
        return 2
    rows = amap.by_scope(plane)
    if args.json:
        print(json.dumps([_row_dict(r) for r in rows], indent=2))
        return 0
    print(f"{plane.value} — {len(rows)} rows")
    for row in rows:
        print(f"  - {row.claim_or_artifact}  ({row.authority_tier.value})")
    return 0


def cmd_validate(args: argparse.Namespace, amap: AuthorityMap) -> int:
    report = validate_authority_map(amap)
    if args.json:
        print(
            json.dumps(
                {
                    "version": report.map_version,
                    "passed": report.passed,
                    "errors": [asdict(i) for i in report.errors],
                    "warnings": [asdict(i) for i in report.warnings],
                },
                indent=2,
            )
        )
    else:
        if report.passed:
            print(
                f"PASS  Authority Map v{report.map_version}: "
                f"{len(amap.rows)} rows, no issues."
            )
        else:
            print(
                f"FAIL  Authority Map v{report.map_version}: "
                f"{len(report.errors)} errors, "
                f"{len(report.warnings)} warnings."
            )
            for issue in report.issues:
                print(
                    f"  {issue.severity:7s}  row #{issue.row_index}  "
                    f"{issue.field_name}: {issue.message}"
                )
    return 0 if report.passed else 1


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="am",
        description="Maestro Authority Map — canon-governance CLI.",
    )
    p.add_argument(
        "--seed",
        help="path to the Authority Map seed YAML (defaults to bundled)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="emit JSON instead of human-readable output",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list all rows")
    sub.add_parser("validate", help="run structural validation")

    show = sub.add_parser("show", help="show row(s) matching a substring")
    show.add_argument("claim", help="case-insensitive substring of claim_or_artifact")

    scope = sub.add_parser("scope", help="filter rows by scope plane")
    scope.add_argument(
        "plane",
        help="one of PROJECT_MAESTRO, WORKSPACE_DEV, BRIDGE_PROJECT_WORKSPACE, UNRESOLVED_SCOPE",
    )

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    seed_path = _resolve_seed(args.seed)
    try:
        amap = load_authority_map(seed_path)
    except AuthorityMapLoadError as exc:
        print(f"load error: {exc}", file=sys.stderr)
        return 2

    dispatch = {
        "list": cmd_list,
        "show": cmd_show,
        "scope": cmd_scope,
        "validate": cmd_validate,
    }
    return dispatch[args.cmd](args, amap)


if __name__ == "__main__":
    raise SystemExit(main())
