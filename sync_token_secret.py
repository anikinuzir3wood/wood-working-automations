"""
Self-Healing YouTube Token Persister for GitHub Actions
Ensures newly refreshed tokens or updated tokens during autopilot execution
are automatically encrypted and persisted back to GitHub Repository Secrets.
"""

import os
import sys
import json
import urllib.request
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def sync_token_file(
    token_path: Path,
    secret_name: str,
    gh_token: str,
    key_id: str,
    public_key_b64: str,
    repo_owner: str,
    repo_name: str
):
    if not token_path.exists():
        print(f"[*] No {token_path.name} found to sync.")
        return

    with open(token_path, "r", encoding="utf-8") as f:
        token_str = f.read().strip()

    if not token_str:
        print(f"[!] {token_path.name} is empty — skipping sync.")
        return

    # Verify token is actually valid or refreshable before syncing
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        creds = Credentials.from_authorized_user_file(str(token_path))
        if creds.expired and creds.refresh_token:
            print(f"[*] {token_path.name} expired; attempting refresh before syncing...")
            creds.refresh(Request())
            token_str = creds.to_json()
            with open(token_path, "w", encoding="utf-8") as f:
                f.write(token_str)
            print(f"[+] {token_path.name} refreshed successfully prior to sync.")
        elif not creds.valid:
            print(f"[!] {token_path.name} is invalid/unrefreshable. Aborting sync to preserve existing secret.")
            return
    except Exception as e:
        print(f"[!] Token verification/refresh failed for {token_path.name} ({e}). Aborting sync to preserve existing secret.")
        return

    from base64 import b64decode, b64encode
    from nacl import public

    # Encrypt token using LibSodium SealedBox
    pubkey_bytes = b64decode(public_key_b64)
    sealed_box = public.SealedBox(public.PublicKey(pubkey_bytes))
    encrypted_bytes = sealed_box.encrypt(token_str.encode("utf-8"))
    encrypted_b64 = b64encode(encrypted_bytes).decode("utf-8")

    # PUT Encrypted Secret
    put_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/{secret_name}"
    payload = json.dumps({
        "encrypted_value": encrypted_b64,
        "key_id": key_id
    }).encode("utf-8")

    req_put = urllib.request.Request(put_url, data=payload, headers={
        "Authorization": f"Bearer {gh_token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "TimberCraft-TokenSync"
    }, method="PUT")

    try:
        with urllib.request.urlopen(req_put) as resp_put:
            if resp_put.status in (201, 204):
                print(f"[+] Successfully auto-synced refreshed {secret_name} to GitHub Secrets! (Status: {resp_put.status})")
            else:
                print(f"[*] Secret update response status for {secret_name}: {resp_put.status}")
    except Exception as e:
        print(f"[!] Failed to update {secret_name} in GitHub Secrets: {e}")


def sync_tokens_to_secrets(repo_owner: str = "anikinuzir3wood", repo_name: str = "wood-working-automations"):
    base_dir = Path(__file__).resolve().parent
    tokens_to_sync = [
        (base_dir / "token.json", "YOUTUBE_TOKEN_JSON"),
        (base_dir / "gdrive_token.json", "GDRIVE_TOKEN_JSON")
    ]

    gh_token = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
    if not gh_token:
        env_file = base_dir / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GH_PAT="):
                        gh_token = line.split("=", 1)[1].strip()
                        break
    if not gh_token:
        print("[*] GH_PAT not configured in environment or .env — skipping automated secret sync.")
        return

    try:
        from nacl import public
    except ImportError:
        print("[!] PyNaCl not installed — skipping secret sync.")
        return

    # Fetch Repository Public Key once
    key_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/public-key"
    req_key = urllib.request.Request(key_url, headers={
        "Authorization": f"Bearer {gh_token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "TimberCraft-TokenSync"
    })

    try:
        with urllib.request.urlopen(req_key) as resp:
            key_data = json.loads(resp.read().decode("utf-8"))
            key_id = key_data["key_id"]
            public_key_b64 = key_data["key"]
    except Exception as e:
        print(f"[!] Could not fetch repo public key (GH_PAT may lack 'repo' scope): {e}")
        return

    for token_path, secret_name in tokens_to_sync:
        sync_token_file(token_path, secret_name, gh_token, key_id, public_key_b64, repo_owner, repo_name)


if __name__ == "__main__":
    sync_tokens_to_secrets()
