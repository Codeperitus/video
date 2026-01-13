from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
import uuid, os

from models.sdxl import generate_image
# from models.animatediff import run_animatediff
# from models.text2video import run_text2video

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# -----------------------
# TEXT → IMAGE
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
        raise HTTPException(404, "File not found")
    return FileResponse(path)


# -----------------------
# TEXT → VIDEO ONLY
# -----------------------
@app.post("/video")
async def video_api(
    prompt: str = Form(...),
    mode: str = Form("text2video")
):
    if mode != "text2video":
        raise HTTPException(400, "Only text2video is supported now")

    video_name = f"{uuid.uuid4().hex}.gif"
    video_path = f"outputs/{video_name}"

    # Placeholder: create a blank GIF (for now)
    # You will replace this with actual model
    with open(video_path, "wb") as f:
        f.write(b"GIF89a")  # Tiny valid GIF header

    return {"url": f"/download/{video_name}"}
