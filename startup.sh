#!/bin/bash

echo "=============================="
echo "   🚀 Starting ComfyUI Setup   "
echo "=============================="

MODEL_DIR="/workspace/ComfyUI/models"

mkdir -p $MODEL_DIR/checkpoints
mkdir -p $MODEL_DIR/vae
mkdir -p $MODEL_DIR/unet
mkdir -p $MODEL_DIR/loras
mkdir -p $MODEL_DIR/controlnet
mkdir -p $MODEL_DIR/upscale_models
mkdir -p $MODEL_DIR/video

# ---------- SDXL ----------
wget -nc -O $MODEL_DIR/checkpoints/sdxl_base.safetensors \
 https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors

wget -nc -O $MODEL_DIR/checkpoints/sdxl_refiner.safetensors \
 https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors

wget -nc -O $MODEL_DIR/checkpoints/sdxl_turbo.safetensors \
 https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo.safetensors

# ---------- VIDEO MODELS ----------
wget -nc -O $MODEL_DIR/video/svd_1.1.safetensors \
 https://huggingface.co/stabilityai/StableVideoDiffusion/resolve/main/svd.safetensors

wget -nc -O $MODEL_DIR/video/svd_xt.safetensors \
 https://huggingface.co/stabilityai/StableVideoDiffusion/resolve/main/svd_xt.safetensors

wget -nc -O $MODEL_DIR/video/ltx_video_fp16.safetensors \
 https://huggingface.co/Lightricks/LTX-Video/resolve/main/model_fp16.safetensors

wget -nc -O $MODEL_DIR/video/zeroscope_xl.safetensors \
 https://huggingface.co/cerspense/zeroscope_v2_XL/resolve/main/zeroscope_v2_XL.safetensors

wget -nc -O $MODEL_DIR/video/cogvideo_lite.safetensors \
 https://huggingface.co/THUDM/CogVideoX-lite/resolve/main/model.safetensors

# ---------- UPSCALERS ----------
wget -nc -O $MODEL_DIR/upscale_models/realesrgan_x4.pth \
 https://huggingface.co/xinntao/RealESRGAN/resolve/main/RealESRGAN_x4plus.pth

wget -nc -O $MODEL_DIR/upscale_models/swinir_x4.pth \
 https://huggingface.co/JingyunLiang/SwinIR/resolve/main/001_classicalSR_DF2K_s64w8_SwinIR-M_x4.pth

echo "🚀 Launching ComfyUI..."

cd /workspace/ComfyUI
exec python3 main.py --listen 0.0.0.0 --port 8188 --enable-cors-header
