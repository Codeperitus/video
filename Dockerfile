FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# System deps
RUN apt-get update && apt-get install -y python3 python3-pip git

# Working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python deps
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 8000

# Start API
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
