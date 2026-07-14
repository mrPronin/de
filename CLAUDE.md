# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python CLI package (`german-verbs`, v0.2.0) for learning German irregular verbs. The verb data itself (YAML files under `verben/`) is the primary content that changes; the Python code in `german_verbs/` is a stable toolset for practicing, displaying, and converting that data. Note most commits are data edits, not code edits.

## Commands

Install in editable mode (required after any code change to `german_verbs/`):

```bash
uv pip install -e .
```

Two CLI entry points (defined in `pyproject.toml` `[project.scripts]`):

```bash
uv run learn-verbs [YAML_FILE] [-n N] [-m MODE] [-s]   # interactive practice REPL
uv run german-verbs <subcommand> [-f YAML_FILE]        # data management
```

`german-verbs` subcommands: `list`, `get <infinitive>`, `get-by-id <id>`, `convert-to-md <file>`, `convert-to-yaml <file>`, `convert-all`, `find-duplicates`.

`convert.py` at the repo root is a standalone shortcut equivalent to `convert-all`.

There is **no test suite, linter config, or CI**. Verify changes by running the CLI commands directly.

## Data model & conventions

Verb data lives in `verben/*.yaml`, keyed by CEFR level / grouping (`irregular-verbs-a1.yaml`, `-a2.yaml`, `-b.yaml`). Each file: a `title` string and a `verbs` list. Each verb has `id`, `infinitiv`, `präteritum`, `partizip`, `person3`, `translations.{english,ukrainian}`, and a free-text `examples` block (see README for the full example shape). **`präteritum` uses a non-ASCII key name (ä)** — preserve it exactly in code and YAML.

- Default data file everywhere is `irregular-verbs-a1.yaml`. Both CLIs and `load_verb_data()` fall back to it.
- `verben/generated/*.md` are **generated artifacts** — produce them via `convert-to-md`/`convert-all`, don't hand-edit. Some YAML files intentionally have no generated MD.
- YAML↔MD round-trips are lossy: MD tables flatten `examples` newlines to `<br>` and escape `<`/`>` as `\<`/`\>` (`converter.py:escape_angle_brackets`). `markdown_to_yaml` reverses this but is explicitly simplified and may not handle all edge cases.
- `person3` is stored parenthetically in the MD infinitive cell (`beginnen (beginnt)`) and parsed back out.

## Architecture

`german_verbs/` package, four functional modules wired together by two Click entry points:

- `verbs.py` — data layer. `load_verb_data()` resolves a filename through a **multi-location search chain**: direct path → module `data/` dir → `verben/` (with and without stripping the path) → cwd. This is why bare filenames like `irregular-verbs-b.yaml` and full paths both work. Also holds lookups (`get_verb_by_id`, `get_verb_by_infinitive`) and display formatting.
- `learn.py` — `learn-verbs` entry point. `VerbLearner` class holds session state and 6 question-type methods (infinitive→forms, präteritum→forms, partizip→forms, english→infinitive, ukrainian→infinitive, german→english). `--mode` selects a single question type by index into `question_types`; empty input at any prompt triggers `_show_verb_help` and re-asks the same question.
- `converter.py` — YAML↔Markdown conversion (see Data model above).
- `colors.py` — Click styling constants shared across `learn.py`.
- `cli.py` — `german-verbs` entry point; thin Click wrappers over `verbs.py` and `converter.py`.

Commands are generally run from the repo root because directory-relative paths (`verben/`, `verben/generated`) are hardcoded in `cli.py` and the `load_verb_data()` search chain.

## Audio files (`audio/`)
Pronunciation audio for German verbs, organized by CEFR level.

### Current status (2026-07-14)

| Level | Verbs | Downloaded | Missing |
|---|---:|---:|---|
| **a1** | 50 | 50 ✅ | 0 |
| **a2** | 9 (with infinitiv) | 9 ✅ | 0 |
| **b** | 16 | 3 | 13 |

### Missing B verbs (13)
`backen`, `befehlen`, `beginnen`, `beißen`, `betrügen`, `bewegen`, `biegen`, `bieten`, `binden`, `blasen`, `braten`, `brechen`, `fangen`

### Source: Wikimedia Commons
Wikimedia Commons hosts crowdsourced native-speaker audio. Files follow the pattern:
```
File:LL-Q188 (deu)-{username}-{word}.{ext}
```
Extensions: `.ogg` (preferred), `.mp3`, or `.wav`.

### Download approach
Wikimedia Commons aggressively blocks programmatic access (HTTP 429). Search API works intermittently; URL endpoints are consistently blocked.

**Stored scripts live in `scripts/download_audio.py`** — do not regenerate inline. If it works, commit the script alongside new audio files.

**Fallback sources (see `doc/004-how-to-download-audio.md`):**
- **Wiktionary bulk dump** (`kaikki.org/dictionary/rawdata.html`, 20.4GB tar) — filter by verb list, no rate limiting
- **Forvo API** (requires key)
- **gTTS** (synthetic but free and fast)
