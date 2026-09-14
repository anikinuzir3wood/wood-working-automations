"""
One-Click Channel Switcher for TimberCraft Automation
Use this when you create your new YouTube channel / Google account:
1. Opens Google OAuth in browser to authenticate your new channel
2. Saves updated token.json locally
3. Automatically pushes the new token to GitHub Secrets in the cloud
"""

import sys
import json
import base64
import urllib.request
from pathlib import Path
from nacl import public

BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

GITHUB_OWNER = "anikinuzir3wood"
GITHUB_REPO = "wood-working-automations"
GITHUB_TOKEN = os.getenv("GH_PAT", "")


def authenticate_new_channel():
    print("=" * 80)
    print("[*] TIMBERCRAFT CHANNEL SWITCHER")
    print("=" * 80)
    print("[*] Opening Google login in your browser...")
    print("[*] Log in with your NEW YouTube channel Google Account.")
    print("-" * 80)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"[+] Successfully authenticated new YouTube channel! Saved to: {TOKEN_FILE.name}")
    except Exception as e:
        print(f"[!] Authentication failed: {e}")
        return False

    # Push to GitHub Secrets
    print("\n[*] Pushing new channel credentials to GitHub Actions cloud...")
    try:
        url_key = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/public-key"
        req_key = urllib.request.Request(url_key, headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TimberCraft"
        })
        with urllib.request.urlopen(req_key) as resp:
            key_info = json.loads(resp.read().decode())

        key_id = key_info["key_id"]
        public_key = public.PublicKey(base64.b64decode(key_info["key"]))
        sealed_box = public.SealedBox(public_key)

        token_str = TOKEN_FILE.read_text(encoding="utf-8")
        encrypted = base64.b64encode(sealed_box.encrypt(token_str.encode("utf-8"))).decode("utf-8")

        put_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/YOUTUBE_TOKEN_JSON"
        payload = json.dumps({"encrypted_value": encrypted, "key_id": key_id}).encode("utf-8")
        req_put = urllib.request.Request(put_url, data=payload, method="PUT", headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TimberCraft",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req_put) as r:
            print(f"[+] GitHub Cloud Secret 'YOUTUBE_TOKEN_JSON' updated! (HTTP {r.status})")

        # Also push new YOUTUBE_CLIENT_SECRETS
        client_str = CLIENT_SECRETS_FILE.read_text(encoding="utf-8")
        enc_client = base64.b64encode(sealed_box.encrypt(client_str.encode("utf-8"))).decode("utf-8")
        put_c_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/YOUTUBE_CLIENT_SECRETS"
        req_put_c = urllib.request.Request(put_c_url, data=json.dumps({"encrypted_value": enc_client, "key_id": key_id}).encode("utf-8"), method="PUT", headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TimberCraft",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req_put_c) as rc:
            print(f"[+] GitHub Cloud Secret 'YOUTUBE_CLIENT_SECRETS' updated! (HTTP {rc.status})")

        print("\n" + "=" * 80)
        print("[+] YOUR NEW CHANNEL IS NOW CONNECTED TO CLOUD AUTOMATION!")
        print("=" * 80 + "\n")
        return True
    except Exception as e:
        print(f"[!] Failed to push secrets to GitHub: {e}")
        return False


if __name__ == "__main__":
    authenticate_new_channel()
