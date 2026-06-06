"""Tests for Quiz Platform database models."""

import pytest
from models import User, Quiz, Question, Result


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, db) -> None:
        """Test creating a new user."""
        user = User(username="newuser", email="new@example.com")
        user.set_password("securepass")
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == "newuser"

    def test_password_hashing(self, sample_user) -> None:
        """Test that passwords are properly hashed."""
        assert sample_user.password_hash != "password123"
        assert sample_user.check_password("password123") is True
        assert sample_user.check_password("wrongpass") is False

    def test_get_average_score_no_results(self, sample_user) -> None:
        """Test average score returns 0 for users with no results."""
        assert sample_user.get_average_score() == 0.0

    def test_user_repr(self, sample_user) -> None:
        """Test user string representation."""
        assert "testuser" in repr(sample_user)


class TestQuizModel:
    """Tests for the Quiz model."""

    def test_create_quiz(self, db) -> None:
        """Test creating a new quiz."""
        quiz = Quiz(title="Test Quiz", description="A quiz", category="Math")
        db.session.add(quiz)
        db.session.commit()

        assert quiz.id is not None
        assert quiz.title == "Test Quiz"

    def test_get_question_count(self, sample_quiz) -> None:
        """Test question count for a quiz."""
        assert sample_quiz.get_question_count() == 1


class TestQuestionModel:
    """Tests for the Question model."""

    def test_check_answer_correct(self, sample_quiz, db) -> None:
        """Test checking a correct answer."""
        question = sample_quiz.questions.first()
        assert question.check_answer("b") is True

    def test_check_answer_incorrect(self, sample_quiz, db) -> None:
        """Test checking an incorrect answer."""
        question = sample_quiz.questions.first()
        assert question.check_answer("a") is False

    def test_check_answer_case_insensitive(self, sample_quiz, db) -> None:
        """Test that answer checking is case insensitive."""
        question = sample_quiz.questions.first()
        assert question.check_answer("B") is True
