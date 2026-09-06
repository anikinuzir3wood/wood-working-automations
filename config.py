"""
Configuration and constants for TimberCraft Automation Engine
Target Market: US Tier-1 YouTube Shorts & Long-form Compilations
Niche: Ancient Mortise-and-Tenon Woodworking (榫卯 - Sunmao & Kumiko Joinery)
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
FOLEY_DIR = ASSETS_DIR / "foley"
OVERLAYS_DIR = ASSETS_DIR / "overlays"
OUTPUT_DIR = BASE_DIR / "output"
SCRATCH_DIR = BASE_DIR / "scratch"

AI33_CONFIG_FILE = BASE_DIR / "ai33_config.json"
MUSIC_LIBRARY_CATALOG = MUSIC_DIR / "music_library.json"

for d in [ASSETS_DIR, MUSIC_DIR, FOLEY_DIR, OVERLAYS_DIR, OUTPUT_DIR, SCRATCH_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Video Dimensions & Framing
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
TARGET_FPS = 60
CROP_FACTOR = 0.92  # 8% crop & subtle zoom to invalidate digital video hash

# Safezone Layout (Avoiding YouTube Shorts bottom and side UI collisions)
MASTHEAD_Y = 240     # Top safezone for pillbox header (below mobile notch & YouTube search/dots)
SUBTITLE_Y = 1420    # Placed above bottom 350px YouTube metadata overlay
BOTTOM_UI_MARGIN = 350

# Voiceover Settings (Edge-TTS)
TTS_VOICE = "en-US-ChristopherNeural"  # Authoritative, calm, BBC/NatGeo baritone
TTS_RATE = "-4%"                       # Deliberate, unhurried cadence
TTS_PITCH = "-2Hz"                     # Deep chest resonance

# Broadcast Mastering Audio Filter Chain (FFmpeg)
BROADCAST_AUDIO_FILTER = (
    "highpass=f=80,"
    "equalizer=f=140:t=q:w=1.2:g=2.8,"
    "equalizer=f=3500:t=q:w=1.5:g=2.2,"
    "acompressor=threshold=-18dB:ratio=4:attack=15:release=120,"
    "alimiter=limit=-1dB"
)

# Background Music Sweet-Spot (Calibrated via 7-level A/B test — DO NOT CHANGE)
# The actual sweet-spot value (-7dB) is defined in audio_engine.py as MUSIC_FIXED_SWEET_SPOT_DB.
# Voice mean = -23.0 dB | Music mean = -26.7 dB | Gap = 3.7 dB
# Result: Warm, clearly audible on all devices, never overpowers voiceover.
MUSIC_SWEET_SPOT_LOCKED = True  # Set to True = sweet spot is calibrated and locked

# Target Duration (Sweet-spot for >100% loop retention)
MIN_DURATION = 30.0
MAX_DURATION = 38.0
OPTIMAL_DURATION = 34.0

# Vetted Rednote (Xiaohongshu) Creator Accounts (Clean domestic footage, zero strikes)
AUDITED_ACCOUNTS = {
    "wood_soul": {
        "name": "木魂",
        "rednote_id": "4354932786",
        "profile_url": "https://www.rednote.com/user/profile/6494eaf9000000002a035dce",
        "style": "Pure hands-only macro woodworking & chisel ASMR"
    },
    "wooden_man": {
        "name": "木头人",
        "rednote_id": "273660019",
        "profile_url": "https://www.rednote.com/user/profile/5b5c62cce8ac2b4b0b47c4cf",
        "style": "Rosewood classical joints, zero gap tolerances"
    },
    "amazing_inventors": {
        "name": "神奇发明家",
        "rednote_id": "485001334",
        "profile_url": "https://www.rednote.com/user/profile/5e60f69400000000010028b4",
        "style": "Dovetail puzzles, secret interlocking sliders"
    }
}
