from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from generate import generate_image
import uuid
import os

app = FastAPI()

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

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"outputs/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
