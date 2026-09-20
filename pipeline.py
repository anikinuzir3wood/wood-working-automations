"""
Master Pipeline Orchestrator for TimberCraft Automation Engine
End-to-End Execution:
1. Video Ingestion / Download
2. AI Director Script & Human-Touch Directives
3. Studio Audio Engine (Edge-TTS baritone + Broadcast Mastering + Sidechain Ducking)
4. Human Touch Visual Engine (Blueprint HUD + Crop/Flip + Speed Ramps + Word-by-Word Captions)
5. Metadata & SEO Generation
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

from config import (
    SCRATCH_DIR, OUTPUT_DIR, AUDITED_ACCOUNTS,
    OPTIMAL_DURATION
)
from downloader import download_stream, probe_video
from video_analyzer import analyze_video_content
from director import ScriptDirector
from audio_engine import AudioEngine
from video_engine import VideoEngine
from metadata_engine import MetadataEngine


class TimberCraftPipeline:
    def __init__(self):
        self.scratch = SCRATCH_DIR
        self.output = OUTPUT_DIR
        self.director = ScriptDirector()
        self.audio_engine = AudioEngine()
        self.video_engine = VideoEngine()
        self.metadata_engine = MetadataEngine()

    def run(
        self,
        raw_video_path: Path,
        video_title: str = "The Impossible Joint",
        custom_plan: dict = None,
        extra_plan_flags: dict = None,
        video_analysis: dict = None
    ) -> Path:
        """Executes the full automated transformation on a raw video."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n================================================================================")
        print(f"[*] STARTING TIMBERCRAFT AUTOMATION PIPELINE [{timestamp}]")
        print(f"================================================================================\n")

        # 1. Probe Raw Footage
        info = probe_video(raw_video_path)
        print(f"[1/5] Raw Video Probed: {info['width']}x{info['height']}, {info['duration']:.1f}s, Codec: {info['codec']}")

        # 1b. Analyze Visual Content (Prioritize pre-computed queue analysis, fallback to live vision)
        if not video_analysis or not video_analysis.get("script_parts"):
            video_analysis = analyze_video_content(str(raw_video_path))
        else:
            print(f"[+] Using Pre-Computed Grounded Visual Analysis for '{video_analysis.get('object', 'Woodcraft')}'")

        if video_analysis.get("reject", False):
            reason = video_analysis.get("reject_reason", "Rejected by visual analysis")
            print(f"\n[!] VIDEO REJECTED: {reason}")
            raise ValueError(f"Content Rejected: {reason}")

        if video_analysis.get("has_foreign_captions", False):
            extra_plan_flags = extra_plan_flags or {}
            extra_plan_flags["has_foreign_captions"] = True

        # 2. Generate Director Script & Human Touch Directives
        plan = custom_plan or self.director.generate_short_plan(topic=video_title, video_analysis=video_analysis)
        # Merge any extra flags (e.g. has_foreign_captions) into plan
        if extra_plan_flags:
            plan.update(extra_plan_flags)
        print(f"[2/5] AI Director Plan Ready:")
        print(f"      - Title: {plan['title']}")
        print(f"      - Masthead: {plan['masthead_text']}")
        print(f"      - Rule of Silence Window: {plan['silence_window']['start']}s -> {plan['silence_window']['end']}s")
        print(f"      - Architectural HUD Overlays: {len(plan['hud_overlays'])} markers")

        # 3. Synthesize & Master Audio
        narration_file = self.scratch / f"narr_{timestamp}.wav"
        music_file = self.scratch / f"music_{timestamp}.wav"
        final_audio = self.scratch / f"master_audio_{timestamp}.wav"

        music_mood = plan.get("music_mood", "chisel_asmr")
        sub_niche = plan.get("sub_niche", "Traditional Woodworking")
        force_new_music = plan.get("force_new_music", False)

        print(f"[3/5] Audio Studio Synthesis:")
        narration_file, actual_segments = self.audio_engine.generate_narration_track(
            plan["narration_segments"],
            plan["target_duration"],
            narration_file,
            silence_window=plan.get("silence_window")
        )
        plan["narration_segments"] = actual_segments
        self.audio_engine.generate_acoustic_music_track(
            duration=plan["target_duration"],
            output_path=music_file,
            mood=music_mood,
            sub_niche=sub_niche,
            force_new=force_new_music
        )
        self.audio_engine.mix_master_audio(narration_file, music_file, plan["silence_window"], final_audio, plan["target_duration"])

        # 4. Synthesize Visuals with Human Touch
        out_video_name = f"TimberCraft_{timestamp}.mp4"
        final_video_path = self.output / out_video_name

        print(f"[4/5] Multi-Layer Visual Synthesis & Honest Thumbnail (FFmpeg):")
        self.video_engine.assemble_human_touch_short(raw_video_path, final_audio, plan, final_video_path)

        # Generate Custom High-CTR Honest Masthead Thumbnail (Part 4 of Blueprint)
        thumb_path = self.output / f"TimberCraft_{timestamp}_thumbnail.jpg"
        self.video_engine.generate_high_ctr_thumbnail(raw_video_path, plan, thumb_path)

        # 5. Generate SEO & YouTube Metadata
        meta_package = self.metadata_engine.generate_metadata(plan.get("title", video_title), video_analysis=video_analysis)
        meta_file = self.output / f"TimberCraft_{timestamp}_metadata.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta_package, f, indent=2, ensure_ascii=False)

        print(f"[5/5] SEO Metadata Package Generated: {meta_file}")
        print(f"\n================================================================================")
        print(f"[+] PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"- Final Master Short: {final_video_path}")
        print(f"- File Size: {final_video_path.stat().st_size / (1024*1024):.2f} MB")
        print(f"- Metadata: {meta_file}")
        print(f"================================================================================\n")

        return final_video_path


def main():
    parser = argparse.ArgumentParser(description="TimberCraft YouTube Shorts Automation Pipeline")
    parser.add_argument("--stream-url", type=str, help="Direct MP4 stream URL from Rednote/Xiaohongshu")
    parser.add_argument("--raw-file", type=str, help="Local path to raw MP4 file")
    parser.add_argument("--title", type=str, default="The Impossible Joint", help="Title theme")

    args = parser.parse_args()
    pipeline = TimberCraftPipeline()

    raw_path = None
    if args.raw_file:
        raw_path = Path(args.raw_file)
    elif args.stream_url:
        dl_path = SCRATCH_DIR / f"raw_download_{datetime.now().strftime('%H%M%S')}.mp4"
        raw_path = download_stream(args.stream_url, dl_path)
    else:
        # Default to the downloaded wood_soul video
        default_raw = SCRATCH_DIR / "raw_wood_soul.mp4"
        if default_raw.exists():
            raw_path = default_raw
        else:
            print("[!] No video provided. Use --stream-url or --raw-file.")
            sys.exit(1)

    pipeline.run(raw_path, video_title=args.title)


if __name__ == "__main__":
    main()
