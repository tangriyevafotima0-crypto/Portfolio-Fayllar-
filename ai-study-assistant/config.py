"""Configuration module for the AI Study Assistant."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables.

    Attributes:
        OPENAI_API_KEY: API key for OpenAI services.
        MODEL_NAME: Name of the language model to use.
        MAX_TOKENS: Maximum tokens per API response.
        TEMPERATURE: Creativity parameter for responses.
        APP_TITLE: Display title for the Streamlit app.
    """

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    APP_TITLE: str = "AI Study Assistant"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
