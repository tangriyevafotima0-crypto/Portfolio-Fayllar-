"""Configuration module for the Quiz Platform application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables.

    Attributes:
        SECRET_KEY: Flask secret key for session management.
        SQLALCHEMY_DATABASE_URI: Database connection string.
        SQLALCHEMY_TRACK_MODIFICATIONS: SQLAlchemy event tracking flag.
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///quiz.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    QUIZZES_PER_PAGE: int = 10
    MIN_PASSWORD_LENGTH: int = 6
