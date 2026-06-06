"""Utility functions for text processing and validation."""

import re
from typing import Optional


def clean_text(text: str) -> str:
    """Clean and normalize input text for processing.

    Removes excessive whitespace, normalizes line breaks,
    and strips leading/trailing whitespace.

    Args:
        text: Raw input text to clean.

    Returns:
        Cleaned and normalized text string.
    """
    text = text.strip()
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'\t', '    ', text)
    return text


def count_words(text: str) -> int:
    """Count the number of words in a text string.

    Args:
        text: The text to count words in.

    Returns:
        Number of words as an integer.
    """
    if not text.strip():
        return 0
    return len(text.split())


def truncate_text(text: str, max_length: int = 3000) -> str:
    """Truncate text to a maximum character length.

    Tries to cut at a sentence boundary to preserve readability.

    Args:
        text: The text to truncate.
        max_length: Maximum number of characters.

    Returns:
        Truncated text, with ellipsis if cut.
    """
    if len(text) <= max_length:
        return text

    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')

    cut_point = max(last_period, last_newline)
    if cut_point > max_length * 0.7:
        return truncated[:cut_point + 1]

    return truncated + "..."


def extract_key_terms(text: str, max_terms: int = 20) -> list[str]:
    """Extract potential key terms from text based on capitalization and frequency.

    Args:
        text: The text to extract terms from.
        max_terms: Maximum number of terms to return.

    Returns:
        List of key terms found in the text.
    """
    words = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)

    word_freq: dict[str, int] = {}
    for word in words:
        if len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1

    sorted_terms = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [term for term, freq in sorted_terms[:max_terms]]


def validate_api_key(api_key: Optional[str]) -> bool:
    """Validate that an API key has the expected format.

    Args:
        api_key: The API key string to validate.

    Returns:
        True if the key appears to be valid format.
    """
    if not api_key:
        return False
    if not api_key.startswith("sk-"):
        return False
    if len(api_key) < 20:
        return False
    return True


def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks for processing.

    Args:
        text: The text to split.
        chunk_size: Maximum characters per chunk.
        overlap: Number of overlapping characters between chunks.

    Returns:
        List of text chunks.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            cut_point = max(last_period, last_newline)
            if cut_point > chunk_size * 0.5:
                chunk = chunk[:cut_point + 1]
                end = start + cut_point + 1

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks
