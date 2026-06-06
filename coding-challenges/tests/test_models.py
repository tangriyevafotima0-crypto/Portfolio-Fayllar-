"""Tests for database models."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pytest
from app import create_app, db
from config import TestConfig
from models.user import User
from models.challenge import Challenge
from models.submission import Submission


@pytest.fixture
def app():
    """Create app for testing."""
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """Create a sample user."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def sample_challenge(app):
    """Create a sample challenge."""
    with app.app_context():
        challenge = Challenge(
            title="Test Challenge",
            description="A test challenge",
            difficulty="easy",
            category="arrays",
            test_cases=json.dumps([{"input": 1, "expected": 2}]),
            points=10,
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge


class TestUserModel:
    """Test suite for the User model."""

    def test_create_user(self, sample_user, app) -> None:
        """Test creating a new user."""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            assert user is not None
            assert user.email == "test@example.com"

    def test_password_hashing(self, sample_user, app) -> None:
        """Test password is properly hashed and verified."""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            assert user.check_password("password123") is True
            assert user.check_password("wrongpassword") is False

    def test_add_points(self, sample_user, app) -> None:
        """Test adding points to a user."""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            user.add_points(25)
            assert user.total_points == 25
            assert user.challenges_solved == 1

    def test_get_stats(self, sample_user, app) -> None:
        """Test getting user statistics."""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            stats = user.get_stats()
            assert stats["username"] == "testuser"
            assert stats["total_points"] == 0
            assert stats["challenges_solved"] == 0


class TestChallengeModel:
    """Test suite for the Challenge model."""

    def test_create_challenge(self, sample_challenge, app) -> None:
        """Test creating a new challenge."""
        with app.app_context():
            challenge = Challenge.query.first()
            assert challenge.title == "Test Challenge"
            assert challenge.difficulty == "easy"

    def test_get_test_cases(self, sample_challenge, app) -> None:
        """Test parsing test cases JSON."""
        with app.app_context():
            challenge = Challenge.query.first()
            cases = challenge.get_test_cases()
            assert len(cases) == 1
            assert cases[0]["input"] == 1
            assert cases[0]["expected"] == 2

    def test_difficulty_color(self, sample_challenge, app) -> None:
        """Test difficulty color mapping."""
        with app.app_context():
            challenge = Challenge.query.first()
            assert challenge.get_difficulty_color() == "text-green-500"

    def test_increment_solved(self, sample_challenge, app) -> None:
        """Test incrementing solved counter."""
        with app.app_context():
            challenge = Challenge.query.first()
            challenge.increment_solved()
            assert challenge.times_solved == 1


class TestSubmissionModel:
    """Test suite for the Submission model."""

    def test_get_result_summary(self, app) -> None:
        """Test submission result summary."""
        with app.app_context():
            submission = Submission(
                user_id=1,
                challenge_id=1,
                code="def solution(x): return x",
                passed=True,
                tests_passed=3,
                tests_total=3,
                points_earned=10,
                execution_time=0.05,
            )
            summary = submission.get_result_summary()
            assert summary["passed"] is True
            assert summary["tests_passed"] == 3
            assert summary["points_earned"] == 10

    def test_get_pass_rate(self, app) -> None:
        """Test pass rate calculation."""
        with app.app_context():
            submission = Submission(
                user_id=1,
                challenge_id=1,
                code="def solution(x): return x",
                tests_passed=2,
                tests_total=4,
            )
            assert submission.get_pass_rate() == 50.0

    def test_pass_rate_zero_tests(self, app) -> None:
        """Test pass rate with zero total tests."""
        with app.app_context():
            submission = Submission(
                user_id=1,
                challenge_id=1,
                code="def solution(x): return x",
                tests_passed=0,
                tests_total=0,
            )
            assert submission.get_pass_rate() == 0.0
