"""
config.py - Central configuration for the LeetCode Competition Tracker.
All secrets are loaded from environment variables.
"""

import os

# ─────────────────────────────────────────────────────────────
# Telegram
# ─────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "").strip()
CHAT_ID: str = os.environ.get("CHAT_ID", "").strip()

# ─────────────────────────────────────────────────────────────
# LeetCode Usernames
# ─────────────────────────────────────────────────────────────
_DEFAULT_MY_USERNAME = "riceeater21"

_DEFAULT_OPPONENT_USERNAMES = [
    "Adarsh200IQ",
    "AbhishekSNair",
    "Akhilesh_M_2204",
    "onShoreApple",
    "anga205",
    "shakirth-anisha",
    "aman-khandelwal",
    "AkshatPrep",
    "abhay14505",
    "AmiteshSinha",
    "krthk200518",
    "KathitJoshi",
]

MY_USERNAME: str = os.environ.get("MY_USERNAME", "").strip() or _DEFAULT_MY_USERNAME

_opponents = os.environ.get("OPPONENT_USERNAMES", "").strip()

if _opponents:
    extra = [u.strip() for u in _opponents.split(",") if u.strip()]
    OPPONENT_USERNAMES = list(dict.fromkeys(_DEFAULT_OPPONENT_USERNAMES + extra))
else:
    OPPONENT_USERNAMES = _DEFAULT_OPPONENT_USERNAMES

# ─────────────────────────────────────────────────────────────
# GitHub Gist Storage
# ─────────────────────────────────────────────────────────────
GIST_ID: str = os.environ.get("GIST_ID", "").strip()
GIST_TOKEN: str = os.environ.get("GIST_TOKEN", "").strip()

# ─────────────────────────────────────────────────────────────
# Tracker Configuration
# ─────────────────────────────────────────────────────────────
INACTIVITY_ESCALATION_MINUTES: int = int(
    os.environ.get("INACTIVITY_ESCALATION_MINUTES", "60")
)

MAX_ALERT_AGE_HOURS: int = int(os.environ.get("MAX_ALERT_AGE_HOURS", "24"))


# ─────────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────────
def validate() -> None:
    """
    Validate required runtime configuration.
    """
    missing = []

    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")

    if not CHAT_ID:
        missing.append("CHAT_ID")

    if not GIST_ID:
        missing.append("GIST_ID")

    if not GIST_TOKEN:
        missing.append("GIST_TOKEN")

    if missing:
        raise EnvironmentError(
            "Missing required environment variables: " + ", ".join(missing)
        )
