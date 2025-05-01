"""Command-line interface for german_verbs."""

import click
from pathlib import Path

from german_verbs.converter import markdown_to_yaml, yaml_to_markdown
from german_verbs.verbs import (
    format_verb_display,
    get_verb_by_id,
    get_verb_by_infinitive,
    list_all_verbs,
    load_verb_data,
)


@click.group()
def main():
    """German Verbs - CLI tool for working with German verb data."""
    pass


@main.command()
@click.argument("verb_id", type=int)
@click.option(
    "--file", "-f",
    help="YAML file to use",
    default="irregular-verbs-a1.yaml"
)
def get_by_id(verb_id, file):
    """Get a verb by its ID."""
    try:
        data = load_verb_data(file)
        verb = get_verb_by_id(verb_id, data)
        click.echo(format_verb_display(verb))
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    return 0


@main.command()
@click.argument("infinitive")
@click.option(
    "--file", "-f",
    help="YAML file to use",
    default="irregular-verbs-a1.yaml"
)
def get(infinitive, file):
    """Get a verb by its infinitive form."""
    try:
        data = load_verb_data(file)
        verb = get_verb_by_infinitive(infinitive, data)
        click.echo(format_verb_display(verb))
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    return 0


@main.command()
@click.option(
    "--file", "-f",
    help="YAML file to use",
    default="irregular-verbs-a1.yaml"
)
def list(file):
    """List all verbs."""
    try:
        data = load_verb_data(file)
        verbs = list_all_verbs(data)

        for verb in verbs:
            output = f"{verb['id']}: {verb['infinitiv']} - "
            output += verb['translations']['english']
            click.echo(output)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        return 1

    return 0


@main.command()
@click.argument("yaml_file")
@click.option(
    "--output-dir", "-o",
    help="Output directory for the generated file"
)
def convert_to_md(yaml_file, output_dir):
    """Convert a YAML file to a Markdown table."""
    try:
        # If the yaml_file doesn't contain a full path,
        # look in the verben directory
        has_no_path = (not yaml_file.startswith('/') and
                       not yaml_file.startswith('./'))
        if has_no_path:
            verben_path = Path("verben")
            yaml_path = verben_path / yaml_file
            if yaml_path.exists():
                yaml_file = str(yaml_path)

        # Default output directory to verben/generated if not specified
        if not output_dir:
            output_dir = "verben/generated"

        output_path = yaml_to_markdown(yaml_file, output_dir)
        click.echo(f"Generated Markdown file: {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    return 0


@main.command()
@click.argument("md_file")
@click.option(
    "--output-dir", "-o",
    help="Output directory for the generated file"
)
def convert_to_yaml(md_file, output_dir):
    """Convert a Markdown table to a YAML file."""
    try:
        output_path = markdown_to_yaml(md_file, output_dir)
        click.echo(f"Generated YAML file: {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    return 0


@main.command()
@click.option(
    "--output-dir",
    "-o",
    help="Output directory for the generated files",
    default="verben/generated"
)
def convert_all(output_dir):
    """Convert all YAML files in the verben directory to Markdown."""
    try:
        verben_dir = Path("verben")
        if not verben_dir.exists():
            click.echo("Error: 'verben' directory not found.", err=True)
            return 1

        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Find all YAML files in the verben directory
        yaml_files = list(verben_dir.glob("*.yaml"))
        if not yaml_files:
            click.echo("No YAML files found in the 'verben' directory.")
            return 0

        # Convert each file
        for yaml_file in yaml_files:
            try:
                output_file = yaml_to_markdown(str(yaml_file), output_dir)
                click.echo(f"Generated: {output_file}")
            except Exception as e:
                click.echo(
                    f"Error converting {yaml_file}: {e}",
                    err=True
                )

        click.echo(f"Converted {len(yaml_files)} files to Markdown.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    return 0


if __name__ == "__main__":
    main()
