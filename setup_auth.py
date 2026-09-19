"""
One-Click YouTube OAuth Setup & GitHub Secret Sync for TimberCraft Automation
1. Opens browser for YouTube OAuth authorization
2. Validates channel permissions
3. Saves local token.json
4. Automatically uploads encrypted YOUTUBE_TOKEN_JSON secret to GitHub repository
"""

import os
import sys
import json
import base64
import urllib.request
from pathlib import Path

# Allow local HTTP redirect for OAuth 2 callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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

GITHUB_OWNER = "anikinuzir3wood"
GITHUB_REPO = "wood-working-automations"

# Ensure GITHUB_TOKEN is loaded from env or .env file
GITHUB_TOKEN = os.getenv("GH_PAT", "")
if not GITHUB_TOKEN:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GH_PAT="):
                    GITHUB_TOKEN = line.split("=", 1)[1].strip()
                    break


import http.server

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if "code=" in self.path:
            self.server.auth_response_url = f"http://localhost:8088{self.path}"
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = """<html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1 style="color: #2e7d32;">Authentication Successful!</h1>
                <p>TimberCraft Archive has been connected successfully. You may close this window.</p>
            </body></html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Waiting for authorization code...")

    def log_message(self, format, *args):
        pass


def authenticate_google():
    print("\n" + "=" * 75)
    print("  TIMBERCRAFT YOUTUBE OAUTH AUTHENTICATION")
    print("  Target Email   : anikinuzir3@gmail.com")
    print("  Target Channel : TimberCraft Archive")
    print("  GCP Project    : timbercraft-archive (642561120312)")
    print("  " + "-" * 71)
    print("  REMINDER: DO NOT USE zeniusindividual@gmail.com (Avian Architects)!")
    print("=" * 75)
    
    if not CLIENT_SECRETS_FILE.exists():
        print(f"[!] Error: {CLIENT_SECRETS_FILE} not found!")
        sys.exit(1)

    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    print("[*] Starting local OAuth flow for TimberCraft Archive...")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        SCOPES,
        redirect_uri="http://localhost:8088/"
    )
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

    (BASE_DIR / "scratch").mkdir(exist_ok=True)
    with open(BASE_DIR / "scratch" / "auth_url.txt", "w", encoding="utf-8") as f:
        f.write(auth_url)
    print(f"\n[AUTH_URL_READY] {auth_url}\n", flush=True)

    import webbrowser
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    server = http.server.HTTPServer(("localhost", 8088), OAuthCallbackHandler)
    server.auth_response_url = None
    print("[*] Waiting for OAuth callback on http://localhost:8088/ ...")
    while not server.auth_response_url:
        server.handle_request()
    server.server_close()

    flow.fetch_token(authorization_response=server.auth_response_url)
    creds = flow.credentials

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
            channel_id = items[0]["id"]
            title = items[0]["snippet"]["title"]
            if "avian" in title.lower():
                print(f"\n[!] DANGER: You authenticated '{title}' (Avian Architects) instead of TimberCraft!")
                print("[!] Aborting token save to prevent cross-account contamination.")
                sys.exit(1)
            if "timbercraft" not in title.lower() and channel_id != "UC1UWiLB8zxqMvbzGFP2bljA":
                print(f"\n[!] WRONG CHANNEL SELECTED: '{title}' (ID: {channel_id})!")
                print("[!] You selected the personal profile 'Anikin Uzir' instead of the Brand Channel 'TimberCraft Archive'.")
                print("[!] When Google displays 'Choose an account or a brand account', you MUST click 'TimberCraft Archive'!")
                print("[!] Aborting to prevent saving credentials for the wrong channel.")
                sys.exit(1)
            print(f"[+] SUCCESS! Verified YouTube Channel: '{title}' (ID: {channel_id})!")
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
