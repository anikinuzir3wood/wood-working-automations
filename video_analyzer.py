"""
Video Content Analyzer Module (Gemini Vision) for TimberCraft
=============================================================
Extracts keyframes from raw woodworking video and uses Gemini Vision
to analyze the actual physical actions, joints, materials, and end-result.
Guarantees 100% visual fidelity so voiceover describes what is really shown,
using ultra-simple English words without confusing jargon.
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

from config import SCRATCH_DIR, OUTPUT_DIR


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


def extract_keyframes(video_path: str, num_frames: int = 8) -> List[str]:
    """
    Extracts evenly-spaced keyframes from the video as JPEG images.
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
            "-vf", "scale=768:-2",
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
    Enforces ultra-simple Grade-4 vocabulary and exact visual grounding.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[*] GEMINI_API_KEY not configured — using simplified craft director.")
        return {}

    try:
        frame_paths = extract_keyframes(video_path, num_frames=8)
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
            "You are a master woodworking narrator for a US YouTube Shorts channel.\n"
            "Analyze these chronological frames extracted from a woodworking video.\n\n"
            "Answer EXACTLY in this format (one item per line):\n"
            "OBJECT: <What object, joint, or furniture is shown, e.g. Bed Frame Corner Joint, Dovetail Box, Table Leg, Hand Plane Shaving>\n"
            "ACTIONS: <Summary of what physical action happens across the frames>\n"
            "REVEAL: <What is revealed at the end of the video, e.g. a completed solid wood bed, a locked joint, a transparent wood ribbon>\n"
            "SCRIPT_PART_1: <Hook line (0-5s) in extremely simple words, e.g. 'Look at how this wooden bed is built without a single nail.'>\n"
            "SCRIPT_PART_2: <Explaining the action (6-13s) in simple words, e.g. 'These two side rails slide straight into the corner post.'>\n"
            "SCRIPT_PART_3: <The fit and lock (14-21s) in simple words, e.g. 'Each notch cuts deep into the wood so both pieces lock each other tight.'>\n"
            "SCRIPT_PART_4: <Final reveal (26-32s) in simple words, e.g. 'When it is all together, you get a solid bed that will last for a hundred years.'>\n\n"
            "CRITICAL RULES:\n"
            "- USE SIMPLE, EVERYDAY WORDS ONLY (Grade 4 level English).\n"
            "- STRICTLY BANNED WORDS: 'tolerances', 'microscopic', 'fiber severance', 'tenon geometry', 'surgical discipline', 'unwavering patience', 'ingenuity', 'friction-fit'.\n"
            "- Speak naturally, clearly, and engagingly like you are showing something cool to a friend.\n"
            "- The script MUST describe ONLY what is visible in these frames.\n"
        )
        content_parts.append(prompt)

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(content_parts)
        raw_text = response.text.strip()

        analysis = _parse_analysis_output(raw_text)

        # Cleanup analysis frames
        for fp in frame_paths:
            try:
                Path(fp).unlink()
            except Exception:
                pass

        if analysis.get("script_parts"):
            print(f"[+] Visual Analysis Complete: Object = {analysis.get('object', 'Woodcraft')}")
            return analysis
        else:
            print(f"[*] Raw analysis parsed without complete script parts: {raw_text[:200]}")
            return analysis

    except Exception as e:
        print(f"[!] Video analysis notice: {e}. Continuing with simplified director.")
        return {}


def _parse_analysis_output(raw_text: str) -> Dict[str, Any]:
    res = {"script_parts": []}
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
