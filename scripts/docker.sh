#!/usr/bin/env bash
set -euo pipefail

MODELS=(tiny base small medium large large-v2 large-v3 large-v3-turbo)
DEFAULT_MODEL="large-v3-turbo"

echo "=== shabbot Docker setup ==="
echo

# --- Check Docker ---
if ! command -v docker &> /dev/null; then
  echo "Docker not found. Install it from https://docs.docker.com/get-docker/"
  exit 1
fi

if ! docker compose version &> /dev/null; then
  echo "Docker Compose plugin not found. Install it from https://docs.docker.com/compose/install/"
  exit 1
fi

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

# --- Tokens ---
echo "Telegram bot token (from https://t.me/BotFather):"
read -rsp "SHABBOT_TOKEN: " SHABBOT_TOKEN
echo

echo "Todoist API token (from https://todoist.com/app/settings/integrations/developer):"
read -rsp "TODOIST_TOKEN: " TODOIST_TOKEN
echo
echo

# --- Write docker.env ---
cat > docker.env << EOF
SHABBOT_TOKEN=$SHABBOT_TOKEN
TODOIST_TOKEN=$TODOIST_TOKEN
WHISPER_MODEL=$WHISPER_MODEL
EOF
chmod 600 docker.env
echo "Config saved to docker.env"
echo

# --- Build and start ---
echo "Building and starting shabbot..."
docker compose up -d --build
echo

echo "=== Done. ==="
echo
echo "The Whisper model will be downloaded on first start (~1.5 GB)."
echo "Watch logs: docker compose logs -f"
