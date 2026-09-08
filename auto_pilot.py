"""
Master Autopilot Runner for TimberCraft Automation
Connects:
1. Queue Manager (Duplicate Protection & Ingestion)
2. TimberCraft Pipeline (AI Director + Audio Engine + Visual Synthesizer)
3. YouTube Pre-Flight Uploader (Unlisted -> 3-min Content ID scan -> Public)
4. Golden Timezone Scheduler (2 PM EDT / 8 PM EDT + Jitter)
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from config import OUTPUT_DIR, SCRATCH_DIR
from queue_manager import QueueManager
from scheduler import DailyScheduler
from pipeline import TimberCraftPipeline
from uploader import YouTubeUploader


class TimberCraftAutopilot:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.qm = QueueManager()
        self.scheduler = DailyScheduler()
        self.pipeline = TimberCraftPipeline()
        self.uploader = YouTubeUploader(dry_run=self.dry_run)

    def process_next_in_queue(self, skip_upload_wait: bool = False, keep_unlisted: bool = False) -> bool:
        """Pulls the next pending video from queue, renders it, and executes pre-flight upload."""
        item = self.qm.get_next_pending()
        if not item:
            print("[!] Queue is empty! No pending videos to process.")
            return False

        item_id = item["item_id"]
        account = item["account"]
        title_theme = item["title_theme"]

        print("\n" + "=" * 80)
        print(f"[*] AUTOPILOT PROCESSING ITEM: {title_theme}")
        print(f"- Account : {account}")
        print(f"- Item ID : {item_id}")
        print("=" * 80 + "\n")

        # 1. Resolve Raw Video Source (Strict Anti-Duplicate Mode)
        raw_source = None

        # Check A: Dedicated pre-downloaded file in assets/raw_sources/<item_id>.mp4
        local_cand = Path(__file__).resolve().parent / "assets" / "raw_sources" / f"{item_id}.mp4"
        if local_cand.exists() and local_cand.stat().st_size > 50000:
            raw_source = local_cand

        # Check B: Explicit local path specified in queue item
        if not raw_source and item.get("local_raw_path"):
            lp = Path(item["local_raw_path"])
            if lp.exists() and lp.stat().st_size > 50000:
                raw_source = lp

        # Check C: Download from direct_stream_url if provided
        if not raw_source and item.get("direct_stream_url"):
            from downloader import download_stream
            cand = SCRATCH_DIR / f"raw_{item_id}.mp4"
            try:
                download_stream(item["direct_stream_url"], cand)
                if cand.exists() and cand.stat().st_size > 50000:
                    raw_source = cand
            except Exception as e:
                print(f"[!] Direct stream download failed for {item_id}: {e}")

        # Strict Verification: NEVER fall back to a generic file
        if not raw_source or not raw_source.exists():
            print(f"[!] ERROR: No unique raw footage available for item {item_id} ('{title_theme}').")
            print(f"    Automated upload safely skipped to protect channel from duplicate uploads.")
            return False

        # Strict Duplicate Protection: Verify content hash was not previously uploaded
        if self.qm.is_raw_hash_processed(raw_source):
            print(f"[!] CRITICAL ANTI-DUPLICATE GUARD:")
            print(f"    Raw footage '{raw_source.name}' was ALREADY processed in a previous upload!")
            print(f"    Aborting immediately to prevent uploading identical video to YouTube.")
            return False

        print(f"[+] Verified Unique Raw Footage: {raw_source.name} ({raw_source.stat().st_size / (1024*1024):.2f} MB)")

        # 2. Execute Pipeline Render
        # Pass foreign captions flag so video engine can blur foreign subs
        extra_plan_flags = {}
        if item.get("has_foreign_captions"):
            extra_plan_flags["has_foreign_captions"] = True
            print("[*] Source flagged with foreign captions — blur + English overlay will be applied.")

        final_video = self.pipeline.run(raw_source, video_title=title_theme, extra_plan_flags=extra_plan_flags)
        meta_file = final_video.with_name(final_video.stem + "_metadata.json")

        with open(meta_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # 3. Execute Pre-Flight Upload
        video_id = self.uploader.upload_preflight_short(
            final_video,
            metadata,
            skip_wait=skip_upload_wait,
            keep_unlisted=keep_unlisted
        )

        # 4. Mark Processed in History (including raw source hash)
        self.qm.mark_processed(
            item_id=item_id,
            account=account,
            output_file=str(final_video),
            title=title_theme,
            youtube_video_id=video_id,
            raw_source_path=raw_source
        )

        print("\n" + "=" * 80)
        print(f"[+] AUTOPILOT ITEM COMPLETED SUCCESSFULLY: {title_theme}")
        print("=" * 80 + "\n")
        return True

    def run_status(self):
        """Displays status of queue, history, schedule, and background music inventory."""
        self.scheduler.print_status()
        history = self.qm.list_history()
        print(f"- Total Videos Processed So Far: {len(history)}")
        for rec in history[-3:]:
            print(f"  * [{rec['account']}] {rec['title']} -> {rec['status']} ({rec.get('youtube_id', 'N/A')})")
        print("=" * 80)
        
        from music_manager import MusicManager
        mm = MusicManager()
        mm.print_library_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TimberCraft Master Autopilot")
    parser.add_argument("--run-next", action="store_true", help="Process and upload next video from queue immediately")
    parser.add_argument("--status", action="store_true", help="Display system status, queue, and next schedule slot")
    parser.add_argument("--dry-run", action="store_true", help="Run without live YouTube credentials")
    parser.add_argument("--skip-wait", action="store_true", help="Skip 3-minute Content ID wait during test")
    parser.add_argument("--keep-unlisted", action="store_true", help="Keep video unlisted for preview/testing")
    parser.add_argument("--ci-mode", action="store_true", help="Run in GitHub Actions CI mode with automatic cleanup")

    args = parser.parse_args()
    autopilot = TimberCraftAutopilot(dry_run=args.dry_run)

    if args.run_next:
        success = autopilot.process_next_in_queue(
            skip_upload_wait=args.skip_wait,
            keep_unlisted=args.keep_unlisted
        )
        if not success:
            print("[!] Processing returned False or Queue was empty.")
            sys.exit(0)  # Don't fail CI if queue is simply empty
        sys.exit(0)
    else:
        autopilot.run_status()
