#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMES_PATTERN="$DIR/frames/frame_%04d.png"
AUDIO="$DIR/audio/bg_music/preview_option_b_scored.mp3"
OUTPUT="$DIR/hexastorm_final_film.mp4"

echo "Encoding final Hexastorm film..."
ffmpeg -y -framerate 30 -i "$FRAMES_PATTERN" -i "$AUDIO" \
    -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -shortest "$OUTPUT"

echo "Success! Final video created at: $OUTPUT"
