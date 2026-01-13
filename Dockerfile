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

# ---------- Install PyTorch ----------
RUN pip install torch==2.1.2 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121

# ---------- Install ComfyUI core requirements ----------
RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

# ---------- Optional extra nodes dependencies ----------
COPY requirements-extra.txt /workspace/requirements-extra.txt
RUN pip install -r /workspace/requirements-extra.txt

# ---------- Install ONLY ComfyUI Manager ----------
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager.git custom_nodes/ComfyUI-Manager

# ---------- Upscalers ----------
RUN pip install realesrgan

# ---------- Include startup script ----------
COPY startup.sh /workspace/startup.sh
RUN chmod +x /workspace/startup.sh

EXPOSE 8188
CMD ["/workspace/startup.sh"]
