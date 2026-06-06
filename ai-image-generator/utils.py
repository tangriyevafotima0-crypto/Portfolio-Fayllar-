"""Utility functions for image processing and file operations."""

import os
import requests
from pathlib import Path


def save_image_from_url(url: str, filename: str, output_dir: str = "generated_images") -> str:
    """Download an image from a URL and save it locally.

    Args:
        url: URL of the image to download.
        filename: Desired filename (without extension).
        output_dir: Directory to save the image in.

    Returns:
        Full path to the saved image file.

    Raises:
        IOError: If the download or save operation fails.
        ValueError: If the URL or filename is empty.
    """
    if not url:
        raise ValueError("URL cannot be empty")
    if not filename:
        raise ValueError("Filename cannot be empty")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not filename.endswith(".png"):
        filename += ".png"

    filepath = output_path / filename

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return str(filepath)


def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable string.

    Args:
        size_bytes: File size in bytes.

    Returns:
        Formatted string (e.g., '2.5 MB').
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def validate_prompt(prompt: str, max_length: int = 4000) -> str:
    """Validate and sanitize an image generation prompt.

    Args:
        prompt: Raw user input prompt.
        max_length: Maximum allowed prompt length.

    Returns:
        Cleaned and validated prompt string.

    Raises:
        ValueError: If prompt is empty or exceeds max length.
    """
    cleaned = prompt.strip()

    if not cleaned:
        raise ValueError("Prompt cannot be empty")

    if len(cleaned) > max_length:
        raise ValueError(f"Prompt exceeds maximum length of {max_length} characters")

    return cleaned
