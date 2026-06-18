#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.config/shabbot"
WHISPER_CACHE="$HOME/.cache/whisper"

echo "=== shabbot uninstall ==="
echo

pipx uninstall shabbot 2> /dev/null && echo "✓ shabbot removed" || echo "shabbot was not installed"

if [[ -d "$CONFIG_DIR" ]]; then
  rm -rf "$CONFIG_DIR"
  echo "✓ config removed ($CONFIG_DIR)"
fi

echo
read -rp "Remove openai-whisper? [y/N] " remove_whisper
if [[ "${remove_whisper,,}" == "y" ]]; then
  pipx uninstall openai-whisper 2> /dev/null && echo "✓ openai-whisper removed" || echo "openai-whisper was not installed"

  if [[ -d "$WHISPER_CACHE" ]]; then
    read -rp "Remove whisper model cache (~$(du -sh "$WHISPER_CACHE" 2> /dev/null | cut -f1))? [y/N] " remove_cache
    if [[ "${remove_cache,,}" == "y" ]]; then
      rm -rf "$WHISPER_CACHE"
      echo "✓ whisper cache removed"
    fi
  fi
fi

echo
echo "=== Done ==="
