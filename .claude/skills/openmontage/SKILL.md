---
name: openmontage
description: Agentic video production with OpenMontage (calesthio/OpenMontage) in a cloud session. Use when the user wants a full video (explainer, product promo, trailer, talking head, short-form clip) built from script, assets, voiceover and edit, rather than a single generated clip.
---

# OpenMontage

Open-source agentic video production system: 12 pipelines (explainer, cinematic, clip-factory, documentary-montage, talking-head, character-animation, localization-dub, podcast-repurpose, hybrid, animation and more), Remotion and HyperFrames rendering, Piper offline TTS. License AGPL-3.0.

## Bootstrap

Cloud containers are ephemeral. Run `toolkit/setup.sh` from this repo. It clones OpenMontage to `~/OpenMontage` and runs `make setup`. Then:

```bash
cd ~/OpenMontage && make preflight
```

## What works without keys (verified 2026-10-30, no GPU)

Editing, stitching, trimming, reframing, subtitles, caption burn-in, audio mixing, colour grade, video analysis, character animation, Pixabay music search.

## What needs keys in `~/OpenMontage/.env`

| Capability | Keys |
|---|---|
| Image and video generation | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` (cloud.higgsfield.ai/api-keys), `FAL_KEY`, `REPLICATE_API_TOKEN`, `MINIMAX_API_KEY` |
| Voiceover | one of the TTS providers listed by `make preflight` |

Never commit `.env`.

## Usage

Read `~/OpenMontage/AGENT_GUIDE.md` and `~/OpenMontage/skills/INDEX.md` first. Pipeline director skills live in `~/OpenMontage/skills/pipelines/<pipeline>/`. The tool registry is the source of truth for what is available:

```bash
cd ~/OpenMontage && .venv/bin/python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

Local GPU models (Wan, Hunyuan, LTX, CogVideo) need `make install-gpu` and an NVIDIA card. Cloud sessions have none.
