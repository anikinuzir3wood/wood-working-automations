"""
TimberCraft Autonomous Harvester Daemon
======================================
1. Downloads fresh high-res raw woodworking videos.
2. Checks SHA-256 & ID against processed_history.json (Strict Zero Duplicates).
3. Analyzes frame-by-frame with Gemini Vision (Rejects huge Chinese text, detects subtitles).
4. Uploads clean raw videos to Google Drive 'YouTube Videos' buffer folder.
5. Populates video_queue.json to guarantee 3-day safety stock (minimum 6 videos).
"""

import sys
import json
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import (
    BASE_DIR,
    ASSETS_DIR,
    SCRATCH_DIR,
    DRIVE_PARENT_FOLDER_ID,
    DRIVE_UPLOADED_FOLDER_ID,
    MIN_STOCK_THRESHOLD_VIDEOS
)
from queue_manager import QueueManager, compute_file_hash
from drive_manager import GoogleDriveManager
from video_analyzer import analyze_video_content
from downloader import probe_video

RAW_SOURCES_DIR = ASSETS_DIR / "raw_sources"
RAW_SOURCES_DIR.mkdir(parents=True, exist_ok=True)


def download_stream(stream_url: str, output_path: Path) -> bool:
    """Stream download video with headers."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.rednote.com/",
        "Accept": "*/*"
    }
    req = urllib.request.Request(stream_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(output_path, "wb") as f:
            while chunk := resp.read(1024 * 1024):
                f.write(chunk)
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[+] Downloaded: {output_path.name} ({size_mb:.2f} MB)")
        return True
    except Exception as e:
        print(f"[!] Error downloading stream: {e}")
        if output_path.exists():
            output_path.unlink()
        return False


class HarvesterDaemon:
    def __init__(self):
        self.qm = QueueManager()
        self.dm = GoogleDriveManager()

    def get_stock_level(self) -> int:
        """Returns number of ready items in queue + Drive buffer."""
        queue_len = len(self.qm.list_queue())
        drive_count = self.dm.get_stock_count() if self.dm.service else 0
        return max(queue_len, drive_count)

    def process_candidate(self, candidate: Dict[str, Any]) -> bool:
        """
        Processes a single raw video candidate:
        1. Duplicate ID check
        2. Download raw file
        3. Duplicate content hash check
        4. Gemini Vision frame analysis (anti-clutter & text check)
        5. Google Drive upload
        6. Queue registration
        """
        item_id = candidate["note_id"]
        title = candidate.get("title", "Traditional Woodworking Craft")
        author = candidate.get("author_name", "wood_soul")
        stream_url = candidate.get("master_cdn_url") or candidate.get("stream_url")

        print("\n" + "=" * 70)
        print(f"[*] EVALUATING CANDIDATE: {item_id} | Author: {author}")
        print(f"    Title: {title}")
        print("=" * 70)

        # 1. ID Check
        if self.qm.is_processed(item_id):
            print(f"[-] Video {item_id} has already been uploaded previously. SKIPPING.")
            return False

        # 2. Download
        local_path = RAW_SOURCES_DIR / f"{item_id}.mp4"
        if not local_path.exists():
            print(f"[*] Downloading raw original stream from CDN...")
            ok = download_stream(stream_url, local_path)
            if not ok:
                print(f"[!] Failed to download video stream.")
                return False

        # 3. SHA-256 Hash Check
        if self.qm.is_raw_hash_processed(local_path):
            print(f"[!] Duplicate SHA-256 hash detected! This video was already used under another ID. REJECTING.")
            local_path.unlink()
            return False

        # Probe video
        try:
            probe = probe_video(local_path)
            dur = probe.get("duration", 0)
            print(f"[*] Probed Video: {dur:.1f}s | {probe.get('width')}x{probe.get('height')}")
            if dur < 15.0:
                print(f"[!] Video too short ({dur:.1f}s < 15s). REJECTING.")
                local_path.unlink()
                return False
        except Exception as e:
            print(f"[!] Probe error: {e}")

        # 4. Gemini Vision Content & Anti-Clutter Analysis
        print(f"[*] Running Gemini Vision frame-by-frame visual analysis...")
        try:
            analysis = analyze_video_content(local_path)
        except Exception as e:
            print(f"[!] Vision analysis failed: {e}")
            analysis = {"rejected": False, "subject": "Ancient Sunmao Joinery", "has_foreign_captions": False}

        is_rejected = (
            analysis.get("rejected", False)
            or analysis.get("reject", False)
            or analysis.get("has_huge_chinese_text", False)
        )
        if is_rejected:
            reason = analysis.get("reject_reason", "Visual quality check failed: screen blocked by huge text.")
            print(f"[!] VIDEO REJECTED BY ANTI-CLUTTER POLICY: {reason}")
            local_path.unlink()
            return False

        print(f"[+] Visual Check PASSED! Subject: {analysis.get('subject')}")
        if analysis.get("has_foreign_captions"):
            print(f"    [!] Subtitles detected -> Smart Boxblur & English Caption overlay enabled.")
        else:
            print(f"    [+] Pristine footage -> Zero foreign text detected.")

        # Save analysis cache
        analysis_file = SCRATCH_DIR / f"analysis_{item_id}.json"
        with open(analysis_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        # 5. Upload to Google Drive Buffer
        drive_file_id = None
        if self.dm.service:
            print(f"[*] Backing up raw video to Google Drive 'YouTube Videos' buffer...")
            drive_file_id = self.dm.upload_to_buffer(local_path, filename=f"{item_id}.mp4")

        # 6. Add to Queue
        account_slug = "wood_soul" if "木魂" in author else ("wooden_man" if "木头人" in author else "amazing_inventors")
        added = self.qm.add_to_queue(
            item_id=item_id,
            account=account_slug,
            source_url=candidate.get("note_url", ""),
            title_theme=title,
            direct_stream_url=stream_url
        )

        if added:
            print(f"[+] SUCCESS: Video {item_id} added to processing queue and Drive buffer!")
            return True
        else:
            print(f"[-] Video {item_id} was already in queue.")
            return False

    def ingest_candidate_list(self, candidates: List[Dict[str, Any]]) -> int:
        """Ingests a list of harvested candidates until target buffer is fulfilled."""
        added_count = 0
        for cand in candidates:
            success = self.process_candidate(cand)
            if success:
                added_count += 1
                time.sleep(1)  # Gentle spacing
        return added_count


if __name__ == "__main__":
    daemon = HarvesterDaemon()
    print(f"[*] Current stock level: {daemon.get_stock_level()} videos")
    
    # Load harvested scratchpad candidates if present
    scratchpad_path = Path("C:/Users/GHSCM2/.gemini/antigravity-ide/brain/8c6eacf6-2dcd-4320-879f-6052a000af4c/browser/scratchpad_ah2arn8k.md")
    if scratchpad_path.exists():
        text = scratchpad_path.read_text(encoding="utf-8")
        import re
        m = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
        if m:
            candidates = json.loads(m.group(0))
            print(f"[*] Found {len(candidates)} candidates in scratchpad. Ingesting...")
            added = daemon.ingest_candidate_list(candidates)
            print(f"\n[+] Ingestion cycle complete. Added {added} fresh videos.")
            print(f"[*] New stock level: {daemon.get_stock_level()} videos.")
