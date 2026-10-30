#!/usr/bin/env bash
# One-time setup for free-image-gen. No API keys, no accounts.
set -euo pipefail
ROOT="${FREE_IMAGE_HOME:-$HOME/.cache/free-image-gen}"
mkdir -p "$ROOT"
if [ ! -x "$ROOT/venv/bin/python" ]; then
  python3 -m venv "$ROOT/venv"
fi
PY="$ROOT/venv/bin/python"
"$PY" -m pip install -q --upgrade pip
"$PY" -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu
"$PY" -m pip install -q diffusers transformers accelerate safetensors pillow numpy "rembg[cpu]"
echo "==> Pre-downloading models"
"$PY" - <<'PYEOF'
from diffusers import DiffusionPipeline
DiffusionPipeline.download("SimianLuo/LCM_Dreamshaper_v7")
from rembg import new_session
new_session("isnet-general-use")
print("models ready")
PYEOF
echo "Ready. Use: $PY .claude/skills/free-image-gen/scripts/generate.py \"prompt\" -o out.png"
