import os
import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from PIL import Image
import imageio
from huggingface_hub import login

# Login to HF
login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

# Base SD model
base_model = "runwayml/stable-diffusion-v1-5"

# Load motion adapter (THIS EXISTS)
motion_adapter = MotionAdapter.from_pretrained(
    "guoyww/animatediff-motion-adapter-v1-5",
    torch_dtype=torch.float16
)

# Build pipeline manually (official method)
ad_pipe = AnimateDiffPipeline.from_pretrained(
    base_model,
    motion_adapter=motion_adapter,
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
