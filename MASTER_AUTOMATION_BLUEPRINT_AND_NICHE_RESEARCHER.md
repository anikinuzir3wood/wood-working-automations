# MASTER NICHE RESEARCH & CHANNEL AUTOMATION ENGINE
## Universal Blueprint for High-RPM YouTube Shorts & Documentaries (US Tier-1 Market)

> **Instructions for the AI Assistant:**
> When this file is provided with a specified niche at the bottom, you must fully absorb the creator's non-negotiable standards, timings, editing philosophy, and safety rules defined in **Part 1 to Part 5**. Then, execute the deep research protocol in **Part 6** by searching Rednote (Xiaohongshu) / TikTok / Douyin, auditing accounts frame-by-frame, and delivering 7 to 10 verified, zero-watermark creator profiles along with custom audio, SEO, and editing requirements for that exact niche.

---

# PART 1: GLOBAL BRANDING, AUDIENCE & RETENTION STRATEGY

1. **Target Market:** **United States (Tier-1)**
   * All content, scripts, humor, pacing, and metadata must be tailored exclusively to US viewer psychology.
   * Maximizes AdSense RPM ($4.00 – $8.00+ in documentary/craft/nature niches).

2. **Publishing Frequency (Strict Anti-Spam Cadence):**
   * **Exactly 2 Shorts Per Day** (No spamming; quality & high retention over volume).
   * **Strict 6-Hour Gap** between uploads so videos never cannibalize each other's algorithm traffic.

3. **Golden US Timezone Schedule (Eastern Time EDT - 48% US Population):**
   * **Slot 1 (US Afternoon Peak):** `2:00 PM EDT` *(Indian Time: 11:30 PM IST)*
   * **Slot 2 (US Prime Evening Peak):** `8:00 PM EDT` *(Indian Time: 5:30 AM IST next morning)*
   * **Humanized Anti-Bot Jitter:** Every automated upload MUST include a random `1 to 10 minute` delay so timestamps appear 100% organic and natural to platform algorithms.

4. **Retention Sweet-Spot Duration (30s to 45s Rule):**
   * **Optimal Length:** Strictly **30 to 45 seconds**.
   * **Algorithmic Science:** YouTube Shorts algorithm virality requires **VVSA (Viewed vs Swiped Away) > 75%** and **APV (Average Percentage Viewed) > 100%** (looping).
   * 55–60s videos suffer from high drop-off rates, whereas 30–42s videos have a 3x higher probability of being re-watched and looped, unlocking algorithmic surges.

5. **The Long-Form Expansion Flywheel (Cash-Cow Model):**
   * Daily Shorts act as the discovery engine to rapidly build 10k–50k subscribers.
   * Every 2 to 3 weeks, compile the top-performing 8 to 12 Short chapters into a **Master 8–10 Minute Long-Form Documentary** with cinematic transitions and grand orchestral scoring.
   * Connect each Short to the Master Documentary using YouTube's native **"Related Video"** button to funnel mobile viewers into high-RPM mid-roll ad revenue.

---

# PART 2: VISUAL QUALITY, TRANSFORMATIVE EDITING & YPP MONETIZATION GUARD

1. **Format Specifications:**
   * Vertical `1080x1920` (9:16 aspect ratio), render target `60 FPS`.
   * Smart 8% Crop & Subtle Zoom (`crop_factor = 0.92`) to clear edge artifacts and establish a unique digital visual hash.
   * Color Enhancement: +12% to +18% contrast, +20% to +25% saturation, and unsharp masking for razor-sharp micro-detail.

2. **YouTube Partner Program (YPP) "Reused Content" Protection (Multi-Source Storytelling Rule):**
   * **The Risk:** Taking a single uninterrupted clip from third-party platforms (even without watermarks) and simply slapping voiceover on top can lead to monetization rejection under YouTube's "Reused Content without significant creative transformation" policy.
   * **The Solution (Mandatory Transformation Standard):**
     * **Multi-Clip Intercutting:** Every Short must combine **2 to 3 distinct angles or source micro-clips** with dynamic 3–4 second cuts.
     * **Subtle Motion & Zoom:** Use gentle push-in zoom ramping (1.0x -> 1.08x) or horizontal mirror flipping on select non-text b-roll clips.
     * **Original Narrative Architecture:** The pacing and story order must be completely reorganized into an original, dramatic documentary arc that cannot be matched to any single original video.

