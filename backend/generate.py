from diffusers import StableDiffusionXLPipeline
import torch
import os

# Load model once at startup
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

def generate_image(prompt, output_path):
    os.makedirs("outputs", exist_ok=True)
    image = pipe(prompt).images[0]
    image.save(output_path)
    return output_path
