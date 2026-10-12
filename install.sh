#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/skills"
DEST_ROOT="${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${OPENCODE_SKILLS_BACKUP_DIR:-$HOME/.config/opencode/skills-backups/$STAMP}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: skills directory not found: $SOURCE_DIR" >&2
  exit 1
fi
mkdir -p "$DEST_ROOT"
installed=0
backed_up=0
while IFS= read -r -d '' skill_file; do
  skill_dir="$(dirname -- "$skill_file")"
  skill_id="$(basename -- "$skill_dir")"
  [[ -f "$skill_dir/SKILL.md" ]] || continue
  dest="$DEST_ROOT/$skill_id"
  if [[ -e "$dest" ]]; then
    backup="$BACKUP_ROOT/$skill_id"
    mkdir -p "$(dirname -- "$backup")"
    cp -a "$dest" "$backup"
    rm -rf -- "$dest"
    backed_up=$((backed_up+1))
  fi
  cp -a "$skill_dir" "$dest"
  installed=$((installed+1))
done < <(find "$SOURCE_DIR" -mindepth 2 -maxdepth 2 -type f -name SKILL.md -print0 | sort -z)

echo "Installed skills: $installed"
echo "Existing skills backed up: $backed_up"
if [[ "$backed_up" -gt 0 ]]; then echo "Backup directory: $BACKUP_ROOT"; fi
echo "OpenCode process and server were not stopped or restarted."
