#!/bin/bash
set -euo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

GHIDRA_VER=12.1.4
GHIDRA_DATE=20260921
GHIDRA_DIR=/opt/ghidra/ghidra_${GHIDRA_VER}_PUBLIC

command -v rea >/dev/null || npm install --global rea-agents

if [ ! -d "$GHIDRA_DIR" ]; then
  tmp=$(mktemp -d)
  curl -fsSL -o "$tmp/ghidra.zip" "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_${GHIDRA_VER}_build/ghidra_${GHIDRA_VER}_PUBLIC_${GHIDRA_DATE}.zip"
  mkdir -p /opt/ghidra
  unzip -q "$tmp/ghidra.zip" -d /opt/ghidra
  rm -rf "$tmp"
fi

[ -z "${CLAUDE_ENV_FILE:-}" ] || echo "export GHIDRA_INSTALL_DIR=$GHIDRA_DIR" >> "$CLAUDE_ENV_FILE"
export GHIDRA_INSTALL_DIR=$GHIDRA_DIR

claude mcp remove rea -s user >/dev/null 2>&1 || true
claude mcp add rea -s user -e GHIDRA_INSTALL_DIR="$GHIDRA_DIR" -- "$(command -v rea)" mcp
rea setup --client claude_code --yes --json >/dev/null
rea doctor --client claude_code --skill --json | grep -q '"healthy":true'
