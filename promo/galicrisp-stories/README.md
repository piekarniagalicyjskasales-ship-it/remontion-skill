# GaliCrisp 5 s Story

9:16, 30 fps, 150 frames. Built with the `remotion-motion-graphics` skill from layers made by `free-image-gen`.

```bash
npm install
npm run audio    # synthesizes public/sfx, no downloads
npm run render   # out/galicrisp-story-5s.mp4
```

Timeline lives in `src/theme.ts` (`beats`, in seconds). Pack rises in, headline words stagger, red pill pops, badges bounce, a sheen sweeps the pack, text exits and the CTA lands.

Swap the product by regenerating layers:

```bash
python .claude/skills/free-image-gen/scripts/product_ad.py PACKSHOT -o /tmp/x.jpg --size 1080x1920 --save-layers promo/galicrisp-stories/public
```

Fonts: Inter, SIL Open Font License 1.1.
