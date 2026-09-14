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


def sync_token_to_secret(repo_owner: str = "anikinuzir3wood", repo_name: str = "wood-working-automations"):
    token_path = Path(__file__).resolve().parent / "token.json"
    if not token_path.exists():
        print("[*] No token.json found to sync.")
        return

    gh_token = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
    if not gh_token:
        print("[*] GH_PAT not configured in environment — skipping automated secret sync.")
        return

    try:
        from base64 import b64decode, b64encode
        from nacl import public
    except ImportError:
        print("[!] PyNaCl not installed — skipping secret sync.")
        return

    secret_name = "YOUTUBE_TOKEN_JSON"

    with open(token_path, "r", encoding="utf-8") as f:
        token_str = f.read().strip()

    if not token_str:
        print("[!] token.json is empty — aborting sync.")
        return

    # 1. Fetch Repository Public Key
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

    # 2. Encrypt token using LibSodium SealedBox
    pubkey_bytes = b64decode(public_key_b64)
    sealed_box = public.SealedBox(public.PublicKey(pubkey_bytes))
    encrypted_bytes = sealed_box.encrypt(token_str.encode("utf-8"))
    encrypted_b64 = b64encode(encrypted_bytes).decode("utf-8")

    # 3. PUT Encrypted Secret
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
                print(f"[*] Secret update response status: {resp_put.status}")
    except Exception as e:
        print(f"[!] Failed to update {secret_name} in GitHub Secrets: {e}")


if __name__ == "__main__":
    sync_token_to_secret()
