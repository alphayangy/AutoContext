#!/usr/bin/env bash
set -euo pipefail

# Auto Context multi-agent install script
# Usage: bash install.sh [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="auto-context"

# Default: install Claude Code global + Cursor project
INSTALL_CLAUDE_GLOBAL=0
INSTALL_CLAUDE_PROJECT=0
INSTALL_CURSOR_PROJECT=0
INSTALL_KIMI_PROJECT=0
INSTALL_ALL=0

print_usage() {
  cat <<EOF
Install Auto Context skill for various AI coding agents.

Usage: bash install.sh [options]

Options:
  --claude-global     Install as a global Claude Code skill
  --claude-project    Install as a project-level Claude Code skill
  --cursor-project    Install as a project-level Cursor skill
  --kimi-project      Install AGENTS.md for Kimi Code in current project
  --all               Install everywhere applicable
  -h, --help          Show this help

Examples:
  bash install.sh --claude-global
  bash install.sh --all
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude-global) INSTALL_CLAUDE_GLOBAL=1 ;;
    --claude-project) INSTALL_CLAUDE_PROJECT=1 ;;
    --cursor-project) INSTALL_CURSOR_PROJECT=1 ;;
    --kimi-project) INSTALL_KIMI_PROJECT=1 ;;
    --all) INSTALL_ALL=1 ;;
    -h|--help) print_usage; exit 0 ;;
    *) echo "Unknown option: $1"; print_usage; exit 1 ;;
  esac
  shift
done

if [[ $INSTALL_ALL -eq 1 ]]; then
  INSTALL_CLAUDE_GLOBAL=1
  INSTALL_CLAUDE_PROJECT=1
  INSTALL_CURSOR_PROJECT=1
  INSTALL_KIMI_PROJECT=1
fi

# If no flags passed, default to Claude Code global + Cursor project
if [[ $INSTALL_CLAUDE_GLOBAL -eq 0 && $INSTALL_CLAUDE_PROJECT -eq 0 && $INSTALL_CURSOR_PROJECT -eq 0 && $INSTALL_KIMI_PROJECT -eq 0 ]]; then
  INSTALL_CLAUDE_GLOBAL=1
  INSTALL_CURSOR_PROJECT=1
fi

copy_skill_files() {
  local target="$1"
  # Remove existing skill directory to avoid symlink/circular copy issues
  rm -rf "$target"
  mkdir -p "$target"
  cp -R "$SCRIPT_DIR/"* "$target/"
  # Remove install script itself from installed copy to avoid clutter
  rm -f "$target/install.sh"
}

install_claude_global() {
  local target="$HOME/.claude/skills/$SKILL_NAME"
  echo "Installing Auto Context for Claude Code (global): $target"
  copy_skill_files "$target"
  echo "  Done. Restart Claude Code if running."
}

install_claude_project() {
  local target=".claude/skills/$SKILL_NAME"
  echo "Installing Auto Context for Claude Code (project): $target"
  copy_skill_files "$target"
  echo "  Done."
}

install_cursor_project() {
  local target=".cursor/skills/$SKILL_NAME"
  echo "Installing Auto Context for Cursor (project): $target"
  copy_skill_files "$target"
  echo "  Done."
}

install_kimi_project() {
  echo "Installing Auto Context for Kimi Code (project): AGENTS.md"
  cp "$SCRIPT_DIR/SKILL.md" "AGENTS.md"
  echo "  Done. Note: Kimi Code uses AGENTS.md directly; you may want to trim SKILL-specific frontmatter."
}

if [[ $INSTALL_CLAUDE_GLOBAL -eq 1 ]]; then
  install_claude_global
fi

if [[ $INSTALL_CLAUDE_PROJECT -eq 1 ]]; then
  install_claude_project
fi

if [[ $INSTALL_CURSOR_PROJECT -eq 1 ]]; then
  install_cursor_project
fi

if [[ $INSTALL_KIMI_PROJECT -eq 1 ]]; then
  install_kimi_project
fi

echo "Install complete."
