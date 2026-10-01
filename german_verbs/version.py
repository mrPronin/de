"""The version `german-verbs --version` prints: `X.Y.Z+<build>`, SemVer build metadata (Phase 8).

There is no build step: the CLIs run from this checkout (`uv run …`, on the Mac and in
mini-agent's `/project`). So the build number says whether the checkout IS a release: the commit
count of tag `german-verbs-vX.Y.Z` while every file of the unit is unchanged since that tag. The
unit is the code, the scripts, both copies of the lesson-notes skill, `pyproject.toml` and
`uv.lock`. `verben/`, `audio/` and `doc/` are data, so the "Rektion: add …" commits never change the
build number. Anything else (an edit, an unreleased commit, no tag, no git) prints `+dev`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from german_verbs import __version__

TAG_PREFIX = "german-verbs-v"
UNIT_PATHS = (
    "german_verbs",
    "scripts",
    "convert.py",
    ".agents/skills",
    ".claude/skills",
    "pyproject.toml",
    "uv.lock",
)


def full_version(root: Path | None = None, version: str = __version__) -> str:
    root = root or Path(__file__).resolve().parent.parent
    tag = f"{TAG_PREFIX}{version}"

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=10
        )

    try:
        if git("rev-parse", "-q", "--verify", f"refs/tags/{tag}").returncode != 0:
            return f"{version}+dev"
        # Working tree against the tag: an uncommitted edit counts as a change too.
        if git("diff", "--quiet", tag, "--", *UNIT_PATHS).returncode != 0:
            return f"{version}+dev"
        count = git("rev-list", "--count", tag)
        if count.returncode != 0 or not count.stdout.strip().isdigit():
            return f"{version}+dev"
        return f"{version}+{count.stdout.strip()}"
    except (OSError, subprocess.SubprocessError):
        return f"{version}+dev"


def print_version(ctx, _param, value):
    """Click callback for an eager `--version`: git runs only when it is asked for."""
    if not value or ctx.resilient_parsing:
        return
    import click

    click.echo(f"german-verbs {full_version()}")
    ctx.exit()
