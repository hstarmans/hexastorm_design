#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLEND_FILE="$DIR/hexastorm_assembly.blend"
OUTPUT_PATTERN="$DIR/frames/frame_####"
START_FRAME="${1:-0}"
END_FRAME="${2:-1625}"

mkdir -p "$DIR/frames"

echo "=========================================="
echo "   HEXASTORM 2K ANIMATION RENDER"
echo "=========================================="
echo "Blend file:   $BLEND_FILE"
echo "Frames:       $START_FRAME to $END_FRAME"
echo "Output:       $OUTPUT_PATTERN.png"
echo "Disk space:   $(df -h "$DIR" | awk 'NR==2 {print $4}') available"
echo "=========================================="

# Find blender executable
if command -v blender &> /dev/null; then
    BLENDER_BIN="blender"
elif [ -f "/snap/bin/blender" ]; then
    BLENDER_BIN="/snap/bin/blender"
elif [ -f "/snap/blender/current/blender" ]; then
    BLENDER_BIN="/snap/blender/current/blender"
else
    echo "ERROR: Blender not found in PATH or /snap/bin/blender"
    exit 1
fi

echo "Using Blender: $($BLENDER_BIN --version | head -n 1)"

# Python one-liner to ensure GPU OptiX/CUDA is enabled in headless mode
GPU_SETUP_CODE="
import bpy
cpref = bpy.context.preferences.addons.get('cycles')
if cpref:
    cy_pref = cpref.preferences
    # Prefer OPTIX, fallback to CUDA
    for dt in ['OPTIX', 'CUDA']:
        try:
            cy_pref.compute_device_type = dt
            cy_pref.get_devices()
            devices = [d for d in cy_pref.devices if d.type == dt]
            if devices:
                for d in devices:
                    d.use = True
                print(f'Cycles headless device configured: {dt} ({len(devices)} device(s))')
                break
        except Exception:
            pass
scene = bpy.context.scene
scene.cycles.device = 'GPU'
"

echo "Starting render..."
exec "$BLENDER_BIN" -b "$BLEND_FILE" -y \
    --python-expr "$GPU_SETUP_CODE" \
    -o "$OUTPUT_PATTERN" \
    -s "$START_FRAME" -e "$END_FRAME" -a
