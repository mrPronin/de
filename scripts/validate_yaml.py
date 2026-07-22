#!/usr/bin/env python3
"""Validate YAML files in the verben/ directory."""

import argparse
import sys
from pathlib import Path

import yaml


def validate_yaml(filepath: Path) -> list[str]:
    """Parse a YAML file and return any errors found."""
    errors: list[str] = []
    try:
        with open(filepath, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        errors.append(f"{filepath}: {exc}")
        return errors

    # Basic sanity checks
    if data is None:
        errors.append(f"{filepath}: file is empty")
        return errors
    if not isinstance(data, dict):
        errors.append(f"{filepath}: expected a mapping at root level")
        return errors

    if "title" not in data:
        errors.append(f"{filepath}: missing 'title' key")

    if "verbs" not in data:
        errors.append(f"{filepath}: missing 'verbs' key")
    else:
        verbs = data["verbs"]
        if not isinstance(verbs, list):
            errors.append(f"{filepath}: 'verbs' must be a list")
        else:
            expected_keys = {"id", "level", "infinitiv", "präteritum", "partizip", "translations"}
            seen_ids: set[int] = set()
            for i, verb in enumerate(verbs, start=1):
                if not isinstance(verb, dict):
                    errors.append(f"{filepath} verb #{i}: expected a mapping")
                    continue
                missing = expected_keys - verb.keys()
                if missing:
                    errors.append(f"{filepath} verb #{i}: missing keys {sorted(missing)}")
                if "id" in verb:
                    vid = verb["id"]
                    if not isinstance(vid, int):
                        errors.append(f"{filepath} verb #{i}: 'id' must be an integer")
                    elif vid in seen_ids:
                        errors.append(f"{filepath} verb #{i}: duplicate 'id' = {vid}")
                    else:
                        seen_ids.add(vid)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate YAML verb files in the verben/ directory."
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="YAML files to validate. If omitted, validates verben/*.yaml",
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    verben = project_root / "verben"

    if not args.files:
        files = sorted(verben.glob("*.yaml"))
        if not files:
            print(f"No .yaml files found in {verben}", file=sys.stderr)
            return 1
    else:
        files = [Path(f) for f in args.files]

    all_errors: list[str] = []
    for f in files:
        errs = validate_yaml(f)
        if errs:
            print(f"\n{'=' * 60}")
            print(f"❌ {f.name}")
            print(f"{'=' * 60}")
            for err in errs:
                print(f"   • {err}")
            all_errors.append(err)

    if all_errors:
        print(f"\n{len(all_errors)} error(s) found.")
        return 1
    else:
        print("✅ All YAML files are valid.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
