# AGENTS.md

Project-local guidance for Pi when working in this repository.
The global AGENTS.md (`~/.pi/agent/AGENTS.md`) applies automatically; this file adds project-specific context.

## What this is

A Python CLI package (`german-verbs`, v0.2.0) for learning German irregular verbs. The verb data itself (YAML files under `verben/`) is the primary content that changes; the Python code in `german_verbs/` is a stable toolset for practicing, displaying, and converting that data. Most commits are data edits, not code edits.

## Commands

```bash
# Install in editable mode (required after any code change to german_verbs/)
uv pip install -e .

# Interactive practice REPL
uv run learn-verbs [YAML_FILE] [-n N] [-m MODE] [-s]

# Data management
uv run german-verbs <subcommand> [-f YAML_FILE]
```

`german-verbs` subcommands: `list`, `get <infinitive>`, `get-by-id <id>`, `convert-to-md <file>`, `convert-to-yaml <file>`, `convert-all`, `find-duplicates`.

`convert.py` at the repo root is a standalone shortcut equivalent to `convert-all`.

`scripts/renumber_yaml.py` renumbers verb IDs sequentially after manual edits (add/remove verbs).
```bash
python3 scripts/renumber_yaml.py verben/irregular-verbs-b.yaml   # single file
python3 scripts/renumber_yaml.py verben/*.yaml                    # all files
```

**No test suite, linter config, or CI.** Verify changes by running the CLI commands directly.

## Data model & conventions

Verb data lives in `verben/*.yaml` (`irregular-verbs-a1.yaml`, `-a2.yaml`, `-b.yaml`). After editing (adding/removing verbs), run `scripts/renumber_yaml.py` to fix sequential IDs. Each file has a `title` string and a `verbs` list. Each verb: `id`, `infinitiv`, `präteritum` (note: **non-ASCII key — preserve the ä**), `partizip`, `person3`, `translations.{english,ukrainian}`, and free-text `examples`.

- Default data file everywhere: `irregular-verbs-a1.yaml`.
- **Never regenerate MD files without explicit user instruction.** Do not run `convert-to-md`, `convert-all`, or `convert.py` unless the user explicitly asks.
- `verben/generated/*.md` are **generated artifacts** — produce via `convert-to-md` / `convert-all`, never hand-edit.
- YAML↔MD round-trips are lossy (examples flattened to `<br>`, angle brackets escaped).
- `person3` stored parenthetically in MD infinitive cell.

## Architecture

`german_verbs/` package, four functional modules + two Click entry points:

| Module | Role |
|---|---|
| `verbs.py` | Data layer: `load_verb_data()` with multi-location search chain, lookups, formatting |
| `learn.py` | `learn-verbs` entry point: `VerbLearner` class, 6 question types, empty-input help |
| `converter.py` | YAML↔Markdown conversion |
| `colors.py` | Click styling constants |
| `cli.py` | `german-verbs` entry point: thin Click wrappers |

Commands are generally run from the repo root (hardcoded `verben/` paths).

## Search MCP throttling

DuckDuckGo search blocks repeated identical queries (bot detection). When a query returns 0 results:
- **Check result count** before retrying — empty responses may be bot-blocked, not genuinely empty.
- **Vary the query** (different keywords/phrasing) instead of repeating the same one.
- **Space out queries** — don't hammer the same search in rapid succession.
- For `search_fetch_content`, use `backend='curl'` (Chrome TLS impersonation) to bypass bot filters.
