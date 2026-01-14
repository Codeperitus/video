FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system deps
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git ffmpeg && \
    apt-get clean

# App directory
WORKDIR /app

# Copy backend app files
COPY . .

# Install python dependencies (GPU version of PyTorch)
RUN pip3 install --upgrade pip

# IMPORTANT: install PyTorch for CUDA 12.4
RUN pip3 install torch --extra-index-url https://download.pytorch.org/whl/cu124

# Install remaining Python deps
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port",  "8000"]
