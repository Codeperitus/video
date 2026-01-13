import torch
from diffusers import OpenSoraPipeline
import imageio

sora_pipe = OpenSoraPipeline.from_pretrained(
    "opensora-team/OpenSora-1.0",
    torch_dtype=torch.float16
).to("cuda")

def run_opensora(prompt, output_path):
    result = sora_pipe(
        prompt=prompt,
        num_frames=16,
        num_inference_steps=30,
        guidance_scale=5.5
    )

    frames = result.frames
    imageio.mimsave(output_path, frames, fps=12)
    return output_path
