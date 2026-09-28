"""
TimberCraft Autonomous Google Drive Replenisher & Archiver
===========================================================
1. Connects to Google Drive folder 'YouTube Videos' (1kl4GK0BsNJU6cOaDZUwM29l0jF-NRQj7).
2. Fetches all uploaded video titles from YouTube Channel 'TimberCraft Archive'.
3. Cross-checks all Drive videos:
   - If ALREADY UPLOADED to YouTube: Instantly moves file to Google Drive 'Uploaded' folder.
   - If FRESH & UN-UPLOADED: Registers video in video_queue.json.
4. Ensures the queue is ALWAYS replenished with safety stock so automation NEVER stops!
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Set

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import (
    DRIVE_PARENT_FOLDER_ID,
    DRIVE_UPLOADED_FOLDER_ID,
    TARGET_STOCK_BUFFER_VIDEOS
)
from queue_manager import QueueManager

GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.json"
YOUTUBE_TOKEN_FILE = BASE_DIR / "token.json"


def get_drive_service():
    """Initializes Google Drive service from gdrive_token.json or token.json."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    env_token = os.getenv("GDRIVE_TOKEN_JSON") or os.getenv("YOUTUBE_TOKEN_JSON", "")
    if env_token.strip():
        try:
            creds = Credentials.from_authorized_user_info(json.loads(env_token.strip()))
        except Exception:
            pass

    if not creds and GDRIVE_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(GDRIVE_TOKEN_FILE))

    if not creds and YOUTUBE_TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(YOUTUBE_TOKEN_FILE))
        except Exception:
            pass

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            print(f"[!] Drive token refresh notice: {e}")

    if not creds:
        raise PermissionError("No Google Drive credentials found! Please run 'python setup_drive_auth.py'.")

    return build("drive", "v3", credentials=creds)


