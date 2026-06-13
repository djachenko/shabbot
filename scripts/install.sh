#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.config/shabbot"
CONFIG_FILE="$CONFIG_DIR/env"

MODELS=(tiny base small medium large large-v2 large-v3 large-v3-turbo)
DEFAULT_MODEL="large-v3-turbo"

echo "=== shabbot setup ==="
echo

# --- Whisper model ---
echo "Whisper model:"
for i in "${!MODELS[@]}"; do
  model="${MODELS[$i]}"
  marker=""
  [[ "$model" == "$DEFAULT_MODEL" ]] && marker=" (default)"
  printf "  %d. %s%s\n" "$((i + 1))" "$model" "$marker"
done
echo
read -rp "Choose [1-${#MODELS[@]}, Enter = ${DEFAULT_MODEL}]: " model_choice

if [[ -z "$model_choice" ]]; then
  WHISPER_MODEL="$DEFAULT_MODEL"
else
  if ! [[ "$model_choice" =~ ^[0-9]+$ ]] || ((model_choice < 1 || model_choice > ${#MODELS[@]})); then
    echo "Invalid choice, using default: $DEFAULT_MODEL"
    WHISPER_MODEL="$DEFAULT_MODEL"
  else
    WHISPER_MODEL="${MODELS[$((model_choice - 1))]}"
  fi
fi

echo "→ $WHISPER_MODEL"
echo

# --- Install whisper ---
echo "Installing openai-whisper..."
pipx install openai-whisper
echo

# --- Download model ---
echo "Downloading $WHISPER_MODEL (~this will take a while)..."
PIPX_VENVS="${PIPX_HOME:-$HOME/.local/pipx}/venvs"
"$PIPX_VENVS/openai-whisper/bin/python" -c "import whisper; whisper.load_model('$WHISPER_MODEL')"
echo

# --- Tokens ---
echo "Telegram bot token (from https://t.me/BotFather):"
read -rsp "SHABBOT_TOKEN: " SHABBOT_TOKEN
echo

echo "Todoist API token (from https://todoist.com/app/settings/integrations/developer):"
read -rsp "TODOIST_TOKEN: " TODOIST_TOKEN
echo
echo

# --- Write config ---
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" << EOF
SHABBOT_TOKEN=$SHABBOT_TOKEN
TODOIST_TOKEN=$TODOIST_TOKEN
WHISPER_MODEL=$WHISPER_MODEL
EOF
chmod 600 "$CONFIG_FILE"
echo "Config saved to $CONFIG_FILE"
echo

# --- Install shabbot ---
echo "Installing shabbot..."
pipx install shabbot
echo

echo "=== Done. Run: shabbot ==="
