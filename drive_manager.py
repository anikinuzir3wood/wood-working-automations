"""
Google Drive Buffer & Archive Manager for TimberCraft Automation
===============================================================
Manages:
1. Video Buffer: Uploads fresh high-resolution raw footage into 'YouTube Videos' folder
2. Duplicate Shield: Automatically archives uploaded videos into 'YouTube Videos/Uploaded' folder
3. Stock Monitoring: Tracks count of pending buffer videos (minimum 6 = 3 days safety stock)
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import (
    BASE_DIR,
    DRIVE_PARENT_FOLDER_ID,
    DRIVE_UPLOADED_FOLDER_ID,
    MIN_STOCK_THRESHOLD_VIDEOS
)

TOKEN_FILE = BASE_DIR / "token.json"
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/drive"
]


class GoogleDriveManager:
    def __init__(self):
        self.service = None
        self.parent_folder_id = DRIVE_PARENT_FOLDER_ID
        self.uploaded_folder_id = DRIVE_UPLOADED_FOLDER_ID
        self._init_service()

    def _init_service(self):
        """Initializes Google Drive API service using token.json."""
        if not TOKEN_FILE.exists():
            print("[!] Warning: token.json not found — Drive Manager operating in local fallback mode.")
            return

        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                        f.write(creds.to_json())
                except Exception as e:
                    print(f"[*] Token refresh notice: {e}")

            self.service = build("drive", "v3", credentials=creds)
            print("[+] Google Drive API service initialized.")
        except Exception as e:
            print(f"[!] Drive API initialization notice: {e}")
            self.service = None

    def upload_to_buffer(self, local_path: Path, filename: Optional[str] = None) -> Optional[str]:
        """Uploads a fresh raw video to the 'YouTube Videos' Google Drive buffer folder."""
        if not self.service:
            print("[*] Drive service unavailable — file stored in local buffer.")
            return None

        if not local_path.exists():
            print(f"[!] Cannot upload non-existent file: {local_path}")
            return None

        from googleapiclient.http import MediaFileUpload

        target_name = filename or local_path.name

        # Check if already present in Drive folder
        existing = self.find_file(target_name, folder_id=self.parent_folder_id)
        if existing:
            print(f"[*] File '{target_name}' already exists in Drive buffer (ID: {existing['id']}).")
            return existing["id"]

        print(f"[*] Uploading '{target_name}' to Google Drive 'YouTube Videos' buffer...")
        file_metadata = {
            "name": target_name,
            "parents": [self.parent_folder_id]
        }
        media = MediaFileUpload(str(local_path), mimetype="video/mp4", resumable=True)
        try:
            req = self.service.files().create(body=file_metadata, media_body=media, fields="id, name")
            file_obj = req.execute()
            print(f"[+] Successfully backed up to Google Drive buffer! File ID: {file_obj.get('id')}")
            return file_obj.get("id")
        except Exception as e:
            print(f"[!] Error uploading to Google Drive: {e}")
            return None

    def move_to_uploaded_archive(self, filename_or_id: str) -> bool:
        """
        Moves a processed/uploaded video file from 'YouTube Videos' into 'Uploaded' folder.
        Guarantees that raw source videos are never accidentally re-used!
        """
        if not self.service:
            return False

        try:
            # If filename was provided instead of file ID, locate it
            file_id = filename_or_id
            if not file_id.startswith("1") or len(file_id) < 15:
                found = self.find_file(filename_or_id, folder_id=self.parent_folder_id)
                if not found:
                    print(f"[*] File '{filename_or_id}' not found in Drive buffer to archive.")
                    return False
                file_id = found["id"]

            # Move file: remove from parent_folder_id and add to uploaded_folder_id
            file_meta = self.service.files().get(fileId=file_id, fields="parents").execute()
            prev_parents = ",".join(file_meta.get("parents", []))

            self.service.files().update(
                fileId=file_id,
                addParents=self.uploaded_folder_id,
                removeParents=prev_parents,
                fields="id, parents"
            ).execute()
            print(f"[+] Successfully archived raw video into Google Drive 'Uploaded' folder! (File ID: {file_id})")
            return True
        except Exception as e:
            print(f"[!] Error archiving file in Google Drive: {e}")
            return False

    def list_buffer_files(self) -> List[Dict[str, Any]]:
        """Lists all available un-uploaded video files in the 'YouTube Videos' folder."""
        if not self.service:
            return []

        try:
            q = f"'{self.parent_folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
            res = self.service.files().list(q=q, fields="files(id, name, size, createdTime)").execute()
            return res.get("files", [])
        except Exception as e:
            print(f"[!] Error listing Drive buffer: {e}")
            return []

    def get_stock_count(self) -> int:
        """Returns the count of available raw videos waiting in Drive buffer."""
        files = self.list_buffer_files()
        return len(files)

    def find_file(self, filename: str, folder_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Finds a file by name inside a specific folder."""
        if not self.service:
            return None
        try:
            q = f"name = '{filename}' and trashed = false"
            if folder_id:
                q += f" and '{folder_id}' in parents"
            res = self.service.files().list(q=q, fields="files(id, name)").execute()
            items = res.get("files", [])
            return items[0] if items else None
        except Exception:
            return None


if __name__ == "__main__":
    dm = GoogleDriveManager()
    if dm.service:
        count = dm.get_stock_count()
        print(f"[Drive Buffer Status] Available videos in 'YouTube Videos': {count}")
        for f in dm.list_buffer_files()[:5]:
            print(f"  - {f['name']} (ID: {f['id']})")
    else:
        print("[!] Drive service not active. Run setup_auth.py with Drive scope.")
