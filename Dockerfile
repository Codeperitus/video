FROM ghcr.io/jemeyer/comfyui:latest

USER root

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone real ComfyUI into /opt (NOT /app)
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui

# Install Python deps
RUN pip install -r /opt/comfyui/requirements.txt

# Install ComfyUI Manager
RUN mkdir -p /opt/comfyui/custom_nodes && \
    cd /opt/comfyui/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

# Install nodes used by templates
RUN cd /opt/comfyui/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

# Expose ComfyUI
EXPOSE 8188

# Start ComfyUI from real repo
CMD ["python", "/opt/comfyui/main.py", "--listen", "0.0.0.0", "--port", "8188"]