def get_youtube_service():
    """Initializes YouTube service from token.json."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    env_token = os.getenv("YOUTUBE_TOKEN_JSON", "")
    if env_token.strip():
        try:
            creds = Credentials.from_authorized_user_info(json.loads(env_token.strip()))
        except Exception:
            pass

    if not creds and YOUTUBE_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(YOUTUBE_TOKEN_FILE))

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            print(f"[!] YouTube token refresh notice: {e}")

    if not creds:
        raise PermissionError("No YouTube credentials found! Please run 'python setup_auth.py'.")

    return build("youtube", "v3", credentials=creds)


def get_all_youtube_uploaded_titles() -> Set[str]:
    """Fetches all titles of uploaded videos on TimberCraft Archive to prevent duplicates."""
    titles = set()
    try:
        yt = get_youtube_service()
        res = yt.channels().list(part="contentDetails", mine=True).execute()
        items = res.get("items", [])
        if not items:
            return titles
        uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

        next_page = None
        while True:
            pl_res = yt.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page
            ).execute()
            for it in pl_res.get("items", []):
                t = it["snippet"]["title"].strip()
                # Clean title for fuzzy comparison
                clean_t = re.sub(r'#Shorts|#shorts', '', t).strip().lower()
                clean_t = re.sub(r'the master carpenter\'s\s*', '', clean_t).strip()
                titles.add(clean_t)
            next_page = pl_res.get("nextPageToken")
            if not next_page:
                break
    except Exception as e:
        print(f"[!] Warning fetching YouTube channel uploads: {e}")

    # Also load from processed_history.json
    hist_file = BASE_DIR / "processed_history.json"
    if hist_file.exists():
        try:
            data = json.loads(hist_file.read_text(encoding="utf-8"))
            for v in data.get("videos", []):
                t = v.get("title", "")
                clean_t = re.sub(r'#Shorts|#shorts', '', t).strip().lower()
                clean_t = re.sub(r'the master carpenter\'s\s*', '', clean_t).strip()
                titles.add(clean_t)
        except Exception:
            pass

    return titles


def normalize_title(name: str) -> str:
    """Normalizes a filename or title for comparison."""
    n = Path(name).stem.lower()
    n = re.sub(r'#shorts|#Shorts', '', n)
    n = re.sub(r'the master carpenter\'s\s*', '', n)
    n = re.sub(r'[^a-z0-9]', ' ', n)
    return ' '.join(n.split())


def is_title_duplicate(filename: str, existing_normalized_titles: Set[str]) -> bool:
    norm_file = normalize_title(filename)
    if not norm_file:
        return False
    for ex in existing_normalized_titles:
        norm_ex = normalize_title(ex)
        if not norm_ex:
            continue
        # Direct equality or high substring overlap
        if norm_file == norm_ex:
            return True
        if len(norm_file) > 10 and (norm_file in norm_ex or norm_ex in norm_file):
            return True
    return False


def get_or_create_uploaded_subfolder(drive, parent_folder_id: str) -> str:
    """Finds or creates an 'Uploaded' subfolder inside YouTube Videos."""
    query = f"'{parent_folder_id}' in parents and name = 'Uploaded' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    res = drive.files().list(q=query, fields="files(id, name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]

    # Fallback to configured ID
    if DRIVE_UPLOADED_FOLDER_ID:
        return DRIVE_UPLOADED_FOLDER_ID

    folder_meta = {
        "name": "Uploaded",
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id]
    }
    created = drive.files().create(body=folder_meta, fields="id").execute()
    return created.get("id")


def move_file_to_uploaded(drive, file_id: str, current_parent_id: str, uploaded_folder_id: str) -> bool:
    """Moves a file in Google Drive from parent folder into 'Uploaded' subfolder."""
    try:
        drive.files().update(
            fileId=file_id,
            addParents=uploaded_folder_id,
            removeParents=current_parent_id,
            fields="id, parents"
        ).execute()
        return True
    except Exception as e:
        print(f"[!] Error moving file {file_id} to Uploaded folder: {e}")
        return False


def sync_drive_buffer_to_queue(batch_size: int = 10) -> int:
    """
    Main Auto-Replenishment Function:
    1. Scans Google Drive 'YouTube Videos' folder.
    2. Identifies already-uploaded duplicates -> moves them to 'Uploaded' folder.
    3. Adds fresh un-uploaded videos to video_queue.json.
    """
    print("\n" + "=" * 75)
    print("  TIMBERCRAFT AUTONOMOUS GOOGLE DRIVE BUFFER SYNC")
    print(f"  Source Folder ID: {DRIVE_PARENT_FOLDER_ID}")
    print("=" * 75)

    drive = get_drive_service()
    qm = QueueManager()

    # 1. Get all YouTube channel videos
    print("[*] Fetching all uploaded videos from YouTube channel to enforce ZERO duplicates...")
    existing_yt_titles = get_all_youtube_uploaded_titles()
    print(f"[+] Total existing uploaded video titles on channel/history: {len(existing_yt_titles)}")

    # 2. Get 'Uploaded' subfolder ID
    uploaded_folder_id = get_or_create_uploaded_subfolder(drive, DRIVE_PARENT_FOLDER_ID)

    # 3. List all files directly in 'YouTube Videos'
    q = f"'{DRIVE_PARENT_FOLDER_ID}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
    res = drive.files().list(
        q=q,
        fields="files(id, name, size, createdTime)",
        pageSize=200,
        orderBy="createdTime"
    ).execute()

    files = res.get("files", [])
    print(f"[+] Found {len(files)} total video file(s) in Google Drive 'YouTube Videos' buffer.")

    # 4. Check each file for duplicate vs fresh
    duplicates_moved = 0
    fresh_candidates = []

    for f in files:
        fname = f["name"]
        fid = f["id"]
        fstem = Path(fname).stem

        # Check by ID in history or by title on YouTube
        if qm.is_processed(fstem) or qm.is_processed(fid) or is_title_duplicate(fname, existing_yt_titles):
            print(f"  [ALREADY ON YOUTUBE] '{fname}' -> Moving to Drive 'Uploaded' folder...")
            moved = move_file_to_uploaded(drive, fid, DRIVE_PARENT_FOLDER_ID, uploaded_folder_id)
            if moved:
                duplicates_moved += 1
        else:
            fresh_candidates.append(f)

    if duplicates_moved > 0:
        print(f"[+] Cleaned up {duplicates_moved} already-uploaded videos into 'Uploaded' folder.")

    print(f"[*] Available fresh un-uploaded videos in Drive: {len(fresh_candidates)}")

    # 5. Populate video_queue.json up to target runway
    current_queue = qm.list_queue()
    existing_q_ids = {item.get("drive_file_id") or item.get("item_id") for item in current_queue}
    existing_q_names = {item.get("title_theme", "").lower() for item in current_queue}

    added_to_queue = 0
    for cand in fresh_candidates:
        if len(qm.list_queue()) >= TARGET_STOCK_BUFFER_VIDEOS:
            print(f"[*] Queue capacity reached ({TARGET_STOCK_BUFFER_VIDEOS} videos). Stopping intake.")
            break

        fid = cand["id"]
        fname = cand["name"]

        if fid in existing_q_ids or normalize_title(fname) in existing_q_names:
            continue

        # Format clean title
        clean_name = Path(fname).stem
        clean_name = re.sub(r'#Shorts|#shorts', '', clean_name).strip()
        clean_title = f"The Master Carpenter's {clean_name} #Shorts"
        masthead = clean_name.upper()
        if len(masthead) > 26:
            masthead = masthead[:23] + "..."

        added = qm.add_to_queue(
            item_id=fid,
            account="drive_buffer",
            source_url=f"https://drive.google.com/file/d/{fid}/view",
            title_theme=clean_title,
            direct_stream_url=None,
            video_analysis={
                "clean_title": clean_title,
                "masthead_text": masthead,
                "drive_file_id": fid,
                "original_filename": fname
            },
            masthead_text=masthead
        )

        if added:
            # Update the item with drive_file_id in queue
            q = qm.list_queue()
            for q_item in q:
                if q_item["item_id"] == fid:
                    q_item["drive_file_id"] = fid
                    q_item["drive_filename"] = fname
                    break
            qm._save_json(qm.queue_file, q)
            added_to_queue += 1
            print(f"  [+] Queued from Drive: '{clean_name}' (Queue Size: {len(q)})")

    print(f"\n[+] Drive Sync Complete! Added {added_to_queue} fresh videos to video_queue.json.")
    print(f"[*] Total active videos waiting in queue: {len(qm.list_queue())}")
    return added_to_queue


if __name__ == "__main__":
    sync_drive_buffer_to_queue()
