"""
AI Director Module for TimberCraft Automation
Generates high-retention NatGeo-style baritone narration scripts,
timing cues, and "Human Touch" directives that EXACTLY MATCH the physical video action.
"""

from typing import Dict, Any, List


class ScriptDirector:
    def __init__(self):
        pass

    def generate_end_grain_sharpness_plan(self) -> Dict[str, Any]:
        """
        Generates a 33.5s production plan tailored to the End-Grain Chisel Slicing footage:
        - Accurately explains why cutting end-grain is the ultimate test of hand tools.
        - Explains diagonal growth rings and cellular wood shear.
        - Matches Blueprint HUD cards to the exact blade contact and ribbon thickness.
        - Implements the Rule of Silence so the pure slicing ASMR shines.
        """
        plan = {
            "title": "The Ultimate 0.05mm Chisel Test: Slicing End Grain #Shorts",
            "masthead_text": "THE ULTIMATE SHARPNESS TEST",
            "target_duration": 33.5,
            
            # Narration script segments (American Baritone - NatGeo style)
            # Exactly matches what the viewer is seeing frame by frame
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
                # === MANDATORY 3-SECOND RULE OF SILENCE (22.5s to 26.5s) ===
                # (NO Narration! Pure acoustic wood shaving slice ASMR)
                {
                    "start": 27.0,
                    "end": 33.0,
                    "text": "peeling a translucent wooden ribbon so thin, light passes right through it. That is what true master sharpness looks like."
                }
            ],
            
            # Rule of Silence Definition (Peak ASMR Slice Payoff)
            "silence_window": {
                "start": 22.5,
                "end": 26.5,
                "reason": "Climax pay-off: Pure acoustic end-grain slice Foley"
            },
            
            # Architectural Blueprint HUD Overlays (Technical measurements matching the exact video)
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
            
            # Speed Ramping Markers (Human Kinetic Editing)
            "speed_ramps": [
                {"start": 0.0, "end": 6.0, "speed": 1.0, "label": "Hook: Blade touches end-grain"},
                {"start": 6.0, "end": 14.0, "speed": 1.0, "label": "Smooth peeling action"},
                {"start": 14.0, "end": 22.5, "speed": 0.9, "label": "Tension build: continuous ribbon"},
                {"start": 22.5, "end": 26.5, "speed": 1.0, "label": "Pure ASMR silence payoff"},
                {"start": 26.5, "end": 33.5, "speed": 1.0, "label": "Translucent ribbon showcase"}
            ],

            # Music Mood & Niche Tag for ai33 / Smart Music Matching
            "music_mood": "chisel_asmr",
            "sub_niche": "Japanese Chisel Metallurgy",
            "force_new_music": False
        }
        return plan

    def generate_short_plan(self, topic: str = "end_grain") -> Dict[str, Any]:
        """Generates plan tailored to topic or defaults to verified sharpness plan."""
        plan = self.generate_end_grain_sharpness_plan()
        lower_t = topic.lower()
        if "sandalwood" in lower_t or "lock" in lower_t or "temple" in lower_t:
            plan["music_mood"] = "temple_joint"
            plan["sub_niche"] = "Ancient Sandalwood Architecture"
        elif "kumiko" in lower_t or "lattice" in lower_t:
            plan["music_mood"] = "kumiko_lattice"
            plan["sub_niche"] = "Japanese Kumiko Joinery"
        elif "dovetail" in lower_t or "puzzle" in lower_t:
            plan["music_mood"] = "kumiko_lattice"
            plan["sub_niche"] = "Mechanical Dovetail Lock"
        return plan


if __name__ == "__main__":
    director = ScriptDirector()
    plan = director.generate_short_plan()
    print("[+] Generated Matched Plan:")
    print(f"Title: {plan['title']}")
    print(f"Masthead: {plan['masthead_text']}")
    print(f"HUD 1: {plan['hud_overlays'][0]['title']} -> {plan['hud_overlays'][0]['specs']}")
