# German Verbs

A Python package for learning German irregular verbs using interactive practice.

## Installation

Use `uv` to install the package in development mode:

```bash
uv pip install -e .
```

## Usage

This package provides two CLI tools for working with German verb data:

* **`learn-verbs`** - Interactive learning and practice
* **`german-verbs`** - Data management, lookups, and conversion

### 1. Interactive Learning (`learn-verbs`)

Practice German verbs interactively. **Defaults to A1 level verbs** (`irregular-verbs-a1.yaml`):

```bash
# Practice with A1 level verbs (default)
uv run learn-verbs

# Practice with verbs starting with 'b'
uv run learn-verbs verben/irregular-verbs-b.yaml

# Practice 10 questions with Ukrainian translations in sequential order
uv run learn-verbs -n 10 -m ukrainian -s

# Practice verbs starting with 'b' with specific options
uv run learn-verbs verben/irregular-verbs-b.yaml -n 5 -m english
```

**Options:**
* `yaml_file`: Use a specific YAML file (default: `irregular-verbs-a1.yaml`)
* `--question-limit`, `-n`: Limit the number of questions (default: 0 = unlimited)
* `--mode`, `-m`: Practice specific types of questions:
  - `random`: All question types (default)
  - `infinitive`: Infinitive → Präteritum & Partizip II 
  - `prateritum`: Präteritum → Infinitive & Partizip II
  - `partizip`: Partizip II → Infinitive & Partizip
  - `english`: English → German infinitive
  - `ukrainian`: Ukrainian → German infinitive
  - `german`: German infinitive → English translation
* `--sequential`, `-s`: Practice verbs in sequential order (instead of random)

### 2. Verb Data Management (`german-verbs`)

Comprehensive CLI tool for managing and converting verb data. **All commands default to A1 level verbs** (`irregular-verbs-a1.yaml`):

```bash
# List all verbs (A1 level by default)
uv run german-verbs list

# List verbs starting with 'b'
uv run german-verbs list -f verben/irregular-verbs-b.yaml

# Look up specific verbs (A1 level by default)
uv run german-verbs get beginnen
uv run german-verbs get-by-id 5

# Look up verbs starting with 'b'
uv run german-verbs get bieten -f verben/irregular-verbs-b.yaml
uv run german-verbs get-by-id 3 -f verben/irregular-verbs-b.yaml

# Convert YAML to Markdown
uv run german-verbs convert-to-md verben/irregular-verbs-a1.yaml
uv run german-verbs convert-all

# Convert Markdown back to YAML
uv run german-verbs convert-to-yaml verben/generated/irregular-verbs-a1.md

# Find duplicate verbs across all YAML files  
uv run german-verbs find-duplicates
```

**Available subcommands:**
* `list`: List all verbs with translations
* `get <infinitive>`: Get detailed information about a verb
* `get-by-id <id>`: Get verb by its ID number
* `convert-to-md <file>`: Convert YAML file to Markdown table
* `convert-to-yaml <file>`: Convert Markdown table back to YAML
* `convert-all`: Convert all YAML files in verben/ directory to Markdown
* `find-duplicates`: Find verbs that appear in multiple YAML files

### Example: Quick Single File Conversion

Convert a single YAML file to Markdown:

```bash
uv run german-verbs convert-to-md verben/irregular-verbs-a1.yaml
```

This creates a formatted Markdown file in the `verben/generated` directory.

### Available Verb Files

The package includes two verb datasets:
* **`irregular-verbs-a1.yaml`** - A1 level verbs (26 verbs) - **Default for all commands**
* **`irregular-verbs-b.yaml`** - Verbs starting with 'b' (16 verbs)

## Interactive Learning Features (`learn-verbs`)

- Press Enter at any question prompt to see the full verb information
- Press Ctrl+C at any time to end the session and see your statistics
- Get instant feedback on correct and incorrect answers
- Review your progress with detailed statistics

## File Formats

### YAML Structure

The YAML files in the `verben` directory have the following structure:

```yaml
title: "Unregelmäßige Verben - A1"
verbs:
  - id: 1
    infinitiv: beginnen
    präteritum: begann
    partizip: hat begonnen
    translations:
      english: to begin
      ukrainian: починати
    person3: beginnt
    examples: |
      mit <Dat>

      **Substantive**:
        der Beginn - початок

      mit der Arbeit = zu arbeiten beginnen
      
      **Präsens**:
        Ich beginne ein neues Buch zu lesen. / I begin to read a new book.
        Ich beginne mit der Arbeit. / I begin with the work.
      
      **Präteritum**:
        Ich begann mit der Arbeit. / I began with the work.
        Er begann das Projekt gestern. / He began the project yesterday.
      
      **Perfekt**:
        Ich habe meine Hausaufgaben begonnen. / I have begun my homework.
        Wir haben das Meeting um 10 Uhr begonnen. / We have begun the meeting at 10 o'clock.
```

## Development

To make changes to the package, edit the files in the `german_verbs` directory, then reinstall the package with:

```bash
uv pip install -e .
``` 