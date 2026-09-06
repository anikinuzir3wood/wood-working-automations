"""
Metadata & White-Hat SEO Engine for TimberCraft Automation
Generates US Tier-1 curiosity titles, structured descriptions, specifications, and tags
tailored to the specific craftsmanship technique.
"""

from typing import Dict, Any, List


class MetadataEngine:
    def __init__(self):
        pass

    def generate_metadata(self, title_theme: str = "Traditional Woodcraft") -> Dict[str, Any]:
        """Generate complete upload-ready metadata package tailored to the specific topic."""
        t = (title_theme or "").lower()

        # 1. Marking gauge / layout precision
        if any(w in t for w in ["marking", "gauge", "划线器", "layout", "pencil", "line"]):
            title = f"{title_theme}: The 0.1mm Layout Secret #Shorts"
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

        # 2. Kumiko lattice
        elif any(w in t for w in ["kumiko", "lattice", "组子", "hexagonal", "grid"]):
            title = f"{title_theme}: Zero-Gap Friction Lock #Shorts"
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

        # 3. Mortise, Tenon, Sunmao
        elif any(w in t for w in ["sunmao", "mortise", "tenon", "榫卯", "joint", "interlock", "corner"]):
            title = f"{title_theme}: 5,000-Year Ancient Joinery #Shorts"
            description = (
                "Chinese Sunmao joinery has kept thousand-year-old timber structures standing through earthquakes, typhoons, and centuries of time.\n\n"
                "Unlike modern metal fasteners that rust and loosen as timber breathes, a classical mortise and tenon joint harnesses the natural "
                "hygroscopic expansion of wood to lock tighter over time. Every mortise keyway is hand-chopped to microscopic tolerances.\n\n"
                "Craftsmanship Specifications:\n"
                "• Joinery Heritage: Classical Chinese Sunmao (榫卯结构)\n"
                "• Assembly: Hand-Cut Mortise & Tenon Interlock\n"
                "• Structural Integrity: Zero Nails, Screws, or Synthetic Adhesive\n"
                "• Clearance Tolerance: 0.05mm Friction Seat\n"
                "• Durability: Multi-Century Self-Tightening Action\n\n"
                "Subscribe to TimberCraft for daily ancient engineering, joinery breakdowns, and timber craftsmanship.\n\n"
                "#Sunmao #Woodworking #MortiseAndTenon #AncientJoinery #Carpentry #Satisfying #Engineering #Shorts"
            )
            tags = [
                "sunmao", "mortise and tenon", "chinese joinery", "ancient woodworking",
                "wood joinery", "hand cut joint", "satisfying fit", "carpentry",
                "timbercraft", "woodworking asmr", "shorts"
            ]
            pinned_comment = "Five thousand years old and still stronger than modern screws. What do you think of Sunmao? 👇"

        # 4. Puzzle, Dovetail, Lock
        elif any(w in t for w in ["puzzle", "lock", "dovetail", "鲁班锁", "secret", "slider", "impossible"]):
            title = f"{title_theme}: The Impossible 3D Joint #Shorts"
            description = (
                "From the outside, this interlocking wooden joint appears physically impossible to assemble or dismantle.\n\n"
                "With diagonal dovetail pins showing on all four faces, geometry suggests the components must collide and bind instantly. "
                "The secret lies in an internal 45-degree sliding vector carved inside the block, allowing the puzzle components to glide "
                "seamlessly into an invisible mechanical lock.\n\n"
                "Craftsmanship Specifications:\n"
                "• Mechanism: 3D Multi-Way Sliding Dovetail Lock (鲁班锁)\n"
                "• Wood Species: Seasoned Dense Rosewood\n"
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

        # 5. Dougong, Architecture, Temple
        elif any(w in t for w in ["dougong", "bracket", "斗拱", "temple", "earthquake", "pavilion", "shrine"]):
            title = f"{title_theme}: Earthquake-Proof Ancient Architecture #Shorts"
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
                "temple architecture", "chinese carpentry", "interlocking timber",
                "timbercraft", "woodworking", "shorts"
            ]
            pinned_comment = "Ancient engineers solved earthquake resilience over 1,500 years ago using only wood. Incredible engineering! 👇"

        # 6. Chisel sharpness, end grain, blade restoration
        elif any(w in t for w in ["end_grain", "chisel", "sharpness", "blade", "plane", "slice", "shaving", "ribbon"]):
            title = f"{title_theme}: Slicing End Grain #Shorts"
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

        # 7. Generic dynamic fallback for any other craftsmanship topic
        else:
            clean = title_theme.replace("#Shorts", "").strip()
            title = f"{clean} #Shorts"
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
