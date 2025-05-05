# German Verbs

A Python package for learning German irregular verbs using interactive practice.

## Installation

Use `uv` to install the package in development mode:

```bash
uv pip install -e .
```

## Usage

### Converting YAML to Markdown

Convert verb data from YAML to Markdown:

```bash
uv run yaml2md verben/irregular-verbs-a1.yaml
```

This will create a formatted Markdown file in the `verben/generated` directory.

### Interactive Learning

Practice German verbs interactively:

```bash
uv run -m german_verbs.learn
# or
uv run learn-verbs verben/irregular-verbs-a1.yaml
```

Options:

* `yaml_file`: Use a specific YAML file (default: irregular-verbs-a1.yaml)
* `--question-limit`, `-n`: Limit the number of questions (default: 0 = unlimited)
* `--mode`, `-m`: Practice specific types of questions:
  - `random`: All question types (default)
  - `infinitive`: Infinitive → Präteritum & Partizip II 
  - `prateritum`: Präteritum → Infinitive & Partizip II
  - `partizip`: Partizip II → Infinitive & Präteritum
  - `english`: English → German forms
  - `ukrainian`: Ukrainian → German forms
* `--sequential`, `-s`: Practice verbs in sequential order (instead of random)

Example:

```bash
# Practice 10 questions with Ukrainian translations in sequential order
uv run -m german_verbs.learn verben/irregular-verbs-a1.yaml -n 10 -m ukrainian -s
```

## Interactive Learning Features

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
    person3: beginnt
    präteritum: begann
    partizip: hat begonnen
    translations:
      english: to begin
      ukrainian: починати
    examples: |
      mit Dat
      
      der Beginn - начало
      
      Präsens: Ich beginne ein neues Buch zu lesen.
      Perfekt: Ich habe meine Hausaufgaben begonnen.
```

## Development

To make changes to the package, edit the files in the `german_verbs` directory, then reinstall the package with:

```bash
uv pip install -e .
``` 