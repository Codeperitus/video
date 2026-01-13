import torch
import imageio
from diffusers import CogVideoXPipeline
import os
from huggingface_hub import login

login(token=os.environ["HUGGINGFACE_HUB_TOKEN"])

cog_pipe = CogVideoXPipeline.from_pretrained(
    "THUDM/CogVideoX-5B",
    torch_dtype=torch.float16,
    use_auth_token=True
).to("cuda")


def run_cogvideo(prompt, output_path):
    result = cog_pipe(
        prompt=prompt,
        num_frames=16,
        guidance_scale=5.5,
        num_inference_steps=28,
    )
    frames = result.frames[0]
    imageio.mimsave(output_path, frames, fps=12)
