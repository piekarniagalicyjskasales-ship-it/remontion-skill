---
name: higgsfield-product-ads
description: Generate advertising photos and short videos of Galicia bakery products (GaliCrisp, Chrupak, Chrupaski, DZIK collab) from a packshot, using the Higgsfield MCP connector. Use when the user attaches a product/packaging photo and asks for an ad, packshot, social post image, key visual or product video.
---

# Higgsfield product ads

Workflow that worked for the GaliCrisp "3 ziarna i sól morska" packshot.

## Steps

1. **Check budget first.** Call `balance`. Free plan has very few credits, so always preflight with `get_cost: true` before the real call.
2. **Upload the packshot yourself.** `media_upload` with the file name and MIME type, then `curl -X PUT -H "Content-Type: <mime>" --data-binary @<file> '<upload_url>'`, then `media_confirm` with `type: "image"`. Never ask the user to re-upload.
3. **Read preferences.** `get_preferences` once per conversation. If `auto_create_project` is false, generate without a folder.
4. **Generate.**
   - Product ads: `marketing_studio_image`, media role `image`, `resolution: "2k"`, aspect `4:5` for Instagram feed, `9:16` for Stories/Reels, `16:9` for web banners. About 2 credits at 2k.
   - Cheap drafts or text-heavy edits: `gpt_image_2_5`, media role `image_references`. About 0.25 credits.
   - Video from the finished still: `generate_video` (Seedance, Kling). Check cost first, video is much more expensive.
5. **Wait and show.** `jobs_wait` with `timeout_seconds <= 15`, repeat until terminal, then download the result URL into `generated/` in this repo.

## Prompt template

Keep the packaging exact. Always say it explicitly:

> Premium advertising photo of the <PRODUCT> package exactly as in the reference: keep the logo, the flavour band '<FLAVOUR TEXT>', the badges and all printed text unchanged and legible. <SCENE>. <LIGHT>. Clean negative space at the top for a headline. Photorealistic commercial food photography.

Scenes that fit the brand: rustic oak board in an artisan bakery, scattered seeds and sea salt matching the flavour, linen cloth, wheat ear, warm morning window light, deep red accent matching the GaliCrisp red.

## Rules

- Generated text on packaging can drift. Inspect the result and say so if the logo or flavour text changed.
- Health claims on the image ("źródło błonnika", "bez cukru") must match what is printed on the real pack (EU regulation 1924/2006).
- For DZIK × Galicia work, follow `BRIEF_GRAFICZNY_WKDZIK_x_GALICIA.md` in the agent-marketing-grafika repo.
