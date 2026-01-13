FROM ghcr.io/jemeyer/comfyui:latest

USER root

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone real upstream ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui

# Install python deps
RUN pip install -r /opt/comfyui/requirements.txt

# Install ComfyUI Manager
RUN mkdir -p /opt/comfyui/custom_nodes && \
    cd /opt/comfyui/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager

# Install video + control nodes
RUN cd /opt/comfyui/custom_nodes && \
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved && \
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux && \
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

EXPOSE 8188

ENTRYPOINT ["python", "/opt/comfyui/main.py", "--listen", "0.0.0.0", "--port", "8188"]
