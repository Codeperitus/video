import torch
import os
from diffusers import AnimateDiffPipeline
from PIL import Image
import imageio
from huggingface_hub import login

# Login to HuggingFace (safe even if not required)
login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

# Load WORKING AnimateDiff model (Lightning version)
ad_pipe = AnimateDiffPipeline.from_pretrained(
    "ByteDance/AnimateDiff-Lightning",
    torch_dtype=torch.float16
).to("cuda")


def run_animatediff(image_path, prompt, output_path):
    # Load input image
    image = Image.open(image_path).convert("RGB")

    # Generate motion frames
    frames = ad_pipe(
        prompt=prompt,
        image=image,
        num_frames=24,
        guidance_scale=3.0,
    ).frames

    # Save as video/gif
    imageio.mimsave(output_path, frames, fps=12)
