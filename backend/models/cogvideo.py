import torch
import imageio
from diffusers import CogVideoXPipeline
import os
from huggingface_hub import login

# Login to HuggingFace
login(token=os.environ.get("HUGGINGFACE_HUB_TOKEN", ""))

# Load CogVideoX 5B (correct repo)
cog_pipe = CogVideoXPipeline.from_pretrained(
    "zai-org/CogVideoX-5b",
    torch_dtype=torch.float16,
).to("cuda")


def run_cogvideo(prompt: str, output_path: str):
    """
    Generate a CogVideoX animation and save as .mp4 or .gif
    """

    result = cog_pipe(
        prompt=prompt,
        num_frames=16,          # Default good animation length
        guidance_scale=5.5,
        num_inference_steps=28,
    )

    # Get generated frames
    frames = result.frames[0]

    # Save video / gif
    imageio.mimsave(output_path, frames, fps=12)
