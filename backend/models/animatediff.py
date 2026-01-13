import torch
import os
from diffusers import AnimateDiffPipeline
from PIL import Image
import imageio
from huggingface_hub import login

login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

# WORKING + COMPATIBLE SDXL ANIMATEDIFF
ad_pipe = AnimateDiffPipeline.from_pretrained(
    "camenduru/animatediff-lightning-sdxl",
    torch_dtype=torch.float16
).to("cuda")

def run_animatediff(image_path, prompt, output_path):
    image = Image.open(image_path).convert("RGB")

    frames = ad_pipe(
        prompt=prompt,
        image=image,
        num_frames=24,
        guidance_scale=3.0,
    ).frames

    imageio.mimsave(output_path, frames, fps=12)
