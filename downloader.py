"""
Downloader Module for Rednote (Xiaohongshu) / Douyin / TikTok
Extracts watermark-free video streams from item notes.
"""

import os
import re
import json
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any
from config import SCRATCH_DIR

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Referer": "https://www.rednote.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,video/*,*/*;q=0.8",
}


def get_video_stream_url_from_html(html: str) -> Optional[str]:
    """Parse HTML and extract direct MP4 stream URL from Rednote CDN."""
    # Pattern 1: Rednote CDN stream URLs
    matches = re.findall(r'http[s]?://sns-v[0-9]+\.rednotecdn\.com/stream/[^"\'\s\\]+', html)
    if matches:
        return matches[0].replace('\\u002F', '/').replace('\\', '')
    
    # Pattern 2: Any 1080p/720p mp4 stream
    matches = re.findall(r'http[s]?://[a-zA-Z0-9.-]+\.(?:rednotecdn|xhscdn)\.com/[^"\'\s\\]+\.mp4', html)
    if matches:
        return matches[0].replace('\\u002F', '/').replace('\\', '')
        
    return None


def download_stream(stream_url: str, output_path: Path) -> Path:
    """Download direct MP4 stream using streaming HTTP request."""
    print(f"[*] Downloading stream: {stream_url}")
    req = urllib.request.Request(stream_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(output_path, "wb") as f:
            while chunk := resp.read(1024 * 1024):
                f.write(chunk)
    print(f"[+] Download complete: {output_path} ({output_path.stat().st_size} bytes)")
    return output_path


def probe_video(video_path: Path) -> Dict[str, Any]:
    """Use ffprobe to get video duration, width, height, and FPS."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_format",
        "-show_streams",
        "-print_format", "json",
        str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    
    v_stream = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    duration = float(data.get("format", {}).get("duration", 0.0))
    
    width = int(v_stream.get("width", 1080)) if v_stream else 1080
    height = int(v_stream.get("height", 1920)) if v_stream else 1920
    
    return {
        "duration": duration,
        "width": width,
        "height": height,
        "codec": v_stream.get("codec_name", "unknown") if v_stream else "unknown"
    }


if __name__ == "__main__":
    test_stream = "http://sns-v27.rednotecdn.com/stream/1/110/130/01e4f527b63081ae0103700196f1b07058_130.mp4"
    out = SCRATCH_DIR / "test_download.mp4"
    if not out.exists():
        download_stream(test_stream, out)
    info = probe_video(out)
    print(f"[+] Probed Video: {info}")
