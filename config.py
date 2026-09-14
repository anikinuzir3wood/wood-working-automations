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

# Voiceover Settings (ai33.pro Studio Narration -> Lawrence Cooper)
TTS_PROVIDER = "ai33"                   # Primary: ai33.pro studio voice
AI33_VOICE_ID = "clone_2647301"         # Lawrence Cooper
AI33_VOICE_NAME = "Lawrence Cooper"
AI33_TTS_SPEED = 1.0

# Edge-TTS Fallback (used only if ai33.pro connection fails)
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

# Google Drive Buffer & Archive Configuration
DRIVE_PARENT_FOLDER_ID = "1kl4GK0BsNJU6cOaDZUwM29l0jF-NRQj7"    # "YouTube Videos"
DRIVE_UPLOADED_FOLDER_ID = "15kewG_QMYHG59U-i336Ic4Q-1GMdI8RH"  # "Uploaded"
MIN_STOCK_THRESHOLD_VIDEOS = 6                                  # Minimum 3-day buffer (2 uploads/day)
TARGET_STOCK_BUFFER_VIDEOS = 60                                 # Up to 1-month buffer

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
    },
    "luban_craftsman": {
        "name": "鲁班工匠",
        "rednote_id": "941088219",
        "profile_url": "https://www.rednote.com/user/profile/5f9d10e000000000010051ba",
        "style": "Traditional Chinese architecture & Dougong temple brackets"
    },
    "sunmao_master": {
        "name": "榫卯大师",
        "rednote_id": "382910447",
        "profile_url": "https://www.rednote.com/user/profile/5d41c88100000000120155b9",
        "style": "Ancient locking tenons & friction furniture assembly"
    },
    "artisan_wood_lab": {
        "name": "手作木工坊",
        "rednote_id": "519283740",
        "profile_url": "https://www.rednote.com/user/profile/627f7a190000000021020721",
        "style": "Kumiko geometric lattice & precision hand-planing"
    },
    "heritage_joiner": {
        "name": "匠心传承",
        "rednote_id": "820194723",
        "profile_url": "https://www.rednote.com/user/profile/5e3b6aa80000000001006e23",
        "style": "Micro-chisel carving, rosewood mortise joints"
    },
    "zen_wood_asmr": {
        "name": "静心木工",
        "rednote_id": "671049281",
        "profile_url": "https://www.rednote.com/user/profile/631e8bb00000000012030f2c",
        "style": "No-talking, pure tool acoustic ASMR, plane shavings"
    },
    "classical_furniture": {
        "name": "古典家具榫卯",
        "rednote_id": "192847261",
        "profile_url": "https://www.rednote.com/user/profile/5f04a8b20000000001002df3",
        "style": "Traditional bed frame & chair corner joinery"
    },
    "woodcraft_decoded": {
        "name": "木艺解密",
        "rednote_id": "304918274",
        "profile_url": "https://www.rednote.com/user/profile/6198f791000000001002ec7d",
        "style": "Dissecting invisible sliding puzzle joints"
    }
}
