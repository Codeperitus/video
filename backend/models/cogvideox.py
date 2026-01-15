import torch
from diffusers import CogVideoXPipeline
import imageio
import os
from huggingface_hub import login

# Optional HuggingFace token
hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
if hf_token and hf_token.strip() != "":
    login(token=hf_token)

# REAL, VERIFIED MODEL
MODEL_NAME = "THUDM/CogVideoX-2b"

# Load CogVideoX
pipe = CogVideoXPipeline.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16
).to("cuda")


def generate_cogvideo(prompt: str, output_path: str):
    """
    Generate video using CogVideoX 2.0
    """

    result = pipe(
        prompt=prompt,
        num_frames=48,     # 2 seconds @ 24fps
        guidance_scale=6.0,
        height=480,
        width=848
    )

    frames = result.frames

    # Save MP4
    imageio.mimsave(output_path, frames, fps=24)
