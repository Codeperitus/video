FROM ghcr.io/jemeyer/comfyui:latest

USER root
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Replace bundled ComfyUI with real upstream git
RUN rm -rf /app/* && \
    git clone https://github.com/comfyanonymous/ComfyUI.git /app

# Install Python deps
RUN pip install -r /app/requirements.txt

# Install ComfyUI Manager
WORKDIR /app/custom_nodes
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager

# Install nodes used by templates
RUN git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

# Expose ComfyUI
EXPOSE 8188

# Start ComfyUI
CMD ["python", "/app/main.py", "--listen", "0.0.0.0", "--port", "8188"]
