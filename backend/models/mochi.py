import torch
from diffusers import MochiPipeline
from huggingface_hub import login
import os, imageio

# Optional: login if token exists
hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
if hf_token and hf_token.strip() != "":
    login(token=hf_token)

# FIXED MODEL NAME
MODEL_NAME = "lumaai/LumaAI-Mochi"

# Load Mochi model on GPU
pipe = MochiPipeline.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16   # torch_dtype deprecated
).to("cuda")


def generate_mochi_video(prompt: str, output_path: str):
    """
    Generate video using Mochi model
    """

    result = pipe(
        prompt=prompt,
        num_frames=96,   # 4 seconds @ 24fps
        fps=24,
        height=720,
        width=1280,
        guidance_scale=5.0
    )

    frames = result.frames

    # Save as MP4
    imageio.mimsave(output_path, frames, fps=24)
