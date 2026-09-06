"""
Batch Queue & History Tracker for TimberCraft Automation
Manages:
- processed_history.json: Prevents duplicate video processing across audited accounts
- video_queue.json: Ingestion queue for automated rendering and scheduling
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from config import BASE_DIR

QUEUE_FILE = BASE_DIR / "video_queue.json"
HISTORY_FILE = BASE_DIR / "processed_history.json"


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of a file for absolute duplicate detection."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            sha.update(chunk)
    return sha.hexdigest()


class QueueManager:
    def __init__(self):
        self.queue_file = QUEUE_FILE
        self.history_file = HISTORY_FILE
        self._init_storage()

    def _init_storage(self):
        """Ensure queue and history files exist with valid JSON structure."""
        if not self.history_file.exists():
            default_history = {
                "processed_ids": [],
                "processed_hashes": [],
                "history": []
            }
            self._save_json(self.history_file, default_history)
        else:
            # Ensure processed_hashes key exists in legacy files
            try:
                hist = self._load_json(self.history_file)
                if "processed_hashes" not in hist:
                    hist["processed_hashes"] = []
                    self._save_json(self.history_file, hist)
            except Exception:
                pass

        if not self.queue_file.exists():
            self._save_json(self.queue_file, [])

    def _load_json(self, file_path: Path) -> Any:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, file_path: Path, data: Any):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def is_processed(self, item_id: str) -> bool:
        """Check if item_id was already processed to guarantee zero duplicate uploads."""
        history = self._load_json(self.history_file)
        return item_id in history.get("processed_ids", [])

    def is_raw_hash_processed(self, file_path: Path) -> bool:
        """Check if this raw video file content has already been processed in any previous upload."""
        if not file_path.exists():
            return False
        file_hash = compute_file_hash(file_path)
        history = self._load_json(self.history_file)
        processed_hashes = history.get("processed_hashes", [])
        return file_hash in processed_hashes

    def mark_processed(
        self,
        item_id: str,
        account: str,
        output_file: str,
        title: str,
        youtube_video_id: Optional[str] = None,
        raw_source_path: Optional[Path] = None
    ):
        """Records a video into history and removes it from queue."""
        history = self._load_json(self.history_file)
        if item_id not in history.get("processed_ids", []):
            history.setdefault("processed_ids", []).append(item_id)

        raw_hash = None
        if raw_source_path and Path(raw_source_path).exists():
            raw_hash = compute_file_hash(Path(raw_source_path))
            if raw_hash not in history.get("processed_hashes", []):
                history.setdefault("processed_hashes", []).append(raw_hash)

        record = {
            "item_id": item_id,
            "account": account,
            "title": title,
            "output_file": str(output_file),
            "youtube_id": youtube_video_id,
            "raw_hash": raw_hash,
            "processed_at": datetime.now().isoformat(),
            "status": "COMPLETED"
        }
        history.setdefault("history", []).append(record)
        self._save_json(self.history_file, history)

        # Update queue status
        queue = self._load_json(self.queue_file)
        queue = [q for q in queue if q.get("item_id") != item_id]
        self._save_json(self.queue_file, queue)
        print(f"[+] Recorded {item_id} into history (Hash: {raw_hash[:12] if raw_hash else 'N/A'}) and removed from queue.")

    def add_to_queue(
        self,
        item_id: str,
        account: str,
        source_url: str,
        title_theme: str,
        direct_stream_url: Optional[str] = None,
        local_raw_path: Optional[str] = None
    ) -> bool:
        """Adds a new item to queue if not already processed."""
        if self.is_processed(item_id):
            print(f"[!] Duplicate Ignored: {item_id} has already been processed.")
            return False

        queue = self._load_json(self.queue_file)
        for item in queue:
            if item.get("item_id") == item_id:
                print(f"[!] Item {item_id} is already pending in the queue.")
                return False

        new_entry = {
            "item_id": item_id,
            "account": account,
            "source_url": source_url,
            "title_theme": title_theme,
            "direct_stream_url": direct_stream_url,
            "local_raw_path": local_raw_path,
            "status": "PENDING",
            "added_at": datetime.now().isoformat()
        }
        queue.append(new_entry)
        self._save_json(self.queue_file, queue)
        print(f"[+] Added {item_id} ('{title_theme}') to queue.")
        return True

    def get_next_pending(self) -> Optional[Dict[str, Any]]:
        """Returns the next pending item from queue."""
        queue = self._load_json(self.queue_file)
        for item in queue:
            if item.get("status") == "PENDING":
                return item
        return None

    def list_queue(self) -> List[Dict[str, Any]]:
        return self._load_json(self.queue_file)

    def list_history(self) -> List[Dict[str, Any]]:
        return self._load_json(self.history_file).get("history", [])


if __name__ == "__main__":
    qm = QueueManager()
    print("[+] Queue Manager Initialized.")
    print(f"Pending Items in Queue: {len(qm.list_queue())}")
    for item in qm.list_queue()[:5]:
        print(f"  - [{item['account']}] {item['title_theme']} ({item['item_id']})")
