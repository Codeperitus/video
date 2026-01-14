import torch
from diffusers import MochiPipeline
from huggingface_hub import login
import os, imageio

# Login using environment variable
login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

MODEL_NAME = "luma-art/mochi-1.5"

# Load Mochi model on GPU using BF16 (best for A100/H100)
pipe = MochiPipeline.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
).to("cuda")


def generate_mochi_video(prompt: str, output_path: str):
    """
    Generate a high-quality video using Mochi 1.5.
    Output is saved as MP4 to the given path.
    """

    result = pipe(
        prompt=prompt,
        num_frames=96,      # 4 seconds at 24fps
        fps=24,
        height=720,         # HD output (safe for VRAM)
        width=1280,
        guidance_scale=5.0
    )

    frames = result.frames

    # Save as MP4
    imageio.mimsave(output_path, frames, fps=24)
