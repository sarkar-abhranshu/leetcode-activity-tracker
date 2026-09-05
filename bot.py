"""
bot.py - Telegram bot command handler for manual workflow triggers.

Usage:
    python bot.py
"""

import logging
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("CHAT_ID", "").strip()
GH_PAT = os.environ.get("GH_PAT", "").strip()
GH_REPO = os.environ.get("GH_REPO", "").strip()  # Format: "username/repo"


def send_telegram_message(text: str) -> bool:
    """Send a message to Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


def trigger_github_workflow() -> bool:
    """Trigger the GitHub Actions workflow."""
    url = f"https://api.github.com/repos/{GH_REPO}/actions/workflows/run.yml/dispatches"
    headers = {
        "Authorization": f"token {GH_PAT}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "ref": "main",  # or "master" depending on your default branch
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        logger.info("Successfully triggered GitHub Actions workflow")
        return True
    except Exception as e:
        logger.error(f"Failed to trigger workflow: {e}")
        return False


def get_updates(offset: int = 0) -> dict:
    """Get updates from Telegram Bot API."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "offset": offset,
        "timeout": 30,
    }

    try:
        resp = requests.get(url, params=params, timeout=35)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"Failed to get updates: {e}")
        return {}


def handle_command(message: dict) -> None:
    """Handle incoming commands."""
    text = message.get("text", "")
    chat_id = str(message.get("chat", {}).get("id", ""))

    # Only respond to the configured chat
    if chat_id != CHAT_ID:
        logger.warning(f"Ignoring message from unauthorized chat: {chat_id}")
        return

    if text == "/fetch":
        logger.info("Received /fetch command")
        send_telegram_message("🔄 Triggering LeetCode tracker...")

        if trigger_github_workflow():
            send_telegram_message("✅ Workflow triggered! Check will run shortly.")
        else:
            send_telegram_message("❌ Failed to trigger workflow. Check logs.")

    elif text == "/help":
        help_text = """
*Available Commands:*
/fetch - Trigger LeetCode activity check
/help - Show this help message
        """
        send_telegram_message(help_text.strip())


def main():
    """Main bot loop."""
    # Validate configuration
    if not all([BOT_TOKEN, CHAT_ID, GH_PAT, GH_REPO]):
        logger.error("Missing required environment variables: BOT_TOKEN, CHAT_ID, GH_PAT, GH_REPO")
        sys.exit(1)

    logger.info("Bot started. Listening for commands...")
    send_telegram_message("🤖 Bot is online! Use /fetch to trigger checks.")

    offset = 0

    while True:
        try:
            data = get_updates(offset)

            if not data.get("ok"):
                logger.error(f"getUpdates failed: {data}")
                continue

            results = data.get("result", [])

            for update in results:
                offset = update["update_id"] + 1

                if "message" in update:
                    handle_command(update["message"])

        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")


if __name__ == "__main__":
    main()
