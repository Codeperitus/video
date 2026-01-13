import os
import torch
import imageio
from diffusers import OpenSoraPipeline
from huggingface_hub import login

login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

sora_pipe = OpenSoraPipeline.from_pretrained(
    "opensora-team/OpenSora-1.0",
    torch_dtype=torch.float16
).to("cuda")

def run_opensora(prompt, output_path):
    result = sora_pipe(
        prompt=prompt,
        num_frames=16,
        num_inference_steps=32,
        guidance_scale=5.0
    )
    imageio.mimsave(output_path, result.frames, fps=12)
