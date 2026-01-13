import torch
from diffusers import CogVideoXPipeline
import imageio
import os

cog_pipe = CogVideoXPipeline.from_pretrained(
    "THUDM/CogVideoX-5B",
    torch_dtype=torch.float16
).to("cuda")

def run_cogvideo(prompt, output_path):
    result = cog_pipe(
        prompt=prompt,
        num_frames=16,
        num_inference_steps=25,
        guidance_scale=6.0
    )

    frames = result.frames[0]
    imageio.mimsave(output_path, frames, fps=12)
    return output_path
