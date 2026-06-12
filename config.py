"""
config.py
---------
Central configuration loader for the YouTube Shorts Bot.

Reads all settings from the .env file and makes them available
to every other module. This means secrets never get hardcoded.

Usage:
    from config import config
    print(config.TARGET_CHANNEL_URL)
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file from the project root
load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """
    Holds all configuration values loaded from environment variables.
    Raises clear errors if required values are missing.
    """

    def __init__(self):
        # --- YouTube API ---
        self.YOUTUBE_API_KEY: str = self._require("YOUTUBE_API_KEY")
        self.YOUTUBE_CLIENT_ID: str = self._require("YOUTUBE_CLIENT_ID")
        self.YOUTUBE_CLIENT_SECRET: str = self._require("YOUTUBE_CLIENT_SECRET")

        # --- Channel Settings ---
        self.TARGET_CHANNEL_URL: str = self._require("TARGET_CHANNEL_URL")
        self.UPLOAD_CHANNEL_ID: str = self._require("UPLOAD_CHANNEL_ID")

        # --- Optional: OpenAI ---
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

        # --- Bot Behavior ---
        self.CHECK_INTERVAL_MINUTES: int = int(
            os.getenv("CHECK_INTERVAL_MINUTES", "30")
        )
        self.MAX_SHORT_DURATION_SECONDS: int = int(
            os.getenv("MAX_SHORT_DURATION_SECONDS", "59")
        )
        self.MIN_CLIP_DURATION_SECONDS: int = int(
            os.getenv("MIN_CLIP_DURATION_SECONDS", "15")
        )

        # --- Folder Paths ---
        self.MUSIC_FOLDER: Path = Path(os.getenv("MUSIC_FOLDER", "./music/tracks"))
        self.DOWNLOADS_FOLDER: Path = Path(os.getenv("DOWNLOADS_FOLDER", "./downloads"))
        self.OUTPUT_FOLDER: Path = Path(os.getenv("OUTPUT_FOLDER", "./output"))

        # Create folders if they don't exist
        self._ensure_folders()

    def _require(self, key: str) -> str:
        """
        Reads a required environment variable.
        If it's missing, logs a warning (won't crash at import time).
        """
        value = os.getenv(key, "")
        if not value:
            logger.warning(
                f"⚠️  Environment variable '{key}' is not set. "
                f"Please add it to your .env file."
            )
        return value

    def _ensure_folders(self):
        """Creates output folders if they don't already exist."""
        for folder in [self.MUSIC_FOLDER, self.DOWNLOADS_FOLDER, self.OUTPUT_FOLDER]:
            folder.mkdir(parents=True, exist_ok=True)
            logger.debug(f"📁 Ensured folder exists: {folder}")

    def is_openai_enabled(self) -> bool:
        """Returns True if an OpenAI API key has been provided."""
        return bool(self.OPENAI_API_KEY)

    def summary(self) -> str:
        """Returns a human-readable config summary (no secrets)."""
        return (
            f"Target Channel  : {self.TARGET_CHANNEL_URL}\n"
            f"Check Interval  : every {self.CHECK_INTERVAL_MINUTES} minutes\n"
            f"Short Duration  : {self.MIN_CLIP_DURATION_SECONDS}–{self.MAX_SHORT_DURATION_SECONDS}s\n"
            f"Music Folder    : {self.MUSIC_FOLDER}\n"
            f"Downloads Folder: {self.DOWNLOADS_FOLDER}\n"
            f"Output Folder   : {self.OUTPUT_FOLDER}\n"
            f"OpenAI Enabled  : {self.is_openai_enabled()}\n"
        )


# Create a single shared instance — import this everywhere
config = Config()