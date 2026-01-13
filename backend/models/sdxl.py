import os
import torch
from diffusers import StableDiffusionXLPipeline
from huggingface_hub import login

login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

def generate_image(prompt, output_path):
    image = pipe(prompt).images[0]
    image.save(output_path)
