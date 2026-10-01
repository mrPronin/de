#!/usr/bin/env bash
# Release `german-verbs`: one version for both CLIs, the lesson-notes skill and the YAML schemas
# (IMPLEMENTATION_PLAN.md, Phase 8). Run AFTER the work is committed and pushed — and, per
# AGENTS.md, only once the operator has approved the push:
#
#   tools/release.sh patch|minor|major     bump from german_verbs/__init__.py
#   tools/release.sh X.Y.Z                 an explicit version (must be higher)
#
# Copied from movie-list's tools/release.sh (the SemVer reference) and adapted to a uv project.
# Refuses unless the tracked tree is clean, HEAD is origin/main, and CHANGELOG.md's
# `## [Unreleased]` section has entries. Then the version in __init__.py, pyproject.toml and
# uv.lock + CHANGELOG.md → one commit "Release german-verbs X.Y.Z", annotated tag
# german-verbs-vX.Y.Z, both pushed in one atomic push. There is nothing to deploy: the CLIs run
# from this checkout, and `--version` says whether it is the release.
set -euo pipefail
cd "$(dirname "$0")/.."

NAME=german-verbs
TAG_PREFIX=german-verbs-v
INIT=german_verbs/__init__.py

die() { echo "release: $*" >&2; exit 1; }
[ $# -eq 1 ] || die "usage: tools/release.sh patch|minor|major|X.Y.Z"

[ "$(git branch --show-current)" = main ] || die "not on main"
[ -z "$(git status --porcelain --untracked-files=no)" ] || die "tracked changes are not committed"
git fetch -q origin main
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] ||
  die "HEAD is not origin/main — push (or pull) first"

cur=$(sed -n 's/^__version__ = "\([^"]*\)".*$/\1/p' "$INIT")
[ "$(sed -n 's/^version = "\(.*\)"$/\1/p' pyproject.toml | head -1)" = "$cur" ] ||
  die "pyproject.toml and $INIT disagree on the version"
IFS=. read -r ma mi pa <<<"$cur"
case $1 in
  major) new="$((ma + 1)).0.0" ;;
  minor) new="$ma.$((mi + 1)).0" ;;
  patch) new="$ma.$mi.$((pa + 1))" ;;
  *)
    [[ $1 =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]] || die "not X.Y.Z: $1"
    [ "$(printf '%s\n%s\n' "$cur" "$1" | sort -V | tail -1)" = "$1" ] && [ "$1" != "$cur" ] ||
      die "$1 is not higher than $cur"
    new=$1 ;;
esac
tag="$TAG_PREFIX$new"
git rev-parse -q --verify "refs/tags/$tag" >/dev/null && die "tag $tag already exists"

python3 - "$new" "$(date +%F)" <<'EOF' || die "CHANGELOG.md: [Unreleased] is missing or empty"
import re, sys
new, day = sys.argv[1:]
s = open("CHANGELOG.md").read()
m = re.search(r"^## \[Unreleased\]\n(.*?)(?=^## \[|\Z)", s, re.M | re.S)
if not m or not m.group(1).strip():
    sys.exit(1)
s = s[: m.start()] + f"## [Unreleased]\n\n## [{new}] - {day}\n" + m.group(1) + s[m.end():]
open("CHANGELOG.md", "w").write(s)
EOF

python3 - "$new" "$NAME" "$INIT" <<'EOF'
import re, sys
new, name, init = sys.argv[1:]
for path, pat in [
    (init, r'(?m)^(__version__ = ")[^"]*(")'),
    ("pyproject.toml", r'(?m)^(version = ")[^"]*(")'),
    ("uv.lock", r'(name = "' + re.escape(name) + r'"\nversion = ")[^"]*(")'),
]:
    s = open(path).read()
    s, n = re.subn(pat, rf"\g<1>{new}\g<2>", s, count=1)
    assert n == 1, f"{path}: version line not found"
    open(path, "w").write(s)
EOF

git add "$INIT" pyproject.toml uv.lock CHANGELOG.md
git commit -q -m "Release $NAME $new"
git tag -a "$tag" -m "$NAME $new"
git push -q --atomic origin main "refs/tags/$tag" ||
  die "push failed; undo locally with: git tag -d $tag && git reset --hard HEAD~1"
echo "released $tag (build $(git rev-list --count "$tag")); this checkout now says $NAME $new+$(git rev-list --count "$tag")"
