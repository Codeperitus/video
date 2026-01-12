FROM ghcr.io/jemeyer/comfyui:latest

USER root

RUN apt update && apt install -y git

RUN cd /app/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

RUN cd /app/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
