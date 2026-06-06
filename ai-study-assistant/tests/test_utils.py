"""Tests for utility functions."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    clean_text,
    count_words,
    truncate_text,
    extract_key_terms,
    validate_api_key,
    split_into_chunks,
)


class TestCleanText:
    """Tests for the clean_text function."""

    def test_removes_extra_whitespace(self) -> None:
        """Test that multiple spaces are reduced to single."""
        result = clean_text("hello   world")
        assert result == "hello world"

    def test_normalizes_newlines(self) -> None:
        """Test that excessive newlines are reduced."""
        result = clean_text("hello\n\n\n\n\nworld")
        assert result == "hello\n\nworld"

    def test_strips_leading_trailing(self) -> None:
        """Test stripping whitespace from ends."""
        result = clean_text("   hello world   ")
        assert result == "hello world"

    def test_replaces_tabs(self) -> None:
        """Test tab replacement with spaces."""
        result = clean_text("hello\tworld")
        assert result == "hello    world"

    def test_empty_string(self) -> None:
        """Test with empty input."""
        result = clean_text("")
        assert result == ""


class TestCountWords:
    """Tests for the count_words function."""

    def test_basic_count(self) -> None:
        """Test counting words in a simple string."""
        assert count_words("hello world") == 2

    def test_empty_string(self) -> None:
        """Test with empty string."""
        assert count_words("") == 0

    def test_whitespace_only(self) -> None:
        """Test with whitespace-only string."""
        assert count_words("   ") == 0

    def test_multiple_spaces(self) -> None:
        """Test with multiple spaces between words."""
        assert count_words("one  two  three") == 3


class TestTruncateText:
    """Tests for the truncate_text function."""

    def test_short_text_unchanged(self) -> None:
        """Test that short text is returned as-is."""
        text = "Short text"
        assert truncate_text(text, 100) == text

    def test_long_text_truncated(self) -> None:
        """Test that long text is truncated."""
        text = "a" * 5000
        result = truncate_text(text, 100)
        assert len(result) <= 104  # 100 + "..."

    def test_cuts_at_sentence(self) -> None:
        """Test that truncation prefers sentence boundaries."""
        text = "First sentence. Second sentence. " + "x" * 3000
        result = truncate_text(text, 50)
        assert result.endswith(".")


class TestValidateApiKey:
    """Tests for the validate_api_key function."""

    def test_valid_key(self) -> None:
        """Test with a valid-format key."""
        assert validate_api_key("sk-" + "a" * 48) is True

    def test_empty_key(self) -> None:
        """Test with empty string."""
        assert validate_api_key("") is False

    def test_none_key(self) -> None:
        """Test with None."""
        assert validate_api_key(None) is False

    def test_wrong_prefix(self) -> None:
        """Test with wrong prefix."""
        assert validate_api_key("pk-" + "a" * 48) is False

    def test_too_short(self) -> None:
        """Test with key too short."""
        assert validate_api_key("sk-abc") is False


class TestExtractKeyTerms:
    """Tests for the extract_key_terms function."""

    def test_extracts_capitalized_words(self) -> None:
        """Test extracting capitalized terms."""
        text = "Python is a language. Machine Learning is popular. Python is great."
        terms = extract_key_terms(text)
        assert "Python" in terms
        assert "Machine Learning" in terms

    def test_empty_text(self) -> None:
        """Test with empty text."""
        terms = extract_key_terms("")
        assert terms == []

    def test_max_terms_limit(self) -> None:
        """Test respecting max_terms parameter."""
        text = " ".join([f"Term{i}" for i in range(50)])
        terms = extract_key_terms(text, max_terms=5)
        assert len(terms) <= 5


class TestSplitIntoChunks:
    """Tests for the split_into_chunks function."""

    def test_short_text_single_chunk(self) -> None:
        """Test that short text returns single chunk."""
        chunks = split_into_chunks("Short text", chunk_size=100)
        assert len(chunks) == 1

    def test_long_text_multiple_chunks(self) -> None:
        """Test that long text is split into multiple chunks."""
        text = "word " * 500
        chunks = split_into_chunks(text, chunk_size=100, overlap=20)
        assert len(chunks) > 1

    def test_overlap_between_chunks(self) -> None:
        """Test that chunks have overlapping content."""
        text = "A" * 300
        chunks = split_into_chunks(text, chunk_size=100, overlap=50)
        assert len(chunks) >= 3
