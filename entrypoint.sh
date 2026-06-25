#!/bin/sh
python -c "import whisper; whisper.load_model('${WHISPER_MODEL:-large-v3-turbo}')"
exec shabbot
