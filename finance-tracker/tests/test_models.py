"""Tests for Finance Tracker data models."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Transaction, TransactionType, Category


class TestTransaction:
    """Tests for the Transaction dataclass."""

    def test_create_valid_transaction(self) -> None:
        """Test creating a valid transaction."""
        t = Transaction(
            amount=50.0,
            category="Food & Dining",
            transaction_type=TransactionType.EXPENSE
        )
        assert t.amount == 50.0
        assert t.category == "Food & Dining"
        assert t.transaction_type == TransactionType.EXPENSE

    def test_create_income_transaction(self) -> None:
        """Test creating an income transaction."""
        t = Transaction(
            amount=3000.0,
            category="Salary",
            transaction_type=TransactionType.INCOME
        )
        assert t.transaction_type == TransactionType.INCOME

    def test_invalid_amount_raises_error(self) -> None:
        """Test that zero or negative amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Transaction(amount=0, category="Food", transaction_type=TransactionType.EXPENSE)

    def test_negative_amount_raises_error(self) -> None:
        """Test that negative amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Transaction(amount=-10, category="Food", transaction_type=TransactionType.EXPENSE)

    def test_empty_category_raises_error(self) -> None:
        """Test that empty category raises ValueError."""
        with pytest.raises(ValueError, match="Category is required"):
            Transaction(amount=10, category="", transaction_type=TransactionType.EXPENSE)

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        t = Transaction(
            amount=25.0,
            category="Shopping",
            transaction_type=TransactionType.EXPENSE,
            description="Books"
        )
        d = t.to_dict()
        assert d["amount"] == 25.0
        assert d["category"] == "Shopping"
        assert d["transaction_type"] == "expense"
        assert d["description"] == "Books"

    def test_from_dict(self) -> None:
        """Test creating transaction from dictionary."""
        data = {
            "amount": 100.0,
            "category": "Salary",
            "transaction_type": "income",
            "description": "Monthly",
            "date": "2024-01-15"
        }
        t = Transaction.from_dict(data)
        assert t.amount == 100.0
        assert t.transaction_type == TransactionType.INCOME

    def test_get_default_expense_categories(self) -> None:
        """Test getting default expense categories."""
        categories = Transaction.get_default_categories(TransactionType.EXPENSE)
        assert "Food & Dining" in categories
        assert len(categories) > 0

    def test_get_default_income_categories(self) -> None:
        """Test getting default income categories."""
        categories = Transaction.get_default_categories(TransactionType.INCOME)
        assert "Salary" in categories


class TestCategory:
    """Tests for the Category dataclass."""

    def test_create_valid_category(self) -> None:
        """Test creating a valid category."""
        cat = Category(name="Food", budget=500.0)
        assert cat.name == "Food"
        assert cat.budget == 500.0

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Category name is required"):
            Category(name="")

    def test_negative_budget_raises_error(self) -> None:
        """Test that negative budget raises ValueError."""
        with pytest.raises(ValueError, match="Budget cannot be negative"):
            Category(name="Food", budget=-100)
