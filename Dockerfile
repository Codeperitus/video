
FROM ghcr.io/jemeyer/comfyui:latest

USER root

# Install git
RUN apt update && apt install -y git

# Install ComfyUI Manager
RUN cd /app/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

# Pre-install common template packs
RUN cd /app/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188"]
