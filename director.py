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
            "title": "The Ancient Sunmao Assembly #Shorts",
            "masthead_text": "ANCIENT SUNMAO ASSEMBLY",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Watch this traditional Sunmao joint assemble under pure friction."
                },
                {
                    "start": 5.0,
                    "end": 12.0,
                    "text": "Unlike modern metal fasteners that rust and loosen, a hand-cut mortise and tenon uses the wood's grain to clamp tighter over time."
                },
                {
                    "start": 12.5,
                    "end": 19.5,
                    "text": "Notice the internal keyways and precision shoulders. Every cut is carved with surgical hand-tool discipline..."
                },
                {
                    "start": 24.5,
                    "end": 30.5,
                    "text": "sliding together with zero play. That is centuries of heritage woodworking in a single joint."
                }
            ],
            "silence_window": {
                "start": 20.0,
                "end": 24.0,
                "reason": "Climax pay-off: Solid wooden mallet tap & interlock ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "SUNMAO JOINERY",
                    "specs": ["Structure: TRADITIONAL SUNMAO", "Heritage: MASTER JOINERY"]
                },
                {
                    "start": 6.0,
                    "end": 12.0,
                    "title": "FIBER EXPANSION",
                    "specs": ["Fastener: ZERO METAL / SCREWS", "Action: SELF-TIGHTENING"]
                },
                {
                    "start": 13.0,
                    "end": 19.0,
                    "title": "INTERNAL WEDGE",
                    "specs": ["Chisel: HAND-CARVED MORTISE", "Interlock: MECHANICAL KEY"]
                },
                {
                    "start": 24.5,
                    "end": 30.5,
                    "title": "ZERO PLAY",
                    "specs": ["Tolerance: 0.05mm FIT", "Grade: HERITAGE CRAFT"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Tenon approaches mortise"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Keyway engagement"},
                {"start": 12.0, "end": 19.5, "speed": 0.95, "label": "Precision alignment"},
                {"start": 19.5, "end": 24.5, "speed": 1.0, "label": "Pure ASMR hammer tap payoff"},
                {"start": 24.5, "end": 31.5, "speed": 1.0, "label": "Seamless locked joint"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Ancient Sunmao Joinery",
            "force_new_music": False
        }

    def generate_corner_tenon_plan(self) -> Dict[str, Any]:
        """Plan for corner mortise & tenon assemblies and frame joinery."""
        return {
            "title": "The Master Tenon Corner Assembly #Shorts",
            "masthead_text": "MASTER TENON CORNER",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Watch this corner joint seat together without a single screw, nail, or drop of glue."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Every surface of this mortise and tenon is hand-chiseled with zero room for error, aligning the structural timber square."
                },
                {
                    "start": 12.0,
                    "end": 19.0,
                    "text": "Notice the internal locking channel. As the tenon seats into the mortise, the wood fibers compress..."
                },
                {
                    "start": 24.0,
                    "end": 30.5,
                    "text": "locking both pieces into a single, unbreakable corner. That is master craftsmanship at work."
                }
            ],
            "silence_window": {
                "start": 19.5,
                "end": 23.5,
                "reason": "Climax pay-off: Solid wooden mallet tap & interlock ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "CORNER TENON",
                    "specs": ["Joint: CORNER MORTISE & TENON", "Assembly: 100% TIMBER INTERLOCK"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "90° ALIGNMENT",
                    "specs": ["Fasteners: ZERO NAILS / GLUE", "Alignment: 90.0° SQUARE"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "FIBER TENSION",
                    "specs": ["Chisel: SURGICAL HAND FIT", "Tension: CELLULAR COMPRESSION"]
                },
                {
                    "start": 24.0,
                    "end": 30.0,
                    "title": "HEIRLOOM LOCK",
                    "specs": ["Tolerance: SUB-MILLIMETER FIT", "Grade: HEIRLOOM JOINERY"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Frame corner approach"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Tenon seating"},
                {"start": 12.0, "end": 19.5, "speed": 0.95, "label": "Precision alignment"},
                {"start": 19.5, "end": 24.0, "speed": 1.0, "label": "Pure ASMR seating tap"},
                {"start": 24.0, "end": 31.5, "speed": 1.0, "label": "Seamless locked corner"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Traditional Corner Joinery",
            "force_new_music": False
        }

    def generate_puzzle_lock_plan(self) -> Dict[str, Any]:
        """Plan for Luban puzzle locks, secret sliders, and 3D dovetails (鲁班锁 / 机关)."""
        return {
            "title": "The 3D Secret Interlocking Dovetail Lock #Shorts",
            "masthead_text": "SECRET DOVETAIL LOCK",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "At first glance, this solid wooden block looks impossible to open."
                },
                {
                    "start": 5.0,
                    "end": 12.0,
                    "text": "Watch the craftsman rotate the piece. Hidden internal tracks allow the wooden segments to slide along an invisible vector."
                },
                {
                    "start": 12.5,
                    "end": 19.0,
                    "text": "Each interlocking pin is carved to microscopic tolerances so the seams remain completely undetectable until moved..."
                },
                {
                    "start": 24.0,
                    "end": 30.5,
                    "text": "revealing the secret interior lock. Pure mechanical genius carved entirely from timber."
                }
            ],
            "silence_window": {
                "start": 19.5,
                "end": 23.5,
                "reason": "Climax pay-off: Smooth sliding wood-on-wood click ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "SECRET LOCK",
                    "specs": ["Geometry: 3D PUZZLE INTERLOCK", "Visual: SEAMLESS ILLUSION"]
                },
                {
                    "start": 6.0,
                    "end": 12.0,
                    "title": "HIDDEN VECTOR",
                    "specs": ["Glide Vector: INTERNAL 45.0°", "Wood: DENSE HARDWOOD"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "SLIDING RAILS",
                    "specs": ["Mechanism: CONCEALED TRACKS", "Clearance: 0.05mm"]
                },
                {
                    "start": 24.0,
                    "end": 30.0,
                    "title": "SECRET REVEAL",
                    "specs": ["Assembly: ZERO GAP REVEAL", "Grade: MASTER PUZZLE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Inspecting block"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Rotating segments"},
                {"start": 12.0, "end": 19.5, "speed": 0.9, "label": "Sliding along vector"},
                {"start": 19.5, "end": 24.0, "speed": 1.0, "label": "Pure ASMR sliding payoff"},
                {"start": 24.0, "end": 31.5, "speed": 1.0, "label": "Open secret compartment"}
            ],
            "music_mood": "kumiko_lattice",
            "sub_niche": "Mechanical Dovetail Lock",
            "force_new_music": False
        }

    def generate_hand_plane_shaving_plan(self) -> Dict[str, Any]:
        """Plan for hand plane tuning, razor shaving, and translucent ribbon ASMR."""
        return {
            "title": "The Satisfying Hand Plane Shaving #Shorts",
            "masthead_text": "0.01mm PLANE SHAVING",
            "target_duration": 31.0,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Watch what happens when a razor-sharp hand plane glides across solid hardwood."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "The blade is tuned so finely it does not scrape—it shears cleanly through wood fibers at a microscopic angle."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "Notice the continuous translucent ribbon peeling off the board, so thin you can read right through it..."
                },
                {
                    "start": 23.5,
                    "end": 29.5,
                    "text": "leaving behind a glass-smooth mirror finish without using a single piece of sandpaper."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Pure acoustic hand plane wood slicing ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "PLANE SETUP",
                    "specs": ["Tool: HAND PLANE", "Sole: TRUED FLAT REFERENCE"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "CELLULAR SHEAR",
                    "specs": ["Bevel: RAZOR-SHARP EDGE", "Cut: ZERO FIBER CRUSH"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "TRANSLUCENT RIBBON",
                    "specs": ["Shaving: 0.01mm RIBBON", "Light: 100% SEE-THROUGH"]
                },
                {
                    "start": 23.5,
                    "end": 29.5,
                    "title": "MIRROR FINISH",
                    "specs": ["Sandpaper: ZERO USED", "Finish: PURE CELLULAR POLISH"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Blade touches board"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Continuous shaving stroke"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Ribbon floating up"},
                {"start": 19.0, "end": 23.0, "speed": 1.0, "label": "Pure ASMR shaving sound"},
                {"start": 23.0, "end": 31.0, "speed": 1.0, "label": "Mirror surface reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Hand Plane Craftsmanship",
            "force_new_music": False
        }

    def generate_dovetail_joint_plan(self) -> Dict[str, Any]:
        """Plan for hand-cut dovetail box joints and cabinetmaker joinery."""
        return {
            "title": "The Precision Dovetail Box Joint #Shorts",
            "masthead_text": "HAND-CUT DOVETAIL JOINT",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "A hand-cut dovetail is the undisputed signature of a master cabinetmaker."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Each pin and tail is carved with a razor chisel to create interlocking mechanical wedges that cannot pull apart."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "Watch the two boards meet. The friction fit is so exact that the grain lines flow seamlessly around the corner..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "leaving zero visible gap along the entire seam. Handcrafted precision at its finest."
                }
            ],
            "silence_window": {
                "start": 19.0,
                "end": 23.0,
                "reason": "Climax pay-off: Tactile wooden mallet seating ASMR"
            },
            "hud_overlays": [
                {
                    "start": 1.0,
                    "end": 5.0,
                    "title": "DOVETAIL JOINT",
                    "specs": ["Joint: HAND-CUT PINS & TAILS", "Fastener: MECHANICAL WEDGE"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "WEDGE GEOMETRY",
                    "specs": ["Angle: 1:8 DOVETAIL SLOPE", "Lock: TENSILE RESISTANCE"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "GRAIN CONTINUITY",
                    "specs": ["Alignment: CORNER GRAIN FLOW", "Clearance: 0.02mm FIT"]
                },
                {
                    "start": 23.5,
                    "end": 29.5,
                    "title": "ZERO-GAP SEAM",
                    "specs": ["Tolerance: ZERO LIGHT LEAK", "Grade: MASTER CABINETRY"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Dovetail alignment"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Pins engaging tails"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Pressing joint flush"},
                {"start": 19.0, "end": 23.0, "speed": 1.0, "label": "Pure ASMR mallet tap"},
                {"start": 23.0, "end": 31.5, "speed": 1.0, "label": "Seamless box corner reveal"}
            ],
            "music_mood": "chisel_asmr",
            "sub_niche": "Handmade Dovetail Joinery",
            "force_new_music": False
        }

    def generate_table_leg_joint_plan(self) -> Dict[str, Any]:
        """Plan for 3-way table leg interlocking joinery."""
        return {
            "title": "The No-Nails Table Leg Joint #Shorts",
            "masthead_text": "3-WAY TABLE LEG JOINT",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "This three-way interlocking joint is the secret to building furniture that lasts generations."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "Two horizontal rails and one vertical leg meet at a single corner, locking together through hand-cut notches."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "Watch how each timber locks the other in place. The downward weight of the table actually drives the joint tighter..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "creating an unbreakable frame with zero wobble. True heirloom woodworking."
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
                    "title": "3-WAY INTERLOCK",
                    "specs": ["Structure: 3-AXIS CORNER", "Fasteners: ZERO HARDWARE"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "RAIL & LEG KEY",
                    "specs": ["Rails: DUAL HORIZONTAL KEYS", "Leg: VERTICAL RECEIVER"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "SELF-LOCKING",
                    "specs": ["Load: GRAVITY CLAMPING", "Action: ANTI-RACKING RIGIDITY"]
                },
                {
                    "start": 23.5,
                    "end": 29.5,
                    "title": "ZERO WOBBLE",
                    "specs": ["Stability: 100% SOLID", "Grade: HEIRLOOM FURNITURE"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Table leg assembly"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Rail slotting into leg"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Dual rail engagement"},
                {"start": 19.0, "end": 23.0, "speed": 1.0, "label": "Pure ASMR seating tap"},
                {"start": 23.0, "end": 31.5, "speed": 1.0, "label": "Rock solid frame reveal"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Heirloom Furniture Joinery",
            "force_new_music": False
        }

    def generate_locking_mortise_dissection_plan(self) -> Dict[str, Any]:
        """Plan for dissecting and taking apart hidden locking mortises and internal wedge joints."""
        return {
            "title": "Dissecting the Hidden Locking Mortise #Shorts",
            "masthead_text": "HIDDEN LOCKING MORTISE",
            "target_duration": 31.5,
            "narration_segments": [
                {
                    "start": 0.0,
                    "end": 4.5,
                    "text": "Let us take apart this hidden locking joint to reveal what is happening inside the timber."
                },
                {
                    "start": 5.0,
                    "end": 11.5,
                    "text": "From the outside, it looks like a simple wood block. But slide out this central wooden keyway..."
                },
                {
                    "start": 12.0,
                    "end": 18.5,
                    "text": "and the internal mortise reveals an opposing wedge mechanism that expands inside the core..."
                },
                {
                    "start": 23.5,
                    "end": 30.0,
                    "text": "trapping the tenon so tightly it can never pull loose. Ingenious joinery hidden in plain sight."
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
                    "title": "JOINT DISSECTION",
                    "specs": ["Inspection: INTERNAL ANATOMY", "Exterior: DECEPTIVELY SIMPLE"]
                },
                {
                    "start": 6.0,
                    "end": 11.5,
                    "title": "CENTRAL KEYWAY",
                    "specs": ["Release: SLIDING LOCK PIN", "Clearance: 0.05mm"]
                },
                {
                    "start": 12.5,
                    "end": 18.5,
                    "title": "EXPANDING WEDGE",
                    "specs": ["Core: INTERNAL OPPOSING WEDGE", "Lock: POSITIVE MECHANICAL TRAP"]
                },
                {
                    "start": 23.5,
                    "end": 29.5,
                    "title": "INGENIOUS DESIGN",
                    "specs": ["Security: ZERO PULL-OUT", "Heritage: MASTER JOINERY"]
                }
            ],
            "speed_ramps": [
                {"start": 0.0, "end": 5.0, "speed": 1.0, "label": "Hook: Disassembling joint"},
                {"start": 5.0, "end": 12.0, "speed": 1.0, "label": "Sliding out locking key"},
                {"start": 12.0, "end": 19.0, "speed": 0.95, "label": "Revealing internal wedge"},
                {"start": 19.0, "end": 23.0, "speed": 1.0, "label": "Pure ASMR sliding sound"},
                {"start": 23.0, "end": 31.5, "speed": 1.0, "label": "Internal mechanism showcase"}
            ],
            "music_mood": "temple_joint",
            "sub_niche": "Concealed Mechanical Joinery",
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

        # 1. Dissecting hidden mortise / internal mechanism (Must be checked before generic lock)
        if any(w in t for w in ["dissect", "hidden", "internal", "拆解"]):
            return self.generate_locking_mortise_dissection_plan()

        # 2. Table leg joint (Must be checked before generic joints)
        if any(w in t for w in ["table leg", "legjoint", "leg"]):
            return self.generate_table_leg_joint_plan()

        # 3. Puzzle, secret lock, slider, magic joint
        if any(w in t for w in ["puzzle", "lock", "鲁班锁", "secret", "slider", "magic", "impossible"]):
            return self.generate_puzzle_lock_plan()

        # 4. Hand plane, shaving, kanna
        if any(w in t for w in ["plane", "shaving", "shave", "刨", "ribbon", "kanna"]):
            return self.generate_hand_plane_shaving_plan()

        # 5. Dovetail box joint
        if any(w in t for w in ["dovetail", "燕尾", "box joint"]):
            return self.generate_dovetail_joint_plan()

        # 6. Master tenon corner assembly
        if any(w in t for w in ["corner assembly", "master tenon", "corner"]):
            return self.generate_corner_tenon_plan()

        # 7. Marking gauge / layout / measurement
        if any(w in t for w in ["marking", "gauge", "划线器", "layout", "pencil", "line"]):
            return self.generate_marking_gauge_plan()

        # 8. Kumiko lattice
        if any(w in t for w in ["kumiko", "lattice", "组子", "hexagonal", "grid"]):
            return self.generate_kumiko_plan()

        # 9. Dougong, Architecture, Temple
        if any(w in t for w in ["dougong", "bracket", "斗拱", "temple", "earthquake", "pavilion", "shrine"]):
            return self.generate_dougong_plan()

        # 10. Chisel sharpness, end grain
        if any(w in t for w in ["end_grain", "chisel", "sharpness", "blade", "slice"]):
            return self.generate_end_grain_sharpness_plan()

        # 11. Traditional Sunmao / Mortise & Tenon
        if any(w in t for w in ["sunmao", "mortise", "tenon", "榫卯", "joint", "interlock"]):
            return self.generate_sunmao_mortise_plan()

        # 12. Generic dynamic fallback for any other craftsmanship topic
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
