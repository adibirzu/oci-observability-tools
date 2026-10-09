#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(unset CDPATH; cd -- "$(dirname -- "$0")" && pwd)
DRY_RUN=0
UNINSTALL=0
LIST_ONLY=0
HARNESS_ARGS=()

usage() {
  echo "Usage: install.sh [--dry-run] [--uninstall] [--list] [claude|codex|gemini|antigravity ...]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --list) LIST_ONLY=1 ;;
    --help|-h) usage; exit 0 ;;
    claude|codex|gemini|antigravity) HARNESS_ARGS+=("$1") ;;
    *) echo "Unknown harness or option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if [ "$LIST_ONLY" -eq 1 ]; then
  echo "claude"
  echo "codex"
  echo "gemini"
  echo "antigravity"
  exit 0
fi

if [ "${#HARNESS_ARGS[@]}" -eq 0 ]; then
  [ -d "$HOME/.claude" ] && HARNESS_ARGS+=("claude")
  [ -d "$HOME/.codex" ] && HARNESS_ARGS+=("codex")
  [ -d "$HOME/.gemini" ] && HARNESS_ARGS+=("gemini")
  [ -d "$HOME/.antigravity" ] && HARNESS_ARGS+=("antigravity")
fi

codex_default="$HOME/.codex/skills"
if [ -d "$HOME/.agents/skills" ]; then
  codex_default="$HOME/.agents/skills"
fi

target_for() {
  case "$1" in
    claude) echo "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}" ;;
    codex) echo "${CODEX_SKILLS_DIR:-$codex_default}" ;;
    antigravity) echo "${AGY_SKILLS_DIR:-$HOME/.antigravity/skills}" ;;
    gemini) echo "${GEMINI_EXT_DIR:-$HOME/.gemini/extensions/oci-observability-tools}" ;;
  esac
}

remove_empty_parents() {
  current=$1
  while [ "$current" != "$HOME" ] && [ "$current" != "/" ]; do
    rmdir "$current" 2>/dev/null || break
    current=$(dirname "$current")
  done
}

uninstall_harness() {
  harness=$1
  target=$(target_for "$harness")
  manifest="$target/.oci-observability-tools.manifest"
  if [ ! -f "$manifest" ]; then
    echo "No install manifest for $harness at $target"
    return
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    while IFS= read -r path; do
      [ -n "$path" ] && echo "WOULD remove $path"
    done < "$manifest"
    echo "WOULD remove $manifest"
    return
  fi
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    if [ -L "$path" ] || [ -f "$path" ]; then
      rm -f "$path"
    elif [ -d "$path" ]; then
      rm -rf "$path"
    fi
  done < "$manifest"
  rm -f "$manifest"
  remove_empty_parents "$target"
}

install_skills_harness() {
  harness=$1
  target=$2
  bundle="$target/oci-observability-tools"
  manifest="$target/.oci-observability-tools.manifest"
  if [ -e "$bundle" ] || [ -L "$bundle" ] || [ -e "$manifest" ]; then
    echo "Skipping $harness: managed path already exists at $target" >&2
    return
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "WOULD copy $ROOT_DIR -> $bundle"
    for skill in "$ROOT_DIR"/skills/*; do
      name=$(basename "$skill")
      echo "WOULD link $bundle/skills/$name -> $target/$name"
    done
    return
  fi
  mkdir -p "$bundle"
  for name in skills references catalog scripts; do
    cp -R "$ROOT_DIR/$name" "$bundle/$name"
  done
  cp "$ROOT_DIR/AGENTS.md" "$bundle/AGENTS.md"
  : > "$manifest"
  for skill in "$ROOT_DIR"/skills/*; do
    name=$(basename "$skill")
    link="$target/$name"
    if [ -e "$link" ] || [ -L "$link" ]; then
      echo "Skipping existing path $link" >&2
      continue
    fi
    ln -s "$bundle/skills/$name" "$link"
    echo "$link" >> "$manifest"
  done
  echo "$bundle" >> "$manifest"
}

install_gemini() {
  target=$1
  manifest="$target/.oci-observability-tools.manifest"
  if [ -e "$target" ] || [ -L "$target" ]; then
    echo "Skipping gemini: path already exists at $target" >&2
    return
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "WOULD copy $ROOT_DIR -> $target"
    return
  fi
  mkdir -p "$target"
  for name in skills references catalog scripts; do
    cp -R "$ROOT_DIR/$name" "$target/$name"
  done
  cp "$ROOT_DIR/gemini-extension.json" "$target/gemini-extension.json"
  cp "$ROOT_DIR/GEMINI.md" "$target/GEMINI.md"
  : > "$manifest"
  for name in skills references catalog scripts gemini-extension.json GEMINI.md; do
    echo "$target/$name" >> "$manifest"
  done
}

for harness in "${HARNESS_ARGS[@]}"; do
  target=$(target_for "$harness")
  if [ "$UNINSTALL" -eq 1 ]; then
    uninstall_harness "$harness"
  elif [ "$harness" = "gemini" ]; then
    install_gemini "$target"
  else
    install_skills_harness "$harness" "$target"
  fi
done
