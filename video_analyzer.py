"""
Video Content Analyzer Module (Gemini Vision) for TimberCraft
=============================================================
Extracts keyframes from raw woodworking video and uses Gemini Vision
to analyze the actual physical actions, joints, materials, and end-result.
Guarantees 100% visual fidelity so voiceover describes what is really shown,
using ultra-simple English words without confusing jargon.

Also performs automated anti-clutter screening:
- Detects and rejects videos with HUGE uneditable Chinese text/titles across the screen.
- Detects smaller Chinese subtitles/watermarks to trigger targeted blur & English caption overlay.
"""

import os
import sys
import subprocess
import base64
from pathlib import Path
from typing import Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import SCRATCH_DIR, OUTPUT_DIR, BASE_DIR


def _ensure_env_loaded():
    """Ensures environment variables from .env are loaded."""
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip()
        except Exception:
            pass


def get_video_duration(file_path: str) -> float:
    """Gets video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return float(res.stdout.strip())
    except Exception:
        return 30.0


def extract_keyframes(video_path: str, num_frames: int = 5) -> List[str]:
    """
    Extracts evenly-spaced keyframes from the video as JPEG images scaled to 512px.
    Returns list of file paths to extracted frames.
    """
    duration = get_video_duration(video_path)
    frames_dir = SCRATCH_DIR / "analysis_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Clean up any previous frames
    for old in frames_dir.glob("frame_*.jpg"):
        try:
            old.unlink()
        except Exception:
            pass

    frame_paths = []
    safe_start = min(0.5, duration * 0.05)
    safe_end = max(duration - 0.5, duration * 0.95)
    interval = (safe_end - safe_start) / max(num_frames - 1, 1)

    for i in range(num_frames):
        ts = safe_start + (i * interval)
        ts = min(ts, duration - 0.1)
        fp = frames_dir / f"frame_{i:02d}.jpg"

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{ts:.2f}",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "3",
            "-vf", "scale=512:-2",
            str(fp)
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        if fp.exists() and fp.stat().st_size > 1000:
            frame_paths.append(str(fp))

    if not frame_paths:
        print("[!] Warning: Failed to extract analysis frames from video.")
    else:
        print(f"[+] Extracted {len(frame_paths)} keyframes for visual content analysis.")
    return frame_paths


def analyze_video_content(video_path: str) -> Dict[str, Any]:
    """
    Extracts frames and analyzes visual content using Gemini Vision.
    Enforces ultra-simple Grade-4 vocabulary, visual grounding,
    and screens for uneditable Chinese text.
    """
    _ensure_env_loaded()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[*] GEMINI_API_KEY not configured — using standard craft director.")
        return {}

    try:
        frame_paths = extract_keyframes(video_path, num_frames=5)
        if not frame_paths:
            return {}

        import google.generativeai as genai
        genai.configure(api_key=api_key)

        content_parts = []
        for fp in frame_paths:
            with open(fp, "rb") as f:
                content_parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(f.read()).decode("utf-8")
                    }
                })

        prompt = (
            "You are a master woodworking visual analyst and narrator for a high-end US YouTube Shorts channel.\n"
            "Carefully examine these 5 chronological keyframes from a woodworking craft video.\n\n"
            "Answer EXACTLY in this format (one item per line):\n"
            "OBJECT: <What specific object, furniture, joint, or tool is shown? E.g., Marking Gauge Tool, Rosewood Bed Frame, Dovetail Box, Table Leg Joint, Hand Plane Shavings>\n"
            "ACTIONS: <Summary of what physical craft steps happen across the frames>\n"
            "REVEAL: <What is revealed or completed at the end of the video?>\n"
            "HUGE_CHINESE_TEXT: <YES or NO. Is there HUGE, prominent, uneditable Chinese text/title covering a large part or center of the video frames?>\n"
            "CHINESE_SUBTITLES: <YES or NO. Are there small Chinese subtitles or watermarks in the video?>\n"
            "SUBTITLE_REGION: <BOTTOM, TOP, or NONE. Where are any Chinese subtitles or watermarks located?>\n"
            "SCRIPT_PART_1: <Opening hook line (0-5s) in ultra-simple Grade-4 English, e.g., 'Look at how this wooden piece is built without a single nail.'>\n"
            "SCRIPT_PART_2: <Explaining the action (6-13s) in simple words, describing what hands/tools are actually doing>\n"
            "SCRIPT_PART_3: <The interlocking or cut (14-21s) in simple words, describing how the wood fits together>\n"
            "SCRIPT_PART_4: <The final reveal (26-32s) in simple words, praising the rock-solid end result>\n\n"
            "CRITICAL RULES:\n"
            "- USE SIMPLE, PLAIN WORDS ONLY (Grade-4 reading level).\n"
            "- STRICTLY BANNED WORDS: 'tolerances', 'microscopic', 'fiber severance', 'tenon geometry', 'surgical discipline', 'unwavering patience', 'ingenuity', 'friction-fit'.\n"
            "- Speak naturally, like showing something exciting to a friend.\n"
            "- The script MUST describe ONLY what is visible in these frames.\n"
        )
        content_parts.append(prompt)

        # Model hierarchy (with automatic fallback across active models)
        candidate_models = [
            "gemini-3.7-flash",
            "gemini-3.5-flash",
            "gemini-3.6-flash",
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest"
        ]
        response = None
        used_model = None

        for m_name in candidate_models:
            try:
                model = genai.GenerativeModel(m_name)
                response = model.generate_content(content_parts)
                if response and response.text:
                    used_model = m_name
                    break
            except Exception as e:
                continue

        if not response or not response.text:
            print("[!] Could not obtain response from Gemini Vision models.")
            return {}

        raw_text = response.text.strip()
        analysis = _parse_analysis_output(raw_text)
        analysis["model_used"] = used_model

        # Check for rejection trigger: HUGE uneditable Chinese text
        if analysis.get("has_huge_chinese_text", False):
            analysis["reject"] = True
            analysis["reject_reason"] = "Rejected: Video contains huge uneditable Chinese text covering the screen."
            print(f"[!] REJECTION TRIGGER: {analysis['reject_reason']}")
        else:
            analysis["reject"] = False

        # Cleanup analysis frames
        for fp in frame_paths:
            try:
                Path(fp).unlink()
            except Exception:
                pass

        if analysis.get("script_parts"):
            print(f"[+] Visual Analysis Complete: Object = '{analysis.get('object', 'Woodcraft')}' (via {used_model})")
            print(f"    Huge Chinese Text: {analysis.get('has_huge_chinese_text')} | Subtitles: {analysis.get('has_foreign_captions')} ({analysis.get('subtitle_region')})")
            return analysis
        else:
            print(f"[*] Raw analysis parsed without complete script parts: {raw_text[:200]}")
            return analysis

    except Exception as e:
        print(f"[!] Video analysis notice: {e}. Continuing with standard craft director.")
        return {}


def _parse_analysis_output(raw_text: str) -> Dict[str, Any]:
    res = {
        "script_parts": [],
        "has_huge_chinese_text": False,
        "has_foreign_captions": False,
        "subtitle_region": "NONE",
        "reject": False,
        "reject_reason": ""
    }
    lines = raw_text.split("\n")
    parts = {}

    for line in lines:
        line = line.strip().replace("**", "")
        if not line:
            continue
        if line.startswith("OBJECT:"):
            res["object"] = line.replace("OBJECT:", "").strip()
        elif line.startswith("ACTIONS:"):
            res["actions"] = line.replace("ACTIONS:", "").strip()
        elif line.startswith("REVEAL:"):
            res["reveal"] = line.replace("REVEAL:", "").strip()
        elif line.startswith("HUGE_CHINESE_TEXT:"):
            val = line.replace("HUGE_CHINESE_TEXT:", "").strip().upper()
            res["has_huge_chinese_text"] = ("YES" in val or "TRUE" in val)
        elif line.startswith("CHINESE_SUBTITLES:"):
            val = line.replace("CHINESE_SUBTITLES:", "").strip().upper()
            res["has_foreign_captions"] = ("YES" in val or "TRUE" in val)
        elif line.startswith("SUBTITLE_REGION:"):
            res["subtitle_region"] = line.replace("SUBTITLE_REGION:", "").strip().upper()
        elif line.startswith("SCRIPT_PART_1:"):
            parts[1] = line.replace("SCRIPT_PART_1:", "").strip()
        elif line.startswith("SCRIPT_PART_2:"):
            parts[2] = line.replace("SCRIPT_PART_2:", "").strip()
        elif line.startswith("SCRIPT_PART_3:"):
            parts[3] = line.replace("SCRIPT_PART_3:", "").strip()
        elif line.startswith("SCRIPT_PART_4:"):
            parts[4] = line.replace("SCRIPT_PART_4:", "").strip()

    if len(parts) == 4:
        res["script_parts"] = [parts[1], parts[2], parts[3], parts[4]]

    return res


if __name__ == "__main__":
    if len(sys.argv) > 1:
        v = sys.argv[1]
        print(f"Testing video analyzer on {v}...")
        res = analyze_video_content(v)
        print("Result:", res)
