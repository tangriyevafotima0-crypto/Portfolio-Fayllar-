"""Pytest fixtures for the Quiz Platform tests."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db as _db, User, Quiz, Question


class TestConfig:
    """Test configuration for the Quiz Platform."""

    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    MIN_PASSWORD_LENGTH = 6
    QUIZZES_PER_PAGE = 10


@pytest.fixture
def app():
    """Create application for testing."""
    application = create_app(TestConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Provide database session for tests."""
    with app.app_context():
        yield _db


@pytest.fixture
def sample_user(db) -> User:
    """Create a sample user for testing."""
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_quiz(db) -> Quiz:
    """Create a sample quiz with questions for testing."""
    quiz = Quiz(
        title="Sample Quiz",
        description="A test quiz",
        category="Science"
    )
    db.session.add(quiz)
    db.session.commit()

    question = Question(
        quiz_id=quiz.id,
        text="What is 2 + 2?",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="6",
        correct_answer="b"
    )
    db.session.add(question)
    db.session.commit()
    return quiz
