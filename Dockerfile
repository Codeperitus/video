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

# ---------- Install PyTorch (MUST COME FIRST) ----------
RUN pip install torch==2.1.2 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121

# ---------- Install ComfyUI core requirements ----------
RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

# ---------- Optional extra nodes requirements ----------
COPY requirements-extra.txt /workspace/requirements-extra.txt
RUN pip install -r /workspace/requirements-extra.txt

# ---------- Video Nodes ----------
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager.git custom_nodes/ComfyUI-Manager
RUN git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff.git custom_nodes/ComfyUI-AnimateDiff
RUN git clone https://github.com/kabachuha/ComfyUI-SVDContent.git custom_nodes/ComfyUI-SVDContent
RUN git clone https://github.com/pythops/ComfyUI-LTXVideo.git custom_nodes/ComfyUI-LTXVideo
RUN git clone https://github.com/ExeterLaboratories/ComfyUI-ZeroScope.git custom_nodes/ComfyUI-ZeroScope
RUN git clone https://github.com/wanghaofan/ComfyUI-CogVideoX.git custom_nodes/ComfyUI-CogVideoX
RUN git clone https://github.com/ltdrdata/ComfyUI-VideoHelperSuite.git custom_nodes/ComfyUI-VideoHelperSuite

# ---------- Image Nodes ----------
RUN git clone https://github.com/cubiq/ComfyUI_essentials.git custom_nodes/ComfyUI_essentials
RUN git clone https://github.com/WASasquatch/was-node-suite-comfyui.git custom_nodes/was-node-suite-comfyui
RUN git clone https://github.com/jags111/ComfyUI_Jags_Node.git custom_nodes/ComfyUI_Jags_Node

# ---------- Upscalers ----------
RUN pip install realesrgan

# ---------- Include startup script ----------
COPY startup.sh /workspace/startup.sh
RUN chmod +x /workspace/startup.sh

EXPOSE 8188
CMD ["/workspace/startup.sh"]
