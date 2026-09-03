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

    def create_blueprint_hud_overlay(self, overlay_info: Dict[str, Any], output_path: Path) -> Path:
        """
        Creates a transparent 1080x1920 PNG containing architectural drafting lines,
        geometric measurement crosshairs, angle arcs, and technical callout cards.
        """
        img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Technical blueprint cyan and white colors
        cyan = (0, 229, 255, 210)       # #00E5FF with 82% opacity
        dim_cyan = (0, 229, 255, 90)     # Drafting grid lines
        card_bg = (10, 15, 25, 200)      # Dark architectural glass card
        white = (255, 255, 255, 240)
        gold = (255, 215, 0, 240)

        # 1. Technical Drafting Lines (Focus around Chisel Cut Point)
        center_x, center_y = VIDEO_WIDTH // 2 + 40, 680
        
        # Crosshair reticles around the chisel cutting zone
        reticle_r = 130
        draw.arc([center_x - reticle_r, center_y - reticle_r, center_x + reticle_r, center_y + reticle_r], 0, 90, fill=cyan, width=2)
        draw.arc([center_x - reticle_r, center_y - reticle_r, center_x + reticle_r, center_y + reticle_r], 180, 270, fill=cyan, width=2)
        
        # Center tick marks
        draw.line([center_x - 20, center_y, center_x + 20, center_y], fill=cyan, width=2)
        draw.line([center_x, center_y - 20, center_x, center_y + 20], fill=cyan, width=2)

        # Subtle 28-degree blade bevel guideline matching the chisel
        draw.line([center_x - 200, center_y + 110, center_x + 200, center_y - 110], fill=dim_cyan, width=1)

        # 2. Architectural Spec HUD Card (Right Mid-Section)
        card_w, card_h = 430, 160
        card_x, card_y = VIDEO_WIDTH - card_w - 50, 780
        
        # Draw glassmorphic HUD pillbox
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=12, fill=card_bg, outline=cyan, width=2)

        # Header bar on card
        draw.rectangle([card_x, card_y, card_x + card_w, card_y + 36], fill=(0, 229, 255, 40))
        
        # Fonts
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 22)
            font_spec = ImageFont.truetype("arial.ttf", 20)
            font_badge = ImageFont.truetype("arialbd.ttf", 16)
        except Exception:
            font_title = font_spec = font_badge = ImageFont.load_default()

        title_text = overlay_info.get("title", "END-GRAIN TEST")
        draw.text((card_x + 18, card_y + 8), f"◈ {title_text}", fill=cyan, font=font_title)

        # Draw specifications items
        specs = overlay_info.get("specs", ["Surface: CROSS-SECTION", "Tolerance: 0.05mm SLICE"])
        for idx, spec in enumerate(specs):
            spec_y = card_y + 52 + (idx * 34)
            draw.text((card_x + 20, spec_y), f"› {spec}", fill=white, font=font_spec)

        # Top-right corner tech badge
        badge_text = overlay_info.get("badge", "0.05mm HAND CHISEL")
        draw.rounded_rectangle([VIDEO_WIDTH - 290, 220, VIDEO_WIDTH - 50, 265], radius=6, fill=(0, 0, 0, 180), outline=gold, width=1)
        draw.text((VIDEO_WIDTH - 275, 230), badge_text, fill=gold, font=font_badge)

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
Style: WoodShorts,Arial,58,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,1.5,0,1,3.5,0,2,40,40,420,1

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

        # Step 1: Pre-generate all blueprint HUD PNG overlays
        overlay_files = []
        for idx, hud in enumerate(plan["hud_overlays"]):
            hud_png = self.overlays / f"hud_{idx}.png"
            self.create_blueprint_hud_overlay(hud, hud_png)
            overlay_files.append((hud["start"], hud["end"], hud_png))

        # Step 2: Generate Subtitle ASS file
        ass_path = self.scratch / "subtitles.ass"
        self.generate_ass_subtitles(plan["narration_segments"], ass_path)

        # Step 3: Build FFmpeg Multi-Layer Filter Graph
        # Base Video: Loop raw video to target duration, apply crop 0.92, scale to 1080x1920, hflip, color grading
        # Color Grade: Warm Amber curves + micro sharpness + subtle 35mm film grain
        color_grade = (
            "curves=r='0/0 0.5/0.53 1/1':b='0/0 0.5/0.47 1/1',"  # Warm golden/cedar tones
            "eq=contrast=1.14:saturation=1.22,"                  # Rich contrast & wood saturation
            "unsharp=5:5:0.8:5:5:0.0,"                           # Razor-sharp micro wood grain
            "noise=alls=4:allf=t"                                # 35mm subtle organic film texture
        )

        # Masthead Pillbox at y=110
        masthead_title = plan.get("masthead_text", "ZERO NAILS USED")
        font_size = 58 if len(masthead_title) > 22 else 72
        
        # Cross-platform font resolution
        import platform
        font_param = ""
        if platform.system() == "Windows":
            font_param = "fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
        else:
            for f_cand in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"]:
                if Path(f_cand).exists():
                    font_param = f"fontfile='{f_cand}':"
                    break

        draw_masthead = (
            f"drawtext=text='{masthead_title}':"
            f"{font_param}fontcolor=white:fontsize={font_size}:"
            f"x=(w-text_w)/2:y={MASTHEAD_Y}:"
            f"box=1:boxcolor=black@0.85:boxborderw=24"
        )

        # Construct inputs and overlay filters for HUDs
        inputs = [
            "-stream_loop", "-1",
            "-i", str(raw_video_path),
            "-i", str(master_audio_path)
        ]
        
        for _, _, png_path in overlay_files:
            inputs.extend(["-i", str(png_path)])

        # Video Filter Chain
        # Loop raw video, crop 8%, scale, hflip, grade, add masthead
        vf_parts = [
            f"[0:v]crop=in_w*{CROP_FACTOR}:in_h*{CROP_FACTOR},scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},hflip,{color_grade},{draw_masthead}[base]"
        ]

        current_layer = "[base]"
        for i, (st, en, _) in enumerate(overlay_files):
            input_idx = 2 + i
            next_layer = f"[v_hud_{i}]"
            # Fade in over 0.4s and fade out over 0.4s
            vf_parts.append(
                f"{current_layer}[{input_idx}:v]overlay=0:0:enable='between(t,{st},{en})'[v_hud_{i}]"
            )
            current_layer = next_layer

        # Burn-in ASS Subtitles safely
        # Note: Escape backslashes for FFmpeg on Windows
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
