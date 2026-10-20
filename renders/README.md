# Hexastorm Animation Rendering & Video Pipeline

This folder contains the Blender 5.2 animation scene and rendering setup for the **Hexastorm** open-hardware laser scanner.

<p align="center">
  <img src="../Images/frame_0000.png" width="90%" alt="Hexastorm Assembly Overview (Render Frame 0000)">
  <br>
  <em>Rendered assembly overview: Hexastorm optical scanhead mounted on the CNC 3018 frame with PCB exposure bed and controller.</em>
</p>

---

## 1. Requirements

- **Blender**: 5.2 LTS (Cycles GPU OptiX or CUDA)
- **Tooling**: [`uv`](https://docs.astral.sh/uv/) and [`ffmpeg`](https://ffmpeg.org/)
- **Target Video Format**: 2560 × 1440 (2K QHD) @ 30 fps (1626 frames total, `0000` to `1625`, ~54.2s)

---

## 2. Installing `pcb2blender`

To render the PCB materials and textures properly, install the `pcb2blender` add-on:

1. **Clone with submodules**:
   ```bash
   git clone --depth 1 --branch support-kicad-10-blender-5.2 https://github.com/hstarmans/pcb2blender.git pcb2blender
   cd pcb2blender
   git submodule update --init --recursive
   ```

2. **Download dependency wheels**:
   ```bash
   uv run --group dev python download_dependencies.py
   ```

3. **Build the extension package**:
   ```bash
   # Linux:
   blender --command extension build --source-dir pcb2blender_importer --output-filepath pcb2blender_importer_5.2.zip

   # Windows (PowerShell):
   & "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --command extension build --source-dir pcb2blender_importer --output-filepath pcb2blender_importer_5.2.zip
   ```

4. **Install and enable in Blender**:
   ```bash
   # Linux:
   blender --command extension install-file pcb2blender_importer_5.2.zip -r user_default -e

   # Windows (PowerShell):
   & "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --command extension install-file pcb2blender_importer_5.2.zip -r user_default -e
   ```

---

## 3. Rendering

Render frames using the provided script [render_animation.sh](file:///home/hexastorm/Documents/hardware/hexastorm_design/renders/render_animation.sh):

```bash
# Render all frames (0 to 1625):
./render_animation.sh

# Or render a specific range (e.g. frames 0 to 559):
./render_animation.sh 0 559
```

To render or preview an individual frame headless:
```bash
blender -b hexastorm_assembly.blend -f 1485
```

Rendered images are written to `frames/frame_####.png`.

---

## 4. Audio Creation & Final Video Assembly

### Audio Creation
- **Voiceover**: Generated via Microsoft Edge TTS using the *Ava Natural* voice profile, paced to match the 6 animation shots (50 seconds).
- **Soundtrack**: A custom scored synth music bed (`audio/bg_music/preview_option_b_scored.mp3`) mixed with dynamic ducking under the voiceover track.

### Video Assembly
Mux the rendered PNG sequence with the audio soundtrack using [encode_video.sh](file:///home/hexastorm/Documents/hardware/hexastorm_design/renders/encode_video.sh):

```bash
./encode_video.sh
```

Or run FFmpeg directly:
```bash
ffmpeg -y -framerate 30 -i "frames/frame_%04d.png" -i "audio/bg_music/preview_option_b_scored.mp3" \
    -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -shortest hexastorm_final_film.mp4
```
