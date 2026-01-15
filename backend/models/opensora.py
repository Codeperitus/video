import os
import torch
from diffusers import DiffusionPipeline
from huggingface_hub import login

MODEL_NAME = "OpenMotionLab/OpenSora-STDiT2-V1.2"

hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
if hf_token:
    login(token=hf_token)

pipe = None

def get_opensora_pipeline():
    global pipe
    if pipe is None:
        pipe = DiffusionPipeline.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16
        ).to("cuda")

    return pipe


def generate_opensora_video(prompt: str, num_frames: int, height: int, width: int):
    pipe = get_opensora_pipeline()

    result = pipe(
        prompt=prompt,
        num_frames=num_frames,
        height=height,
        width=width,
        guidance_scale=7.5
    )

    # diffusers new API → sometimes video stored as "frames"
    if hasattr(result, "frames"):
        frames = result.frames[0]
    else:
        frames = result.videos[0]

    return frames
