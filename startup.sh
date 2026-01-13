#!/bin/bash
set -e
echo "=== Starting ComfyUI ==="

cd /workspace/ComfyUI

exec python3 main.py --listen 0.0.0.0 --port 8188 --enable-cors-header