3. **Watermark Filtering Rules (Updated):**
   * **HARD REJECT:** Any video with **bouncing/jumping/floating watermarks** that move across the frame. These are impossible to remove cleanly.
   * **ALLOWED (with edit):** Small **static watermarks** in a corner can be cropped or masked out during the 8% smart crop phase.
   * **ALLOWED (with trim):** If the video **thumbnail/first frame has text** but the actual video content is clean, simply **trim the thumbnail intro portion** (first 1-2 seconds) and use the clean remainder.
   * **ALLOWED (with caption swap):** If the video has **Chinese captions/subtitles burned in**, apply a **localized blur mask** over the original caption area and overlay our own **English narration captions** on top. This both removes the foreign text and adds original editorial value.
   * **Qualified (Goldmine):** 100% pure camera recordings, clean telephoto/macro optics, zero subtitles, and natural field sound.

4. **Pacing & Hook Philosophy:**
   * **First 1.5 Seconds Rule:** Immediate high-stakes physical action. No generic intros, no logo animations, no Wikipedia-style factual statements.
   * **Visual Transformation:** The viewer must witness progressive craftsmanship from raw material to impossible finished creation.

---

# PART 3: AUDIO ARCHITECTURE & DYNAMIC SIDECHAIN DUCKING

1. **Voice Persona:**
   * **Tone:** Authoritative, calm, curious, and awe-inspiring (Discovery Channel / National Geographic / BBC Earth style).
   * **Accent:** Neutral American Baritone.
   * **Cadence:** Unhurried, deliberate delivery with slow pacing (`rate = -4%`, `pitch = -2Hz`).

2. **Legal & Copyright Safety (Zero Celebrity Clones):**
   * **STRICT PROHIBITION:** Never clone living or famous celebrity voices (e.g. David Attenborough, Morgan Freeman). Avoids YouTube AI-Impersonation strikes and California Right of Publicity violations.
   * **Approved Engine:** Commercially licensed broadcast neural voices (e.g. `en-US-ChristopherNeural`, `en-US-AndrewNeural`) or licensed professional voice actors.

3. **Broadcast Studio Mastering Chain (FFmpeg Audio Filter):**
   Every voiceover must undergo studio post-processing before final muxing:
   * `highpass=f=80`: Removes low-end rumble and microphone pops.
   * `equalizer=f=140:t=q:w=1.2:g=2.8`: Deep chest warmth and broadcast resonance.
   * `equalizer=f=3500:t=q:w=1.5:g=2.2`: Consonant presence and crystal-clear diction for mobile phone speakers.
   * `acompressor`: Studio dynamic compression to balance whispers and loud moments.
   * `alimiter=limit=-1dB`: Prevents digital clipping and distortion.

4. **Dynamic Sidechain Ducking (`sidechaincompress`):**
   * **The Upgrade:** Instead of a static `-22dB` volume cut (which makes background music sound dead or thin), use FFmpeg's **`sidechaincompress`** filter!
   * **How It Operates:** The voiceover audio serves as the trigger signal. When narration speaks, the background music dynamically compresses by 14–16dB. During natural speech pauses and dramatic beats, the music swells up organically to fill the silence, creating a genuine BBC/Netflix documentary sonic texture!

---

# PART 4: HIGH-CTR HONEST THUMBNAILS & SHORTS FEED BAKE-IN STRATEGY

1. **100% Honest & Authentic:**
   * Extracted directly from the **authentic raw footage** at peak action (35%–40% duration mark).
   * Never use fake CGI, cartoonish AI, exaggerated arrows, or misleading clickbait that violates YouTube Creator Policies.

2. **Shorts Mobile App Thumbnail Limitation & Bake-In Strategy:**
   * **The Reality:** YouTube Data API v3 `thumbnails().set()` works reliably for desktop/search, but the YouTube mobile app's Shorts shelf frequently overrides custom API thumbnails and picks a frame directly from the video stream!
   * **The Bulletproof Fix (Timeline Bake-In):**
     * In addition to uploading the custom thumbnail via API, the video rendering pipeline **bakes the clean Masthead Text Banner directly onto Frame 0.0s – 1.0s of the MP4 video timeline**!
     * If YouTube's mobile algorithm defaults to the first frame or peak action frame, the viewer on the mobile Shorts feed STILL sees the bold, high-CTR masthead title banner!

