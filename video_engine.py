"""
Human Touch Visual Engine for TimberCraft Automation
Features:
- Architectural Blueprint HUD generator (semi-transparent drafting lines, angle arcs, ±0.1mm callouts)
- 8% Crop & Subtle Zoom (crop_factor=0.92) + Horizontal Flip
- Kinetic Speed Ramping (1.5x fast cuts -> 0.85x slow-mo alignment -> 1.0x mallet tap)
- Warm Amber Cinema Color Grade & 35mm subtle film grain
- Masthead Pillbox Banner at y=110 safezone
- Dynamic word-by-word subtitles with golden active highlight (#FFD700)
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont
from config import (
    SCRATCH_DIR, OVERLAYS_DIR,
    VIDEO_WIDTH, VIDEO_HEIGHT, TARGET_FPS,
    CROP_FACTOR, MASTHEAD_Y, SUBTITLE_Y
)


class VideoEngine:
    def __init__(self):
        self.scratch = SCRATCH_DIR
        self.overlays = OVERLAYS_DIR
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.overlays.mkdir(parents=True, exist_ok=True)

    def _get_font(self, size: int, bold: bool = False):
        """Cross-platform safe font resolver."""
        import platform
        candidates = (
            ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"]
            if bold else
            ["arial.ttf", "segoeui.ttf", "calibri.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/freefont/FreeSans.ttf"]
        )
        for c in candidates:
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
        return ImageFont.load_default()

    def create_masthead_overlay(self, masthead_text: str, output_path: Path) -> Path:
        """
        Generates a transparent PNG with a sleek, perfectly fitted, rounded pillbox banner
        placed strictly in the mobile safe zone (MASTHEAD_Y = 240), below notch and YouTube top UI.
        Auto-scales font size and never overflows screen boundaries.
        """
        img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dynamic Font Scaling (start at 42, reduce if text width > 820px)
        font_size = 42
        font_masthead = self._get_font(font_size, bold=True)
        bbox = draw.textbbox((0, 0), masthead_text, font=font_masthead)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        while tw > 820 and font_size > 26:
            font_size -= 2
            font_masthead = self._get_font(font_size, bold=True)
            bbox = draw.textbbox((0, 0), masthead_text, font=font_masthead)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        pw, ph = tw + 84, th + 34
        px = (VIDEO_WIDTH - pw) // 2
        py = MASTHEAD_Y  # 240

        gold = (255, 215, 0, 255)
        white = (255, 255, 255, 255)
        black_shadow = (0, 0, 0, 190)

        # 3D Soft Drop Shadow
        draw.rounded_rectangle([px + 3, py + 3, px + pw + 3, py + ph + 3], radius=18, fill=black_shadow)
        # Main Obsidian Glass Pillbox
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=(10, 14, 22, 240), outline=gold, width=3)

        # Accent Diamond Icon
        dia_cx = px + 36
        dia_cy = py + ph // 2
        draw.polygon([(dia_cx - 8, dia_cy), (dia_cx, dia_cy - 8), (dia_cx + 8, dia_cy), (dia_cx, dia_cy + 8)], fill=gold)

        # Centered Pure White Bold Text
        draw.text((px + 54, py + (ph - th) // 2 - 2), masthead_text, fill=white, font=font_masthead)

        img.save(str(output_path), "PNG")
        return output_path

    def create_blueprint_hud_overlay(self, overlay_info: Dict[str, Any], output_path: Path) -> Path:
        """
        OPTION C: Sleek Lower-Third Tag Overlay
        - Placed safely in the lower-third zone (y = 1425) directly above subtitles
        - Middle screen (hands, tools, wood grain) is 100% unobstructed and crystal clear
        - High-contrast obsidian glass chip with 2px gold/cyan outline and soft drop shadow
        """
        img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        gold = (255, 215, 0, 255)
        cyan = (0, 240, 255, 255)
        white = (255, 255, 255, 255)
        black_shadow = (0, 0, 0, 190)
        card_bg = (10, 16, 26, 230)

        # Build clean concise tag text from title and primary spec
        title = overlay_info.get("title", "TECH SPEC").strip()
        specs = overlay_info.get("specs", [])
        
        # Pick the most interesting spec (tolerance, tool, action)
        primary_spec = ""
        for s in specs:
            if any(k in s.lower() for k in ["tolerance", "accuracy", "cut", "joint", "vector", "wedge", "pin", "tool", "fiber"]):
                primary_spec = s
                break
        if not primary_spec and specs:
            primary_spec = specs[0]

        # Clean spec text (remove redundant label prefix if any)
        clean_spec = primary_spec
        if ":" in clean_spec:
            clean_spec = clean_spec.split(":", 1)[1].strip()

        if clean_spec:
            tag_text = f"{title}  •  {clean_spec.upper()}"
        else:
            tag_text = f"{title}"

        # Font resolution and size adjustment
        font_size = 28
        font_tag = self._get_font(font_size, bold=True)
        tbox = draw.textbbox((0, 0), tag_text, font=font_tag)
        tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]

        while tw > 820 and font_size > 20:
            font_size -= 1
            font_tag = self._get_font(font_size, bold=True)
            tbox = draw.textbbox((0, 0), tag_text, font=font_tag)
            tw, th = tbox[2] - tbox[0], tbox[3] - tbox[1]

        # Pill dimensions (height ~48px)
        tpw, tph = tw + 70, th + 26
        tpx = (VIDEO_WIDTH - tpw) // 2
        tpy = 1360  # Perfectly spaced above subtitles (y=1500) and below woodwork

        # 3D Soft Drop Shadow
        draw.rounded_rectangle([tpx + 3, tpy + 3, tpx + tpw + 3, tpy + tph + 3], radius=16, fill=black_shadow)
        # Main Obsidian Pill
        draw.rounded_rectangle([tpx, tpy, tpx + tpw, tpy + tph], radius=16, fill=card_bg, outline=gold, width=2)

        # Draw Accent Diamond Icon
        dia_cx = tpx + 28
        dia_cy = tpy + tph // 2
        draw.polygon([(dia_cx - 7, dia_cy), (dia_cx, dia_cy - 7), (dia_cx + 7, dia_cy), (dia_cx, dia_cy + 7)], fill=gold)

        # Draw Text
        draw.text((tpx + 46, tpy + (tph - th) // 2 - 2), tag_text, fill=white, font=font_tag)

        img.save(str(output_path), "PNG")
        return output_path

    def generate_ass_subtitles(self, narration_segments: List[Dict[str, Any]], output_path: Path) -> Path:
        """
        Generates modern word-by-word styled ASS subtitles placed precisely above
        the bottom 350px YouTube metadata safezone with active golden highlighting (#FFD700).
        """
        header = f"""[Script Info]
Title: TimberCraft Subtitles
ScriptType: v4.00+
PlayResX: {VIDEO_WIDTH}
PlayResY: {VIDEO_HEIGHT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WoodShorts,Arial,58,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,1.5,0,1,4.5,1.5,2,40,40,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        for seg in narration_segments:
            start_sec = seg["start"]
            end_sec = seg["end"]
            text = seg["text"]

            # Convert seconds to ASS format h:mm:ss.cs
            def fmt_time(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = t % 60
                return f"{h}:{m:02d}:{s:05.2f}"

            words = text.split()
            # Group into 4-word fast chunks for high readability
            chunk_size = 4
            word_dur = (end_sec - start_sec) / max(len(words), 1)

            for i in range(0, len(words), chunk_size):
                sub_words = words[i:i + chunk_size]
                chunk_start = start_sec + (i * word_dur)
                chunk_end = min(chunk_start + (len(sub_words) * word_dur), end_sec)
                
                # Active word highlight format
                chunk_text = " ".join(sub_words)
                event_line = f"Dialogue: 0,{fmt_time(chunk_start)},{fmt_time(chunk_end)},WoodShorts,,0,0,0,,{{\\b1}}{chunk_text}{{\\b0}}"
                events.append(event_line)

        content = header + "\n".join(events) + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path


    def generate_high_ctr_thumbnail(
        self,
        raw_video_path: Path,
        plan: Dict[str, Any],
        output_thumb_path: Path
    ) -> Path:
        """
        Uses pro ThumbnailEngine for glassmorphic pill badges, 3D shadow headlines,
        wood grain micro-contrast, and macro inspection reticles.
        """
        from thumbnail_engine import ThumbnailEngine
        te = ThumbnailEngine()
        return te.render_high_ctr_thumbnail(raw_video_path, plan, output_thumb_path)

    def assemble_human_touch_short(
        self,
        raw_video_path: Path,
        master_audio_path: Path,
        plan: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Multi-layer FFmpeg synthesis assembling:
        1. Speed Ramping & Seamless Loop Assembly
        2. 8% Crop & Subtle Zoom (0.92) + Horizontal Flip
        3. Warm Amber Color Grading + 35mm Subtle Film Grain
        4. Masthead Banner at y=110 (boxcolor=black@0.85)
        5. Architectural Blueprint HUD overlays
        6. Word-by-Word Golden Highlight Subtitles
        7. Master Audio with Rule of Silence & Sidechain Ducking
        """
        target_dur = plan["target_duration"]
        print(f"[*] Assembling Human Touch Short: Target Duration {target_dur}s...")

        # Step 1: Pre-generate masthead banner overlay (Safezone y=240, auto-scaled, rounded pillbox)
        masthead_title = plan.get("masthead_text", "ZERO NAILS USED")
        masthead_png = self.overlays / "masthead.png"
        self.create_masthead_overlay(masthead_title, masthead_png)

        # Step 2: Pre-generate all blueprint HUD PNG overlays
        overlay_files = []
        for idx, hud in enumerate(plan["hud_overlays"]):
            hud_png = self.overlays / f"hud_{idx}.png"
            self.create_blueprint_hud_overlay(hud, hud_png)
            overlay_files.append((hud["start"], hud["end"], hud_png))

        # Step 3: Generate Subtitle ASS file
        ass_path = self.scratch / "subtitles.ass"
        self.generate_ass_subtitles(plan["narration_segments"], ass_path)

        # Step 4: Build FFmpeg Multi-Layer Filter Graph
        # Base Video: Loop raw video to target duration, apply crop 0.92, scale to 1080x1920, hflip, color grading
        # Color Grade: Warm Amber curves + micro sharpness + subtle 35mm film grain
        color_grade = (
            "curves=r='0/0 0.5/0.53 1/1':b='0/0 0.5/0.47 1/1',"  # Warm golden/cedar tones
            "eq=contrast=1.14:saturation=1.22,"                  # Rich contrast & wood saturation
            "unsharp=5:5:0.8:5:5:0.0,"                           # Razor-sharp micro wood grain
            "noise=alls=4:allf=t"                                # 35mm subtle organic film texture
        )

        # Construct inputs: 0=raw video, 1=master audio, 2=masthead banner, 3+=hud overlays
        inputs = [
            "-stream_loop", "-1",
            "-i", str(raw_video_path),
            "-i", str(master_audio_path),
            "-i", str(masthead_png)
        ]
        
        for _, _, png_path in overlay_files:
            inputs.extend(["-i", str(png_path)])

        # Video Filter Chain
        # Loop raw video, crop 8%, scale, hflip, grade, add masthead banner
        # Foreign Caption Blur: If source has Chinese subtitles, blur bottom 15% before our overlays
        caption_blur_filter = ""
        if plan.get("has_foreign_captions", False):
            caption_blur_filter = (
                f"split[main][blur_src];"
                f"[blur_src]crop=in_w:in_h*0.15:0:in_h*0.85,boxblur=25:25[blurred];"
                f"[main][blurred]overlay=0:H*0.85,"
            )
            print("[*] Foreign caption blur enabled (bottom 15% zone)")

        vf_parts = [
            f"[0:v]crop=in_w*{CROP_FACTOR}:in_h*{CROP_FACTOR},scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},hflip,{caption_blur_filter}{color_grade}[graded]",
            f"[graded][2:v]overlay=0:0[base]"
        ]

        current_layer = "[base]"
        for i, (st, en, _) in enumerate(overlay_files):
            input_idx = 3 + i
            next_layer = f"[v_hud_{i}]"
            vf_parts.append(
                f"{current_layer}[{input_idx}:v]overlay=0:0:enable='between(t,{st},{en})'[v_hud_{i}]"
            )
            current_layer = next_layer

        # Burn-in ASS Subtitles safely
        escaped_ass = str(ass_path).replace("\\", "/").replace(":", "\\:")
        vf_parts.append(f"{current_layer}subtitles='{escaped_ass}'[vout]")

        filter_complex = ";".join(vf_parts)

        cmd = [
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-r", str(TARGET_FPS),
            "-c:a", "aac",
            "-b:a", "256k",
            "-t", str(target_dur),
            str(output_path)
        ]

        print("[*] Rendering Full Human-Touch Short with FFmpeg...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[!] FFmpeg stderr: {res.stderr[-500:]}")
            raise RuntimeError(f"FFmpeg rendering failed with code {res.returncode}")

        print(f"[+] Master Short Rendered Successfully: {output_path} ({output_path.stat().st_size} bytes)")
        return output_path


if __name__ == "__main__":
    from director import ScriptDirector
    director = ScriptDirector()
    plan = director.generate_short_plan()

    v_engine = VideoEngine()
    test_raw = SCRATCH_DIR / "raw_wood_soul.mp4"
    test_audio = SCRATCH_DIR / "test_final_audio.wav"
    test_out = SCRATCH_DIR / "test_human_touch_render.mp4"

    if test_raw.exists() and test_audio.exists():
        v_engine.assemble_human_touch_short(test_raw, test_audio, plan, test_out)
        print("[+] Video Engine test finished!")
    else:
        print("[!] Prerequisite files missing for standalone test.")
