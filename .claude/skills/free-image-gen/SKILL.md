---
name: free-image-gen
description: Free, local image generation with no API key, no account and no fees. Use by default whenever the user asks to generate, create or make an image, photo, picture, background, ad or packshot and has not named a paid service. Two modes. Text-to-image for scenes and backgrounds. Product ad from a packshot, where the real pack is cut out and placed on a generated scene so logos and printed text stay exact. Runs on CPU.
---

# free-image-gen

Everything runs inside the session. Nothing is sent to a paid API and no sign-up is needed.

| Part | What | License |
|---|---|---|
| Image model | `SimianLuo/LCM_Dreamshaper_v7` from Hugging Face, 4 steps, not gated | MIT |
| Runtime | `diffusers` + `torch` CPU wheels from PyPI | Apache-2.0 / BSD |
| Cut-out | `rembg` with the `isnet-general-use` model | MIT |

## 1. Setup, once per session

```bash
bash .claude/skills/free-image-gen/scripts/setup.sh
```

Creates `~/.cache/free-image-gen/venv` and pre-downloads the model, about 4 GB in total. Takes 2 to 4 minutes. Use `PY=~/.cache/free-image-gen/venv/bin/python` below.

## 2. Text to image

```bash
$PY .claude/skills/free-image-gen/scripts/generate.py "PROMPT" -o generated/name.png -W 512 -H 640 --seed 3
```

- About 50 seconds per 512 × 640 image on 4 CPU cores. Larger sizes grow roughly with pixel count.
- Write prompts in English, describe a photo: subject, setting, light, lens, mood.
- The model cannot write readable text. Add text afterwards, never in the prompt.

## 3. Product ad from a packshot (preferred for real products)

```bash
$PY .claude/skills/free-image-gen/scripts/product_ad.py PACKSHOT -o generated/ad.jpg \
    --headline "Chrupie naturalnie" --subline "3 ziarna i sól morska" --seed 11
```

What it does:

1. Cuts the product out of the packshot. Separate objects such as claim badges are detected and placed beside the pack.
2. Generates a warm tabletop scene at half size, upscales it and blurs it slightly, which reads as depth of field.
3. Places the real pack with a contact shadow and a soft drop shadow.
4. Adds the headline and a brand-red pill with the subline.

Useful flags: `--size 1080x1920` for Stories, `--size 1920x1080` for banners, `--bg-image scene.png` to reuse a background, `--save-bg` to keep one, `--extras none` to hide badges, `--accent "#C8102E"` for the pill colour, `--pack-height 0.6`.

## 4. Check before delivering

Open the result with the Read tool and check it. Look at the pack position, that the headline does not collide with the pack, and the background mood. Try another `--seed` if the scene is off. The pack can look soft when the source packshot is small. Ask for a packshot of at least 1500 px height for print work.

## Limits

- No GPU in cloud sessions, so this is the fast small model. Z-Image Turbo or FLUX.2 klein give better scenes but need far more RAM or a GPU.
- Video is out of scope here. For animated ads use the `remotion-motion-graphics` skill with these stills.
- Claims on the image must match the printed pack, per EU regulation 1924/2006.
