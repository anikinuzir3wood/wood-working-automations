"""
Metadata & White-Hat SEO Engine for TimberCraft Automation
Generates US Tier-1 curiosity titles, structured descriptions, specifications, and tags
tailored to the specific craftsmanship technique.
"""

import re
from typing import Dict, Any, List, Optional


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


class MetadataEngine:
    def __init__(self):
        pass

    def generate_metadata(
        self,
        title_theme: str = "Traditional Woodcraft",
        video_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate complete upload-ready metadata package tailored to the specific topic."""
        clean_theme = sanitize_english_text(title_theme, fallback="Traditional Woodcraft")
        t = clean_theme.lower()

        obj = ""
        actions = ""
        reveal = ""
        if video_analysis:
            obj = sanitize_english_text(video_analysis.get("object", ""), fallback="")
            actions = sanitize_english_text(video_analysis.get("actions", ""), fallback="")
            reveal = sanitize_english_text(video_analysis.get("reveal", ""), fallback="")

        # Vision-Grounded Priority: If visual analysis provided specific object/actions, use them directly!
        if obj and (actions or reveal):
            clean = clean_theme.replace("#Shorts", "").strip()
            if not clean or clean.lower() in ["traditional woodcraft", "master craftsmanship"]:
                clean = f"The Hand-Crafted {obj}"
            
            title = f"{clean} #Shorts" if not clean.endswith("#Shorts") else clean
            action_text = f"{actions}. " if actions else ""
            reveal_text = f"{reveal}. " if reveal else ""
            description = (
                f"Master craftsmanship breakdown: Exploring the techniques and fine tolerances behind {obj.lower()}.\n\n"
                f"{action_text}{reveal_text}\n\n"
                "In traditional timber craft, every cut, shaving, and joint responds directly to the natural density and grain direction "
                "of the wood. Guided entirely by hand tools and disciplined muscle memory, master carpenters achieve fits that modern machines "
                "struggle to replicate.\n\n"
                "Craftsmanship Specifications:\n"
                f"• Focus Technique: {obj}\n"
                "• Method: 100% Traditional Hand Tools & Joinery\n"
                "• Tolerance: Sub-millimeter Heirloom Precision\n"
                "• Fasteners: 100% Interlocking Solid Timber (Zero Hardware / Glue)\n\n"
                "Subscribe to TimberCraft for daily master woodworking, antique restoration, and joinery showcases.\n\n"
                f"#{obj.replace(' ', '')} #Woodworking #Craftsmanship #HandTools #Carpentry #Woodwork #Artisan #Satisfying #Shorts"
            )
            tags = [
                obj.lower(), "woodworking", "master carpenter", "hand tools", "traditional woodwork",
                "wood craftsmanship", "satisfying wood", "timbercraft", "wood joinery",
                "artisan woodcraft", "shorts"
            ]
            pinned_comment = f"What do you think of this {obj.lower()} technique? Let us know in the comments 👇"
            return {
                "title": title,
                "description": description,
                "tags": tags,
                "pinned_comment": pinned_comment
            }

        base_theme = clean_theme.replace("#Shorts", "").strip()

        # 1. Dissecting hidden mortise / internal mechanism
        if any(w in t for w in ["dissect", "hidden", "internal", "拆解"]):
            title = f"{base_theme}: Secret Internal Lock #Shorts"
            description = (
                "Taking apart a hidden locking mortise to reveal what happens inside the timber.\n\n"
                "From the outside, it appears to be a solid block of wood. But sliding out the central wooden keyway "
                "unlocks an internal expanding wedge mechanism carved directly into the core, trapping the tenon so tightly "
                "it can never work loose under tension.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joint Anatomy: Concealed Expanding Wedge Mortise\n"
                "• Locking Mechanism: Hand-Carved Sliding Keyway Pin\n"
                "• Structural Clearance: 0.05mm Friction Fit\n"
                "• Fasteners: 100% Solid Timber (Zero Hardware / Glue)\n"
                "• Heritage: Traditional Mechanical Joinery\n\n"
                "Subscribe to TimberCraft for daily joinery breakdowns, internal mechanisms, and master craftsmanship.\n\n"
                "#Woodworking #Joinery #MechanicalWood #HiddenLock #HandTools #Carpentry #Woodwork #ASMR #Shorts"
            )
            tags = [
                "woodworking", "hidden joint", "locking mortise", "secret joint",
                "internal joinery", "woodworking asmr", "satisfying fit", "carpentry",
                "hand tools", "timbercraft", "master woodworker", "shorts"
            ]
            pinned_comment = "Did you expect that expanding wedge inside? Tell us what you think below 👇"

        # 2. Table leg joint
        elif any(w in t for w in ["table leg", "legjoint", "leg"]):
            title = f"{base_theme}: 3-Way Zero-Wobble Lock #Shorts"
            description = (
                "This three-way interlocking corner joint is the secret to building heirloom furniture that lasts generations.\n\n"
                "Two horizontal apron rails and one vertical leg intersect at a single junction, locking together through hand-cut "
                "interlocking notches. Downward table weight drives the joint tighter under compression, creating an unbreakable "
                "frame with zero racking or wobble.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joint Style: 3-Axis Interlocking Table Corner\n"
                "• Fasteners: 100% Interlocking Timber (Zero Screws/Nails)\n"
                "• Mechanics: Gravity-Assisted Mechanical Lock\n"
                "• Tolerance: Hand-Chiseled Sub-Millimeter Seat\n"
                "• Durability: Multi-Generational Heirloom Rigidity\n\n"
                "Subscribe to TimberCraft for daily master furniture joinery, timber framing, and artisan techniques.\n\n"
                "#Woodworking #TableJoint #FurnitureMaking #Joinery #NoNails #HandmadeFurniture #Carpentry #Shorts"
            )
            tags = [
                "table joint", "furniture joinery", "woodworking", "zero hardware",
                "table leg", "interlocking wood", "woodworking asmr", "hand tools",
                "timbercraft", "carpentry", "shorts"
            ]
            pinned_comment = "Three pieces of timber locking into one solid corner without a single screw. What do you think? 👇"

        # 3. Puzzle, Dovetail, Lock
        elif any(w in t for w in ["puzzle", "lock", "鲁班锁", "secret", "slider", "magic", "impossible"]):
            title = f"{base_theme}: The Impossible 3D Joint #Shorts"
            description = (
                "From the outside, this interlocking wooden joint appears physically impossible to assemble or dismantle.\n\n"
                "With diagonal dovetail pins showing on all four faces, geometry suggests the components must collide and bind instantly. "
                "The secret lies in an internal 45-degree sliding vector carved inside the block, allowing the puzzle components to glide "
                "seamlessly into an invisible mechanical lock.\n\n"
                "Craftsmanship Specifications:\n"
                "• Mechanism: 3D Multi-Way Sliding Dovetail Lock (鲁班锁)\n"
                "• Wood Species: Seasoned Dense Hardwood\n"
                "• Sliding Vector: 45.0° Hidden Keyway Track\n"
                "• Internal Clearance: 0.05mm Micro-Tolerance\n"
                "• Joint Type: Invisible Friction Puzzle Assembly\n\n"
                "Subscribe to TimberCraft for daily puzzle joinery, impossible woodwork, and artisan mechanical marvels.\n\n"
                "#Woodworking #PuzzleLock #ImpossibleJoint #Dovetail #MechanicalWood #Satisfying #Artisan #Shorts"
            )
            tags = [
                "impossible joint", "puzzle lock", "woodworking puzzle", "secret dovetail",
                "satisfying wood slide", "luban lock", "wood joinery", "hand tools",
                "timbercraft", "woodworking asmr", "shorts"
            ]
            pinned_comment = "Did you guess how the hidden sliding track worked before the reveal? 👇"

        # 4. Hand plane shaving / razor plane
        elif any(w in t for w in ["plane", "shaving", "shave", "刨", "ribbon", "kanna"]):
            title = f"{base_theme}: 0.01mm Translucent Ribbon #Shorts"
            description = (
                "Watch what happens when a razor-sharp hand plane glides across solid hardwood.\n\n"
                "The blade is tuned with such precision that it does not scrape—it shears cleanly through vertical cellulose fibers "
                "at a microscopic angle. A continuous, see-through wooden ribbon floats up from the sole, leaving a mirror-smooth "
                "burnished surface without using any sandpaper.\n\n"
                "Craftsmanship Specifications:\n"
                "• Tool: Traditional Wood Hand Plane (鉋 / 刨子)\n"
                "• Blade: Hand-Forged High Carbon Steel Razor Edge\n"
                "• Shaving Thickness: 0.01mm Translucent Micro-Ribbon\n"
                "• Surface Finish: Pure Cellular Polish (Zero Sandpaper)\n"
                "• Action: Cellular Grain Shear\n\n"
                "Subscribe to TimberCraft for daily hand plane ASMR, tool tuning, and master woodworking.\n\n"
                "#HandPlane #Woodworking #ASMR #WoodShaving #Satisfying #HandTools #Carpentry #MirrorFinish #Shorts"
            )
            tags = [
                "hand plane", "wood shavings", "woodworking asmr", "satisfying wood",
                "razor sharp", "hand tools", "plane shaving", "mirror finish",
                "timbercraft", "woodcraft", "shorts"
            ]
            pinned_comment = "A shaving so thin you can read right through it! Have you ever tuned a hand plane to this level? 👇"

        # 5. Dovetail box joint
        elif any(w in t for w in ["dovetail", "燕尾", "box joint"]):
            title = f"{base_theme}: Zero-Gap Hand-Cut Joint #Shorts"
            description = (
                "A hand-cut dovetail joint is the undisputed signature of a master cabinetmaker.\n\n"
                "Each pin and tail is laid out by hand and carved with a razor chisel to create interlocking mechanical wedges "
                "that physically cannot pull apart. As the two boards meet, the friction fit seats the corner completely flush, "
                "allowing the wood grain to flow seamlessly around the box.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joinery Style: Traditional Hand-Cut Dovetail\n"
                "• Wedge Ratio: 1:8 Mechanical Locking Slope\n"
                "• Cutting Method: Japanese Dozuki Saw & Razor Chisel\n"
                "• Tolerance: 0.02mm Light-Tight Fit\n"
                "• Application: Heirloom Cabinetry & Fine Boxes\n\n"
                "Subscribe to TimberCraft for daily fine woodworking, dovetail masterclasses, and hand-cut joinery.\n\n"
                "#Dovetail #Woodworking #Cabinetmaking #HandTools #Joinery #PrecisionCraft #Carpentry #Shorts"
            )
            tags = [
                "dovetail joint", "hand cut dovetail", "woodworking", "cabinetmaking",
                "joinery", "woodworking asmr", "hand tools", "chisel work",
                "timbercraft", "satisfying fit", "shorts"
            ]
            pinned_comment = "Nothing beats the feeling of pressing a hand-cut dovetail together with zero light leaks. Tell us below 👇"

        # 6. Master tenon corner assembly
        elif any(w in t for w in ["corner assembly", "master tenon", "corner"]):
            title = f"{base_theme}: 90° Precision Frame Lock #Shorts"
            description = (
                "Watch this corner frame joint seat together without a single screw, nail, or drop of glue.\n\n"
                "Every surface of this mortise and tenon is hand-chiseled with zero room for error, aligning the structural "
                "timber perfectly square at 90 degrees. As the tenon seats into the mortise, wood fibers compress under "
                "pure friction to create an unbreakable corner.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joint: Hand-Cut Corner Mortise & Tenon\n"
                "• Assembly: 100% Timber Friction Seat\n"
                "• Fasteners: Zero Screws, Nails, or Adhesives\n"
                "• Squareness: 90.0° Verified True\n"
                "• Heritage: Traditional Timber Framing Craft\n\n"
                "Subscribe to TimberCraft for daily mortise and tenon breakdowns, frame joinery, and timbercraft.\n\n"
                "#MortiseAndTenon #Woodworking #Joinery #TimberFrame #HandTools #Carpentry #Satisfying #Shorts"
            )
            tags = [
                "mortise and tenon", "corner joint", "woodworking", "timber framing",
                "hand cut joint", "wood joinery", "satisfying fit", "carpentry",
                "timbercraft", "hand tools", "shorts"
            ]
            pinned_comment = "True square without a single fastener. What do you think of this corner tenon? 👇"

        # 7. Marking gauge / layout precision
        elif any(w in t for w in ["marking", "gauge", "划线器", "layout", "pencil", "line"]):
            title = f"{base_theme}: The 0.1mm Layout Secret #Shorts"
            description = (
                "Before a single chisel or hand saw touches the timber, a master carpenter wins the battle with layout.\n\n"
                "Unlike a soft graphite pencil that rubs off and creates a fuzzy, inaccurate line, a precision marking gauge "
                "uses a hardened pin to score directly across the grain. This microscopic incision severs wood fibers cleanly, "
                "leaving an unmistakable knife-edge groove that acts as a physical wall for saw teeth and chisel bevels.\n\n"
                "Craftsmanship Specifications:\n"
                "• Layout Tool: Handmade Hardwood Marking Gauge (木工划线器)\n"
                "• Scribing Pin: Hardened Brass / Steel Pin\n"
                "• Alignment Tolerance: 0.10mm Knife-Edge Line\n"
                "• Material: Dense Quarter-Sawn Hardwood\n"
                "• Function: Zero-Gap Joinery Reference Wall\n\n"
                "Subscribe to TimberCraft for daily master woodworking, joinery secrets, and tool precision.\n\n"
                "#Woodworking #MarkingGauge #Joinery #PrecisionCraft #HandTools #Carpentry #Woodwork #Shorts"
            )
            tags = [
                "woodworking", "marking gauge", "woodworking layout", "precision carpentry",
                "hand tools", "joinery tricks", "woodworking asmr", "wood marking",
                "master carpenter", "timbercraft", "woodworking hacks", "shorts"
            ]
            pinned_comment = "Do you prefer a traditional marking gauge or a wheel gauge for layout? Tell us below 👇"

        # 8. Kumiko lattice
        elif any(w in t for w in ["kumiko", "lattice", "组子", "hexagonal", "grid"]):
            title = f"{base_theme}: Zero-Gap Friction Lock #Shorts"
            description = (
                "In traditional Japanese Kumiko, dozens of delicate wooden slats lock together without a single nail or drop of glue.\n\n"
                "Every single component is beveled on custom wooden guide blocks, shaved to exact 60-degree angles using a razor-sharp "
                "kanna hand plane. If a dimension is off by even the thickness of a human hair (0.02mm), the entire geometric lattice "
                "either buckles or collapses under pressure.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joinery Style: Traditional Japanese Kumiko (组子细工)\n"
                "• Fasteners: Zero Nails / Zero Glue (Pure Friction Lock)\n"
                "• Wood Species: Aged Hinoki Cypress & Japanese Cedar\n"
                "• Guide Tolerance: ±0.02mm Hand-Planed Bevel\n"
                "• Pattern: Classical Asa-no-ha Geometric Star\n\n"
                "Subscribe to TimberCraft for daily master joinery, Japanese carpentry, and ancient techniques.\n\n"
                "#Kumiko #Woodworking #JapaneseCarpentry #Joinery #ZeroGlue #Satisfying #ASMR #Craftsmanship #Shorts"
            )
            tags = [
                "kumiko", "japanese woodworking", "zero nail joinery", "kumiko lattice",
                "woodworking asmr", "satisfying wood fit", "japanese carpentry", "kanna plane",
                "master joiner", "timbercraft", "hand tools", "shorts"
            ]
            pinned_comment = "The sound when the final piece snaps in... pure satisfaction! Have you ever tried Kumiko? 👇"

        # 9. Dougong, Architecture, Temple
        elif any(w in t for w in ["dougong", "bracket", "斗拱", "temple", "earthquake", "pavilion", "shrine"]):
            title = f"{base_theme}: Earthquake-Proof Ancient Architecture #Shorts"
            description = (
                "How did ancient wooden pagodas survive magnitude 8.0 earthquakes for over a thousand years without collapsing?\n\n"
                "The answer is Dougong: an ingenious stepped cantilever bracket system. Instead of fighting seismic ground energy with rigid "
                "brute force, Dougong joints flex, absorb shock waves through controlled micro-friction, and self-center automatically.\n\n"
                "Craftsmanship Specifications:\n"
                "• Architectural Structure: Imperial Dougong Cantilever Bracket (斗拱)\n"
                "• Mechanical Function: Dissipative Seismic Shock Absorption\n"
                "• Fasteners: 100% Interlocking Timber (Zero Nails/Bolts)\n"
                "• Load Distribution: Three-Dimensional Vector Dissipation\n"
                "• Heritage: UNESCO World Heritage Timber Engineering\n\n"
                "Subscribe to TimberCraft for daily architectural masterworks and ancient engineering breakdowns.\n\n"
                "#Dougong #Architecture #Woodworking #EarthquakeProof #AncientEngineering #TimberFrame #Shorts"
            )
            tags = [
                "dougong", "ancient architecture", "earthquake proof wood", "timber frame",
                "temple architecture", "heritage carpentry", "interlocking timber",
                "timbercraft", "woodworking", "shorts"
            ]
            pinned_comment = "Ancient engineers solved earthquake resilience over 1,500 years ago using only wood. Incredible engineering! 👇"

        # 10. Chisel sharpness, end grain
        elif any(w in t for w in ["end_grain", "chisel", "sharpness", "blade", "slice"]):
            title = f"{base_theme}: Slicing End Grain #Shorts"
            description = (
                "To any master woodworker, end-grain is the ultimate and most unforgiving test of an edge.\n\n"
                "Unlike face grain, end-grain consists of microscopic vertical cellulose tubes bundled together like drinking straws. "
                "If a chisel has even a single microscopic nick or improper bevel geometry, the fibers tear, crush, and splinter immediately.\n\n"
                "Craftsmanship Specifications:\n"
                "• Cut Surface: End-Grain Cross Section (端面切削)\n"
                "• Wood Species: Aged Dense-Ring Pine (16+ rings per inch)\n"
                "• Chisel Type: Hand-Forged Japanese Oire Nomi (平凿)\n"
                "• Bevel Angle: 28.0° Razor Edge with Mirror Polish\n"
                "• Ribbon Thickness: 0.05mm Translucent Micro-Shaving\n\n"
                "Subscribe to TimberCraft for daily master craftsmanship, tool restoration, and ancient woodworking breakdowns.\n\n"
                "#Woodworking #Chisel #Satisfying #ASMR #EndGrain #Woodwork #HandTools #JapaneseCarpentry #Craftsmanship #Shorts"
            )
            tags = [
                "woodworking", "chisel sharpness", "end grain", "japanese chisel",
                "woodworking asmr", "satisfying slice", "hand tools", "oire nomi",
                "wood shavings", "razor sharp", "craftsmanship", "carpentry", "shorts"
            ]
            pinned_comment = "Have you ever seen end-grain cut this smoothly? Tell us what steel you use below 👇"

        # 11. Traditional Sunmao / Mortise & Tenon
        elif any(w in t for w in ["sunmao", "mortise", "tenon", "榫卯", "joint", "interlock"]):
            title = f"{base_theme}: Ancient Self-Locking Joinery #Shorts"
            description = (
                "Traditional Sunmao joinery has kept thousand-year-old timber structures standing through centuries of natural elements.\n\n"
                "Unlike modern metal fasteners that rust and loosen as timber breathes, a classical mortise and tenon joint harnesses the natural "
                "hygroscopic expansion of wood to lock tighter over time. Every mortise keyway is hand-chopped to microscopic tolerances.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joinery Heritage: Traditional Sunmao (榫卯结构)\n"
                "• Assembly: Hand-Cut Mortise & Tenon Interlock\n"
                "• Structural Integrity: Zero Nails, Screws, or Synthetic Adhesive\n"
                "• Clearance Tolerance: 0.05mm Friction Seat\n"
                "• Durability: Multi-Century Self-Tightening Action\n\n"
                "Subscribe to TimberCraft for daily ancient engineering, joinery breakdowns, and timber craftsmanship.\n\n"
                "#Sunmao #Woodworking #MortiseAndTenon #AncientJoinery #Carpentry #Satisfying #Engineering #Shorts"
            )
            tags = [
                "sunmao", "mortise and tenon", "ancient joinery", "traditional woodworking",
                "wood joinery", "hand cut joint", "satisfying fit", "carpentry",
                "timbercraft", "woodworking asmr", "shorts"
            ]
            pinned_comment = "Stronger than modern screws through pure friction. What do you think of traditional Sunmao? 👇"

        # 12. Vision-grounded or Generic dynamic fallback
        else:
            clean = clean_theme.replace("#Shorts", "").strip()
            if not clean or clean.lower() in ["traditional woodcraft", "master craftsmanship"]:
                clean = f"The Hand-Crafted {obj}" if obj else "Traditional Woodcraft"
            
            title = f"{clean} #Shorts" if not clean.endswith("#Shorts") else clean

            if obj and (actions or reveal):
                action_text = f"{actions}. " if actions else ""
                reveal_text = f"{reveal}. " if reveal else ""
                description = (
                    f"Master craftsmanship breakdown: Exploring the techniques and fine tolerances behind {obj.lower()}.\n\n"
                    f"{action_text}{reveal_text}\n\n"
                    "In traditional timber craft, every cut, shaving, and joint responds directly to the natural density and grain direction "
                    "of the wood. Guided entirely by hand tools and disciplined muscle memory, master carpenters achieve fits that modern machines "
                    "struggle to replicate.\n\n"
                    "Craftsmanship Specifications:\n"
                    f"• Focus Technique: {obj}\n"
                    "• Method: 100% Traditional Hand Tools & Joinery\n"
                    "• Tolerance: Sub-millimeter Heirloom Precision\n"
                    "• Fasteners: 100% Interlocking Solid Timber (Zero Hardware / Glue)\n\n"
                    "Subscribe to TimberCraft for daily master woodworking, antique restoration, and joinery showcases.\n\n"
                    f"#{obj.replace(' ', '')} #Woodworking #Craftsmanship #HandTools #Carpentry #Woodwork #Artisan #Satisfying #Shorts"
                )
                tags = [
                    obj.lower(), "woodworking", "master carpenter", "hand tools", "traditional woodwork",
                    "wood craftsmanship", "satisfying wood", "timbercraft", "wood joinery",
                    "artisan woodcraft", "shorts"
                ]
                pinned_comment = f"What do you think of this {obj.lower()} technique? Let us know in the comments 👇"
            else:
                description = (
                    f"Master craftsmanship breakdown: Exploring the techniques and fine tolerances behind {clean.lower()}.\n\n"
                    "In traditional timber craft, every cut, shaving, and joint responds directly to the natural density and grain direction "
                    "of the wood. Guided entirely by hand tools and disciplined muscle memory, master carpenters achieve fits that modern machines "
                    "struggle to replicate.\n\n"
                    "Craftsmanship Specifications:\n"
                    f"• Focus Technique: {clean}\n"
                    "• Method: 100% Traditional Hand Tools & Joinery\n"
                    "• Tolerance: Sub-millimeter Heirloom Precision\n"
                    "• Finish: Pure Hand-Planed & Chiseled Surface\n\n"
                    "Subscribe to TimberCraft for daily master woodworking, antique restoration, and joinery showcases.\n\n"
                    "#Woodworking #Craftsmanship #HandTools #Carpentry #Woodwork #Artisan #Satisfying #Shorts"
                )
                tags = [
                    "woodworking", "master carpenter", "hand tools", "traditional woodwork",
                    "wood craftsmanship", "satisfying wood", "timbercraft", "wood joinery",
                    "artisan woodcraft", "shorts"
                ]
                pinned_comment = f"What do you think of this master technique? Let us know in the comments 👇"

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "pinned_comment": pinned_comment
        }


if __name__ == "__main__":
    meta = MetadataEngine()
    for t in [
        "The Precision Marking Gauge Trick",
        "The Zero-Gap Kumiko Joint",
        "The Hand-Cut Sunmao Assembly",
        "The 3D Secret Dovetail Puzzle",
        "The Ancient Dougong Bracket",
        "The 0.05mm Chisel Test"
    ]:
        data = meta.generate_metadata(t)
        print(f"\n[TOPIC: {t}]")
        print(f"Title: {data['title']}")
        print(f"Tags: {data['tags'][:4]}")
        print(f"Snippet: {data['description'][:100]}...")
