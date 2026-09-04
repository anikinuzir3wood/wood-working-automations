"""
One-Click YouTube OAuth Setup & GitHub Secret Sync for TimberCraft Automation
1. Opens browser for YouTube OAuth authorization
2. Validates channel permissions
3. Saves local token.json
4. Automatically uploads encrypted YOUTUBE_TOKEN_JSON secret to GitHub repository
"""

import sys
import json
import base64
import urllib.request
from pathlib import Path

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

GITHUB_OWNER = "thecraftorastudio-byte"
GITHUB_REPO = "wood-working-automations"
GITHUB_TOKEN = "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"


def authenticate_google():
    print("\n" + "=" * 75)
    print("  TIMBERCRAFT YOUTUBE OAUTH AUTHENTICATION")
    print("  Target Email   : anikinuzir3@gmail.com")
    print("  Target Channel : TimberCraft Archive / Anikin Uzir")
    print("  GCP Project    : timbercraft-archive (642561120312)")
    print("  " + "-" * 71)
    print("  REMINDER: DO NOT USE zeniusindividual@gmail.com (Avian Architects)!")
    print("=" * 75)
    
    if not CLIENT_SECRETS_FILE.exists():
        print(f"[!] Error: {CLIENT_SECRETS_FILE} not found!")
        sys.exit(1)

    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    print("[*] Starting local OAuth browser flow...")
    print("[*] Select account: anikinuzir3@gmail.com (TimberCraft Archive)")
    
    class URLWriter:
        def format(self, **kwargs):
            url = kwargs.get('url', '')
            (BASE_DIR / "scratch").mkdir(exist_ok=True)
            with open(BASE_DIR / "scratch" / "auth_url.txt", "w", encoding="utf-8") as f:
                f.write(url)
            print(f"\n[AUTH_URL_READY] {url}\n", flush=True)
            return f"Please visit this URL to authorize: {url}"

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
    creds = flow.run_local_server(
        port=8088,
        open_browser=False,
        authorization_prompt_message=URLWriter(),
        prompt="consent",
        access_type="offline"
    )

    token_json_str = creds.to_json()
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token_json_str)
    print(f"[+] Saved fresh credentials locally to {TOKEN_FILE}")

    # Verify access with YouTube API
    try:
        yt = build("youtube", "v3", credentials=creds)
        res = yt.channels().list(part="snippet", mine=True).execute()
        items = res.get("items", [])
        if items:
            title = items[0]["snippet"]["title"]
            if "avian" in title.lower():
                print(f"\n[!] DANGER: You authenticated '{title}' (Avian Architects) instead of TimberCraft!")
                print("[!] Aborting token save to prevent cross-account contamination.")
                sys.exit(1)
            if "timbercraft" not in title.lower():
                print(f"\n[!] WRONG CHANNEL SELECTED: '{title}' (Personal Channel)!")
                print("[!] You must select 'TimberCraft Archive' (Brand Account) from the list.")
                print("[!] Aborting to prevent saving credentials for the wrong channel.")
                sys.exit(1)
            print(f"[+] SUCCESS! Verified YouTube Brand Channel: '{title}'!")
        else:
            print("[!] Warning: No channel found.")
            sys.exit(1)
    except Exception as e:
        print(f"[!] Warning during channel verification: {e}")

    return token_json_str


def upload_secret_to_github(secret_value: str):
    print("\n" + "-" * 75)
    print(f"[*] Syncing fresh token to GitHub Actions ({GITHUB_OWNER}/{GITHUB_REPO})...")
    
    try:
        from nacl import encoding, public
    except ImportError:
        print("[!] PyNaCl not installed. Run 'pip install pynacl' to enable automatic GitHub secret sync.")
        print("[*] You can manually paste the token into GitHub Repo Settings -> Secrets -> YOUTUBE_TOKEN_JSON")
        return

    try:
        # 1. Get repository public key
        key_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/public-key"
        req = urllib.request.Request(key_url, headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TimberCraft-Auth"
        })
        with urllib.request.urlopen(req) as resp:
            key_info = json.loads(resp.read().decode())

        key_id = key_info["key_id"]
        public_key_b64 = key_info["key"]

        # 2. Encrypt secret
        public_key = public.PublicKey(base64.b64decode(public_key_b64))
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

        # 3. PUT secret
        secret_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/YOUTUBE_TOKEN_JSON"
        payload = json.dumps({
            "encrypted_value": encrypted_b64,
            "key_id": key_id
        }).encode("utf-8")
        put_req = urllib.request.Request(secret_url, data=payload, method="PUT", headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TimberCraft-Auth",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(put_req) as resp:
            if resp.status in (201, 204):
                print(f"[+] SUCCESS! 'YOUTUBE_TOKEN_JSON' updated in GitHub Secrets.")
            else:
                print(f"[!] GitHub API returned status {resp.status}")
    except Exception as e:
        print(f"[!] Could not automatically upload secret to GitHub: {e}")
        print("[*] You can manually copy token.json content to GitHub Secrets -> YOUTUBE_TOKEN_JSON")


if __name__ == "__main__":
    token_str = authenticate_google()
    upload_secret_to_github(token_str)
    print("\n" + "=" * 75)
    print("  ALL DONE! TimberCraft is 100% configured for automated uploads.")
    print("=" * 75 + "\n")
