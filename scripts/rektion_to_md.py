#!/usr/bin/env python3
"""Generate the Rektion Markdown table from its YAML source.

Renders one section per case (Akk, then Dat): heading, rules, optional note,
and a table numbered from 1 within the section. Angle brackets are escaped
(`<Akk>` -> `\\<Akk\\>`), an entry's `note` is appended to the verb cell
after `<br><br>`, and its `example` list fills the Beispiele column joined
by `<br>`, matching the conventions in german_verbs/converter.py.

Usage:
    python scripts/rektion_to_md.py [YAML_FILE] [-o MD_FILE]

Defaults to verben/rektion/verben-mit-prapositionen.yaml ->
verben/verben-mit-prapositionen.md.
"""

import argparse
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_YAML = PROJECT_ROOT / "verben/rektion/verben-mit-prapositionen.yaml"
DEFAULT_MD = PROJECT_ROOT / "verben/verben-mit-prapositionen.md"
CASES = ["Akk", "Dat"]


def escape(text: str) -> str:
    return text.replace("<", "\\<").replace(">", "\\>")


def render(data: dict) -> str:
    rules = data.get("rules", {})
    notes = data.get("notes", {})
    verbs = data["verbs"]

    unknown = {v["case"] for v in verbs} - set(CASES)
    if unknown:
        raise ValueError(f"unknown case(s): {sorted(unknown)}")

    out = [f"# {data['title']}", ""]
    for case in CASES:
        out += [f"## Verb + Präposition + {case}", ""]
        if rules.get(case):
            out += list(rules[case]) + [""]
        if notes.get(case):
            out += notes[case].rstrip("\n").split("\n") + [""]
        out += [
            "| N | Präposition | Verb | Übersetzung ua | Übersetzung en | Beispiele |",
            "|---|---|---|---|---|---|",
        ]
        rows = [v for v in verbs if v["case"] == case]
        for n, v in enumerate(rows, start=1):
            verb = escape(v["verb"])
            if v.get("note"):
                verb += "<br><br>" + escape(v["note"])
            t = v.get("translations", {})
            examples = "<br>".join(escape(x) for x in v.get("example", []))
            out.append(
                f"| {n} | {v['präposition']} | {verb} | "
                f"{escape(t.get('ukrainian', ''))} | {escape(t.get('english', ''))} | "
                f"{examples} |"
            )
        out.append("")
    return "\n".join(out[:-1]) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("yaml_file", nargs="?", type=Path, default=DEFAULT_YAML)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    with open(args.yaml_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    try:
        md = render(data)
    except (KeyError, ValueError) as exc:
        print(f"{args.yaml_file}: {exc}", file=sys.stderr)
        return 1

    args.output.write_text(md, encoding="utf-8")
    print(f"Wrote {args.output} ({len(data['verbs'])} verbs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
