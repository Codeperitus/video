# ---------- Base CUDA Image ----------
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# ---------- System updates ----------
RUN apt-get update && apt-get install -y \
    git wget curl ffmpeg python3 python3-pip python3-venv build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# ---------- Clone Latest ComfyUI ----------
RUN git clone https://github.com/comfyanonymous/ComfyUI.git

WORKDIR /workspace/ComfyUI

# ---------- Core dependencies ----------
RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

# ---------- Performance Enhancements ----------
RUN pip install xformers==0.0.23 \
    flash-attn \
    einops \
    accelerate \
    triton

# ---------- Extra video libraries ----------
RUN pip install \
    opencv-python \
    imageio imageio-ffmpeg \
    scenedetect \
    moviepy \
    onnxruntime onnxruntime-gpu \
    timm \
    transformers \
    decord

# ---------- Install ComfyUI Manager ----------
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager.git custom_nodes/ComfyUI-Manager

# ---------- Video Nodes ----------
RUN git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git custom_nodes/comfyui_controlnet_aux
RUN git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff.git custom_nodes/ComfyUI-AnimateDiff
RUN git clone https://github.com/kabachuha/ComfyUI-SVDContent.git custom_nodes/ComfyUI-SVDContent
RUN git clone https://github.com/ltdrdata/ComfyUI-VideoHelperSuite.git custom_nodes/ComfyUI-VideoHelperSuite
RUN git clone https://github.com/pythops/ComfyUI-LTXVideo.git custom_nodes/ComfyUI-LTXVideo
RUN git clone https://github.com/ExeterLaboratories/ComfyUI-ZeroScope.git custom_nodes/ComfyUI-ZeroScope
RUN git clone https://github.com/wanghaofan/ComfyUI-CogVideoX.git custom_nodes/ComfyUI-CogVideoX

# ---------- Image Nodes ----------
RUN git clone https://github.com/cubiq/ComfyUI_essentials.git custom_nodes/ComfyUI_essentials
RUN git clone https://github.com/WASasquatch/was-node-suite-comfyui.git custom_nodes/was-node-suite-comfyui
RUN git clone https://github.com/jags111/ComfyUI_Jags_Node.git custom_nodes/ComfyUI_Jags_Node

# ---------- Upscale / 4K Nodes ----------
RUN git clone https://github.com/ltdrdata/ComfyUI-Upscale-Tools.git custom_nodes/ComfyUI-Upscale-Tools
RUN pip install realesrgan

# ---------- Auto model download script ----------
COPY startup.sh /workspace/startup.sh
RUN chmod +x /workspace/startup.sh

EXPOSE 8188
CMD ["/workspace/startup.sh"]
