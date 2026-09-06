"""
Source Video Harvester for TimberCraft Automation
Downloads clean, distinct videos directly from creator accounts
into assets/raw_sources/ and registers them in video_queue.json.
"""

import sys
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from config import BASE_DIR, ASSETS_DIR
from queue_manager import QueueManager, compute_file_hash

RAW_SOURCES_DIR = ASSETS_DIR / "raw_sources"
RAW_SOURCES_DIR.mkdir(parents=True, exist_ok=True)


def download_raw_video(stream_url: str, target_path: Path) -> bool:
    """Download video stream directly with custom user-agent."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.rednote.com/"
    }
    req = urllib.request.Request(stream_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp, open(target_path, "wb") as out_f:
            while chunk := resp.read(1024 * 1024):
                out_f.write(chunk)
        print(f"[+] Downloaded: {target_path.name} ({target_path.stat().st_size / (1024*1024):.2f} MB)")
        return True
    except Exception as e:
        print(f"[!] Failed to download {stream_url}: {e}")
        if target_path.exists():
            target_path.unlink()
        return False


def register_harvested_video(
    item_id: str,
    account: str,
    title_theme: str,
    stream_url: str,
    source_page_url: str
) -> bool:
    """Downloads raw video locally and adds it to queue with duplicate checking."""
    qm = QueueManager()
    if qm.is_processed(item_id):
        print(f"[-] Item {item_id} has already been processed.")
        return False

    target_file = RAW_SOURCES_DIR / f"{item_id}.mp4"
    if not target_file.exists():
        success = download_raw_video(stream_url, target_file)
        if not success:
            return False

    # Check content hash
    if qm.is_raw_hash_processed(target_file):
        print(f"[!] Content hash matches an already processed video! Rejecting duplicate.")
        target_file.unlink()
        return False

    # Add to queue
    added = qm.add_to_queue(
        item_id=item_id,
        account=account,
        source_url=source_page_url,
        title_theme=title_theme,
        direct_stream_url=stream_url
    )
    return added


if __name__ == "__main__":
    print("[+] Harvest Source Videos Utility Initialized.")
    qm = QueueManager()
    print(f"Current Queue Length: {len(qm.list_queue())}")
    for item in qm.list_queue():
        local_f = RAW_SOURCES_DIR / f"{item['item_id']}.mp4"
        exists_str = "EXISTS" if local_f.exists() else "STREAM-ONLY"
        print(f"  * [{item['account']}] {item['title_theme']} -> {exists_str} ({local_f.name})")
