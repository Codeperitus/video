FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive

# System deps
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

# Install matching TorchVision
RUN pip install --no-cache-dir torchvision==0.18.0

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
