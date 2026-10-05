# Changelog

All notable changes to `german-verbs` are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**One version covers the unit**: both CLIs (`german-verbs`, `learn-verbs`), the scripts and
`convert.py`, the `lesson-notes` skill (both copies), and the YAML schemas. Verb data, audio and
generated Markdown are content, not releases, and never appear here.

- **MAJOR**: something outside the code must change in step: the Rektion YAML schema the
  lesson-notes skill reads (`verben/rektion/verben-mit-prapositionen.yaml`), the verb YAML schema
  `scripts/validate_yaml.py` checks (existing files would stop loading), or a CLI command or flag
  mini-agent's `/project` uses (verb quiz, lookup).
- **MINOR**: something new that all of them keep working with: a subcommand, a flag, a practice
  mode, an optional YAML field.
- **PATCH**: fixes, and changes to text only a person reads.

`german-verbs --version` (and `learn-verbs --version`) prints `german-verbs X.Y.Z+<build>`:
`<build>` is the release tag's commit count while the unit's files are unchanged since that tag,
and `+dev` otherwise. Release with `tools/release.sh …` after an approved push (README →
Versioning). Each entry names the plan phase it came from.

## [Unreleased]

### Added
- `lesson-notes` skill (both copies) also writes a Wörterbuch and saves `notes.md` + `woerterbuch.md` to `lessons/<course>/<YYYYMMDD>/` instead of answering only in chat (Phase 9).

### Changed
- `lesson-notes` titles: `# DE-<Course> - <YYYYMMDD>: <lesson title>` for the notes and `…: Wörterbuch` for the vocabulary (Phase 9).

## [1.0.0] - 2026-10-01

First tagged release: the state after Phases 1–7, plus Phase 8. Continues from `0.2.0`
(2025-05-13), the last untagged bump.

### Added
- `--version` on both CLIs prints `german-verbs X.Y.Z+<build>` (Phase 8).
- `tools/release.sh`: bumps `__init__.py`, `pyproject.toml` and `uv.lock`, moves this section under
  the new version, tags `german-verbs-vX.Y.Z` and pushes the commit and the tag together (Phase 8).
- Already present at 1.0.0: `german-verbs list | get | get-by-id | convert-to-md | convert-to-yaml
  | convert-all | find-duplicates`, `learn-verbs` with seven practice modes, the Rektion YAML and
  its Markdown generator, and the `lesson-notes` skill (Phases 1–7).

### Fixed
- `german_verbs/__init__.py` said `0.1.0` while `pyproject.toml` said `0.2.0`; both now agree, and
  the release script keeps them in step (Phase 8).
