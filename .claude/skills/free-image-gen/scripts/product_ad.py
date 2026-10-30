#!/usr/bin/env python3
"""Free product ad from a packshot: real pack cut out and placed on an
AI-generated scene. Packaging text stays 100% faithful because the pack
pixels are never regenerated. No API key, no account, runs on CPU.

  python product_ad.py packshot.webp -o ad.jpg \
      --headline "Chrupie naturalnie" --subline "3 ziarna i sól morska"

Options worth knowing:
  --size 1080x1350        output size (4:5 feed). 1080x1920 for Stories.
  --bg-prompt "..."       scene description, keep the centre empty
  --bg-image scene.png    reuse an existing background instead of generating
  --bg-ready              the --bg-image is already graded, e.g. from --save-layers
  --save-layers DIR       write background, product and badges as separate PNGs for video
  --extras badges         also place the other cut-out objects (badges) beside the pack
  --seed 7                change the generated scene
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))

DEFAULT_BG = (
    "eye level close-up photo of a rustic oak wooden table top, empty space in the centre, "
    "warm golden artisan bakery interior blurred in the background, a few flax seeds, sesame "
    "and sea salt flakes scattered on the wood, linen cloth and wheat ears at the sides, "
    "warm morning sunlight, bokeh, professional food photography, 35mm, vibrant warm tones"
)

FONT_CANDIDATES = {
    "bold": [
        "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ],
    "regular": [
        "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ],
}


def font(kind: str, size: int):
    for path in FONT_CANDIDATES[kind]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def cut_objects(packshot: Path):
    """Remove the background and split the result into separate objects,
    largest first. The largest is the product, the rest are extras."""
    from rembg import new_session, remove

    src = Image.open(packshot).convert("RGB")
    cut = remove(src, session=new_session("isnet-general-use"))
    alpha = np.array(cut.split()[-1]) > 128
    cols = alpha.any(0)
    segments, start = [], None
    for x, on in enumerate(list(cols) + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            segments.append((start, x))
            start = None
    objects = []
    for x0, x1 in segments:
        sub = alpha[:, x0:x1]
        rows = np.where(sub.any(1))[0]
        # split a column band into vertically separated objects (stacked badges)
        bands, s, prev = [], rows[0], rows[0]
        for r in rows[1:]:
            if r - prev > 8:
                bands.append((s, prev + 1))
                s = r
            prev = r
        bands.append((s, prev + 1))
        for y0, y1 in bands:
            box = (x0, y0, x1, y1)
            piece = cut.crop(box)
            objects.append(piece.crop(piece.getbbox()))
    objects.sort(key=lambda im: im.width * im.height, reverse=True)
    return objects


def make_background(size, prompt, seed, bg_image, ready=False):
    w, h = size
    if bg_image and ready:
        bg = Image.open(bg_image).convert("RGB")
        scale = max(w / bg.width, h / bg.height)
        bg = bg.resize((round(bg.width * scale), round(bg.height * scale)), Image.LANCZOS)
        left, top = (bg.width - w) // 2, (bg.height - h) // 2
        return bg.crop((left, top, left + w, top + h))
    if bg_image:
        bg = Image.open(bg_image).convert("RGB")
    else:
        from generate import generate

        gw, gh = (w // 2) // 8 * 8, (h // 2) // 8 * 8
        bg = generate(prompt, gw, gh, seed=seed)[0]
    # cover-fit, then soften: the scene sits behind the pack, so depth of
    # field hides the upscale
    scale = max(w / bg.width, h / bg.height)
    bg = bg.resize((round(bg.width * scale), round(bg.height * scale)), Image.LANCZOS)
    left, top = (bg.width - w) // 2, (bg.height - h) // 2
    bg = bg.crop((left, top, left + w, top + h)).filter(ImageFilter.GaussianBlur(2.5))
    bg = ImageEnhance.Color(bg).enhance(1.25)
    bg = ImageEnhance.Contrast(bg).enhance(1.06)
    bg = Image.blend(bg, Image.new("RGB", bg.size, (255, 196, 120)), 0.10)  # warm grade
    return vignette(bg)


def vignette(img, strength=0.35):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    mask = np.clip(1 - strength * np.clip(d - 0.35, 0, None), 0, 1)
    arr = np.array(img).astype(np.float32) * mask[..., None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))


def scale_sharp(im, height):
    s = height / im.height
    out = im.resize((max(1, round(im.width * s)), round(height)), Image.LANCZOS)
    if s > 1:
        rgb = out.convert("RGB").filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
        rgb.putalpha(out.split()[-1])
        out = rgb
    return out


def place_with_shadow(canvas, obj, x, y):
    w, h = obj.size
    # soft drop shadow from the alpha
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    a = obj.split()[-1].point(lambda v: v * 0.45)
    blk = Image.new("RGBA", obj.size, (25, 12, 5, 255))
    blk.putalpha(a)
    shadow.paste(blk, (x + w // 25, y + h // 40), blk)
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(6, w // 18)))
    # contact shadow on the board
    contact = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(contact)
    d.ellipse((x - w * 0.08, y + h - h * 0.03, x + w * 1.08, y + h + h * 0.035), fill=(20, 10, 4, 150))
    contact = contact.filter(ImageFilter.GaussianBlur(max(5, w // 14)))
    canvas.alpha_composite(contact)
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(obj, (x, y))


def safe_zone(w, h):
    """Top text start and pack bottom. Tall formats (Stories, Reels) keep
    clear of the platform UI at the top and bottom ~12% of the frame."""
    if h / w > 1.5:
        return int(h * 0.15), 0.83
    return int(h * 0.055), 0.92


def draw_text(canvas, headline, subline, color, accent):
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    y = safe_zone(w, h)[0]
    if headline:
        size = int(w * 0.095)
        f = font("bold", size)
        while d.textlength(headline, font=f) > w * 0.86 and size > 20:
            size -= 2
            f = font("bold", size)
        tw = d.textlength(headline, font=f)
        x = (w - tw) / 2
        # legibility: soft dark halo behind the text
        halo = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(halo).text((x, y), headline, font=f, fill=(0, 0, 0, 150))
        canvas.alpha_composite(halo.filter(ImageFilter.GaussianBlur(size // 6)))
        d.text((x, y), headline, font=f, fill=color)
        y += int(size * 1.45)
    if subline:
        size = int(w * 0.042)
        f = font("regular", size)
        tw = d.textlength(subline, font=f)
        pad_x, pad_y = int(size * 0.7), int(size * 0.35)
        x = (w - tw) / 2
        d.rounded_rectangle((x - pad_x, y - pad_y, x + tw + pad_x, y + size + pad_y * 1.6),
                            radius=size, fill=accent)
        d.text((x, y), subline, font=f, fill=(255, 255, 255, 255))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packshot")
    ap.add_argument("-o", "--out", default="ad.jpg")
    ap.add_argument("--size", default="1080x1350")
    ap.add_argument("--bg-prompt", default=DEFAULT_BG)
    ap.add_argument("--bg-image")
    ap.add_argument("--bg-ready", action="store_true", help="--bg-image is already graded (e.g. a saved layer); only crop it")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--headline", default="")
    ap.add_argument("--subline", default="")
    ap.add_argument("--text-color", default="#FFF8EC")
    ap.add_argument("--accent", default="#C8102E", help="pill colour behind the subline")
    ap.add_argument("--pack-height", type=float, default=0.58, help="pack height as share of canvas")
    ap.add_argument("--extras", choices=["none", "badges"], default="badges")
    ap.add_argument("--save-bg", help="also save the generated background here for reuse")
    ap.add_argument("--save-layers", help="directory for separate layers (background.png, product.png, extra-N.png) for animation")
    a = ap.parse_args()

    t0 = time.time()
    w, h = (int(v) for v in a.size.lower().split("x"))
    objects = cut_objects(Path(a.packshot))
    product, extras = objects[0], objects[1:]

    bg = make_background((w, h), a.bg_prompt, a.seed, a.bg_image, a.bg_ready)
    if a.save_bg:
        bg.save(a.save_bg)
    if a.save_layers:
        layers = Path(a.save_layers)
        layers.mkdir(parents=True, exist_ok=True)
        bg.save(layers / "background.png")
        product.save(layers / "product.png")
        for i, ex in enumerate(extras, 1):
            ex.save(layers / f"extra-{i}.png")
    canvas = bg.convert("RGBA")

    pack = scale_sharp(product, h * a.pack_height)
    px = (w - pack.width) // 2
    py = int(h * safe_zone(w, h)[1]) - pack.height
    place_with_shadow(canvas, pack, px, py)

    if a.extras == "badges" and extras:
        bh = int(pack.width * 0.42)
        slot_x = px + pack.width + int(w * 0.04)
        if slot_x + bh > w - int(w * 0.03):
            slot_x = w - int(w * 0.03) - bh
        by = py + int(pack.height * 0.18)
        for ex in extras[:3]:
            b = scale_sharp(ex, bh * ex.height / max(ex.width, ex.height))
            place_with_shadow(canvas, b, slot_x, by)
            by += b.height + int(bh * 0.15)

    draw_text(canvas, a.headline, a.subline, a.text_color, a.accent)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rgb = canvas.convert("RGB")
    if out.suffix.lower() in (".jpg", ".jpeg"):
        rgb.save(out, quality=92)
    else:
        rgb.save(out)
    print(out)
    print(f"done in {time.time() - t0:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
