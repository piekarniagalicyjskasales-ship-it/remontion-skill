# Creative toolkit for Galicia bakery

Everything installed and learned in the Claude session of 2026-10-30, kept here because cloud containers are wiped after each session.

## Restore in a new session

```bash
bash toolkit/setup.sh
```

The skills in `.claude/skills/` also load automatically when this repo is opened in Claude Code.

## Skills

| Skill | Source | Purpose |
|---|---|---|
| `agent-browser` | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Browser automation CLI. The SKILL.md is a stub, run `agent-browser skills get core` for the real guide |
| `remotion-motion-graphics` | this repo | Code-driven motion graphics with Remotion |
| `higgsfield-product-ads` | written in this session | Ad photos and videos from a packshot via the Higgsfield connector |
| `openmontage` | written in this session | Bootstrap and use OpenMontage for full video production |
| `free-image-gen` | written in this session | Free local image generation on CPU, no keys or accounts. Product ads keep the real pack pixels |

## Research notes

**wide-trace/open-higgsfield** is a Next.js studio over the Higgsfield platform API with 38 models: 8 image, 30 video (Soul, Seedance 2/2.5, Kling 3, Wan, Flux, LTX, MiniMax, PixVerse, Grok). It generates nothing locally, needs a Higgsfield `id:secret` key plus the API base URL, and its Vercel Blob upload route is unauthenticated.

**Recommended repos** for image and video generation, checked 2026-10-30:

| Repo | Stars | License | Note |
|---|---|---|---|
| calesthio/OpenMontage | 73k | AGPL-3.0 | Agentic video production, no GPU needed, supports Higgsfield |
| heygen-com/hyperframes | 76k | Apache-2.0 | HTML to MP4 renderer, no AI generation |
| Comfy-Org/ComfyUI | 144k | GPL-3.0 | Local image and video models, needs GPU |
| Wan-Video/Wan2.2 | 18k | Apache-2.0 | Open video model, 24 GB+ VRAM |
| Lightricks/LTX-Video | 11k | Apache-2.0 | Open video model |

Cloud sessions have no GPU (4 CPU, 15 GB RAM). Hosted APIs or the small local model in `free-image-gen` are the options. Pollinations still answered without a key on 2026-10-30, but its docs now require sign-up, so it is not used.

## Generated assets

`generated/galicrisp-3-ziarna-stories-9x16.jpg` and `generated/galicrisp-3-ziarna-story-5s.mp4`: Stories still and a 5 s animated Story with synthesized sound. Fully local and free. Source project in `promo/galicrisp-stories`.

`generated/galicrisp-3-ziarna-ad-free-local-4x5.jpg`: same product made with `free-image-gen`, fully local, no cost. The pack and badges are the original pixels, so all printed text is exact. The scene comes from LCM Dreamshaper v7.

`generated/galicrisp-3-ziarna-ad-4x5.jpg`: GaliCrisp 3 ziarna i sól morska, 4:5 ad, Higgsfield `marketing_studio_image` at 2k, 2 credits. The small text on the two round badges came out distorted, so retouch or regenerate before print.
