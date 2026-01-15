import os
import torch
import imageio
from diffusers import DiffusionPipeline
from huggingface_hub import login

hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
if hf_token and hf_token.strip():
    login(token=hf_token)

# ✅ Correct model
MODEL_NAME = "OpenMotionLab/OpenSora-STDiT2-V1.2"

pipe = None

def get_pipe():
    global pipe
    if pipe is None:
        pipe = DiffusionPipeline.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16
        ).to("cuda")
    return pipe

def generate_opensora_video(prompt: str, output_path: str):
    pipe = get_pipe()

    result = pipe(
        prompt=prompt,
        num_frames=56,
        height=512,
        width=896,
        guidance_scale=7.5
    )

    frames = getattr(result, "frames", None)
    if frames is None:
        frames = result.videos[0]

    imageio.mimsave(output_path, frames, fps=24)
