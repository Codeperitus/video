import torch
from diffusers import AnimateDiffPipeline
import imageio
from PIL import Image
import os

ad_pipe = AnimateDiffPipeline.from_pretrained(
    "guoyww/AnimateDiff-SDXL",
    torch_dtype=torch.float16,
).to("cuda")

def run_animatediff(image_path, motion_style, output_path):
    image = Image.open(image_path).convert("RGB")

    if motion_style == "cinematic":
        motion_prompt = "slight camera motion, breathing effect, subtle movement"
    else:
        motion_prompt = "dynamic camera motion, head turn, strong sway, zoom in"

    frames = ad_pipe(
        prompt=motion_prompt,
        image=image,
        num_frames=16,
        guidance_scale=3.0,
    ).frames

    imageio.mimsave(output_path, frames, fps=12)
    return output_path
