FROM ghcr.io/jemeyer/comfyui:latest

USER root

RUN apt-get update && apt-get install -y git

RUN cd /app/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

RUN cd /app/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

# Let Manager detect ComfyUI version correctly
RUN cd /opt/comfyui && \
    git init && \
    git remote add origin https://github.com/comfyanonymous/ComfyUI.git && \
    git fetch origin && \
    git reset --hard origin/master
