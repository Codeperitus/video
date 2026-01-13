from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import uuid, os

# Load model modules
from models.sdxl import generate_image
from models.animatediff import run_animatediff

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# -----------------------
# TEXT → IMAGE (SDXL)
# -----------------------
@app.post("/generate")
def text_to_image(prompt: str = Form(...)):
    try:
        output_path = f"outputs/{uuid.uuid4().hex}.png"
        generate_image(prompt, output_path)
        return {"url": f"/download/{os.path.basename(output_path)}"}
    except Exception as e:
        raise HTTPException(500, str(e))


# -----------------------
# DOWNLOAD FILE
# -----------------------
@app.get("/download/{file}")
def download(file: str):
    path = f"outputs/{file}"
    if not os.path.exists(path):
        return {"error": "file not found"}
    return FileResponse(path)


# -----------------------
# MULTI-MODE VIDEO GENERATOR
# -----------------------
@app.post("/video")
async def video_api(
    prompt: str = Form(...),
    mode: str = Form(...),  
    file1: UploadFile = File(None)
):
    video_name = f"{uuid.uuid4().hex}.gif"   # FIXED
    video_path = f"outputs/{video_name}"

    img_path = None
    if file1:
        img_path = f"uploads/{uuid.uuid4().hex}.png"
        with open(img_path, "wb") as f:
            f.write(await file1.read())

    if mode == "animatediff":
        if not img_path:
            raise HTTPException(400, "AnimatedDiff needs an image")
        run_animatediff(img_path, prompt, video_path)

    else:
        raise HTTPException(400, "Invalid mode")

    return {"url": f"/download/{video_name}"}
