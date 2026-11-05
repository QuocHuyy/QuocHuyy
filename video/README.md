# Domain Expansion — profile video

Source for a 20-second vertical video (1080×1920, 30fps) of this GitHub profile, made for TikTok / Instagram Reels.

| File | What it does |
|---|---|
| `scene.html` | Canvas animation. `renderAt(t)` draws the frame at time `t`, so every render gives the same frames |
| `render.js` | Playwright opens `scene.html` and saves 600 PNG frames (`node render.js all`), or a few test frames (`node render.js preview 3.2 10.9`) |
| `audio.py` | Synthesizes the original 120 BPM soundtrack and sound effects to `audio.wav` (numpy only) |
| `snap-hero.js` | Rasterizes `../assets/hero.svg` to `hero_city.png` for the skyline scene |
| `sheet.py` | Builds a contact sheet from frames: `python3 sheet.py out.png frames/f0100.png ...` |
| `build.sh` | Runs everything and writes `quochuy-domain-expansion.mp4` |

Requirements: Node with Playwright and Chromium, Python 3 with numpy, ffmpeg, and the Unifont font
(`/usr/share/fonts/opentype/unifont/`, Debian/Ubuntu package `fonts-unifont`).

```bash
./video/build.sh
```

Stats in the video (919 commits, 937 contributions, 11-day streak, top languages) are hard-coded in `scene.html`
from the stats card of 2026-11-05; edit `s6` there to refresh them.
