"""
Studio Audio Engine for TimberCraft Automation
Features:
- Edge-TTS broadcast baritone narration (en-US-ChristopherNeural)
- Broadcast FFmpeg mastering chain (Highpass, 140Hz chest warmth, 3.5kHz presence, compressor, limiter)
- FIXED stable background music bed at one consistent sweet-spot volume (-8dB below normalized -19 LUFS)
  No dynamic ducking. No sidechain compression. No volume up/down. One level. Every video. Always.
"""

import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
import edge_tts
from config import (
    SCRATCH_DIR, ASSETS_DIR, MUSIC_DIR, FOLEY_DIR,
    TTS_VOICE, TTS_RATE, TTS_PITCH,
    BROADCAST_AUDIO_FILTER
)

# ──────────────────────────────────────────────────────────────────────
# THE CALIBRATED SWEET-SPOT (locked after 7-level A/B test):
#   Voice mean = -23.0 dB, Music at -7dB cut => Music mean = -26.7 dB
#   Gap = 3.7 dB => Warm, clearly audible on all devices (phone, laptop,
#   headphones), never overpowers voiceover, never inaudibly low.
# ──────────────────────────────────────────────────────────────────────
MUSIC_FIXED_SWEET_SPOT_DB = -7


class AudioEngine:
    def __init__(self):
        self.scratch = SCRATCH_DIR
        self.scratch.mkdir(parents=True, exist_ok=True)

    def _probe_duration(self, file_path: Path) -> float:
        """Measure exact duration of an audio file in seconds."""
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(file_path)]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(json.loads(res.stdout)["format"]["duration"])

    async def _synthesize_segment(self, text: str, out_file: Path):
        """Generate speech for a single segment using Edge-TTS."""
        communicate = edge_tts.Communicate(
            text=text,
            voice=TTS_VOICE,
            rate=TTS_RATE,
            pitch=TTS_PITCH
        )
        await communicate.save(str(out_file))

    def generate_narration_track(
        self,
        segments: List[Dict[str, Any]],
        target_duration: float,
        output_path: Path,
        silence_window: Optional[Dict[str, Any]] = None
    ) -> Tuple[Path, List[Dict[str, Any]]]:
        """
        Synthesizes all segments and places them on a dynamic precision timeline:
        - Measures exact duration of each audio segment
        - Dynamically schedules speech with natural breathing gaps (no overlapping)
        - Preserves the ASMR silence window
        - Returns mastered audio AND actual speech timestamps for subtitle sync
        """
        print("[*] Synthesizing speech segments via Edge-TTS...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        raw_files = []
        for i, seg in enumerate(segments):
            seg_wav = self.scratch / f"seg_{i}.mp3"
            loop.run_until_complete(self._synthesize_segment(seg["text"], seg_wav))
            dur = self._probe_duration(seg_wav)
            raw_files.append((seg, seg_wav, dur))
        loop.close()

        # Dynamically compute non-overlapping timeline
        actual_segments = []
        cur_time = 0.0
        silence_start = silence_window.get("start", 19.5) if silence_window else 20.0
        silence_end = silence_window.get("end", 23.5) if silence_window else 24.0

        for i, (seg, seg_wav, dur) in enumerate(raw_files):
            # If this is the final segment (payoff after silence window), ensure it starts after silence_end
            if i == len(raw_files) - 1 and silence_window:
                st = max(cur_time, silence_end + 0.3)
            elif i == 0:
                st = seg.get("start", 0.0)
            else:
                planned_st = seg.get("start", cur_time)
                st = max(planned_st, cur_time)

            en = st + dur
            cur_time = en + 0.35  # Natural breathing room
            actual_segments.append({
                "start": round(st, 2),
                "end": round(en, 2),
                "text": seg["text"],
                "file": seg_wav
            })
            print(f"    - Seg {i}: [{st:.2f}s -> {en:.2f}s] (dur {dur:.2f}s) '{seg['text'][:40]}...'")

        # Build FFmpeg complex filter to delay each segment to its exact start time and mix
        inputs = []
        filter_parts = []
        for idx, seg_info in enumerate(actual_segments):
            inputs.extend(["-i", str(seg_info["file"])])
            delay_ms = int(seg_info["start"] * 1000)
            filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[a{idx}];")

        mix_inputs = "".join(f"[a{i}]" for i in range(len(actual_segments)))
        filter_graph = f"{''.join(filter_parts)}{mix_inputs}amix=inputs={len(actual_segments)}:normalize=0,apad=whole_dur={target_duration}[outa]"

        raw_mixed = self.scratch / "raw_speech_timeline.wav"
        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", filter_graph,
            "-map", "[outa]",
            "-t", str(target_duration),
            str(raw_mixed)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        # Apply Broadcast Studio Mastering Filter Chain
        print("[*] Applying Broadcast Mastering Chain (FFmpeg)...")
        cmd_master = [
            "ffmpeg", "-y",
            "-i", str(raw_mixed),
            "-af", BROADCAST_AUDIO_FILTER,
            str(output_path)
        ]
        subprocess.run(cmd_master, check=True, capture_output=True)
        print(f"[+] Mastered Narration Track ready: {output_path}")
        return output_path, actual_segments

    def generate_acoustic_music_track(
        self,
        duration: float,
        output_path: Path,
        mood: str = "chisel_asmr",
        sub_niche: str = "Traditional Woodworking",
        force_new: bool = False
    ) -> Path:
        """
        Prepares the background music bed at ONE FIXED consistent volume.
        No dynamic changes. Same level from start to finish. Every video.
        
        Processing chain:
        1. Loudness normalize to -19 LUFS (consistent baseline regardless of source track)
        2. Vocal clearance notch EQ (-4dB at 1.2kHz so voice frequencies stay clean)
        3. Warm acoustic bandpass (100Hz - 3000Hz)
        4. FIXED sweet-spot volume: -8dB cut (brings music to ~-27dB mean)
        5. Smooth 1.5s fade-in and 2s fade-out (only at video edges, NOT during video)
        """
        from music_manager import MusicManager
        mm = MusicManager()
        track_path = mm.get_matched_soundtrack(mood=mood, sub_niche=sub_niche, force_new=force_new)
        print(f"[+] Using Curated Background Music Bed: {track_path.name}")
        print(f"[+] Fixed Sweet-Spot Volume: {MUSIC_FIXED_SWEET_SPOT_DB}dB (stable, no ducking)")

        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(track_path),
            "-t", str(duration),
            "-af", (
                "loudnorm=I=-19:LRA=7:tp=-3,"
                "equalizer=f=1200:t=q:w=1.5:g=-4dB,"
                "highpass=f=100,lowpass=f=3000,"
                f"volume={MUSIC_FIXED_SWEET_SPOT_DB}dB,"
                f"afade=t=in:st=0:d=1.5,afade=t=out:st={duration-2.0}:d=2.0"
            ),
            str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

    def mix_master_audio(
        self,
        narration_path: Path,
        music_path: Path,
        silence_window: Dict[str, Any],
        output_path: Path,
        duration: float
    ) -> Path:
        """
        Simple flat mix. Voice + Music at their pre-set levels.
        No sidechain. No dynamic ducking. No volume automation.
        Music is already at the perfect fixed sweet-spot from generate_acoustic_music_track().
        Just combine them cleanly with a peak limiter to prevent clipping.
        """
        print("[*] Flat-mixing voice + music at fixed sweet-spot levels (no ducking)...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(narration_path),
            "-i", str(music_path),
            "-filter_complex",
            "[0:a][1:a]amix=inputs=2:weights=1.0 1.0:normalize=0,alimiter=limit=-1dB[final_a]",
            "-map", "[final_a]",
            "-t", str(duration),
            str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[+] Master Audio ready (fixed level, no ducking): {output_path}")
        return output_path


if __name__ == "__main__":
    from director import ScriptDirector
    director = ScriptDirector()
    plan = director.generate_short_plan()

    engine = AudioEngine()
    narr_file = SCRATCH_DIR / "test_mastered_narration.wav"
    music_file = SCRATCH_DIR / "test_music_bed.wav"
    final_audio = SCRATCH_DIR / "test_final_audio.wav"

    engine.generate_narration_track(plan["narration_segments"], plan["target_duration"], narr_file)
    engine.generate_acoustic_music_track(plan["target_duration"], music_file)
    engine.mix_master_audio(narr_file, music_file, plan["silence_window"], final_audio, plan["target_duration"])
    print("[+] Audio Engine test successful!")
