import os
import uuid
import torch
import imageio

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from diffusers import DiffusionPipeline
from huggingface_hub import login

# --------------------------
# FASTAPI INIT
# --------------------------
app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# --------------------------
# SDXL IMAGE GENERATOR (your existing code)
# --------------------------
from models.sdxl import generate_image


# --------------------------
# COGVIDE2 VIDEO MODEL CONFIG
# --------------------------
MODEL_NAME = "zai-org/CogVideoX-2b"

hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
if hf_token:
    login(token=hf_token)

video_pipe = None


def get_video_pipeline():
    global video_pipe
    if video_pipe is None:
        video_pipe = DiffusionPipeline.from_pretrained(
            MODEL_NAME,
            dtype=torch.float16,
            device_map="balanced"
        )
    return video_pipe


def generate_cogvideo_video(prompt: str):
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()

    pipe = get_video_pipeline()

    result = pipe(
        prompt,
        num_frames=25  # safe for H200
    )

    if hasattr(result, "frames"):
        frames = result.frames[0]
    else:
        frames = result.videos[0]

    return frames


def save_video(frames, output_path: str, fps: int = 8):
    imageio.mimsave(output_path, frames, fps=fps)
    return output_path


# --------------------------
# ROUTE: TEXT → IMAGE (SDXL)
# --------------------------
@app.post("/generate")
def text_to_image(prompt: str = Form(...)):
    try:
        file_name = f"{uuid.uuid4().hex}.png"
        output_path = f"outputs/{file_name}"

        generate_image(prompt, output_path)

        return {"url": f"/download/{file_name}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------
# ROUTE: DOWNLOAD ANY OUTPUT
# --------------------------
@app.get("/download/{file}")
def download(file: str):
    path = f"outputs/{file}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


# --------------------------
# ROUTE: TEXT → VIDEO (NEW COGVIDEOX)
# --------------------------
@app.post("/video")
async def generate_video(prompt: str = Form(...)):
    try:
        video_name = f"{uuid.uuid4().hex}.mp4"
        output_path = f"outputs/{video_name}"

        frames = generate_cogvideo_video(prompt)
        save_video(frames, output_path)

        return {"url": f"/download/{video_name}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------
# HEALTH CHECK
# --------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "image_model": "SDXL",
        "video_model": "CogVideoX-2B"
    }
