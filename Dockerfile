FROM ghcr.io/jemeyer/comfyui:latest

USER root

# Install git
RUN apt update && apt install -y git

# Convert bundled ComfyUI into real git repo (Manager requires this)
RUN cd /app && \
    git init && \
    git remote add origin https://github.com/comfyanonymous/ComfyUI.git && \
    git fetch && \
    git reset --hard origin/master && \
    git submodule update --init --recursive

# Install ComfyUI Manager
RUN cd /app/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

# Install template-required nodes
RUN cd /app/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

# Always start ComfyUI correctly
ENTRYPOINT ["python", "/app/main.py", "--listen", "0.0.0.0", "--port", "8188"]
