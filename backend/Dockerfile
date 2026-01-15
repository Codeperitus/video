FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# System deps
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git ffmpeg && \
    apt-get clean

WORKDIR /app
COPY . .

RUN pip3 install --upgrade pip

# PyTorch GPU (CUDA 12.1 which is correct for diffusers + CUDA 12.4 runtime)
RUN pip3 install torch==2.3.0 --extra-index-url https://download.pytorch.org/whl/cu121

# Install needed libs
RUN pip3 install --upgrade diffusers transformers accelerate einops sentencepiece

# Project requirements
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
