#!/usr/bin/env bash
# Restore the creative toolkit in a fresh cloud session.
#   bash toolkit/setup.sh            # skills + agent-browser + OpenMontage
#   SKIP_OPENMONTAGE=1 bash toolkit/setup.sh
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Installing skills into ~/.claude/skills"
mkdir -p "$HOME/.claude/skills"
for dir in "$REPO_DIR"/.claude/skills/*/; do
  name="$(basename "$dir")"
  rm -rf "$HOME/.claude/skills/$name"
  cp -rL "$dir" "$HOME/.claude/skills/$name"
  echo "    $name"
done

echo "==> Installing agent-browser CLI and its Chrome"
if ! command -v agent-browser >/dev/null 2>&1; then
  npm i -g agent-browser
fi
agent-browser install

echo "==> Setting up free local image generation (no keys, no accounts)"
bash "$REPO_DIR/.claude/skills/free-image-gen/scripts/setup.sh"

if [ "${SKIP_OPENMONTAGE:-0}" != "1" ]; then
  OM_DIR="${OPENMONTAGE_DIR:-$HOME/OpenMontage}"
  echo "==> Installing OpenMontage into $OM_DIR"
  if [ ! -d "$OM_DIR/.git" ]; then
    GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/calesthio/OpenMontage "$OM_DIR"
  fi
  (cd "$OM_DIR" && make setup)
  echo "    Add API keys to $OM_DIR/.env (HIGGSFIELD_API_KEY/SECRET, FAL_KEY, ...)"
fi

echo "Done. Start a new Claude session so the skills are picked up."
