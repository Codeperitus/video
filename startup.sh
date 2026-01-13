#!/bin/bash

MODEL_DIR="/workspace/ComfyUI/models"
mkdir -p $MODEL_DIR/checkpoints
mkdir -p $MODEL_DIR/vae
mkdir -p $MODEL_DIR/unet
mkdir -p $MODEL_DIR/text_encoders
mkdir -p $MODEL_DIR/controlnet
mkdir -p $MODEL_DIR/loras
mkdir -p $MODEL_DIR/upscale_models
mkdir -p $MODEL_DIR/video

echo "Downloading SDXL Base…"
wget -nc -O $MODEL_DIR/checkpoints/sdxl_base.safetensors \
 https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors

echo "Downloading SDXL Refiner…"
wget -nc -O $MODEL_DIR/checkpoints/sdxl_refiner.safetensors \
 https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors


echo "Downloading SDXL Turbo…"
wget -nc -O $MODEL_DIR/checkpoints/sdxl_turbo.safetensors \
 https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo.safetensors

# ---------- VIDEO MODELS ----------
echo "Downloading SVD 1.1…"
wget -nc -O $MODEL_DIR/video/svd_1.1.safetensors \
 https://huggingface.co/stabilityai/StableVideoDiffusion/resolve/main/svd.safetensors

echo "Downloading SVD-XT…"
wget -nc -O $MODEL_DIR/video/svd_xt.safetensors \
 https://huggingface.co/stabilityai/StableVideoDiffusion/resolve/main/svd_xt.safetensors

echo "Downloading LTXVideo 1.1…"
wget -nc -O $MODEL_DIR/video/ltx_video_fp16.safetensors \
 https://huggingface.co/Lightricks/LTX-Video/resolve/main/model_fp16.safetensors

echo "Downloading ZeroScope XL…"
wget -nc -O $MODEL_DIR/video/zeroscope_xl.safetensors \
 https://huggingface.co/cerspense/zeroscope_v2_XL/resolve/main/zeroscope_v2_XL.safetensors

echo "Downloading CogVideoX Lite (free T2V)…"
wget -nc -O $MODEL_DIR/video/cogv_lite.safetensors \
 https://huggingface.co/THUDM/CogVideoX-lite/resolve/main/model.safetensors

# ---------- UPSCALERS ----------
echo "Downloading 4K Upscaler…"
wget -nc -O $MODEL_DIR/upscale_models/realesrgan_x4.pth \
 https://huggingface.co/xinntao/RealESRGAN/resolve/main/RealESRGAN_x4plus.pth

echo "Starting ComfyUI…"
cd /workspace/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 --enable-cors-header
