# ---------- Base CUDA Image ----------
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# ---------- System updates ----------
RUN apt-get update && apt-get install -y \
    git wget curl ffmpeg python3 python3-pip python3-venv build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# ---------- Clone Latest ComfyUI ----------
RUN git clone https://github.com/comfyanonymous/ComfyUI.git

WORKDIR /workspace/ComfyUI

# ---------- Install PyTorch (correct version for ComfyUI) ----------
# Torch 2.3.1 + CUDA 12.1 + torchvision/torchaudio
RUN pip install --upgrade pip
RUN pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --extra-index-url https://download.pytorch.org/whl/cu121

# ---------- Install ComfyUI core requirements ----------
RUN pip install -r requirements.txt

# ---------- Install ONLY ComfyUI Manager ----------
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager.git custom_nodes/ComfyUI-Manager

# ---------- Copy minimal startup script ----------
COPY startup.sh /workspace/startup.sh
RUN chmod +x /workspace/startup.sh

EXPOSE 8188

CMD ["bash", "/workspace/startup.sh"]
