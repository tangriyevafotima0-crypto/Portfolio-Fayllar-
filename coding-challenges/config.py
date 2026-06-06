"""Application configuration module."""

import os


class Config:
    """Configuration class for the Flask application.

    Loads settings from environment variables with sensible defaults
    for development.
    """

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///challenges.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = os.environ.get("FLASK_DEBUG", "1") == "1"
    CHALLENGES_DIR: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "challenges"
    )
    MAX_CODE_LENGTH: int = 10000
    EXECUTION_TIMEOUT: int = 5
    POINTS_EASY: int = 10
    POINTS_MEDIUM: int = 25
    POINTS_HARD: int = 50


class TestConfig(Config):
    """Testing configuration."""

    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    WTF_CSRF_ENABLED: bool = False
