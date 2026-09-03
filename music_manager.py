"""
Music Manager & ai33.pro / Suno AI Connector for TimberCraft Automation
Features:
- Connects to user's ai33.pro account via ai33_config.json
- Caches and tracks reuse of woodworking-matched background music
- Intelligent reuse policy: Never wastes API credits/time generating when a matched track exists
- Only generates new tracks when genuinely required or requested
- Tailors prompts specifically for Woodworking (acoustic strings, marimba, minimal, zero drums/vocals)
- Pre-seeds and maintains high-fidelity acoustic library (Chisel ASMR, Ancient Temple, Kumiko Lattice)
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List

# Ensure UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from config import MUSIC_DIR, SCRATCH_DIR, BASE_DIR, AI33_CONFIG_FILE, MUSIC_LIBRARY_CATALOG


class MusicManager:
    def __init__(self):
        self.music_dir = MUSIC_DIR
        self.music_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = AI33_CONFIG_FILE
        self.catalog_file = MUSIC_LIBRARY_CATALOG
        self.config = self._load_config()
        self.catalog = self._load_catalog()
        self._init_library()

    def _load_config(self) -> Dict[str, Any]:
        """Loads ai33.pro configuration."""
        if not self.config_file.exists():
            default_config = {
                "provider": "ai33.pro",
                "api_key": os.getenv("AI33_API_KEY", ""),
                "base_url": "https://api.ai33.pro",
                "suno_model": "chirp-v3.5",
                "account_status": "ready",
                "smart_reuse_enabled": True,
                "instructions": "Enter your ai33.pro API key in 'api_key'. If left empty, the engine automatically reuses and generates local acoustic woodworking soundscapes."
            }
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            return default_config

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"api_key": os.getenv("AI33_API_KEY", ""), "base_url": "https://api.ai33.pro"}

    def _load_catalog(self) -> Dict[str, Any]:
        """Loads music library catalog with metadata and reuse counts."""
        if self.catalog_file.exists():
            try:
                with open(self.catalog_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"tracks": []}

    def _save_catalog(self):
        """Persists catalog data."""
        with open(self.catalog_file, "w", encoding="utf-8") as f:
            json.dump(self.catalog, f, indent=2, ensure_ascii=False)

    def _init_library(self):
        """Pre-seeds the music library with 3 high-quality, non-intrusive acoustic woodworking tracks."""
        track_1 = self.music_dir / "woodworking_zen_pizzicato.wav"
        track_2 = self.music_dir / "ancient_temple_marimba.wav"
        track_3 = self.music_dir / "kumiko_acoustic_drone.wav"

        # 1. Chisel & End Grain Slicing (Delicate Marimba + Pizzicato Plucks)
        if not track_1.exists():
            print("[*] Seeding Music Library: woodworking_zen_pizzicato.wav...")
            synth_1 = (
                "aevalsrc='0.05*sin(2*PI*174.61*t)*exp(-0.7*mod(t,2)) + "
                "0.04*sin(2*PI*261.63*t)*exp(-1.1*mod(t,1.5)) + "
                "0.03*sin(2*PI*329.63*t)*exp(-1.4*mod(t,1)) + "
                "0.02*sin(2*PI*523.25*t)*exp(-2.2*mod(t,0.5))':s=44100:d=45"
            )
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", synth_1,
                "-af", "lowpass=f=2400,highpass=f=100,volume=-8dB",
                str(track_1)
            ]
            subprocess.run(cmd, capture_output=True)

        # 2. Heavy Architectural Joinery / Sandalwood Lock (Deep Resonant Wooden Marimba)
        if not track_2.exists():
            print("[*] Seeding Music Library: ancient_temple_marimba.wav...")
            synth_2 = (
                "aevalsrc='0.06*sin(2*PI*130.81*t)*exp(-0.6*mod(t,3)) + "
                "0.04*sin(2*PI*196.00*t)*exp(-0.9*mod(t,2)) + "
                "0.03*sin(2*PI*293.66*t)*exp(-1.3*mod(t,1.5))':s=44100:d=45"
            )
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", synth_2,
                "-af", "lowpass=f=2000,highpass=f=80,volume=-8dB",
                str(track_2)
            ]
            subprocess.run(cmd, capture_output=True)

        # 3. Geometric Kumiko Lattice / Secret Dovetail (Harmonic Wooden Drone & Soft Plucks)
        if not track_3.exists():
            print("[*] Seeding Music Library: kumiko_acoustic_drone.wav...")
            synth_3 = (
                "aevalsrc='0.04*sin(2*PI*146.83*t)*exp(-0.5*mod(t,4)) + "
                "0.03*sin(2*PI*220.00*t)*exp(-0.8*mod(t,2.5)) + "
                "0.02*sin(2*PI*369.99*t)*exp(-1.2*mod(t,1.8)) + "
                "0.015*sin(2*PI*440.00*t)*exp(-1.8*mod(t,1.0))':s=44100:d=45"
            )
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", synth_3,
                "-af", "lowpass=f=2200,highpass=f=90,volume=-8dB",
                str(track_3)
            ]
            subprocess.run(cmd, capture_output=True)

        # Sync files into catalog if missing
        existing_filenames = {t["filename"] for t in self.catalog.get("tracks", [])}
        preseeds = [
            {
                "filename": "woodworking_zen_pizzicato.wav",
                "mood": "chisel_asmr",
                "title": "Zen Pizzicato Chisel Bed",
                "reuse_count": 0,
                "source": "local_acoustic_studio"
            },
            {
                "filename": "ancient_temple_marimba.wav",
                "mood": "temple_joint",
                "title": "Ancient Temple Resonance",
                "reuse_count": 0,
                "source": "local_acoustic_studio"
            },
            {
                "filename": "kumiko_acoustic_drone.wav",
                "mood": "kumiko_lattice",
                "title": "Kumiko Harmonic Lattice Drone",
                "reuse_count": 0,
                "source": "local_acoustic_studio"
            }
        ]

        for p in preseeds:
            if p["filename"] not in existing_filenames and (self.music_dir / p["filename"]).exists():
                self.catalog["tracks"].append(p)

        self._save_catalog()

    def get_ai33_prompt_for_new_track(self, mood: str = "chisel_asmr", sub_niche: str = "Traditional Woodworking") -> Dict[str, str]:
        """
        Generates the exact Suno AI / ai33.pro prompt tailored specifically for Woodworking documentaries:
        - Minimalist, acoustic, transparent bed
        - Strictly NO drums, NO brass, NO vocals, NO heavy beats
        - Won't overpower spoken narration
        """
        if "temple" in mood or "lock" in mood or "sandalwood" in mood:
            styles = "ancient wooden marimba, deep cello resonance, bamboo percussion clicks, meditative documentary score, calm, organic, 75 bpm, instrumental"
            title = f"Ancient Joinery Bed - {sub_niche}"
        elif "kumiko" in mood or "dovetail" in mood or "puzzle" in mood:
            styles = "delicate fingerpicked acoustic guitar, subtle pizzicato strings, warm wooden tone, atmospheric documentary background, peaceful, 80 bpm, instrumental"
            title = f"Kumiko Precision Bed - {sub_niche}"
        else:
            styles = "minimalist acoustic documentary soundtrack, delicate pizzicato cello plucks, warm wooden marimba, gentle organic atmosphere, transparent background music, zero vocals, zero drums, 80 bpm"
            title = f"Woodcraft Minimalist Bed - {sub_niche}"

        return {
            "title": title,
            "tags": styles,
            "prompt": (
                "Pure acoustic documentary background music. Delicate pizzicato strings, warm wooden marimba plucks. "
                "Organic, unobtrusive, peaceful tempo. Zero percussion, zero drums, zero vocals, transparent audio bed."
            )
        }

    def generate_with_ai33(self, mood: str, sub_niche: str) -> Optional[Path]:
        """
        Calls ai33.pro API if credentials are provided.
        Falls back to acoustic synthesis if key is not configured or network fails.
        """
        api_key = self.config.get("api_key", "").strip() or os.getenv("AI33_API_KEY", "").strip()
        prompt_data = self.get_ai33_prompt_for_new_track(mood=mood, sub_niche=sub_niche)

        if not api_key:
            print(f"[*] ai33.pro Account Notice: No API key found in ai33_config.json.")
            print(f"    (You can add your ai33.pro key in ai33_config.json to generate via cloud)")
            print(f"[*] Synthesizing high-grade acoustic studio soundtrack locally for '{mood}'...")

            # Synthesize specialized track locally
            timestamp = int(time.time())
            filename = f"woodwork_{mood}_{timestamp}.wav"
            out_track = self.music_dir / filename

            synth_custom = (
                "aevalsrc='0.05*sin(2*PI*164.81*t)*exp(-0.7*mod(t,2.2)) + "
                "0.04*sin(2*PI*246.94*t)*exp(-1.0*mod(t,1.6)) + "
                "0.025*sin(2*PI*329.63*t)*exp(-1.5*mod(t,1.1))':s=44100:d=45"
            )
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", synth_custom,
                "-af", "lowpass=f=2200,highpass=f=90,volume=-8dB",
                str(out_track)
            ]
            subprocess.run(cmd, capture_output=True)

            entry = {
                "filename": filename,
                "mood": mood,
                "title": prompt_data["title"],
                "reuse_count": 0,
                "source": "local_acoustic_studio"
            }
            self.catalog["tracks"].append(entry)
            self._save_catalog()
            return out_track

        # Live ai33.pro API Call
        try:
            import requests
            base_url = self.config.get("base_url", "https://api.ai33.pro").rstrip("/")
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }

            # Verify credits first
            try:
                c_resp = requests.get(f"{base_url}/v1/credits", headers=headers, timeout=5)
                if c_resp.status_code == 200:
                    credits = c_resp.json().get("credits", "unknown")
                    print(f"[+] ai33.pro Connected: {credits} credits available for account {self.config.get('account_email', '')}")
            except Exception:
                pass

            url = f"{base_url}/v1s/task/music-generation"
            payload = {
                "create_mode": "custom",
                "title": prompt_data["title"],
                "tags": prompt_data["tags"],
                "prompt": prompt_data["prompt"],
                "make_instrumental": True
            }

            print(f"[*] Connecting to ai33.pro API -> Dispatching music task: '{prompt_data['title']}'...")
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                task_id = data.get("task_id") or data.get("data", {}).get("task_id")
                if task_id:
                    print(f"    ai33.pro Task Dispatched: {task_id}. Waiting for generation...")
                    for _ in range(20):
                        time.sleep(4)
                        t_resp = requests.get(f"{base_url}/v1/task/{task_id}", headers=headers, timeout=10)
                        if t_resp.status_code == 200:
                            t_data = t_resp.json()
                            audio_url = t_data.get("audio_url") or t_data.get("data", {}).get("audio_url")
                            if audio_url:
                                timestamp = int(time.time())
                                filename = f"ai33_{mood}_{timestamp}.mp3"
                                out_track = self.music_dir / filename
                                r_dl = requests.get(audio_url, timeout=30)
                                with open(out_track, "wb") as f:
                                    f.write(r_dl.content)

                                entry = {
                                    "filename": filename,
                                    "mood": mood,
                                    "title": prompt_data["title"],
                                    "reuse_count": 0,
                                    "source": "ai33.pro"
                                }
                                self.catalog["tracks"].append(entry)
                                self._save_catalog()
                                print(f"[+] ai33.pro Soundtrack Generated & Saved: {filename}")
                                return out_track
            print(f"[!] ai33.pro API response: {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            print(f"[!] ai33.pro connection error: {e}")

        # Fallback to existing
        return None

    def get_matched_soundtrack(self, mood: str = "chisel_asmr", sub_niche: str = "Woodworking", force_new: bool = False) -> Path:
        """
        Smart Music Selector:
        - Reuses existing matched track from library.
        - Rotates tracks of the same mood to provide subtle variety across videos.
        - Only generates when:
          1. force_new is True, OR
          2. No matching track exists in the library.
        """
        # Ensure files physically exist
        valid_tracks = []
        for t in self.catalog.get("tracks", []):
            p = self.music_dir / t["filename"]
            if p.exists():
                valid_tracks.append((t, p))

        if not valid_tracks:
            self._init_library()
            for t in self.catalog.get("tracks", []):
                p = self.music_dir / t["filename"]
                if p.exists():
                    valid_tracks.append((t, p))

        # Check if we should reuse or generate new
        matching = []
        for meta, path in valid_tracks:
            # Mood similarity match
            track_mood = meta.get("mood", "")
            if (mood in track_mood) or (track_mood in mood):
                matching.append((meta, path))
            elif ("temple" in mood or "lock" in mood or "sandalwood" in mood) and ("temple" in track_mood or "marimba" in track_mood):
                matching.append((meta, path))
            elif ("kumiko" in mood or "dovetail" in mood or "puzzle" in mood) and ("kumiko" in track_mood or "drone" in track_mood):
                matching.append((meta, path))
            elif ("chisel" in mood or "sharp" in mood or "slice" in mood) and ("pizzicato" in track_mood or "chisel" in track_mood):
                matching.append((meta, path))

        if not force_new and matching:
            # Pick track with lowest reuse count for gentle rotation
            matching.sort(key=lambda x: x[0].get("reuse_count", 0))
            chosen_meta, chosen_path = matching[0]
            chosen_meta["reuse_count"] = chosen_meta.get("reuse_count", 0) + 1
            self._save_catalog()

            print(f"\n[+] SMART MUSIC ENGINE: Reusing Cached Soundtrack '{chosen_path.name}'")
            print(f"    - Matched Mood : {mood}")
            print(f"    - Times Reused : {chosen_meta['reuse_count']}")
            print(f"    - Status       : No new API credit used (Saved cost & time)")
            return chosen_path

        # If force_new or no match found:
        print(f"\n[*] SMART MUSIC ENGINE: New track required for mood: '{mood}'")
        new_track = self.generate_with_ai33(mood=mood, sub_niche=sub_niche)
        if new_track and new_track.exists():
            return new_track

        # Fallback to first available
        fallback_meta, fallback_path = valid_tracks[0]
        fallback_meta["reuse_count"] = fallback_meta.get("reuse_count", 0) + 1
        self._save_catalog()
        print(f"[+] Using Fallback Soundtrack: {fallback_path.name}")
        return fallback_path

    def print_library_status(self):
        """Prints current music library inventory and ai33 connection status."""
        print("=" * 80)
        print("TIMBERCRAFT BACKGROUND MUSIC INVENTORY & ai33.pro STATUS")
        print("=" * 80)
        api_key = self.config.get("api_key", "")
        masked_key = (api_key[:6] + "..." + api_key[-4:]) if len(api_key) > 10 else ("NOT SET (Using Local Acoustic Engine)" if not api_key else "CONFIGURED")
        print(f"ai33.pro Account API Key : {masked_key}")
        print(f"Provider Endpoint        : {self.config.get('base_url', 'https://api.ai33.pro')}")
        print(f"Smart Reuse Enabled      : {self.config.get('smart_reuse_enabled', True)}")
        print(f"Tracks in Library        : {len(self.catalog.get('tracks', []))}\n")

        for idx, t in enumerate(self.catalog.get("tracks", []), 1):
            file_exists = (self.music_dir / t["filename"]).exists()
            status = "READY" if file_exists else "MISSING"
            print(f"{idx}. [{status}] {t['filename']}")
            print(f"   Title: {t.get('title', 'N/A')} | Mood: {t.get('mood', 'N/A')} | Reused: {t.get('reuse_count', 0)} times | Source: {t.get('source', 'local')}")
        print("=" * 80)


if __name__ == "__main__":
    mm = MusicManager()
    mm.print_library_status()
    print("\n--- Testing Mood Matcher ---")
    track = mm.get_matched_soundtrack("chisel_asmr")
    print(f"Selected: {track}")
