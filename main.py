"""
main.py
-------
Entry point for the YouTube Shorts Bot.

Run this file to start the bot:
    python main.py

Currently (Phase 1): Only verifies that the project structure
and configuration are set up correctly. More phases will be
connected here as they are built.
"""

import sys
from utils import get_logger
from config import config

logger = get_logger(__name__)


def check_environment() -> bool:
    """
    Verifies that the environment is set up correctly before running.

    Returns:
        True if everything looks good, False if there are problems.
    """
    logger.info("🔍 Checking environment setup...")

    problems = []

    # Check required config values
    required_fields = [
        ("YOUTUBE_API_KEY", config.YOUTUBE_API_KEY),
        ("YOUTUBE_CLIENT_ID", config.YOUTUBE_CLIENT_ID),
        ("YOUTUBE_CLIENT_SECRET", config.YOUTUBE_CLIENT_SECRET),
        ("TARGET_CHANNEL_URL", config.TARGET_CHANNEL_URL),
        ("UPLOAD_CHANNEL_ID", config.UPLOAD_CHANNEL_ID),
    ]

    for field_name, field_value in required_fields:
        if not field_value:
            problems.append(f"Missing required config: {field_name}")

    if problems:
        logger.error("❌ Environment check failed:")
        for problem in problems:
            logger.error(f"   • {problem}")
        logger.error("👉 Please create a .env file based on .env.example")
        return False

    logger.info("✅ Environment check passed!")
    return True


def main():
    """Main entry point."""
    logger.info("=" * 50)
    logger.info("🎬 YouTube Shorts Bot — Starting Up")
    logger.info("=" * 50)

    # Print config summary (no secrets shown)
    logger.info("📋 Current Configuration:\n" + config.summary())

    # Check that everything is set up
    if not check_environment():
        logger.critical("Cannot start bot — fix the issues above first.")
        sys.exit(1)

    logger.info("✅ Phase 1 complete — architecture is ready.")
    logger.info("⏳ Waiting for Phase 2: Channel Monitoring...")


if __name__ == "__main__":
    main()