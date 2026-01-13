import os
import torch
import imageio
from diffusers import CogVideoXPipeline
from huggingface_hub import login

login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

# Correct official repo
MODEL_ID = "THUDM/cogvideox-5b"

cog_pipe = CogVideoXPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16
).to("cuda")

def run_cogvideo(prompt, output_path):
    result = cog_pipe(
        prompt=prompt,
        num_frames=16,
        guidance_scale=5.5,
        num_inference_steps=28
    )
    frames = result.frames[0]
    imageio.mimsave(output_path, frames, fps=12)
