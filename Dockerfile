FROM ghcr.io/jemeyer/comfyui:latest

USER root

RUN apt update && apt install -y git

# Make bundled ComfyUI look like a real git repo for Manager
RUN cd /app && \
    git remote set-url origin https://github.com/comfyanonymous/ComfyUI.git || true && \
    git fetch origin && \
    git reset --hard origin/master && \
    git submodule update --init --recursive

# Install ComfyUI Manager
RUN cd /app/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

# Install nodes needed by templates
RUN cd /app/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

# Correct startup
ENTRYPOINT ["python", "/app/main.py", "--listen", "0.0.0.0", "--port", "8188"]
