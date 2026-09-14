# Workspace Rules & Channel Mapping Guidelines

## CRITICAL: Channel Identity & Account Isolation Rule

Always maintain strict separation between the user's automation projects. NEVER mix credentials, client_secrets, or authentication tokens across them.

### Channel 1: TimberCraft (Wood Working Automations)
- **Directory**: `c:\Antigravity Test Folder\Wood Working Automations`
- **Google Account**: `anikinuzir3@gmail.com`
- **YouTube Channel**: TimberCraft Archive / Anikin Uzir
- **Google Cloud Project**: `timbercraft-archive` (Project Number: `642561120312`)
- **OAuth Client ID**: `642561120312-0irhu5s5ckofct4t41r7fb2co7qk8ctk.apps.googleusercontent.com`
- **GitHub Repository**: `anikinuzir3wood/wood-working-automations`

### Channel 2: Avian Architects (Wildlife Documentary)
- **Directory**: `c:\Antigravity Test Folder\Avian Architects Automation`
- **Google Account**: `zeniusindividual@gmail.com`
- **YouTube Channel**: Avian Architects (`@TheAvianArchitects`)
- **GitHub Repository**: `thecraftorastudio-byte/avian-architects-automation`

---

## Mandatory Reminder Protocol

Whenever instructing the user to log in, authenticate, configure Google Cloud APIs, or update GitHub secrets:
1. **ALWAYS explicitly specify both the Channel Name AND the exact Gmail address.**
2. **Warn the user clearly if they are about to log in, so they never select the wrong account by mistake.**
3. In all authentication scripts (`setup_auth.py`), display a bold warning banner with the expected email and channel before initiating the browser flow.
