"""
AI Director Module for TimberCraft Automation
Generates high-retention narration scripts, timing cues, and "Human Touch" directives.
CRITICAL MANDATE:
- Uses ONLY ULTRA-SIMPLE, plain English words (Grade 4 level).
- NO difficult or pretentious jargon (banned: tolerances, microscopic, fiber severance, surgical discipline, unwavering patience).
- Strictly matches the actual physical video action visible on screen.
- Supports Gemini Vision analysis when available for 100% grounded narration.
"""

from typing import Dict, Any, List, Optional
import re


def sanitize_english_text(text: str, fallback: str = "Traditional Woodcraft") -> str:
    """Removes all Chinese/CJK characters, Chinese social tags, and cleans whitespace."""
    if not text:
        return fallback
    # Strip bracketed tags like [话题], [标签], [视频], etc.
    cleaned = re.sub(r'\[.*?\]', '', text)
    # Strip all Chinese/CJK characters
    cleaned = re.sub(r'[\u4e00-\u9fff]+', '', cleaned)
    # Clean hashtags and whitespace
    cleaned = re.sub(r'#\s*#', '#', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if len(cleaned) < 3 or not any(c.isalpha() for c in cleaned):
        return fallback
    return cleaned


class ScriptDirector:
    def __init__(self):
        pass

    def generate_vision_grounded_plan(self, topic: str, analysis: Dict[str, Any], target_duration: Optional[float] = None) -> Dict[str, Any]:
        """Builds a customized short plan directly from Gemini Vision frame analysis scaling to full raw video length."""
        raw_obj = analysis.get("object", "")
        clean_obj = sanitize_english_text(raw_obj, fallback="Traditional Woodcraft")
        
        raw_clean_topic = topic.replace("#Shorts", "").strip()
        clean_topic = sanitize_english_text(raw_clean_topic, fallback=clean_obj)
        if clean_topic.lower() in ["traditional woodcraft", "master craftsmanship", "shorts"] and clean_obj:
            clean_topic = f"The Hand-Crafted {clean_obj}"

        masthead = clean_obj.upper()
        if len(masthead) > 26:
            masthead = masthead[:23] + "..."

        # Determine full video duration (allow full raw length up to YouTube Shorts 180s limit)
        dur = target_duration or analysis.get("duration") or 32.0
        dur = min(max(float(dur), 15.0), 180.0)
        dur = round(dur, 1)

        parts = analysis.get("script_parts", [])
        if len(parts) < 4:
            return self.generate_dynamic_craft_plan(topic, target_duration=dur)

        final_title = f"{clean_topic} #Shorts" if not clean_topic.endswith("#Shorts") else clean_topic

        # Dynamically distribute speech, silence window, and HUD across full duration
        t_hook = 0.0
        t_action = round(dur * 0.18, 1)
        t_assembly = round(dur * 0.45, 1)
        t_silence_start = round(dur * 0.72, 1)
        t_silence_dur = max(3.0, min(6.0, round(dur * 0.09, 1)))  # 3s to 6s pure ASMR window
        t_silence_end = round(t_silence_start + t_silence_dur, 1)
        if t_silence_end >= dur - 2.5:
            t_silence_end = round(dur - 3.0, 1)
            t_silence_start = round(t_silence_end - 3.0, 1)
        t_reveal = round(t_silence_end + 0.4, 1)

        return {
            "title": final_title,
            "masthead_text": masthead,
            "target_duration": dur,
            "narration_segments": [
                {"start": t_hook, "end": round(t_action - 0.5, 1), "text": parts[0]},
                {"start": t_action, "end": round(t_assembly - 0.5, 1), "text": parts[1]},
                {"start": t_assembly, "end": round(t_silence_start - 0.5, 1), "text": parts[2]},
                {"start": t_reveal, "end": round(dur - 0.2, 1), "text": parts[3]}
            ],
            "silence_window": {
                "start": t_silence_start,
                "end": t_silence_end,
                "reason": "Climax pay-off: Pure acoustic wood joinery ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": round(t_action, 1),
                    "title": "TRADITIONAL WOODCRAFT",
                    "specs": ["Design: ZERO NAILS", "Method: 100% WOOD"]
                },
                {
                    "start": round(t_action + 0.5, 1),
                    "end": round(t_assembly, 1),
                    "title": "CORNER INTERLOCK",
                    "specs": ["Joint: SLIDE & LOCK", "Fit: CLEAN WOOD"]
                },
                {
                    "start": round(t_assembly + 0.5, 1),
                    "end": round(t_silence_start, 1),
                    "title": "SOLID FRAME",
                    "specs": ["Holding: PURE FRICTION", "Strength: HEIRLOOM"]
                },
                {
                    "start": round(t_reveal, 1),
                    "end": round(dur - 0.3, 1),
                    "title": "FINISHED PIECE",
                    "specs": ["Quality: LIFETIME BUILD", "Craft: MASTER HAND"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": t_action, "speed": 1.0, "label": "Opening"},
                {"start": t_action, "end": t_assembly, "speed": 1.0, "label": "Interlocking action"},
                {"start": t_assembly, "end": t_silence_start, "speed": 1.0, "label": "Locking"},
                {"start": t_silence_start, "end": t_silence_end, "speed": 1.0, "label": "ASMR lock"},
                {"start": t_silence_end, "end": dur, "speed": 1.0, "label": "Full reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Traditional Woodworking",
            "force_new_music": False
        }

    def generate_bed_frame_joint_plan(self) -> Dict[str, Any]:
        """Plan for bed frame corner joinery (matching traditional rosewood bed assembly)."""
        return {
            "title": "The Zero-Nail Bed Frame Joint #Shorts",
            "masthead_text": "ZERO-NAIL BED JOINT",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Look at how this entire wooden bed is built without a single nail or screw."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Two side rails slide straight into the corner post through clean, hand-cut slots."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "The wood hooks together so tightly that the weight of the bed locks it right in place..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "giving you a rock-solid bed built to last for generations. No wobble, no screws, just pure wood."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Solid wood joint seating ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "BED FRAME CORNER",
                    "specs": ["Joint: 3-WAY SUNMAO", "Hardware: ZERO NAILS"]
                },
                {
                    "start": 6.0,
                    "end": 12.0,
                    "title": "SLIDING RAILS",
                    "specs": ["Timber: ROSEWOOD", "Connection: HAND-CUT"]
                },
                {
                    "start": 13.0,
                    "end": 18.5,
                    "title": "SELF-LOCKING WEIGHT",
                    "specs": ["Strength: INTERLOCKING", "Hold: LIFETIME"]
                },
                {
                    "start": 24.0,
                    "end": 29.5,
                    "title": "FINISHED BED",
                    "specs": ["Design: SOLID WOOD", "Durability: HEIRLOOM"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Opening"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Rails slide"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Locking"},
                {"start": 19.0, "end": 23.5, "speed": 1.0, "label": "Pure ASMR tap"},
                {"start": 23.5, "end": 31.5, "speed": 1.0, "label": "Bed reveal"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Classical Chinese Furniture",
            "force_new_music": False
        }

    def generate_marking_gauge_plan(self) -> Dict[str, Any]:
        """Plan for layout, marking gauge, and measuring accuracy."""
        return {
            "title": "The Master Carpenter's Marking Trick #Shorts",
            "masthead_text": "CLEAN LINE LAYOUT",
            "target_duration": 31.8,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.5,
                    "text": "Before you cut any wood, you must start with a clean, straight line."
                },
                {
                    "start": 6.0,
                    "end": 13.8,
                    "text": "Watch this brass pin glide across the wood, cutting a tiny line instead of using a pencil."
                },
                {
                    "start": 14.2,
                    "end": 22.0,
                    "text": "A pencil mark is too wide, but this small cut gives the hand saw an exact track to follow..."
                },
                {
                    "start": 26.5,
                    "end": 31.5,
                    "text": "so when you make the cut, both pieces fit together with zero gaps. Perfect every time."
                }
            ],
            "silence_window": {
                "start": 22.2,
                "end": 26.2,
                "reason": "Climax pay-off: Pure acoustic wood scoring & gauge sliding ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "LAYOUT LINE",
                    "specs": ["Tool: HARDWOOD GAUGE", "Guide: SHARP PIN"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "CLEAN CUT",
                    "specs": ["Pin: BRASS TIP", "Action: KNIFE SCORE"]
                },
                {
                    "start": 14.5,
                    "end": 21.5,
                    "title": "SAW TRACK",
                    "specs": ["Groove: PHYSICAL GUIDE", "Square: 90.0 TRUE"]
                },
                {
                    "start": 26.5,
                    "end": 31.0,
                    "title": "ZERO GAP FIT",
                    "specs": ["Result: TIGHT JOINT", "Grade: MASTER BUILD"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Gauge contact"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Smooth scoring stroke"},
                {"start": 14.0, "end": 22.0, "speed": 0.95, "label": "Knife line detail"},
                {"start": 22.0, "end": 26.5, "speed": 1.0, "label": "Pure ASMR sliding payoff"},
                {"start": 26.5, "end": 31.8, "speed": 1.0, "label": "Clean fit showcase"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Precision Woodworking Layout",
            "force_new_music": False
        }

    def generate_kumiko_plan(self) -> Dict[str, Any]:
        """Plan for Kumiko lattice joinery."""
        return {
            "title": "The Zero-Nail Japanese Kumiko Joint #Shorts",
            "masthead_text": "ZERO-NAIL KUMIKO LATTICE",
            "target_duration": 33.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "Look at how all these tiny wooden strips fit together without any glue or nails."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Each piece is cut by hand with a sharp hand plane so the angles match exactly."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "Watch them slide into place. The pieces fit so snug that friction holds the whole pattern together..."
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "text": "Hear that little snap? That means it is locked in tight, creating a beautiful wooden grid."
                }
            ],
            "silence_window": {
                "start": 22.2,
                "end": 26.8,
                "reason": "Climax pay-off: Pure wood friction click & snap ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "KUMIKO GRID",
                    "specs": ["Style: JAPANESE LATTICE", "Hardware: ZERO NAILS"]
                },
                {
                    "start": 7.0,
                    "end": 14.0,
                    "title": "HAND PLANE CUT",
                    "specs": ["Angle: 60.0 DEGREE", "Tool: SHARP KANNA"]
                },
                {
                    "start": 15.0,
                    "end": 22.0,
                    "title": "SNUG FIT",
                    "specs": ["Hold: WOOD FRICTION", "Fit: ZERO PLAY"]
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "title": "FINISHED PATTERN",
                    "specs": ["Pattern: STAR LATTICE", "Art: HANDMADE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Lattice overview"},
                {"start": 6.0, "end": 14.5, "speed": 1.0, "label": "Shaving angles"},
                {"start": 14.5, "end": 22.2, "speed": 0.95, "label": "Careful slotting"},
                {"start": 22.2, "end": 27.0, "speed": 1.0, "label": "Pure ASMR snap"},
                {"start": 27.0, "end": 33.5, "speed": 1.0, "label": "Full lattice reveal"}
            ],
            "music_mood": "kumiko_lattice",
            "sub_niche": "Japanese Kumiko Lattice",
            "force_new_music": False
        }

    def generate_sunmao_mortise_plan(self) -> Dict[str, Any]:
        """Plan for traditional Sunmao mortise and tenon joinery."""
        return {
            "title": "The Ancient No-Nail Wood Joint #Shorts",
            "masthead_text": "ANCIENT SUNMAO JOINT",
            "target_duration": 31.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Watch these two pieces of wood lock together without nails or glue."
                },
                {
                    "start": 5.0,
                    "end": 12.0,
                    "text": "One piece has a hole cut inside, and the other piece has a matching wooden peg."
                },
                {
                    "start": 12.5,
                    "end": 19.5,
                    "text": "When they slide together, the wood fits so tight that they clamp each other in place..."
                },
                {
                    "start": 24.5,
                    "end": 30.5,
                    "text": "making a joint that will stay strong for hundreds of years. The beauty of real woodwork."
                }
            ],
            "silence_window": {
                "start": 20.0,
                "end": 24.0,
                "reason": "Climax pay-off: Wood mallet tap & acoustic seat ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "SUNMAO CRAFT",
                    "specs": ["Origin: ANCIENT CHINA", "Nails: ZERO"]
                },
                {
                    "start": 6.0,
                    "end": 12.0,
                    "title": "PEG & SLOT",
                    "specs": ["Cut: HAND CHISEL", "Type: MORTISE TENON"]
                },
                {
                    "start": 13.0,
                    "end": 19.5,
                    "title": "TIGHT CLAMP",
                    "specs": ["Hold: WOOD GRAIN", "Strength: ROCK SOLID"]
                },
                {
                    "start": 25.0,
                    "end": 30.5,
                    "title": "FINISHED FIT",
                    "specs": ["Life: GENERATIONS", "Seam: SEAMLESS"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Joint overview"},
                {"start": 5.0, "end": 12.5, "speed": 1.0, "label": "Alignment"},
                {"start": 12.5, "end": 20.0, "speed": 0.95, "label": "Sliding home"},
                {"start": 20.0, "end": 24.5, "speed": 1.0, "label": "Pure ASMR tap"},
                {"start": 24.5, "end": 31.0, "speed": 1.0, "label": "Locked joint"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Ancient Sunmao Joinery",
            "force_new_music": False
        }

    def generate_puzzle_lock_plan(self) -> Dict[str, Any]:
        """Plan for secret puzzle locks, Luban locks, and slider joints."""
        return {
            "title": "The Secret Wooden Puzzle Box #Shorts",
            "masthead_text": "SECRET WOOD PUZZLE",
            "target_duration": 31.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Can you guess how this wooden secret puzzle opens?"
                },
                {
                    "start": 5.0,
                    "end": 12.0,
                    "text": "At first it looks like a solid block of wood with no seams. But push the first sliding piece..."
                },
                {
                    "start": 12.5,
                    "end": 19.0,
                    "text": "and the hidden tracks inside begin to move, unlocking the next piece one by one..."
                },
                {
                    "start": 24.0,
                    "end": 30.5,
                    "text": "until the whole puzzle opens right up. Pure wood magic with zero metal parts."
                }
            ],
            "silence_window": {
                "start": 19.5,
                "end": 23.5,
                "reason": "Climax pay-off: Tactile sliding wood clicking ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "WOOD PUZZLE",
                    "specs": ["Type: LUBAN LOCK", "Metal: ZERO"]
                },
                {
                    "start": 6.0,
                    "end": 12.0,
                    "title": "HIDDEN SLIDERS",
                    "specs": ["Mechanism: WOOD TRACKS", "Fit: INVISIBLE"]
                },
                {
                    "start": 13.0,
                    "end": 19.0,
                    "title": "STEP UNLOCK",
                    "specs": ["Code: PHYSICAL KEYS", "Action: SMOOTH SLIDE"]
                },
                {
                    "start": 24.5,
                    "end": 30.5,
                    "title": "BOX OPEN",
                    "specs": ["Secret: REVEALED", "Craft: 100% TIMBER"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Solid block view"},
                {"start": 5.0, "end": 12.5, "speed": 1.0, "label": "First slide"},
                {"start": 12.5, "end": 19.5, "speed": 0.95, "label": "Track unlocking"},
                {"start": 19.5, "end": 24.0, "speed": 1.0, "label": "Pure ASMR slide"},
                {"start": 24.0, "end": 31.0, "speed": 1.0, "label": "Open reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Chinese Puzzle Box Joinery",
            "force_new_music": False
        }

    def generate_hand_plane_shaving_plan(self) -> Dict[str, Any]:
        """Plan for hand plane shaving ASMR."""
        return {
            "title": "The Paper-Thin Wood Shaving Trick #Shorts",
            "masthead_text": "RAZOR PLANE SHAVING",
            "target_duration": 30.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Listen to this sharp hand plane glide across the wood."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "The blade is so sharp it does not scratch or tear. It cuts thin wood ribbons like paper."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "See how the wood ribbon peels off in one piece, so clear you can see right through it..."
                },
                {
                    "start": 23.5,
                    "end": 29.5,
                    "text": "leaving the wood smooth as glass without using any sandpaper at all."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Pure acoustic plane hiss & wood shaving ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "HAND PLANE",
                    "specs": ["Tool: WOOD PLANE", "Blade: RAZOR SHARP"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "CLEAN SHAVE",
                    "specs": ["Action: SMOOTH SLICE", "Tear: ZERO"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "PAPER THIN",
                    "specs": ["Thickness: SEE THROUGH", "Ribbon: FULL LENGTH"]
                },
                {
                    "start": 24.0,
                    "end": 29.5,
                    "title": "GLASS SMOOTH",
                    "specs": ["Sandpaper: ZERO USED", "Finish: PURE WOOD"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Plane contact"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Long shaving stroke"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Translucent ribbon"},
                {"start": 19.0, "end": 23.5, "speed": 1.0, "label": "Pure ASMR plane hiss"},
                {"start": 23.5, "end": 30.0, "speed": 1.0, "label": "Mirror wood finish"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Master Hand Plane ASMR",
            "force_new_music": False
        }

    def generate_dovetail_joint_plan(self) -> Dict[str, Any]:
        """Plan for classic hand-cut dovetail joinery."""
        return {
            "title": "The Perfect Hand-Cut Dovetail Joint #Shorts",
            "masthead_text": "HAND-CUT DOVETAIL",
            "target_duration": 30.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Look at how these wooden dovetail cuts fit together."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Each wooden notch is shaped like a fan, so once they slide in, they can never pull apart."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "Watch the two boards meet. The fit is so tight you cannot even see the line where they join..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "locking both sides together forever. Simple cuts that make the strongest boxes."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Wood mallet tapping pins into tails ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "DOVETAIL JOINT",
                    "specs": ["Joint: PINS & TAILS", "Cut: HAND CHISELED"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "FAN SHAPE",
                    "specs": ["Design: ANGLE WEDGES", "Pull: CANNOT SEPARATE"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "ZERO SEAM",
                    "specs": ["Fit: TIGHT GRAIN", "Gap: ZERO"]
                },
                {
                    "start": 24.0,
                    "end": 30.0,
                    "title": "SOLID BOX",
                    "specs": ["Strength: LIFETIME", "Hardware: ZERO"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Dovetail pins"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Aligning wedge"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Pins slide in"},
                {"start": 19.0, "end": 23.5, "speed": 1.0, "label": "Pure ASMR tap"},
                {"start": 23.5, "end": 30.5, "speed": 1.0, "label": "Solid locked corner"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Handmade Dovetail Joinery",
            "force_new_music": False
        }

    def generate_corner_tenon_plan(self) -> Dict[str, Any]:
        """Plan for corner tenon and structural framing assembly."""
        return {
            "title": "The Master Wood Corner Assembly #Shorts",
            "masthead_text": "CORNER TENON ASSEMBLY",
            "target_duration": 31.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Watch this corner joint slide together without a single nail or screw."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Every side of this joint is cut by hand to line up square and true."
                },
                {
                    "start": 12.0,
                    "end": 19.0,
                    "text": "As the pieces slide into place, the wood presses together tight..."
                },
                {
                    "start": 24.0,
                    "end": 30.5,
                    "text": "locking into a solid corner that will never pull apart. Simple, strong, and built to last."
                }
            ],
            "silence_window": {
                "start": 19.5,
                "end": 23.5,
                "reason": "Climax pay-off: Deep wood frame seating & mallet resonance ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "FRAME CORNER",
                    "specs": ["Joint: 90 DEGREE SQUARE", "Hardware: ZERO"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "HAND CUT",
                    "specs": ["Method: CHISEL & SAW", "Angle: TRUE SQUARE"]
                },
                {
                    "start": 12.5,
                    "end": 19.0,
                    "title": "TIGHT SLIDE",
                    "specs": ["Fit: SNUG FIT", "Hold: WOOD COMPRESSION"]
                },
                {
                    "start": 24.5,
                    "end": 30.5,
                    "title": "LOCKED FRAME",
                    "specs": ["Durability: HEIRLOOM", "Strength: ROCK SOLID"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Corner view"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Slow alignment"},
                {"start": 12.0, "end": 19.5, "speed": 0.95, "label": "Sliding home"},
                {"start": 19.5, "end": 24.0, "speed": 1.0, "label": "Pure ASMR mallet tap"},
                {"start": 24.0, "end": 31.0, "speed": 1.0, "label": "Completed corner"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Traditional Timber Framing",
            "force_new_music": False
        }

    def generate_dougong_plan(self) -> Dict[str, Any]:
        """Plan for ancient Dougong temple bracket joinery."""
        return {
            "title": "The Temple Roof Bracket That Beat Earthquakes #Shorts",
            "masthead_text": "ANCIENT DOUGONG BRACKET",
            "target_duration": 34.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "This wooden roof bracket is how ancient temples survived big earthquakes for a thousand years."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Built with stacked wooden blocks, they hold up massive roofs without using a single nail or bolt."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "When the ground shakes, the wooden blocks bend and slide just enough to absorb the shock..."
                },
                {
                    "start": 27.0,
                    "end": 33.5,
                    "text": "protecting the entire building from falling down. Genius building skills made only from wood."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Deep temple gong resonance & wooden interlocking ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "DOUGONG BRACKET",
                    "specs": ["Origin: ANCIENT TEMPLE", "Fasteners: ZERO"]
                },
                {
                    "start": 7.0,
                    "end": 14.0,
                    "title": "STACKED WOOD",
                    "specs": ["Blocks: INTERLOCKING", "Load: MASSIVE ROOF"]
                },
                {
                    "start": 15.0,
                    "end": 22.0,
                    "title": "EARTHQUAKE PROOF",
                    "specs": ["Action: SHOCK ABSORB", "Flex: WOOD FRICTION"]
                },
                {
                    "start": 27.0,
                    "end": 33.5,
                    "title": "STANDING STRONG",
                    "specs": ["History: 1000+ YEARS", "Result: ZERO DAMAGE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Temple bracket"},
                {"start": 6.0, "end": 14.5, "speed": 1.0, "label": "Stacking blocks"},
                {"start": 14.5, "end": 22.5, "speed": 0.95, "label": "Interlocking flex"},
                {"start": 22.5, "end": 27.0, "speed": 1.0, "label": "Pure acoustic gong ASMR"},
                {"start": 27.0, "end": 34.0, "speed": 1.0, "label": "Completed temple structure"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Ancient Chinese Architecture",
            "force_new_music": False
        }

    def generate_end_grain_sharpness_plan(self) -> Dict[str, Any]:
        """Plan for chisel sharpness end-grain cutting test."""
        return {
            "title": "The Razor Chisel End-Grain Test #Shorts",
            "masthead_text": "CHISEL SHARPNESS TEST",
            "target_duration": 33.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "Cutting the end of a wood block is the hardest test for any sharp tool."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "If the blade was even a little bit dull, it would crush the wood and leave rough marks."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "Instead, look at this chisel slice straight through the wood like it was soft butter..."
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "text": "peeling off a paper-thin curl and leaving the surface smooth as glass. That is real sharpness."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Crisp end-grain shearing hiss ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "END GRAIN TEST",
                    "specs": ["Hardness: MAXIMUM", "Test: RAZOR SHARP"]
                },
                {
                    "start": 7.0,
                    "end": 14.0,
                    "title": "RAZOR BLADE",
                    "specs": ["Steel: HAND FORGED", "Edge: ZERO DULL"]
                },
                {
                    "start": 15.0,
                    "end": 22.0,
                    "title": "BUTTER CUT",
                    "specs": ["Action: CLEAN SLICE", "Resistance: ZERO"]
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "title": "GLASS FINISH",
                    "specs": ["Surface: MIRROR SMOOTH", "Quality: RAZOR EDGE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Chisel approach"},
                {"start": 6.0, "end": 14.5, "speed": 1.0, "label": "Entering end grain"},
                {"start": 14.5, "end": 22.5, "speed": 0.95, "label": "Smooth shear"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR slice hiss"},
                {"start": 26.5, "end": 33.5, "speed": 1.0, "label": "Glass surface reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Chisel Sharpness & Metallurgy",
            "force_new_music": False
        }

    def generate_table_leg_joint_plan(self) -> Dict[str, Any]:
        """Plan for 3-way table leg interlocking joinery."""
        return {
            "title": "The Three-Way Table Leg Joint #Shorts",
            "masthead_text": "3-WAY TABLE LEG JOINT",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "This three-way wood joint is how strong tables are built without nails or screws."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Two rails and one upright leg all meet at the exact same corner, fitting like puzzle pieces."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "Watch how each piece locks the other in place. The heavier the table gets, the tighter it holds..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "making a rock-solid table that never shakes. Real woodworking that lasts forever."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Solid wood mallet seating tap ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "TABLE CORNER",
                    "specs": ["Pieces: 3-WAY INTERLOCK", "Nails: ZERO"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "PUZZLE NOTCH",
                    "specs": ["Cut: HAND CRAFTED", "Fit: MATCHING SLOTS"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "WEIGHT LOCK",
                    "specs": ["Load: TIGHTENS JOINT", "Wobble: ZERO"]
                },
                {
                    "start": 24.0,
                    "end": 30.0,
                    "title": "SOLID TABLE",
                    "specs": ["Strength: UNBREAKABLE", "Build: LIFETIME"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "3 pieces view"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Sliding together"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Corner interlock"},
                {"start": 19.0, "end": 23.5, "speed": 1.0, "label": "Pure ASMR tap"},
                {"start": 23.5, "end": 31.5, "speed": 1.0, "label": "Solid table leg"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Classical Chinese Furniture",
            "force_new_music": False
        }

    def generate_locking_mortise_dissection_plan(self) -> Dict[str, Any]:
        """Plan for hidden locking mortise joints."""
        return {
            "title": "The Secret Hidden Wood Joint #Shorts",
            "masthead_text": "HIDDEN LOCKING JOINT",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Let us open up this wooden joint to see what is hidden inside."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "From the outside it looks like a plain block of wood. But when you slide the center pin out..."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "you can see the inside cut has a secret lock that hooks both pieces together..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "holding so tight it can never pull loose. A clever secret hidden right inside the wood."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Tactile sliding wood friction ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "HIDDEN JOINT",
                    "specs": ["Look: PLAIN BLOCK", "Inside: SECRET LOCK"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "CENTER PIN",
                    "specs": ["Key: WOODEN SLIDER", "Action: UNLOCK"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "INSIDE HOOK",
                    "specs": ["Cut: SECRET NOTCH", "Hold: LOCKED TIGHT"]
                },
                {
                    "start": 24.0,
                    "end": 30.0,
                    "title": "INGENIOUS CRAFT",
                    "specs": ["Metal: ZERO USED", "Craft: 100% TIMBER"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Solid block"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Slide pin out"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Inside secret"},
                {"start": 19.0, "end": 23.5, "speed": 1.0, "label": "Pure ASMR slide"},
                {"start": 23.5, "end": 31.5, "speed": 1.0, "label": "Revealed mechanism"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Traditional Woodworking",
            "force_new_music": False
        }

    def generate_dynamic_craft_plan(self, topic: str, target_duration: Optional[float] = None) -> Dict[str, Any]:
        """Dynamic plan synthesizer for any custom woodworking topic scaling to full raw video length."""
        raw_clean = topic.replace("#Shorts", "").strip()
        clean_topic = sanitize_english_text(raw_clean, fallback="Traditional Woodcraft")
        masthead = clean_topic.upper()
        if len(masthead) > 26:
            masthead = masthead[:23] + "..."

        dur = target_duration or 32.0
        dur = min(max(float(dur), 15.0), 180.0)
        dur = round(dur, 1)

        t_hook = 0.0
        t_action = round(dur * 0.18, 1)
        t_assembly = round(dur * 0.45, 1)
        t_silence_start = round(dur * 0.72, 1)
        t_silence_dur = max(3.0, min(6.0, round(dur * 0.09, 1)))
        t_silence_end = round(t_silence_start + t_silence_dur, 1)
        if t_silence_end >= dur - 2.5:
            t_silence_end = round(dur - 3.0, 1)
            t_silence_start = round(t_silence_end - 3.0, 1)
        t_reveal = round(t_silence_end + 0.4, 1)

        return {
            "title": f"{clean_topic} #Shorts",
            "masthead_text": masthead,
            "target_duration": dur,
            "narration_segments": [
                {
                    "start": t_hook,
                    "end": round(t_action - 0.5, 1),
                    "text": "In traditional woodworking, building by hand takes time and steady hands."
                },
                {
                    "start": t_action,
                    "end": round(t_assembly - 0.5, 1),
                    "text": "Every cut is made to follow the natural grain of the wood, with zero nails and zero screws."
                },
                {
                    "start": t_assembly,
                    "end": round(t_silence_start - 0.5, 1),
                    "text": "Watch closely as the woodworker fits the pieces together by hand, making sure every corner is flush..."
                },
                {
                    "start": t_reveal,
                    "end": round(dur - 0.2, 1),
                    "text": "giving you a clean, solid piece of woodwork that will last a lifetime. That is true craft."
                }
            ],
            "silence_window": {
                "start": t_silence_start,
                "end": t_silence_end,
                "reason": "Climax pay-off: Pure acoustic craftsman hands ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": round(t_action, 1),
                    "title": "MASTER WORK",
                    "specs": ["Craft: TRADITIONAL WOODCRAFT", "Method: 100% MANUAL"]
                },
                {
                    "start": round(t_action + 0.5, 1),
                    "end": round(t_assembly, 1),
                    "title": "GRAIN DYNAMICS",
                    "specs": ["Surface: HAND FINISHED", "Nails: ZERO"]
                },
                {
                    "start": round(t_assembly + 0.5, 1),
                    "end": round(t_silence_start, 1),
                    "title": "CLEAN FIT",
                    "specs": ["Fit: FLUSH EDGES", "Seam: TIGHT"]
                },
                {
                    "start": round(t_reveal, 1),
                    "end": round(dur - 0.3, 1),
                    "title": "FINAL REVEAL",
                    "specs": ["Quality: LIFETIME BUILD", "Grade: HEIRLOOM"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": t_action, "speed": 1.0, "label": "Opening craft"},
                {"start": t_action, "end": t_assembly, "speed": 1.0, "label": "Detailed work"},
                {"start": t_assembly, "end": t_silence_start, "speed": 1.0, "label": "Fitting together"},
                {"start": t_silence_start, "end": t_silence_end, "speed": 1.0, "label": "Pure ASMR payoff"},
                {"start": t_silence_end, "end": dur, "speed": 1.0, "label": "Finished reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Traditional Woodworking",
            "force_new_music": False
        }

    def _scale_plan_to_duration(self, plan: Dict[str, Any], target_duration: Optional[float]) -> Dict[str, Any]:
        """Ensures any selected plan (template or dynamic) matches target_duration across all timing cues."""
        if not target_duration:
            return plan

        dur = min(max(float(target_duration), 15.0), 180.0)
        dur = round(dur, 1)
        orig_dur = float(plan.get("target_duration", 32.0))
        if abs(orig_dur - dur) < 0.2:
            plan["target_duration"] = dur
            return plan

        scale = dur / orig_dur if orig_dur > 0 else 1.0
        plan["target_duration"] = dur

        # Scale narration segments
        if "narration_segments" in plan:
            scaled_segs = []
            for seg in plan["narration_segments"]:
                st = round(seg["start"] * scale, 1)
                en = round(min(seg["end"] * scale, dur - 0.2), 1)
                scaled_segs.append({"start": st, "end": en, "text": seg["text"]})
            plan["narration_segments"] = scaled_segs

        # Scale silence window
        if "silence_window" in plan and isinstance(plan["silence_window"], dict):
            sw = plan["silence_window"]
            st = round(sw.get("start", 22.0) * scale, 1)
            en = round(sw.get("end", 26.0) * scale, 1)
            if en >= dur - 2.5:
                en = round(dur - 3.0, 1)
                st = round(en - 3.5, 1)
            plan["silence_window"] = {
                "start": max(0.0, st),
                "end": max(st + 2.0, en),
                "reason": sw.get("reason", "Climax pay-off: Pure acoustic wood joinery ASMR")
            }

        # Scale HUD overlays
        if "hud_overlays" in plan:
            scaled_huds = []
            for hud in plan["hud_overlays"]:
                st = round(hud["start"] * scale, 1)
                en = round(min(hud["end"] * scale, dur - 0.2), 1)
                scaled_huds.append({
                    "start": st,
                    "end": en,
                    "title": hud.get("title", "MASTER WORK"),
                    "specs": hud.get("specs", [])
                })
            plan["hud_overlays"] = scaled_huds

        # Scale speed ramps
        if "speed_ramps" in plan:
            scaled_ramps = []
            for ramp in plan["speed_ramps"]:
                st = round(ramp["start"] * scale, 1)
                en = round(min(ramp["end"] * scale, dur), 1)
                scaled_ramps.append({
                    "start": st,
                    "end": en,
                    "speed": ramp.get("speed", 1.0),
                    "label": ramp.get("label", "Craft")
                })
            plan["speed_ramps"] = scaled_ramps

        return plan

    def generate_short_plan(self, topic: str = "end_grain", video_analysis: Dict[str, Any] = None, target_duration: Optional[float] = None) -> Dict[str, Any]:
        """
        Dynamically selects or synthesizes a plan matching the specific video.
        If video_analysis is provided from Gemini Vision, grounds narration
        directly in what is actually visible on screen with simple words.
        Scales plan duration to the exact length of the raw video (up to 180s).
        """
        # 0. Vision-grounded priority: If video analysis provided 4 simple script parts, use them!
        if video_analysis and video_analysis.get("script_parts"):
            return self.generate_vision_grounded_plan(topic, video_analysis, target_duration=target_duration)

        t = (topic or "").lower()

        # 1. Bed frame joint / corner post (checked first for bed/furniture assembly)
        if any(w in t for w in ["bed", "bed frame", "corner assembly"]):
            plan = self.generate_bed_frame_joint_plan()
        elif any(w in t for w in ["dissect", "hidden", "internal", "拆解"]):
            plan = self.generate_locking_mortise_dissection_plan()
        elif any(w in t for w in ["table leg", "legjoint", "leg"]):
            plan = self.generate_table_leg_joint_plan()
        elif any(w in t for w in ["puzzle", "lock", "鲁班锁", "secret", "slider", "magic", "impossible"]):
            plan = self.generate_puzzle_lock_plan()
        elif any(w in t for w in ["plane", "shaving", "shave", "刨", "ribbon", "kanna"]):
            plan = self.generate_hand_plane_shaving_plan()
        elif any(w in t for w in ["dovetail", "燕尾", "box joint"]):
            plan = self.generate_dovetail_joint_plan()
        elif any(w in t for w in ["master tenon", "corner"]):
            plan = self.generate_corner_tenon_plan()
        elif any(w in t for w in ["marking", "gauge", "划线器", "layout", "pencil", "line"]):
            plan = self.generate_marking_gauge_plan()
        elif any(w in t for w in ["kumiko", "lattice", "组子", "hexagonal", "grid"]):
            plan = self.generate_kumiko_plan()
        elif any(w in t for w in ["dougong", "bracket", "斗拱", "temple", "earthquake", "pavilion", "shrine"]):
            plan = self.generate_dougong_plan()
        elif any(w in t for w in ["end_grain", "chisel", "sharpness", "blade", "slice"]):
            plan = self.generate_end_grain_sharpness_plan()
        elif any(w in t for w in ["sunmao", "mortise", "tenon", "榫卯", "joint", "interlock"]):
            plan = self.generate_sunmao_mortise_plan()
        else:
            return self.generate_dynamic_craft_plan(topic, target_duration=target_duration)

        return self._scale_plan_to_duration(plan, target_duration=target_duration)


if __name__ == "__main__":
    director = ScriptDirector()
    for test_topic in [
        "The Zero-Nail Bed Frame Joint",
        "The Precision Marking Gauge Trick",
        "The Zero-Gap Kumiko Joint",
        "The 3-Way Table Leg Joint"
    ]:
        p = director.generate_short_plan(test_topic)
        print(f"[{test_topic}] -> Title: {p['title']} | Masthead: {p['masthead_text']}")
        for s in p['narration_segments']:
            print(f"   [{s['start']}-{s['end']}s] {s['text']}")
