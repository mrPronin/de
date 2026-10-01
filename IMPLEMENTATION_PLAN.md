# German Verbs — Implementation Plan

## Goal

Help a learner practice German irregular verbs. The repository is primarily a **curated dataset** of irregular verbs (grouped by CEFR level in `verben/*.yaml`) plus a small, stable Python CLI toolset (`german_verbs/`) to practice, look up, and convert that data. The main ongoing outcome is expanding and correcting the verb data; the code is a supporting tool.

## Current Status

Delivered and working:
- Two CLI entry points: `learn-verbs` (interactive practice) and `german-verbs` (data management/conversion).
- Verb datasets: A1, A2 (60 verbs), and a "b" grouping under `verben/`.
- YAML↔Markdown conversion, duplicate detection, per-verb lookups.
- YAML validation script (`scripts/validate_yaml.py`) for consistency checks.
- Reference table of verbs with fixed prepositions (Rektion): `verben/rektion/verben-mit-prapositionen.yaml` (38 Akk + 28 Dat, UA/EN) → generated `verben/verben-mit-prapositionen.md` via `scripts/rektion_to_md.py`.

In progress:
- Ongoing data authoring/curation (A2 verbs are the most recent active work).

No known blockers. There is no automated test suite, linter, or CI.

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | Core data model + CLI toolset | done |
| 2 | YAML↔Markdown conversion + escaping | done |
| 3 | Interactive practice modes | done |
| 4 | Data curation (A1 → A2 → beyond) | in progress |
| 5 | Maintenance scripts | done |
| 6 | Testing / linting / CI | planned |
| 7 | `lesson-notes` agent skill (Claude Code + Codex) | done |
| 8 | SemVer: `--version`, CHANGELOG, `german-verbs-v1.0.0` | in progress |

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
├── .claude/skills/lesson-notes/SKILL.md # Claude Code skill: /lesson-notes [YYYYMMDD]
├── .agents/skills/lesson-notes/SKILL.md # Codex copy of the same skill: $lesson-notes
├── convert.py                  # standalone shortcut ≈ `german-verbs convert-all`
├── scripts/                    # maintenance utilities
│   ├── rektion_to_md.py       # verben/rektion/*.yaml → verben/verben-mit-prapositionen.md
│   ├── renumber_yaml.py       # renumber verb IDs after manual edits
│   └── validate_yaml.py       # validate YAML syntax and schema
├── pyproject.toml              # package + [project.scripts] entry points
├── german_verbs/
│   ├── verbs.py                # data layer: load, lookup, display formatting
│   ├── learn.py                # learn-verbs: VerbLearner + 6 question types
│   ├── converter.py            # YAML↔Markdown conversion
│   ├── cli.py                  # german-verbs Click command group
│   └── colors.py               # Click styling constants
└── verben/
    ├── irregular-verbs-a1.yaml # default data file everywhere
    ├── irregular-verbs-a2.yaml # 60 A2-level verbs
    ├── irregular-verbs-b.yaml  # B-level verbs
    ├── verben-mit-prapositionen.md # generated from rektion/ YAML (do not hand-edit)
    ├── rektion/verben-mit-prapositionen.yaml # Rektion source of truth, own schema; subfolder keeps it out of verben/*.yaml tooling
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

## Phase 5: Maintenance Scripts — done

### Problem
Manual edits to YAML files (adding/removing verbs) leave ID gaps and duplicates, requiring tedious manual renumbering.

### Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
| Standalone script | `scripts/renumber_yaml.py` | No install needed; runs with stdlib (`re`, `sys`, `pathlib`) |
| Target detection | Match `- id:` lines inside `verbs:` block | Avoids renumbering unrelated YAML fields |

### Key Changes
`scripts/renumber_yaml.py` — renames verb IDs sequentially from 1. Defaults to A1 file; accepts one or more paths.

### Usage
```bash
python3 scripts/renumber_yaml.py verben/irregular-verbs-b.yaml   # single file
python3 scripts/renumber_yaml.py verben/*.yaml                    # all files
python3 scripts/renumber_yaml.py                                  # defaults to A1
```

### Verification
Run against any YAML file, then `grep "id:"` to confirm sequential numbering.

#### YAML Validation Script (`scripts/validate_yaml.py`)

Added to catch schema issues before they enter the repo:
- Validates YAML syntax (via `yaml.safe_load`)
- Checks required keys: `id`, `level`, `infinitiv`, `präteritum`, `partizip`, `translations`
- Detects duplicate IDs
- Reports missing keys per verb

```bash
python3 scripts/validate_yaml.py                    # all verben/*.yaml
python3 scripts/validate_yaml.py verben/file.yaml  # specific file
```

#### Rektion MD Generator (`scripts/rektion_to_md.py`)

Renders `verben/rektion/verben-mit-prapositionen.yaml` to `verben/verben-mit-prapositionen.md`: one section per case (Akk, Dat) with rules, optional note and a table numbered from 1 per section; `<`/`>` escaped, `note` appended to the verb cell after `<br><br>`, `example` list rendered as the Beispiele column (`<br>`-joined), same as `converter.py`.

```bash
python3 scripts/rektion_to_md.py                        # default YAML → default MD
python3 scripts/rektion_to_md.py path.yaml -o out.md
```

Verified: output is byte-identical to the MD exported from the Apple Note.

## Phase 7: `lesson-notes` agent skill — done

### Problem
Bilingual lesson notes (тези заняття) from noisy B1 lesson transcripts were produced by a long ad-hoc prompt each time; the format (UA/DE headings, articles on nouns, Rektion tables, typical mistakes, Organisatorisches) had to be re-explained.

### Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
| Scope | Project-level skill, not global | Tied to this repo: offers to add new Rektion verbs to `verben/rektion/verben-mit-prapositionen.yaml` |
| Two agents | Separate copies: `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex) | Codex reads repo skills from `$REPO_ROOT/.agents/skills` and has no `$ARGUMENTS`/`argument-hint`; Codex copy takes the date from the message and spells out the `md-to-pdf` call instead of pointing to the global CLAUDE.md |
| Output | Chat by default, file only on request | Matches how the notes are used; PDF via `md-to-pdf` beside the transcript |
| Rektion sync | Offer only, never auto-edit | Data edits stay explicit |

### Key Changes
- `.claude/skills/lesson-notes/SKILL.md`, `.agents/skills/lesson-notes/SKILL.md`.

### Usage
```text
/lesson-notes 20260917     # Claude Code (no arg → newest lesson with a transcript)
$lesson-notes 20260917     # Codex
```

### Dependencies
Lesson transcripts in `~/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/DE-B1-<YYYYMMDD>_transcript.md` (outside the repo).

### Verification
Format derived from the notes produced for lesson 20260915. Skill invocation itself not yet run in either agent.

## Phase 8: SemVer — `--version`, CHANGELOG, `german-verbs-v1.0.0` — in progress

### Problem
The operator asked to apply semver.org to every sibling repo of mini-agent (mini-agent Phase 155;
movie-list Phase 19 is the reference). The package had been bumped once by hand (`0.1.0` →
`0.2.0`, 2025-05-13, `d981da1`) but never tagged, `german_verbs/__init__.py` still said `0.1.0`, and
neither CLI had `--version`.

### Design Decisions
| Decision | Choice | Rationale |
|---|---|---|
| What the version covers | both CLIs, scripts, `convert.py`, the lesson-notes skill (both copies), the YAML schemas | They change together; verb data is content |
| What is breaking | the Rektion YAML schema (the skill reads it), the verb schema (`validate_yaml.py`), the CLI commands mini-agent's `/project` runs | Those are the only consumers |
| Start | `1.0.0` (operator, 2026-10-01) | Used from Signal through `/project`. Continues from the untagged `0.2.0` |
| Build number | the tag's commit count while the unit's files are unchanged since the tag, else `+dev` | The CLIs run from the checkout. Almost every commit is data ("Rektion: add …"), and those must not turn a release into `+dev` |
| `--version` | an eager click option on both CLIs, computed only when asked | `git` runs only for `--version`, not on every quiz |
| No deploy gate, no skill check | none | Nothing is shipped. The skill doesn't call the CLIs, so there is nothing to drift |
| Approvals | every edit, and the commit and push, approved by the operator first | AGENTS.md hard rules |

### Key Changes
`german_verbs/version.py` (new), `german_verbs/__init__.py` (`0.2.0`), `german_verbs/cli.py` and
`german_verbs/learn.py` (`--version`), `tools/release.sh` (new), `CHANGELOG.md` (new), README
*Versioning*, CLAUDE.md and AGENTS.md.

### Verification
- `uv run german-verbs --version` and `uv run learn-verbs --version` → `german-verbs 0.2.0+dev`;
  `german-verbs get sein` still works.
- The version logic was checked against a throwaway git repo: no tag → `+dev`; at the tag → `+1`;
  a data commit after the tag → still `+1`; a code edit → `+dev`.

## Known Issues & Workarounds

- **Lossy YAML↔MD round-trip.** `markdown_to_yaml` is explicitly simplified; treat generated MD as output-only and keep YAML authoritative. Permanent by design.
- **Non-ASCII key `präteritum`** (with `ä`) is used throughout data and code. Must be preserved exactly; easy to break with careless edits.
- **Path-relative commands.** CLI assumes it runs from the repo root; running elsewhere breaks `verben/`/`verben/generated/` resolution. Permanent (acceptable for a personal tool).
- **No automated tests.** All verification is manual via the CLIs.

## Decision Log

| Date | Decision | Reason |
|---|---|---|
| 2026-07-13 | Introduced `IMPLEMENTATION_PLAN.md` and root `CLAUDE.md` | Document project direction and give coding agents fast onboarding |
| 2026-07-14 | Removed "bleiben" from b.yaml; added `scripts/renumber_yaml.py` | "bleiben" is A1-level (verified via DuckDuckGo); renumber script prevents manual ID errors after data edits |
| 2026-07-22 | Added `scripts/validate_yaml.py` for YAML schema validation | Catch missing keys and duplicates early; provide a lightweight linter |
| 2026-07-22 | Filled all 60 A2 verbs from external reference list | Based on repeatso.com's curated A2 irregular verb list; validated with YAML parser |
| 2026-09-24 | Exported Apple Note "DE - 09 - Verben mit festen Präpositionen (Rektion)" to `verben/verben-mit-prapositionen.md` as plain MD (not YAML) | Different shape from irregular-verb schema (no forms, preposition + case instead); filled 18 missing EN translations and fixed `jemanend`→`jemanden`, `jemandem um etwas bitten`→`jemanden …` (bitten takes Akk). The Apple Note itself still has the old content |
| 2026-09-24 | Converted `verben-mit-prapositionen.md` to `verben/rektion/verben-mit-prapositionen.yaml` (50 entries, IDs 1–50 across Akk then Dat) | Subfolder rather than `verben/` because the validator, `convert-all` and `find-duplicates` glob `verben/*.yaml` non-recursively and would choke on the non-irregular schema; avoids code changes. MD kept alongside |
| 2026-09-24 | Made the Rektion YAML the source of truth; added `scripts/rektion_to_md.py` to generate the MD. YAML `rules` became per-case lists and the *sich freuen* hint moved to `notes.Akk` | One place to edit instead of syncing two files by hand; restructured rules so the generated MD matches the original layout exactly. Standalone script (not a `german-verbs` subcommand) because the schema is unrelated to `converter.py` |
| 2026-09-24 | Added optional `example` list to Rektion YAML (36 of 53 entries), extracted from lesson transcript `DE-B1-20260908_transcript.md`; `rektion_to_md.py` now also escapes `<`/`>` in translations | Transcript is noisy speech-to-text, so sentences were taken from the teacher's corrections and grammar-fixed rather than copied verbatim; examples are rendered to a Beispiele column joined by `<br>`. Escaping fix: a UA translation `<щось>` would otherwise render as an invisible HTML tag |
| 2026-09-24 | Rektion list grown to 64 entries (36 Akk + 28 Dat) incl. remaining lesson verbs; wrote `example` for the 17 entries the transcript didn't cover, so every entry now has examples | Each entry gets a statement plus the matching question form (wo-/da-compound for things, Präposition + wen/wem for persons), mirroring the lesson's question-building rule. Author-written examples, not from the transcript |
| 2026-09-28 | Added `lesson-notes` skill for Claude Code and Codex as two separate copies | Codex skill discovery (`.agents/skills`) and argument handling differ from Claude Code; the two files must be kept in sync by hand |
| 2026-10-01 | SemVer from `1.0.0`, tag `german-verbs-v*`; the build number counts while the unit's files equal the tag (data commits don't count); no deploy gate (Phase 8) | mini-agent Phase 155's rules for a tool that runs from its checkout |

## Future Work

- Add a minimal test suite (conversion round-trip, `load_verb_data` resolution, lookups) and a linter — Phase 6.
- Continue verb data curation beyond A2 (B1, B2, C1, C2).
- Consider spaced-repetition / progress persistence across sessions (currently stats are per-session only).
- Consider consolidating grouping scheme (CEFR-level files vs. letter-based `-b` file) to avoid overlap; `find-duplicates` exists partly to manage this.
- Add audio pronunciation files for all 60 A2 verbs (currently only 9/60 have audio).
