#!/usr/bin/env bash
# Build the Jekyll site (from the `builder` branch) and publish the static
# output to the `master` branch, which GitHub Pages serves at thomaspaul.dev.
#
# Hardened vs. the original:
#   * aborts on ANY error (set -euo pipefail) so a bad build never reaches master
#   * initialises the `_posts` submodule so blog posts can't silently vanish
#   * validates the build (index.html, CNAME, posts present) before publishing
#   * publishes via an isolated clone and only pushes when the build is valid
#
# Usage (from the repo root, on the `builder` branch):
#   bash publish.sh

set -euo pipefail

# Always operate from the repo root (directory containing this script).
cd "$(dirname "$0")"
REPO="$(pwd)"
SITE="$REPO/_site"
REMOTE="$(git config --get remote.origin.url)"
BRANCH="master"

echo ">> Repo:   $REPO"
echo ">> Remote: $REMOTE"

# 0. Load rbenv if present, so `bundle`/`jekyll` are available even in a
#    non-interactive shell (e.g. `bash publish.sh`). Harmless if not installed
#    (e.g. CI using system Ruby).
if [ -d "$HOME/.rbenv" ]; then
  export RBENV_ROOT="$HOME/.rbenv"
  export PATH="$RBENV_ROOT/bin:$PATH"
  eval "$(rbenv init - bash)"
fi

# Fail early with a clear message if the Ruby toolchain still isn't available.
command -v bundle >/dev/null 2>&1 || {
  echo "ERROR: 'bundle' not found on PATH. Install Ruby/Bundler (or fix rbenv) and retry."
  exit 1
}

# 1. Ensure the posts submodule (_posts -> kaizen) is present and checked out.
echo ">> Updating submodules (_posts)..."
git submodule update --init --recursive

# 2. Install gems and build the site fresh.
echo ">> bundle install..."
bundle install
echo ">> Building site..."
rm -rf "$SITE"
bundle exec jekyll build

# 3. Validate the build BEFORE touching the live branch.
echo ">> Validating build..."
[ -s "$SITE/index.html" ]     || { echo "ERROR: _site/index.html missing/empty. Aborting."; exit 1; }
[ -s "$SITE/assets/CNAME" ]   || { echo "ERROR: _site/assets/CNAME missing. Aborting."; exit 1; }
POSTS="$(find "$SITE" -regextype posix-extended -regex '.*/20[0-9]{2}/.*\.html' | wc -l)"
[ "$POSTS" -ge 1 ]            || { echo "ERROR: no blog posts in build (submodule empty?). Aborting."; exit 1; }
echo "   OK: index.html present, CNAME present, $POSTS post page(s)."

# 4. Publish to master via an isolated clone (can't corrupt the working repo).
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
echo ">> Cloning $BRANCH (shallow) into $TMP ..."
git clone --depth 1 --branch "$BRANCH" "$REMOTE" "$TMP/site"
cd "$TMP/site"

echo ">> Replacing published files with the fresh build..."
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$SITE/." .

# GitHub Pages needs the CNAME at the root of the published branch.
cp "$SITE/assets/CNAME" ./CNAME
echo "   root CNAME = $(cat ./CNAME)"

git add -A
if git diff --cached --quiet; then
  echo ">> No changes vs current $BRANCH. Nothing to publish."
  exit 0
fi

echo ">> Publishing these changes:"
git diff --cached --stat | tail -n 40
git commit -m "Site updated"
echo ">> Pushing to origin/$BRANCH ..."
git push origin "$BRANCH"
echo ">> Done. Live at https://www.thomaspaul.dev/"
