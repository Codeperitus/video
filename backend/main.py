from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
import uuid, os

# Image model
from models.sdxl import generate_image

# Video model (CogVideoX)
from models.cogvideox import generate_cogvideo

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ---------------- TEXT → IMAGE ----------------
@app.post("/generate")
def text_to_image(prompt: str = Form(...)):
    try:
        output_path = f"outputs/{uuid.uuid4().hex}.png"
        generate_image(prompt, output_path)
        return {"url": f"/download/{os.path.basename(output_path)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{file}")
def download(file: str):
    path = f"outputs/{file}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


# ---------------- TEXT → VIDEO (CogVideoX) ----------------
@app.post("/cogvideo")
async def cogvideo(prompt: str = Form(...)):
    try:
        video_name = f"{uuid.uuid4().hex}.mp4"
        output_path = f"outputs/{video_name}"

        generate_cogvideo(prompt, output_path)

        return {"url": f"/download/{video_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {
        "status": "running",
        "image_model": "SDXL",
        "video_model": "CogVideoX 2.0"
    }
