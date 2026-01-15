import imageio

def save_video(frames, output_path: str, fps: int = 24):
    imageio.mimsave(output_path, frames, fps=fps)
    return output_path
