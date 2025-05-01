#!/usr/bin/env python3
"""
Quick script to convert YAML to Markdown.
Run this from the command line to convert all YAML files to Markdown.
"""

from pathlib import Path
from german_verbs.converter import yaml_to_markdown


def main():
    """Convert all YAML files in verben directory to Markdown."""
    verben_dir = Path("verben")
    output_dir = verben_dir / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    yaml_files = list(verben_dir.glob("*.yaml"))
    print(f"Found {len(yaml_files)} YAML files.")
    
    for yaml_file in yaml_files:
        try:
            output_file = yaml_to_markdown(str(yaml_file), str(output_dir))
            print(f"Generated: {output_file}")
        except Exception as e:
            print(f"Error converting {yaml_file}: {e}")
    
    print("Conversion complete.")


if __name__ == "__main__":
    main() 