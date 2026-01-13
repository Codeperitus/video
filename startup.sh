#!/bin/bash
set -e
echo "=== Starting ComfyUI (Clean Build) ==="

cd /workspace/ComfyUI

# Prevent numpy 2.0 crashes
pip install "numpy<2" --quiet

echo "Launching Server..."
exec python3 main.py --listen 0.0.0.0 --port 8188 --enable-cors-header
