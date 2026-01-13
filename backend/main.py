from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import os

from generate import generate_image
from animate_diff import run_animatediff
from cogvideo import run_cogvideo
from opensora import run_opensora


app = FastAPI()

# -----------------------
# TEXT TO IMAGE (SDXL)
# -----------------------
class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
def generate(prompt: Prompt):
    try:
        output_path = f"outputs/{uuid.uuid4().hex}.png"
        generate_image(prompt.prompt, output_path)
        return {"url": f"/download/{os.path.basename(output_path)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# DOWNLOAD
# -----------------------
@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"outputs/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


# -----------------------
# GEMINI-STYLE VIDEO GENERATOR
# -----------------------
@app.post("/veo-video")
async def veo_video(
    prompt: str = Form(...),
    mode: str = Form(...),   # animatediff / cogvideo / opensora
    file1: UploadFile = File(None),
    file2: UploadFile = File(None),
    file3: UploadFile = File(None),
):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Save user images
    images = []
    for f in [file1, file2, file3]:
        if f:
            img_path = f"uploads/{uuid.uuid4().hex}.png"
            with open(img_path, "wb") as w:
                w.write(await f.read())
            images.append(img_path)

    # Output video name
    video_name = f"{uuid.uuid4().hex}.mp4"
    video_path = f"outputs/{video_name}"

    # -----------------------
    # CHOOSE MODEL
    # -----------------------
    if mode == "animatediff":
        if len(images) == 0:
            raise HTTPException(status_code=400, detail="AnimatedDiff needs at least 1 image.")
        run_animatediff(images[0], "cinematic", video_path)

    elif mode == "cogvideo":
        run_cogvideo(prompt, video_path)

    elif mode == "opensora":
        run_opensora(prompt, video_path)

    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

    return {"url": f"/download/{video_name}"}
