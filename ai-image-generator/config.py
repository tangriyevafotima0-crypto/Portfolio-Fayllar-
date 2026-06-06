"""Configuration module for the AI Image Generator."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables.

    Attributes:
        OPENAI_API_KEY: API key for OpenAI services.
        OUTPUT_DIR: Directory for saving generated images.
        DEFAULT_SIZE: Default image generation size.
    """

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "generated_images")
    DEFAULT_SIZE: str = "1024x1024"

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is set.

        Returns:
            True if configuration is valid.

        Raises:
            ValueError: If OPENAI_API_KEY is not set.
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True
