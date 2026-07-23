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

german-verbs subcommands: `list`, `get <infinitive>`, `get-by-id <id>`, `convert-to-md <file>`, `convert-to-yaml <file>`, `convert-all`, `find-duplicates`.

convert.py at the repo root is a standalone shortcut equivalent to `convert-all`.

scripts/renumber_yaml.py renumbers verb IDs sequentially after manual edits (add/remove verbs).
python3 scripts/renumber_yaml.py verben/irregular-verbs-b.yaml   # single file
python3 scripts/renumber_yaml.py verben/*.yaml                    # all files

scripts/validate_yaml.py validates YAML syntax and schema (required keys, duplicate IDs).
python3 scripts/validate_yaml.py                    # all verben/*.yaml
python3 scripts/validate_yaml.py verben/file.yaml   # specific file
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

## Audio files (`audio/`)
Pronunciation audio for German verbs, organized by CEFR level.

### Current status (2026-07-22)

| Level | Verbs | Downloaded | Missing |
|---|---:|---:|---:|
| **a1** | 50 | 50 ✅ | 0 |
| **a2** | 60 | 9 ✅ | 51 |
| **b** | 16 | 3 | 13 |

**Total: 62/126 verbs have audio.**

### Missing B verbs (13)
`backen`, `befehlen`, `beginnen`, `beißen`, `betrügen`, `bewegen`, `biegen`, `bieten`, `binden`, `blasen`, `braten`, `brechen`, `fangen`

### Source: Wikimedia Commons
Wikimedia Commons hosts crowdsourced native-speaker audio for German words. Files follow the pattern:
```
File:LL-Q188 (deu)-{username}-{word}.{ext}
```
Extensions: `.ogg` (preferred), `.mp3`, or `.wav`.

### Download approach
Wikimedia Commons aggressively blocks programmatic access (HTTP 429). The search API works intermittently, but endpoints returning file URLs (`imageinfo`, page HTML) are consistently blocked.

**Stored scripts live in `scripts/download_audio.py`** — do not regenerate inline. If it works, commit the script alongside new audio files.

**Fallback sources (from `doc/004-how-to-download-audio.md`):**
- **Wiktionary bulk dump** (`kaikki.org/dictionary/rawdata.html`, 20.4GB tar) — filter by verb list, no rate limiting
- **Chrome DevTools MCP + verben.de** — control a real browser to scrape `verben.de/verben/{word}` pages, capture native-speaker TTS audio via network inspection (bypasses bot detection)
- **Wikimedia Commons** — primary source, crowdsourced native-speaker audio (rate-limited but works with sleep/retry)

## ⚠️ HARD RULE: No edits without asking

**Never modify files without explicit user confirmation.** This is a hard rule.

- Before editing any file (YAML, MD, or otherwise), you **must**:
  1. Show the user the current state of the file/section
  2. Show the user the proposed changes
  3. Ask for explicit approval (e.g., "Shall I make this change?" or "Please confirm")
- The user must explicitly say something like "yes", "go ahead", "do it", or confirm the change before proceeding.
- If the user has not explicitly confirmed, **do not edit**. Ask again.
- This rule applies to all files, including `verben/*.yaml`, `AGENTS.md`, etc.

## ⚠️ HARD RULE: No commits/pushes without asking

**Never commit or push changes to the repository without explicit user confirmation.** This is a hard rule.

- Before running `git commit` or `git push`, you **must**:
  1. Show the user the changes that would be committed
  2. Ask for explicit approval (e.g., "Shall I commit and push these changes?")
- The user must explicitly say something like "yes", "go ahead", "commit it", or confirm the commit before proceeding.
- If the user has not explicitly confirmed, **do not commit or push**. Ask again.

## ⚠️ LESSONS LEARNED: Data verification before reporting

When comparing data (e.g., YAML vs. Apple Notes), always:
1. **Use `grep` first** to locate the exact entry, then read the full file section
2. **Verify the complete data** before making comparison reports — never assume from partial file views
3. **Double-check** when a user questions a report — trust the user over your memory of what you read
4. **Show the full relevant data** to the user before making claims about completeness or differences
