# German Verbs — Implementation Plan

## Goal

Help a learner practice German irregular verbs. The repository is primarily a **curated dataset** of irregular verbs (grouped by CEFR level in `verben/*.yaml`) plus a small, stable Python CLI toolset (`german_verbs/`) to practice, look up, and convert that data. The main ongoing outcome is expanding and correcting the verb data; the code is a supporting tool.

## Current Status

Delivered and working:
- Two CLI entry points: `learn-verbs` (interactive practice) and `german-verbs` (data management/conversion).
- Verb datasets: A1, A2, and a "b" grouping under `verben/`.
- YAML↔Markdown conversion, duplicate detection, per-verb lookups.

In progress:
- Ongoing data authoring/curation (A2 verbs are the most recent active work — see `verben/irregular-verbs-a2.yaml`).

No known blockers. There is no automated test suite, linter, or CI.

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | Core data model + CLI toolset | done |
| 2 | YAML↔Markdown conversion + escaping | done |
| 3 | Interactive practice modes | done |
| 4 | Data curation (A1 → A2 → beyond) | in progress |
| 5 | Testing / linting / CI | planned |

## Architecture

Data-centric project. The YAML files are the source of truth; Python modules read/transform them. Two Click entry points wrap four functional modules.

```
verben/*.yaml  ──load_verb_data()──►  verbs.py  ──►  cli.py (german-verbs)
                                          │            learn.py (learn-verbs)
                                          └──►  converter.py  ──►  verben/generated/*.md
```

Directory-relative paths (`verben/`, `verben/generated/`) are hardcoded, so commands are normally run from the repo root.

## Project Structure

```
de/
├── convert.py                  # standalone shortcut ≈ `german-verbs convert-all`
├── pyproject.toml              # package + [project.scripts] entry points
├── german_verbs/
│   ├── verbs.py                # data layer: load, lookup, display formatting
│   ├── learn.py                # learn-verbs: VerbLearner + 6 question types
│   ├── converter.py            # YAML↔Markdown conversion
│   ├── cli.py                  # german-verbs Click command group
│   └── colors.py               # Click styling constants
└── verben/
    ├── irregular-verbs-a1.yaml # default data file everywhere
    ├── irregular-verbs-a2.yaml
    ├── irregular-verbs-b.yaml
    └── generated/*.md          # generated artifacts (do not hand-edit)
```

## Technology Stack

- Python ≥ 3.8
- [Click](https://click.palletsprojects.com/) ≥ 8.0 — CLI framework and terminal styling
- [PyYAML](https://pyyaml.org/) ≥ 6.0 — data (de)serialization
- [uv](https://github.com/astral-sh/uv) — env/package management (`uv pip install -e .`, `uv run`)
- setuptools build backend

## Phase 1: Core data model + CLI toolset — done

### Problem
Need a structured, editable store of irregular verbs and a way to query it.

### Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
| Data format | YAML files under `verben/` | Human-editable, diff-friendly, the actual work product |
| Grouping | One file per CEFR level / grouping | Keeps files small; enables per-level practice |
| Default file | `irregular-verbs-a1.yaml` | A1 is the entry level; sensible default for all commands |
| File resolution | Multi-location search chain in `load_verb_data()` | Both bare filenames and full paths resolve without user friction |

### Key Changes
`verbs.py` (`load_verb_data`, `get_verb_by_id`, `get_verb_by_infinitive`, `format_verb_display`, `list_all_verbs`); `cli.py` command group with `list`/`get`/`get-by-id`/`find-duplicates`.

### Usage
```bash
uv run german-verbs list
uv run german-verbs get beginnen
uv run german-verbs get-by-id 5 -f verben/irregular-verbs-b.yaml
uv run german-verbs find-duplicates
```

### Verification
Run the commands above from the repo root against existing YAML files.

## Phase 2: YAML↔Markdown conversion + escaping — done

### Problem
Need human-readable Markdown tables of the verb data, and a path back to YAML.

### Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
| MD representation | Single table, `examples` newlines → `<br>` | Fits multi-line content into one table cell |
| Angle brackets | Escape `<`/`>` as `\<`/`\>` | Prevents Markdown renderers treating grammar notation (e.g. `<Dat>`) as HTML |
| Reverse conversion | Simplified `markdown_to_yaml` | Round-trip is lossy and best-effort; YAML remains source of truth |

### Key Changes
`converter.py` (`yaml_to_markdown`, `markdown_to_yaml`, `escape_angle_brackets`); `cli.py` `convert-to-md`/`convert-to-yaml`/`convert-all`; root `convert.py`.

### Usage
```bash
uv run german-verbs convert-to-md verben/irregular-verbs-a1.yaml
uv run german-verbs convert-all
```

### Verification
Convert a YAML file and inspect `verben/generated/<name>.md`.

## Phase 3: Interactive practice modes — done

### Problem
Need drilling of verb forms and translations in multiple directions.

### Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
| Question types | 6 (infinitive/präteritum/partizip forms; en→de; uk→de; de→en) | Covers both morphology and vocabulary in both directions |
| `--mode` | Selects a single question type by index | Lets learners focus on a weak area |
| Empty input | Shows full verb help, re-asks same question | Non-punishing hint mechanism |
| Order | Random by default, `--sequential` opt-in | Random for recall; sequential for structured review |

### Key Changes
`learn.py` (`VerbLearner`, six `_question_*` methods, `run_practice_session`, `show_statistics`); `colors.py`.

### Usage
```bash
uv run learn-verbs
uv run learn-verbs verben/irregular-verbs-b.yaml -n 10 -m ukrainian -s
```

### Verification
Run a short session (`-n 3`) and confirm scoring/help behavior.

## Known Issues & Workarounds

- **Lossy YAML↔MD round-trip.** `markdown_to_yaml` is explicitly simplified; treat generated MD as output-only and keep YAML authoritative. Permanent by design.
- **Non-ASCII key `präteritum`** (with `ä`) is used throughout data and code. Must be preserved exactly; easy to break with careless edits.
- **Path-relative commands.** CLI assumes it runs from the repo root; running elsewhere breaks `verben/`/`verben/generated/` resolution. Permanent (acceptable for a personal tool).
- **No automated tests.** All verification is manual via the CLIs.

## Decision Log

| Date | Decision | Reason |
|---|---|---|
| 2026-07-13 | Introduced `IMPLEMENTATION_PLAN.md` and root `CLAUDE.md` | Document project direction and give coding agents fast onboarding |

## Future Work

- Add a minimal test suite (conversion round-trip, `load_verb_data` resolution, lookups) and a linter — Phase 5.
- Continue verb data curation beyond A2.
- Consider spaced-repetition / progress persistence across sessions (currently stats are per-session only).
- Consider consolidating grouping scheme (CEFR-level files vs. letter-based `-b` file) to avoid overlap; `find-duplicates` exists partly to manage this.
