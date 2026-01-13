import torch, os
from diffusers import AnimateDiffPipeline
from PIL import Image
import imageio
from huggingface_hub import login

login(token=os.environ["HUGGINGFACE_HUB_TOKEN"])

# Load AnimateDiff-SDXL
ad_pipe = AnimateDiffPipeline.from_pretrained(
    "guoyww/AnimateDiff-SDXL",
    torch_dtype=torch.float16,
    use_auth_token=True
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
