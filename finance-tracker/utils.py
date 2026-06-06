"""Utility functions for formatting and validation."""

from datetime import date, datetime
from typing import Optional


def format_currency(amount: float, currency: str = "$") -> str:
    """Format a number as currency string.

    Args:
        amount: The monetary amount to format.
        currency: Currency symbol to use. Defaults to '$'.

    Returns:
        Formatted currency string (e.g., '$1,234.56').
    """
    if amount < 0:
        return f"-{currency}{abs(amount):,.2f}"
    return f"{currency}{amount:,.2f}"


def validate_amount(amount: float) -> float:
    """Validate a transaction amount.

    Args:
        amount: The amount to validate.

    Returns:
        The validated amount.

    Raises:
        ValueError: If amount is not positive or not a valid number.
    """
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    if amount > 1_000_000_000:
        raise ValueError("Amount exceeds maximum allowed value")
    return round(float(amount), 2)


def validate_date(date_string: str) -> str:
    """Validate a date string in ISO format.

    Args:
        date_string: Date string to validate (YYYY-MM-DD).

    Returns:
        Validated date string.

    Raises:
        ValueError: If date format is invalid.
    """
    try:
        parsed = datetime.strptime(date_string, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_string}'. Use YYYY-MM-DD.")


def get_month_name(date_string: str) -> str:
    """Extract month name from a date string.

    Args:
        date_string: Date in YYYY-MM-DD or YYYY-MM format.

    Returns:
        Full month name (e.g., 'January').
    """
    try:
        if len(date_string) == 7:
            date_string += "-01"
        parsed = datetime.strptime(date_string, "%Y-%m-%d")
        return parsed.strftime("%B %Y")
    except ValueError:
        return "Unknown"


def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage safely.

    Args:
        part: The portion value.
        total: The total value.

    Returns:
        Percentage value, or 0 if total is zero.
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)
