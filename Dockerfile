FROM ghcr.io/jemeyer/comfyui:latest

USER root

# Install git (jemeyer image is Debian-based, not Alpine)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Ensure ComfyUI is a real git repo so Manager can verify version
WORKDIR /app
RUN git init && \
    git remote add origin https://github.com/comfyanonymous/ComfyUI.git && \
    git fetch origin && \
    git reset --hard origin/master

# Install ComfyUI-Manager
WORKDIR /app/custom_nodes
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager

# Install required custom nodes
RUN git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

# Correct startup for Northflank (no CLI override needed)
ENTRYPOINT ["python", "/app/main.py", "--listen", "0.0.0.0", "--port", "8188"]
