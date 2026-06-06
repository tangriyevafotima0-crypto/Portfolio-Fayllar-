"""Tests for the QuizGenerator class."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from quiz_generator import QuizGenerator


class TestQuizGeneratorValidation:
    """Test input validation for QuizGenerator."""

    def test_empty_text_raises_error(self) -> None:
        """Test that empty text raises ValueError."""
        generator = QuizGenerator.__new__(QuizGenerator)
        generator.config = type("Config", (), {"MODEL_NAME": "test", "MAX_TOKENS": 100, "OPENAI_API_KEY": "sk-test"})()

        with pytest.raises(ValueError, match="Source text cannot be empty"):
            generator.generate_quiz("", 5)

    def test_invalid_num_questions_raises_error(self) -> None:
        """Test that invalid question count raises ValueError."""
        generator = QuizGenerator.__new__(QuizGenerator)
        generator.config = type("Config", (), {"MODEL_NAME": "test", "MAX_TOKENS": 100, "OPENAI_API_KEY": "sk-test"})()

        with pytest.raises(ValueError, match="Number of questions must be between"):
            generator.generate_quiz("Some text here", 0)

        with pytest.raises(ValueError, match="Number of questions must be between"):
            generator.generate_quiz("Some text here", 21)

    def test_validate_question_valid(self) -> None:
        """Test question validation with valid data."""
        generator = QuizGenerator.__new__(QuizGenerator)
        question = {
            "question": "What is Python?",
            "options": ["A language", "A snake", "A tool", "A game"],
            "correct_answer": 0,
        }
        assert generator._validate_question(question) is True

    def test_validate_question_missing_fields(self) -> None:
        """Test question validation with missing fields."""
        generator = QuizGenerator.__new__(QuizGenerator)
        question = {"question": "What is Python?"}
        assert generator._validate_question(question) is False

    def test_validate_question_invalid_options(self) -> None:
        """Test question validation with too few options."""
        generator = QuizGenerator.__new__(QuizGenerator)
        question = {
            "question": "What is Python?",
            "options": ["Only one"],
            "correct_answer": 0,
        }
        assert generator._validate_question(question) is False

    def test_parse_valid_json(self) -> None:
        """Test parsing valid JSON response."""
        generator = QuizGenerator.__new__(QuizGenerator)
        response = '[{"question": "Test?", "options": ["A", "B", "C", "D"], "correct_answer": 0}]'
        result = generator._parse_quiz_response(response)
        assert len(result) == 1
        assert result[0]["question"] == "Test?"

    def test_parse_invalid_json(self) -> None:
        """Test parsing invalid JSON returns fallback."""
        generator = QuizGenerator.__new__(QuizGenerator)
        result = generator._parse_quiz_response("not valid json at all")
        assert len(result) == 1
        assert "issue" in result[0]["question"].lower() or "try" in result[0]["question"].lower()
