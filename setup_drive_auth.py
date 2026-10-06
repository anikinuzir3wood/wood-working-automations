"""
One-Click Google Drive OAuth Setup & GitHub Secret Sync for TimberCraft Automation
===================================================================================
1. Connects to Google Drive to manage:
   - Reading fresh raw videos from 'YouTube Videos' folder (1kl4GK0BsNJU6cOaDZUwM29l0jF-NRQj7)
   - Archiving uploaded videos into 'YouTube Videos/Uploaded' folder
2. Saves local gdrive_token.json
3. Automatically syncs GDRIVE_TOKEN_JSON secret to GitHub repository anikinuzir3wood/wood-working-automations
"""

import os
import sys
import json
import base64
import urllib.request
import http.server
from pathlib import Path

# Allow local HTTP redirect for OAuth 2 callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive"
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


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if "code=" in self.path:
            full_url = f"http://localhost:8088{self.path}"
            try:
                flow = self.server.flow
                flow.fetch_token(authorization_response=full_url)
                creds = flow.credentials

                from googleapiclient.discovery import build
                drive_service = build("drive", "v3", credentials=creds)
                about = drive_service.about().get(fields="user").execute()
                user_email = about.get("user", {}).get("emailAddress", "Unknown")

                print(f"[+] Connected Google Drive Account: {user_email}")

                self.server.verified_creds = creds
                self.server.user_email = user_email
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = f"""<html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: #2e7d32; font-size: 32px;">&#10004; Google Drive Authentication Successful!</h1>
                    <h2 style="color: #1b5e20;">Account: {user_email}</h2>
                    <p style="font-size: 18px;">TimberCraft Google Drive buffer connected. You may close this window.</p>
                </body></html>"""
                self.wfile.write(html.encode("utf-8"))
            except Exception as e:
                print(f"[!] Error handling OAuth response: {e}")
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Waiting for authorization...")

    def log_message(self, format, *args):
        pass


def upload_secret_to_github(secret_name: str, secret_value: str):
    print("\n" + "-" * 75)
    print(f"[*] Syncing {secret_name} to GitHub Actions ({GITHUB_OWNER}/{GITHUB_REPO})...")
    
    try:
        from nacl import encoding, public
    except ImportError:
        print("[!] PyNaCl not installed. Run 'pip install pynacl' to enable automatic GitHub secret sync.")
        return

    try:
        key_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/public-key"
        req = urllib.request.Request(key_url, headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TimberCraft-Auth"
        })
        with urllib.request.urlopen(req) as resp:
            key_data = json.loads(resp.read().decode())
            key_id = key_data["key_id"]
            public_key_b64 = key_data["key"]

        public_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder)
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

        secret_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/secrets/{secret_name}"
        payload = json.dumps({
            "encrypted_value": encrypted_b64,
            "key_id": key_id
        }).encode("utf-8")

        req = urllib.request.Request(secret_url, data=payload, method="PUT", headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "User-Agent": "TimberCraft-Auth"
        })
        with urllib.request.urlopen(req) as resp:
            if resp.status in (201, 204):
                print(f"[+] SUCCESS: {secret_name} successfully encrypted and synced to GitHub Actions!")
            else:
                print(f"[!] Warning: GitHub API returned status {resp.status}")
    except Exception as e:
        print(f"[!] GitHub secret sync notice: {e}")


def authenticate_drive():
    print("\n" + "=" * 80)
    print("  🔴 CRITICAL ACCOUNT VERIFICATION: TIMBERCRAFT ARCHIVE 🔴")
    print("  " + "-" * 76)
    print("  Channel Name    : TimberCraft Archive / Anikin Uzir")
    print("  Expected Email  : anikinuzir3@gmail.com")
    print("  Google Cloud    : timbercraft-studio (Project #1051808411017)")
    print("  Drive Folder    : 1kl4GK0BsNJU6cOaDZUwM29l0jF-NRQj7 ('YouTube Videos')")
    print("  GitHub Repo     : anikinuzir3wood/wood-working-automations")
    print("  " + "-" * 76)
    print("  ⚠️ WARNING: DO NOT AUTHENTICATE WITH zeniusindividual@gmail.com!")
    print("  Only log in with: anikinuzir3@gmail.com")
    print("=" * 80 + "\n")

    if not CLIENT_SECRETS_FILE.exists():
        print(f"[!] Error: {CLIENT_SECRETS_FILE} not found!")
        sys.exit(1)

    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        SCOPES,
        redirect_uri="http://localhost:8088/"
    )
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

    (BASE_DIR / "scratch").mkdir(exist_ok=True)
    with open(BASE_DIR / "scratch" / "drive_auth_url.txt", "w", encoding="utf-8") as f:
        f.write(auth_url)
    print(f"\n[AUTH_URL_READY] {auth_url}\n", flush=True)

    server = http.server.HTTPServer(("0.0.0.0", 8088), OAuthCallbackHandler)
    server.flow = flow
    server.verified_creds = None
    server.user_email = None

    print("[*] Waiting for Google Drive OAuth callback on http://localhost:8088/ ...")
    while not server.verified_creds:
        server.handle_request()
    server.server_close()

    creds = server.verified_creds
    token_json_str = creds.to_json()
    with open(GDRIVE_TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token_json_str)
    print(f"[+] Saved fresh Drive credentials to {GDRIVE_TOKEN_FILE}")

    # Sync to GitHub Actions Secrets
    upload_secret_to_github("GDRIVE_TOKEN_JSON", token_json_str)

    return token_json_str


if __name__ == "__main__":
    authenticate_drive()
