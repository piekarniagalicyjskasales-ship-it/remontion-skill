#!/usr/bin/env python3
"""Free, local text-to-image on CPU. No API key, no account.

Model: SimianLuo/LCM_Dreamshaper_v7 (MIT, not gated). 4 steps is enough.

  python generate.py "a sourdough loaf on an oak board" -o out.png
  python generate.py "..." -W 768 -H 960 --seed 7 -n 2
"""
import argparse
import os
import sys
import time
from pathlib import Path

MODEL_ID = os.environ.get("FREE_IMAGE_MODEL", "SimianLuo/LCM_Dreamshaper_v7")
NEGATIVE = "blurry, lowres, deformed, watermark, text, logo, jpeg artifacts"

_pipe = None


def load_pipe():
    global _pipe
    if _pipe is None:
        import torch
        from diffusers import DiffusionPipeline

        torch.set_num_threads(os.cpu_count() or 4)
        _pipe = DiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32, safety_checker=None)
        _pipe.to("cpu")
        _pipe.set_progress_bar_config(disable=True)
    return _pipe


def snap(v: int) -> int:
    return max(256, (v // 8) * 8)


def generate(prompt: str, width=512, height=512, steps=4, guidance=8.0, seed=None, count=1):
    import torch

    pipe = load_pipe()
    gen = torch.Generator("cpu").manual_seed(seed) if seed is not None else None
    result = pipe(
        prompt=prompt,
        width=snap(width),
        height=snap(height),
        num_inference_steps=steps,
        guidance_scale=guidance,
        num_images_per_prompt=count,
        generator=gen,
        output_type="pil",
    )
    return result.images


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt")
    ap.add_argument("-o", "--out", default="image.png", help="output file; with -n >1 an index is appended")
    ap.add_argument("-W", "--width", type=int, default=512)
    ap.add_argument("-H", "--height", type=int, default=512)
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--guidance", type=float, default=8.0)
    ap.add_argument("--seed", type=int)
    ap.add_argument("-n", "--count", type=int, default=1)
    a = ap.parse_args()

    t0 = time.time()
    images = generate(a.prompt, a.width, a.height, a.steps, a.guidance, a.seed, a.count)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    for i, img in enumerate(images):
        path = out if len(images) == 1 else out.with_name(f"{out.stem}-{i + 1}{out.suffix}")
        img.save(path)
        print(path)
    print(f"done in {time.time() - t0:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
