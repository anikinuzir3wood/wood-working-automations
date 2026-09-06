"""
AI Director Module for TimberCraft Automation
Generates high-retention NatGeo-style baritone narration scripts,
timing cues, and "Human Touch" directives that EXACTLY MATCH the physical video action.
"""

from typing import Dict, Any, List
import re


class ScriptDirector:
    def __init__(self):
        pass

    def generate_marking_gauge_plan(self) -> Dict[str, Any]:
        """Plan for layout, marking gauge (划线器), and measuring accuracy."""
        return {
            "title": "The Master Carpenter's 0.1mm Marking Trick #Shorts",
            "masthead_text": "0.1mm PRECISION LAYOUT",
            "target_duration": 31.8,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.5,
                    "text": "Before a single chisel touches the timber, a master carpenter wins the battle with layout."
                },
                {
                    "start": 6.0,
                    "end": 13.8,
                    "text": "Watch how the brass pin of this handmade marking gauge scores across the grain, severing wood fibers cleanly rather than tearing them like a pencil."
                },
                {
                    "start": 14.2,
                    "end": 22.0,
                    "text": "This microscopic knife line creates an undeniable physical groove for the hand saw and chisel to track against..."
                },
                # Silence window: crisp scoring ASMR
                {
                    "start": 26.5,
                    "end": 31.5,
                    "text": "guaranteeing zero-gap tolerances before the cut even begins. True precision is never an accident."
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
                    "title": "LAYOUT GEOMETRY",
                    "specs": ["Tool: HARDWOOD GAUGE", "Tolerance: 0.10mm LINE"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "FIBER SEVERANCE",
                    "specs": ["Pin: HARDENED BRASS", "Action: CLEAN KNIFE CUT"]
                },
                {
                    "start": 14.5,
                    "end": 21.5,
                    "title": "REFERENCE FENCE",
                    "specs": ["Fence: PARALLEL ALIGNMENT", "Square: 90.0° TRUE"]
                },
                {
                    "start": 26.5,
                    "end": 31.0,
                    "title": "ZERO-GAP TRACK",
                    "specs": ["Groove: PHYSICAL GUIDE", "Grade: MASTER TOLERANCE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Gauge contact"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Smooth scoring stroke"},
                {"start": 14.0, "end": 22.0, "speed": 0.95, "label": "Tension: knife line detail"},
                {"start": 22.0, "end": 26.5, "speed": 1.0, "label": "Pure ASMR sliding payoff"},
                {"start": 26.5, "end": 31.8, "speed": 1.0, "label": "Zero-gap alignment showcase"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Precision Woodworking Layout",
            "force_new_music": False
        }

    def generate_kumiko_plan(self) -> Dict[str, Any]:
        """Plan for Kumiko lattice joinery (组子细工)."""
        return {
            "title": "The Zero-Gap Japanese Kumiko Joint #Shorts",
            "masthead_text": "ZERO-GAP KUMIKO JOINERY",
            "target_duration": 33.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "In traditional Japanese Kumiko, dozens of delicate wooden slats lock together without a single nail or drop of glue."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Each piece is beveled on a custom wooden guide block, shaved at exact sixty-degree angles with a razor-sharp hand plane."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "Watch the tension fit. If the dimension is off by the thickness of a single human hair, the entire lattice will warp..."
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "text": "Hear that acoustic snap? That pure friction lock is the hallmark of master joinery passed down for centuries."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Pure acoustic wooden lattice snap ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "KUMIKO LATTICE",
                    "specs": ["Fasteners: ZERO NAILS / GLUE", "Pattern: ASA-NO-HA"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "MICRO-BEVELING",
                    "specs": ["Guide Angle: 60.0° BEVEL", "Plane: JAPANESE KANNA"]
                },
                {
                    "start": 15.0,
                    "end": 21.5,
                    "title": "FRICTION LOCK",
                    "specs": ["Tolerance: ±0.02mm HAIR", "Wood: AGED HINOKI CYPRESS"]
                },
                {
                    "start": 27.0,
                    "end": 32.5,
                    "title": "ACOUSTIC SNAP",
                    "specs": ["Joint: FULL MECHANICAL FIT", "Grade: HERITAGE CRAFT"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Lattice assembly"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Beveling details"},
                {"start": 14.0, "end": 22.5, "speed": 0.9, "label": "Tension build: final piece"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR snap payoff"},
                {"start": 26.5, "end": 33.5, "speed": 1.0, "label": "Flawless geometric showcase"}
            ],
            "music_mood": "kumiko_lattice",
            "sub_niche": "Japanese Kumiko Joinery",
            "force_new_music": False
        }

    def generate_sunmao_mortise_plan(self) -> Dict[str, Any]:
        """Plan for classical mortise & tenon and Sunmao architecture (榫卯)."""
        return {
            "title": "The Ancient Chinese Sunmao Assembly #Shorts",
            "masthead_text": "ANCIENT SUNMAO ASSEMBLY",
            "target_duration": 34.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "Chinese Sunmao joinery has kept thousand-year-old timber structures standing through massive earthquakes."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Unlike modern screws that loosen over decades, this mortise and tenon joint uses wood's natural grain expansion to clamp tighter over time."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "Notice the internal wedge and interlocking keyways. Each mortise is carved completely by hand with surgical precision..."
                },
                {
                    "start": 27.0,
                    "end": 33.5,
                    "text": "sliding together with zero play. That is five millennia of architectural genius in a single joint."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Solid wooden mallet tap & interlock ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "SUNMAO JOINERY",
                    "specs": ["Structure: CLASSICAL CHINESE", "History: 5000+ YEARS"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "FIBER EXPANSION",
                    "specs": ["Fastener: ZERO METAL / SCREWS", "Action: SELF-TIGHTENING"]
                },
                {
                    "start": 15.0,
                    "end": 21.5,
                    "title": "INTERNAL WEDGE",
                    "specs": ["Chisel: HAND-CARVED MORTISE", "Interlock: MECHANICAL KEY"]
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "title": "ZERO PLAY",
                    "specs": ["Tolerance: 0.05mm FIT", "Grade: IMPERIAL HERITAGE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Tenon approaches mortise"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Keyway engagement"},
                {"start": 14.0, "end": 22.5, "speed": 0.95, "label": "Precision alignment"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR hammer tap payoff"},
                {"start": 26.5, "end": 34.0, "speed": 1.0, "label": "Seamless locked joint"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Ancient Sunmao Joinery",
            "force_new_music": False
        }

    def generate_puzzle_lock_plan(self) -> Dict[str, Any]:
        """Plan for Luban puzzle locks, secret sliders, and 3D dovetails (鲁班锁 / 机关)."""
        return {
            "title": "The 3D Secret Interlocking Dovetail Lock #Shorts",
            "masthead_text": "SECRET DOVETAIL LOCK",
            "target_duration": 33.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "From the outside, this wooden joint appears completely impossible to assemble or pull apart."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Look closely at the diagonal dovetail angles on all four faces. Simple geometry says these surfaces should collide and jam immediately."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "The secret is hidden within. Internal diagonal sliding tracks allow the two blocks to glide along a hidden forty-five-degree vector..."
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "text": "until the secret puzzle keys engage. Invisible, seamless, and completely mind-bending."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Smooth sliding wood-on-wood click ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "IMPOSSIBLE JOINT",
                    "specs": ["Geometry: 4-WAY INTERLOCK", "Visual: MECHANICAL ILLUSION"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "DIAGONAL VECTOR",
                    "specs": ["Glide Vector: 45.0° INTERNAL", "Wood: DENSE ROSEWOOD"]
                },
                {
                    "start": 15.0,
                    "end": 21.5,
                    "title": "INTERNAL TRACKS",
                    "specs": ["Mechanism: 3D SLIDING RAILS", "Clearance: 0.05mm"]
                },
                {
                    "start": 27.0,
                    "end": 32.5,
                    "title": "SEAMLESS LOCK",
                    "specs": ["Assembly: ZERO GAP REVEAL", "Grade: MASTER PUZZLE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Visual illusion"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Rotating 4 faces"},
                {"start": 14.0, "end": 22.5, "speed": 0.9, "label": "Sliding diagonal vector"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR sliding payoff"},
                {"start": 26.5, "end": 33.5, "speed": 1.0, "label": "Complete seamless block"}
            ],
            "music_mood": "kumiko_lattice",
            "sub_niche": "Mechanical Dovetail Lock",
            "force_new_music": False
        }

    def generate_dougong_plan(self) -> Dict[str, Any]:
        """Plan for Dougong cantilever temple brackets (斗拱)."""
        return {
            "title": "The Ancient Dougong Bracket: Earthquake-Proof Wood #Shorts",
            "masthead_text": "EARTHQUAKE-PROOF DOUGONG",
            "target_duration": 34.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "This interlocking wooden bracket is the true secret behind ancient temples surviving magnitude eight earthquakes."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Known as Dougong, these stepped cantilever blocks distribute massive roof weight through friction without a single nail or bolt."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "When seismic tremors shake the earth, the joints flex, absorb shock waves, and self-center automatically..."
                },
                {
                    "start": 27.0,
                    "end": 33.5,
                    "text": "converting destructive kinetic energy into friction. Ancient architectural engineering at its finest."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Resonant wooden interlock ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "DOUGONG BRACKET",
                    "specs": ["Structure: IMPERIAL CANTILEVER", "Function: SEISMIC SHOCK DISSIPATOR"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "STEPPED CANTILEVER",
                    "specs": ["Fasteners: ZERO NAILS / GLUE", "Load: 3D DISSIPATIVE TRANSFER"]
                },
                {
                    "start": 15.0,
                    "end": 21.5,
                    "title": "SEISMIC DAMPING",
                    "specs": ["Flex: CONTROLLED MICRO-PLAY", "Action: KINETIC ABSORPTION"]
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "title": "SELF-CENTERING",
                    "specs": ["Interlock: FULL RECOVERY", "Grade: UNESCO MASTERWORK"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Complex bracket assembly"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Stepped block placement"},
                {"start": 14.0, "end": 22.5, "speed": 0.95, "label": "Tension: load test"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR seating payoff"},
                {"start": 26.5, "end": 34.0, "speed": 1.0, "label": "Earthquake proof structure"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Ancient Sandalwood Architecture",
            "force_new_music": False
        }

    def generate_end_grain_sharpness_plan(self) -> Dict[str, Any]:
        """Plan for chisel sharpness, razor plane, and end-grain slicing demonstrations."""
        return {
            "title": "The Ultimate 0.05mm Chisel Test: Slicing End Grain #Shorts",
            "masthead_text": "THE ULTIMATE SHARPNESS TEST",
            "target_duration": 33.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.8,
                    "text": "To a master carpenter, end grain is the ultimate and most brutal test of an edge."
                },
                {
                    "start": 6.2,
                    "end": 14.0,
                    "text": "Notice those tight diagonal growth rings. If this hand-forged steel were even slightly dull, these vertical wood fibers would crush and splinter."
                },
                {
                    "start": 14.5,
                    "end": 22.0,
                    "text": "Instead, watch the blade glide at a microscopic angle. It shears cleanly through individual cellulose walls..."
                },
                {
                    "start": 27.0,
                    "end": 33.0,
                    "text": "peeling a translucent wooden ribbon so thin, light passes right through it. That is what true master sharpness looks like."
                }
            ],
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Pure acoustic end-grain slice Foley"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "END-GRAIN TEST",
                    "specs": ["Surface: CROSS-SECTION", "Tolerance: 0.05mm SLICE"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "CELLULAR SHEAR",
                    "specs": ["Bevel: 28.0° RAZOR EDGE", "Grain: 16 RINGS / INCH"]
                },
                {
                    "start": 15.0,
                    "end": 21.5,
                    "title": "TRANSLUCENT RIBBON",
                    "specs": ["Fiber Status: ZERO CRUSH", "Shear: PURE CELLULOSE"]
                },
                {
                    "start": 27.0,
                    "end": 32.5,
                    "title": "MICROSCOPIC POLISH",
                    "specs": ["Uniformity: 100% PARALLEL", "Grade: MASTER FINISH"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Blade touches end-grain"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Smooth peeling action"},
                {"start": 14.0, "end": 22.5, "speed": 0.9, "label": "Tension build: continuous ribbon"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR silence payoff"},
                {"start": 26.5, "end": 33.5, "speed": 1.0, "label": "Translucent ribbon showcase"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Japanese Chisel Metallurgy",
            "force_new_music": False
        }

    def generate_dynamic_craft_plan(self, topic: str) -> Dict[str, Any]:
        """Dynamic plan synthesizer for any custom woodworking topic."""
        clean_topic = topic.replace("#Shorts", "").strip()
        masthead = clean_topic.upper()
        if len(masthead) > 28:
            masthead = masthead[:25] + "..."

        return {
            "title": f"{clean_topic} #Shorts",
            "masthead_text": masthead,
            "target_duration": 32.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 5.5,
                    "text": f"In master woodworking, {clean_topic.lower()} requires unwavering patience and surgical discipline."
                },
                {
                    "start": 6.0,
                    "end": 14.0,
                    "text": "Every cut and shaving responds to the natural density and grain direction of the timber. One slight slip ruins weeks of work."
                },
                {
                    "start": 14.5,
                    "end": 21.5,
                    "text": "Watch closely as the craftsman guides the hand tool with feather-light pressure, aligning microscopic surfaces..."
                },
                {
                    "start": 26.5,
                    "end": 31.8,
                    "text": "revealing flawless tolerances that modern machines simply cannot match. That is master craftsmanship."
                }
            ],
            "silence_window": {
                "start": 22.0,
                "end": 26.0,
                "reason": "Climax pay-off: Pure acoustic craftsman hands ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 6.0,
                    "title": "MASTER WORK",
                    "specs": ["Craft: TRADITIONAL WOODCRAFT", "Patience: 100% MANUAL"]
                },
                {
                    "start": 7.0,
                    "end": 13.5,
                    "title": "GRAIN DYNAMICS",
                    "specs": ["Surface: HAND FINISHED", "Fiber: ZERO SPLINTER"]
                },
                {
                    "start": 14.5,
                    "end": 21.0,
                    "title": "PRECISION FIT",
                    "specs": ["Tolerance: SUB-MILLIMETER", "Alignment: PERFECT TRUE"]
                },
                {
                    "start": 26.5,
                    "end": 31.5,
                    "title": "FINAL REVEAL",
                    "specs": ["Finish: HAND TOOL MASTER", "Grade: HEIRLOOM QUALITY"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Opening craft"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Detailed work"},
                {"start": 14.0, "end": 22.0, "speed": 0.95, "label": "Critical alignment"},
                {"start": 22.0, "end": 26.0, "speed": 1.0, "label": "Pure ASMR payoff"},
                {"start": 26.0, "end": 32.0, "speed": 1.0, "label": "Finished reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Traditional Woodworking",
            "force_new_music": False
        }

    def generate_short_plan(self, topic: str = "end_grain") -> Dict[str, Any]:
        """
        Dynamically selects or synthesizes a plan matching the specific video topic.
        Never defaults to end-grain unless the topic specifically relates to chisel sharpness.
        """
        t = (topic or "").lower()

        # 1. Marking gauge / layout / measurement
        if any(w in t for w in ["marking", "gauge", "划线器", "layout", "pencil", "line"]):
            return self.generate_marking_gauge_plan()

        # 2. Kumiko lattice
        if any(w in t for w in ["kumiko", "lattice", "组子", "hexagonal", "grid"]):
            return self.generate_kumiko_plan()

        # 3. Mortise, Tenon, Sunmao
        if any(w in t for w in ["sunmao", "mortise", "tenon", "榫卯", "joint", "interlock", "corner"]):
            return self.generate_sunmao_mortise_plan()

        # 4. Puzzle, Dovetail, Lock
        if any(w in t for w in ["puzzle", "lock", "dovetail", "鲁班锁", "secret", "slider", "impossible"]):
            return self.generate_puzzle_lock_plan()

        # 5. Dougong, Architecture, Temple
        if any(w in t for w in ["dougong", "bracket", "斗拱", "temple", "earthquake", "pavilion", "shrine"]):
            return self.generate_dougong_plan()

        # 6. Chisel sharpness, end grain, blade restoration
        if any(w in t for w in ["end_grain", "chisel", "sharpness", "blade", "plane", "slice", "shaving", "ribbon"]):
            return self.generate_end_grain_sharpness_plan()

        # 7. Generic dynamic fallback for any other craftsmanship topic
        return self.generate_dynamic_craft_plan(topic)


if __name__ == "__main__":
    director = ScriptDirector()
    for test_topic in [
        "The Precision Marking Gauge Trick",
        "The Zero-Gap Kumiko Joint",
        "The Hand-Cut Sunmao Assembly",
        "The 3D Secret Dovetail Puzzle",
        "The Dougong Temple Bracket",
        "The 0.05mm Chisel End-Grain Test"
    ]:
        p = director.generate_short_plan(test_topic)
        print(f"[{test_topic}] -> Title: {p['title']} | Masthead: {p['masthead_text']} | Mood: {p['music_mood']}")
