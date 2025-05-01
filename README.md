# German Verbs

A Python package for working with German verb data.

## Installation

You can install the package using uv:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On Windows:
# .venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install the package
uv pip install -e .
```

Or using pip:

```bash
pip install -e .
```

## Usage

### Command Line

List all available verbs:
```bash
german-verbs list
```

Get a verb by ID:
```bash
german-verbs get-by-id 1
```

Get a verb by infinitive:
```bash
german-verbs get beginnen
```

### Converting YAML to Markdown

There are several ways to convert YAML files to Markdown:

#### Using uv run (Recommended)

The most reliable way to run the conversion script:

```bash
# Convert a specific YAML file
uv run yaml2md verben/irregular-verbs-a1.yaml

# Specify a custom output directory
uv run yaml2md verben/irregular-verbs-a1.yaml -o path/to/output
```

#### Using the installed script

If the package is properly installed with entry points:

```bash
yaml2md verben/irregular-verbs-a1.yaml
```

#### Using the german-verbs CLI

```bash
# Convert a specific file
german-verbs convert-to-md verben/irregular-verbs-a1.yaml

# Convert all YAML files
german-verbs convert-all
```

### Python API

```python
from german_verbs.verbs import get_verb_by_infinitive, format_verb_display
from german_verbs.converter import yaml_to_markdown

# Get data for "beginnen"
verb = get_verb_by_infinitive("beginnen")

# Display formatted info
print(format_verb_display(verb))

# Convert a file
yaml_to_markdown("verben/irregular-verbs-a1.yaml", "verben/generated")
```

## Project Structure

- `verben/`: Contains the raw verb data files (YAML, MD)
- `verben/generated/`: Contains generated output files
- `german_verbs/`: Python package with code for working with verb data 