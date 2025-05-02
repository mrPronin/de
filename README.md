# German Verbs

A Python package for working with German verb data.

## Installation

You can install the package using uv (recommended):

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On Windows:
# .venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install the package in development mode
uv pip install -e .
```

Or using standard pip:

```bash
pip install -e .
```

## Usage

### Interactive Learning

Practice your German irregular verbs with the interactive learning script:

```bash
# Run directly after installation
learn-verbs

# Or specify a custom YAML file
learn-verbs verben/irregular-verbs-a1.yaml

# Using uv run (if you haven't installed the package)
uv run -m german_verbs.learn verben/irregular-verbs-a1.yaml
```

Options:

```bash
# Limit the number of questions
learn-verbs --question-limit 10

# Practice a specific type of question
learn-verbs --mode infinitive  # From infinitive to other forms
learn-verbs --mode prateritum  # From präteritum to other forms
learn-verbs --mode partizip    # From partizip to other forms
learn-verbs --mode english     # From English translation
learn-verbs --mode ukrainian   # From Ukrainian translation
```

When answering questions, you can:
- Type the correct answer
- Type `?` to see help about the current verb

### Command Line Tools

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

#### Using the installed script

```bash
# Convert a specific YAML file
yaml2md verben/irregular-verbs-a1.yaml

# Specify a custom output directory
yaml2md verben/irregular-verbs-a1.yaml -o path/to/output
```

#### Using the german-verbs CLI

```bash
# Convert a specific file
german-verbs convert-to-md verben/irregular-verbs-a1.yaml

# Convert all YAML files
german-verbs convert-all
```

## Project Structure

- `verben/`: Contains the raw verb data files (YAML)
- `verben/generated/`: Contains generated output files (MD)
- `german_verbs/`: Python package with code for working with verb data 