"""
High-CTR Professional Thumbnail Engine for TimberCraft Woodworking Shorts
Generates YouTube-compliant, high-converting 9:16 and 16:9 thumbnails:
Features:
1. Micro-contrast & cedar wood grain saturation enhancement
2. Frosted glassmorphic pillbox with gold/amber accent outline
3. High-impact curiosity headline with multi-layer 3D shadow
4. Macro inspection reticle ring pointing to the impossible joint / razor shaving
5. Safezone layout strictly respecting YouTube Shorts mobile UI boundaries
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, MASTHEAD_Y, CROP_FACTOR, SCRATCH_DIR
)

# Niche-Specific Curiosity Hook Database
THUMBNAIL_HOOKS = {
    "chisel_asmr": {
        "tag": "[ 0.001mm TOLERANCE ]",
        "headline": "SEE-THROUGH WOOD?",
        "badge": "TRANSLUCENT CELL",
        "reticle_pos": (480, 820)
    },
    "temple_joint": {
        "tag": "[ ZERO GLUE * ZERO NAILS ]",
        "headline": "HOW DOES IT LOCK?",
        "badge": "SECRET SLIDER",
        "reticle_pos": (540, 960)
    },
    "kumiko_lattice": {
        "tag": "[ 0.00mm TOLERANCE ]",
        "headline": "NO NAILS * NO SCREWS",
        "badge": "FRICTION LOCK",
        "reticle_pos": (540, 920)
    },
    "default": {
        "tag": "[ ZERO NAILS USED ]",
        "headline": "IMPOSSIBLE WOOD JOINT?",
        "badge": "SECRET LOCK",
        "reticle_pos": (540, 940)
    }
}


class ThumbnailEngine:
    def __init__(self):
        self._init_fonts()

    def _init_fonts(self):
        """Cross-platform font loader with reliable fallbacks."""
        bold_paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
        ]
        heavy_paths = [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/ariblk.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]

        bold_file = next((p for p in bold_paths if os.path.exists(p)), None)
        heavy_file = next((p for p in heavy_paths if os.path.exists(p)), bold_file)

        try:
            if bold_file:
                self.font_tag = ImageFont.truetype(bold_file, 34)
                self.font_badge = ImageFont.truetype(bold_file, 30)
            else:
                self.font_tag = self.font_badge = ImageFont.load_default()

            if heavy_file:
                self.font_head = ImageFont.truetype(heavy_file, 72)
            else:
                self.font_head = ImageFont.load_default()
        except Exception:
            self.font_tag = self.font_badge = self.font_head = ImageFont.load_default()

    def extract_clean_frame(self, raw_video_path: Path, seek_sec: float, out_frame: Path) -> Path:
        """Extracts and color-grades a crisp, unblurred still frame."""
        color_grade = (
            "curves=r='0/0 0.5/0.53 1/1':b='0/0 0.5/0.47 1/1',"
            "eq=contrast=1.18:saturation=1.28,"
            "unsharp=5:5:1.0:5:5:0.0"
        )
        vf = f"crop=in_w*{CROP_FACTOR}:in_h*{CROP_FACTOR},scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},{color_grade}"

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(seek_sec),
            "-i", str(raw_video_path),
            "-vframes", "1",
            "-vf", vf,
            "-q:v", "2",
            str(out_frame)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return out_frame

    def render_high_ctr_thumbnail(
        self,
        raw_video_path: Path,
        plan: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Bakes professional, high-CTR graphic overlays onto the extracted action frame:
        - Wood grain contrast & warmth enhancement
        - Cinematic top & bottom vignette gradients
        - Category Pillbox Badge (Gold outline on translucent dark amber)
        - High-impact curiosity headline with multi-layer 3D shadow
        - Macro inspection reticle ring highlighting the exact wood joint contact
        """
        mood = plan.get("music_mood", "default")
        hook_info = THUMBNAIL_HOOKS.get(mood, THUMBNAIL_HOOKS["default"])

        # Override headline if plan has specific masthead
        tag_text = hook_info["tag"]
        head_text = plan.get("masthead_text", hook_info["headline"])
        badge_text = hook_info["badge"]
        cx, cy = hook_info.get("reticle_pos", (540, 920))

        # 1. Extract peak action frame at 38% duration
        seek_sec = max(plan.get("target_duration", 34.0) * 0.38, 2.5)
        temp_frame = SCRATCH_DIR / "temp_thumb_raw.jpg"
        self.extract_clean_frame(raw_video_path, seek_sec, temp_frame)

        base_img = Image.open(temp_frame).convert("RGBA")
        W, H = base_img.size

        # 2. Image Enhancements (Sharpness & Richness)
        base_img = ImageEnhance.Sharpness(base_img).enhance(1.28)
        base_img = ImageEnhance.Color(base_img).enhance(1.15)

        # 3. Soft Gradient Vignette for Safezones
        vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        v_draw = ImageDraw.Draw(vignette)
        for y in range(360):
            alpha = int(210 * (1.0 - (y / 360.0)**1.4))
            v_draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
        for y in range(H - 420, H):
            ratio = (y - (H - 420)) / 420.0
            alpha = int(190 * (ratio**1.4))
            v_draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
        base_img = Image.alpha_composite(base_img, vignette)

        # 4. Draw Overlays
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 4a. Top Category Tag Pill
        tag_bbox = draw.textbbox((0, 0), tag_text, font=self.font_tag)
        tag_w = tag_bbox[2] - tag_bbox[0]
        tag_h = tag_bbox[3] - tag_bbox[1]
        tag_x = (W - tag_w) // 2
        tag_y = 110
        pad_x, pad_y = 36, 12

        draw.rounded_rectangle(
            [tag_x - pad_x, tag_y - pad_y, tag_x + tag_w + pad_x, tag_y + tag_h + pad_y],
            radius=22,
            fill=(16, 10, 5, 220),
            outline=(245, 158, 11, 240),
            width=3
        )
        draw.text((tag_x, tag_y), tag_text, font=self.font_tag, fill=(255, 193, 7, 255))

        # 4b. Bold Main Headline with 3D Drop Shadow
        head_bbox = draw.textbbox((0, 0), head_text, font=self.font_head)
        head_w = head_bbox[2] - head_bbox[0]
        head_h = head_bbox[3] - head_bbox[1]
        head_x = (W - head_w) // 2
        head_y = tag_y + tag_h + 36

        # Multi-layer shadow
        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (0, 6)]:
            draw.text((head_x + dx, head_y + dy), head_text, font=self.font_head, fill=(0, 0, 0, 245))
        draw.text((head_x, head_y), head_text, font=self.font_head, fill=(255, 255, 255, 255))

        # 4c. Macro Focus Reticle Ring on Wood Joint
        radius = 100
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=(255, 215, 0, 190), width=4)
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 69, 0, 230))

        # Reticle crosshair ticks
        draw.line([(cx - radius - 18, cy), (cx - radius + 14, cy)], fill=(255, 215, 0, 220), width=3)
        draw.line([(cx + radius - 14, cy), (cx + radius + 18, cy)], fill=(255, 215, 0, 220), width=3)
        draw.line([(cx, cy - radius - 18), (cx, cy - radius + 14)], fill=(255, 215, 0, 220), width=3)
        draw.line([(cx, cy + radius - 14), (cx, cy + radius + 18)], fill=(255, 215, 0, 220), width=3)

        # 4d. Callout Badge attached to Reticle
        badge_bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        bw = badge_bbox[2] - badge_bbox[0]
        bh = badge_bbox[3] - badge_bbox[1]
        bx = min(cx + radius + 22, W - bw - 40)
        by = cy - bh // 2

        draw.rounded_rectangle([bx - 14, by - 8, bx + bw + 14, by + bh + 8], radius=12, fill=(0, 0, 0, 215), outline=(255, 215, 0, 210), width=2)
        draw.text((bx, by), badge_text, font=self.font_badge, fill=(255, 255, 255, 255))
        draw.line([(cx + radius, cy), (bx - 14, cy)], fill=(255, 215, 0, 200), width=2)

        # 5. Composite and Save High-Res Thumbnail
        final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
        final_img.save(str(output_path), "JPEG", quality=95)
        print(f"[+] High-CTR Pro Thumbnail created: {output_path.name}")
        return output_path
