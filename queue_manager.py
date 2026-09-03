"""
Batch Queue & History Tracker for TimberCraft Automation
Manages:
- processed_history.json: Prevents duplicate video processing across audited accounts
- video_queue.json: Ingestion queue for automated rendering and scheduling
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from config import BASE_DIR

QUEUE_FILE = BASE_DIR / "video_queue.json"
HISTORY_FILE = BASE_DIR / "processed_history.json"


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
                "history": []
            }
            self._save_json(self.history_file, default_history)

        if not self.queue_file.exists():
            default_queue = [
                {
                    "item_id": "67acb36a000000002903f7ac",
                    "account": "wooden_man",
                    "source_url": "https://www.rednote.com/discovery/item/67acb36a000000002903f7ac",
                    "title_theme": "The Ancient Sandalwood Lock",
                    "status": "PENDING",
                    "added_at": datetime.now().isoformat()
                },
                {
                    "item_id": "6803c43a000000001d02f0d2",
                    "account": "amazing_inventors",
                    "source_url": "https://www.rednote.com/discovery/item/6803c43a000000001d02f0d2",
                    "title_theme": "The 3D Secret Dovetail",
                    "status": "PENDING",
                    "added_at": datetime.now().isoformat()
                },
                {
                    "item_id": "65cb662d000000000700528a",
                    "account": "wood_soul",
                    "source_url": "https://www.rednote.com/discovery/item/65cb662d000000000700528a",
                    "title_theme": "The Zero-Gap Kumiko Joint",
                    "status": "PENDING",
                    "added_at": datetime.now().isoformat()
                }
            ]
            self._save_json(self.queue_file, default_queue)

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

    def mark_processed(
        self,
        item_id: str,
        account: str,
        output_file: str,
        title: str,
        youtube_video_id: Optional[str] = None
    ):
        """Records a video into history and removes it from queue."""
        history = self._load_json(self.history_file)
        if item_id not in history["processed_ids"]:
            history["processed_ids"].append(item_id)
        
        record = {
            "item_id": item_id,
            "account": account,
            "title": title,
            "output_file": str(output_file),
            "youtube_id": youtube_video_id,
            "processed_at": datetime.now().isoformat(),
            "status": "COMPLETED"
        }
        history["history"].append(record)
        self._save_json(self.history_file, history)

        # Update queue status
        queue = self._load_json(self.queue_file)
        queue = [q for q in queue if q.get("item_id") != item_id]
        self._save_json(self.queue_file, queue)
        print(f"[+] Recorded {item_id} into history and removed from queue.")

    def add_to_queue(
        self,
        item_id: str,
        account: str,
        source_url: str,
        title_theme: str
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
            "status": "PENDING",
            "added_at": datetime.now().isoformat()
        }
        queue.append(new_entry)
        self._save_json(self.queue_file, queue)
        print(f"[+] Added {item_id} to queue.")
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
    for item in qm.list_queue():
        print(f"  - [{item['account']}] {item['title_theme']} ({item['item_id']})")
