#!/usr/bin/env python3
"""Renumber verb IDs sequentially in a verbs YAML file.

Use this after manually adding or removing verbs to fix gaps/duplicates.

Usage:
    python scripts/renumber_yaml.py [YAML_FILE]

Defaults to verben/irregular-verbs-a1.yaml if no file is given.
Supports multiple files separated by spaces.
"""

import re
import sys
from pathlib import Path

DEFAULT_FILE = "verben/irregular-verbs-a1.yaml"


def renumber_yaml(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    
    in_verbs_list = False
    counter = 0
    new_lines = []
    
    for line in lines:
        # Detect start of verbs list
        if re.match(r"^verbs:", line):
            in_verbs_list = True
            new_lines.append(line)
            continue
        
        # Detect end of verbs list (next top-level key or EOF)
        if in_verbs_list and re.match(r"^[a-zA-Z_]", line):
            in_verbs_list = False
            
        # Renumber id fields inside the verbs list
        if in_verbs_list:
            match = re.match(r"^(\s*-\s+)id:\s*\d+(\s*)$", line)
            if match:
                counter += 1
                line = f"{match.group(1)}id: {counter}{match.group(2)}"
        
        new_lines.append(line)
    
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Renumbered {counter} verbs in {path}")


def main():
    files = sys.argv[1:] or [DEFAULT_FILE]
    for f in files:
        p = Path(f)
        if not p.exists():
            print(f"Not found: {f}", file=sys.stderr)
            sys.exit(1)
        renumber_yaml(p)


if __name__ == "__main__":
    main()
