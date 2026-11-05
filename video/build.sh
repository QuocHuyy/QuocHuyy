#!/usr/bin/env bash
# Build quochuy-domain-expansion.mp4 (1080x1920, 20s, 30fps) from source.
# Needs: node + playwright (Chromium), python3 + numpy, ffmpeg, Unifont installed.
set -euo pipefail
cd "$(dirname "$0")"
node snap-hero.js
rm -rf frames && node render.js all
python3 audio.py
ffmpeg -y -loglevel error -framerate 30 -i frames/f%04d.png -i audio.wav \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high -movflags +faststart \
  -c:a aac -b:a 192k -shortest quochuy-domain-expansion.mp4
echo "done: $(pwd)/quochuy-domain-expansion.mp4"
