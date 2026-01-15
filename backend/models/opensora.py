import os
import torch
import imageio
from diffusers import AutoPipelineForText2Video
from huggingface_hub import login

# Optional HF auth
hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
if hf_token and hf_token.strip() != "":
    login(token=hf_token)

MODEL_NAME = "OpenMotionLab/OpenSora-STDiT-v3-2B"

# Load Open-Sora 2B
pipe = AutoPipelineForText2Video.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16
).to("cuda")


def generate_opensora_video(prompt: str, output_path: str):
    """
    Generate cinematic video using Open-Sora 2.0 (2B)
    """
    result = pipe(
        prompt=prompt,
        num_frames=56,    # ~2.3 seconds at 24fps
        height=512,
        width=896,
        guidance_scale=7.5
    )

    frames = result.frames

    # Save as MP4
    imageio.mimsave(output_path, frames, fps=24)
