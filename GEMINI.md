# Workspace Rules & Channel Mapping Guidelines

## CRITICAL: Channel Identity & Account Isolation Rule

Always maintain strict separation between the user's automation projects. NEVER mix credentials, client_secrets, or authentication tokens across them.

### Channel 1: TimberCraft (Wood Working Automations)
- **Directory**: `c:\Antigravity Test Folder\Wood Working Automations`
- **Google Account**: `anikinuzir3@gmail.com`
- **YouTube Channel**: TimberCraft Archive / Anikin Uzir
- **Google Cloud Project**: `timbercraft-studio` (Project Number: `1051808411017`)
- **OAuth Client ID**: `1051808411017-u2ak3nq8ujttgns06om51eetibt86s5h.apps.googleusercontent.com`
- **Google Drive Buffer Folder**: `1kl4GK0BsNJU6cOaDZUwM29l0jF-NRQj7` ("YouTube Videos")
- **GitHub Repository**: `anikinuzir3wood/wood-working-automations`

### Channel 2: Avian Architects (Wildlife Documentary)
- **Directory**: `c:\Antigravity Test Folder\Avian Architects Automation`
- **Google Account**: `zeniusindividual@gmail.com`
- **YouTube Channel**: Avian Architects (`@TheAvianArchitects`)
- **GitHub Repository**: `thecraftorastudio-byte/avian-architects-automation`

---

## Mandatory Operational Protocols (TimberCraft)

### 1. Infinite Loop Autonomous Stock Refill (2-Day Advance Rule)
- **Watchdog Trigger**: Whenever remaining un-uploaded stock drops to `<= 4 videos` (2-day safety runway at 2 uploads/day), system automatically triggers replenishment.
- **Strict Video Screening**:
  - **Zero Hard Chinese Text**: Reject any video with prominent uneditable Chinese banners or center captions.
  - **Zero Commercial IP / Copyright**: Reject cartoon/anime characters (e.g. Naruto) and copyrighted trademarks. Pure craft action only (hands, chisels, saws, joints, turning, ASMR).
  - **Zero Duplicates**: Verify SHA-256 digital hash and Rednote ID against `processed_history.json` before accepting.
- **Direct Cloud Sync**: All accepted raw video files MUST be uploaded directly to Google Drive `YouTube Videos` folder (`1kl4GK0BsNJU6cOaDZUwM29l0jF-NRQj7`).
- **Embedded Analysis**: Embed pre-analyzed Gemini Vision data (`gemini-3.5-flash`), unique 4-part scripts, and clean English titles directly into `video_queue.json` and push to GitHub `master`.

### 2. White-Hat Pre-Flight Copyright Protocol
- **Initial Upload Status**: Always upload as strictly `UNLISTED`.
- **Content ID Buffer**: Enforce mandatory 3-minute (180s) pause for YouTube audio/visual fingerprint scan.
- **Copyright Inspection**: Query YouTube API status. If any claim or restriction exists, KEEP UNLISTED permanently to preserve 0-strike channel health.
- **Public Promotion**: Promote from `UNLISTED` to `PUBLIC` ONLY after 100% clean verification.

---

## Mandatory Reminder Protocol

Whenever instructing the user to log in, authenticate, configure Google Cloud APIs, or update GitHub secrets:
1. **ALWAYS explicitly specify both the Channel Name AND the exact Gmail address.**
2. **Warn the user clearly if they are about to log in, so they never select the wrong account by mistake.**
3. In all authentication scripts (`setup_auth.py`), display a bold warning banner with the expected email and channel before initiating the browser flow.