3. **Masthead Safezone Placement (`y=110`):**
   * Text banner MUST sit in the top foliage/background safezone (`y=110`).
   * **NEVER cover the main subject:** The central subject, focal action, and fine craftsmanship must remain 100% visible and unobstructed.
   * Completely avoids collision with YouTube Shorts bottom overlays (title, avatar, subscribe button, audio tag).

4. **World-Standard Typography (WCAG 21:1 Contrast):**
   * **Font Color:** Crisp Pure White (`#FFFFFF`).
   * **Backdrop:** 85% Deep Black pillbox banner with 24px padding (`boxcolor=black@0.85:boxborderw=24`).
   * **Border:** 2px solid black outline for maximum edge definition.
   * **Dynamic Font Scaling:**
     * Short text (≤ 17 chars): `84pt Heavy Bold` (e.g., `THE MASTER WEAVER`)
     * Medium text (18–23 chars): `68pt Bold` (e.g., `NATURE'S ANCIENT MASON`)
     * Long text (> 23 chars): `56pt Bold`

---

# PART 5: WHITE-HAT SEO & METADATA ARCHITECTURE

1. **Title Formula:**
   * Clean, intriguing, curiosity-driven titles under 70 characters without spammy all-caps.
   * Example: *"The Master Knot: How Weaver Birds Build Architectural Marvels"*

2. **Structured Documentary Description:**
   * **Paragraph 1:** Engaging narrative hook explaining the physical biomechanics / craftsmanship.
   * **Specifications Section:** Subject scientific/formal name, materials used, duration, unique structural features.
   * **Call to Action:** Clean subscribe prompt for the channel handle.
   * **Curated Tags & Hashtags:** Tier-1 search tags + 5 to 7 niche-specific hashtags (e.g., `#Shorts #Documentary #Craftsmanship`).

3. **Pre-Flight Copyright Guard:**
   * Upload first as `UNLISTED`.
   * Wait 3 minutes for YouTube Content ID to scan for audio/visual claims.
   * Automatically promote to `PUBLIC` only if 100% clean with zero claims.

---

# PART 6: DEEP RESEARCH & AUDITING PROTOCOL (AI EXECUTION INSTRUCTIONS)

When a specific niche is entered in **Part 7 below**, you must perform the following autonomous research workflow:

1. **Search Query Matrix Generation:**
   * Generate 10+ advanced search terms in Chinese (for Rednote/Xiaohongshu and Douyin) and English (for TikTok).
   * Include terms for raw footage (`无字幕`, `4K实拍`, `原声`), craftsmanship full process (`全过程`), and high-retention close-ups.

2. **Discover & Audit 7 to 10 Creator Accounts:**
   * For each discovered account, extract:
     * Creator Name & Platform Profile URL
     * Platform User ID
     * Content Focus & Craftsmanship Style
     * Cleanliness Rating (1 to 10) and Watermark Audit (Pass / Fail)
     * Cross-platform check (Confirm whether they already have an active YouTube/Instagram presence to prevent duplicate uploads).

3. **Niche Production Complexity Analysis:**
   * Determine whether this niche requires:
     * **Light Processing:** Direct clean footage + multi-clip cuts + voiceover + masthead thumbnail.
     * **Heavy Re-Editing:** 1–3s micro-cuts, mirror flips, custom sound Foley reconstruction, or Seedance AI b-roll intercuts.

4. **Audio & Music Prompt Package:**
   * Provide custom Suno AI / ai33.pro prompts tailored to the acoustics and mood of this specific niche.

---

# PART 7: YOUR NICHE INPUT (FILL BELOW TO EXECUTE)

*(Enter your new niche or channel idea below. You can provide any topic — from wildlife and ancient woodworking to miniature cooking, mechanical restoration, or kinetic art. Once filled, instruct the AI to execute the research!)*

```text
================================================================================
NEW CHANNEL NICHE INPUT FORM
================================================================================

1. NICHE / TOPIC NAME     : [Enter your niche topic here, e.g. "Japanese Traditional Woodworking - Kumiko Joinery"]
2. TARGET PLATFORM        : [e.g. YouTube Shorts + Long-form Compilation]
3. PRIMARY TONE           : [e.g. ASMR Satisfying / BBC Earth Documentary / Mind-Blowing Engineering]
4. SPECIFIC PREFERENCES   : [e.g. Pure ASMR sound with minimal voiceover, OR full Attenborough-style educational narration]
5. SPECIAL CONSTRAINTS    : [e.g. Focus exclusively on raw wooden chisel carving, no modern power tools]

================================================================================
```
