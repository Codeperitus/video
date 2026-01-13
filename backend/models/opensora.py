import torch
import os
import imageio
from diffusers import OpenSoraPipeline
from huggingface_hub import login

login(token=os.environ["HUGGINGFACE_HUB_TOKEN"])

sora_pipe = OpenSoraPipeline.from_pretrained(
    "opensora-team/OpenSora-1.0",
    torch_dtype=torch.float16,
    use_auth_token=True
).to("cuda")


def run_opensora(prompt, output_path):
    result = sora_pipe(
        prompt=prompt,
        num_frames=16,
        num_inference_steps=32,
        guidance_scale=5.0
    )
    frames = result.frames
    imageio.mimsave(output_path, frames, fps=12)
