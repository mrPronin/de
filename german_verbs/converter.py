"""Module for converting between YAML and Markdown formats."""

import sys
from pathlib import Path

import yaml

from german_verbs.verbs import load_verb_data


def yaml_to_markdown(yaml_file: str, output_dir: str = None) -> str:
    """Convert a YAML verb file to Markdown format.

    Args:
        yaml_file: Path to the YAML file to convert.
        output_dir: Optional directory to write the output file.

    Returns:
        Path to the generated Markdown file.
    """
    # Load the YAML data
    data = load_verb_data(yaml_file)

    # Create the Markdown content
    md_lines = []

    # Add the title
    md_lines.append(f"# {data['title']}")
    md_lines.append("")

    # Create the table header
    header = "| N  | Infinitiv (3rd Person Singular) | Präteritum | "
    header += "Partizip II | Übersetzung | Beispiele |"
    md_lines.append(header)
    md_lines.append("|----|---------------------------------|------------|"
                    "-------------|-------------|-----------|")

    # Add each verb to the table
    for verb in data["verbs"]:
        # Format translations
        english = verb['translations']['english']
        ukrainian = verb['translations']['ukrainian']
        translations = f"{english} / {ukrainian}"

        # Use examples directly (now a simple string)
        examples = verb.get("examples", "").replace(";", "<br>").strip()

        # Add the verb row
        prefix = f"| {verb['id']} | {verb['infinitiv']} ({verb['person3']}) | "
        suffix = f"{verb['präteritum']} | {verb['partizip']} | "
        translations = f"{translations}"
        row = f"{prefix}{suffix}{translations} | {examples} |"
        md_lines.append(row)

    # Join the lines to create the full Markdown content
    md_content = "\n".join(md_lines)

    # Determine output filename
    base_name = Path(yaml_file).stem
    output_filename = f"{base_name}.md"

    if output_dir:
        # Ensure the output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = Path(output_dir) / output_filename
    else:
        # Default to the "generated" subdirectory of where the YAML file is
        yaml_dir = Path(yaml_file).parent
        output_dir = yaml_dir / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename

    # Write the content to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return str(output_path)


def markdown_to_yaml(md_file: str, output_dir: str = None) -> str:
    """Convert a Markdown verb file to YAML format.

    Note: This is a more complex operation and requires parsing Markdown
    tables. This implementation is simplified and may not handle
    all edge cases.

    Args:
        md_file: Path to the Markdown file to convert.
        output_dir: Optional directory to write the output file.

    Returns:
        Path to the generated YAML file.
    """
    # Read the Markdown file
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Split the content into lines
    lines = md_content.strip().split("\n")

    # Extract the title (first line starting with #)
    title = ""
    for line in lines:
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            break

    # Find the table rows
    table_rows = []
    in_table = False
    for line in lines:
        if line.startswith("|") and "---" not in line:
            if not in_table and "Infinitiv" in line:
                # This is the header row
                in_table = True
                continue
            if in_table and line.strip():
                table_rows.append(line)

    # Parse table rows into verb dictionaries
    verbs = []
    for i, row in enumerate(table_rows):
        # Split the row into cells, removing the first and last empty cells
        cells = [cell.strip() for cell in row.split("|")[1:-1]]

        if len(cells) < 5:
            continue  # Skip rows with insufficient data

        # Extract the verb ID
        verb_id = int(cells[0])

        # Extract infinitive and 3rd person singular
        infinitiv_cell = cells[1]
        if "(" in infinitiv_cell and ")" in infinitiv_cell:
            infinitiv = infinitiv_cell.split("(")[0].strip()
            person3 = infinitiv_cell.split("(")[1].split(")")[0].strip()
        else:
            infinitiv = infinitiv_cell
            person3 = ""

        # Extract präteritum and partizip
        präteritum = cells[2]
        partizip = cells[3]

        # Extract translations
        translations_cell = cells[4]
        if "/" in translations_cell:
            english = translations_cell.split("/")[0].strip()
            ukrainian = translations_cell.split("/")[1].strip()
        else:
            english = translations_cell
            ukrainian = ""

        # Extract examples as a simple string
        examples = ""
        if len(cells) > 5:
            # Replace <br> with semicolons for the simplified format
            examples = cells[5].replace("<br>", ";")

        # Create the verb dictionary
        verb = {
            "id": verb_id,
            "infinitiv": infinitiv,
            "person3": person3,
            "präteritum": präteritum,
            "partizip": partizip,
            "translations": {
                "english": english,
                "ukrainian": ukrainian
            },
            "examples": examples
        }

        verbs.append(verb)

    # Create the complete data structure
    data = {
        "title": title,
        "verbs": verbs
    }

    # Determine output filename
    base_name = Path(md_file).stem
    output_filename = f"{base_name}.yaml"

    if output_dir:
        # Ensure the output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = Path(output_dir) / output_filename
    else:
        # Default to the same directory as the Markdown file
        output_path = Path(md_file).parent / output_filename

    # Write the content to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=120)

    return str(output_path)


def yaml_to_md_cli():
    """CLI entry point for the yaml2md command."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert German verb YAML files to Markdown"
    )
    parser.add_argument("yaml_file", help="Path to the YAML file to convert")
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory (default: verben/generated)",
        default="verben/generated"
    )

    args = parser.parse_args()

    try:
        output_path = yaml_to_markdown(args.yaml_file, args.output_dir)
        print(f"Generated Markdown file: {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(yaml_to_md_cli())
