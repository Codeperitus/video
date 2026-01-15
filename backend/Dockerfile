FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# System deps
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git ffmpeg && \
    apt-get clean

# App directory
WORKDIR /app
COPY . .

RUN pip3 install --upgrade pip

# ------------------------------------------------------
# Install CORRECT PyTorch GPU version (CUDA 12.1)
# CUDA 12.4 wheels DO NOT EXIST yet — this is REQUIRED
# ------------------------------------------------------
RUN pip3 install torch==2.3.0 --extra-index-url https://download.pytorch.org/whl/cu121

# ------------------------------------------------------
# Install diffusers + transformers (latest)
# ------------------------------------------------------
RUN pip3 install --upgrade diffusers transformers

# ------------------------------------------------------
# Install project requirements
# ------------------------------------------------------
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
