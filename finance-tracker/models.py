"""Data models for the Finance Tracker application."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import date
from typing import Optional
import uuid


class TransactionType(Enum):
    """Enum representing transaction types."""

    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    """Represents a financial transaction.

    Attributes:
        amount: Transaction amount in currency units.
        category: Category classification.
        transaction_type: Whether income or expense.
        description: Optional description or note.
        date: Date of the transaction (ISO format string).
        id: Unique transaction identifier.
    """

    amount: float
    category: str
    transaction_type: TransactionType
    description: str = ""
    date: str = field(default_factory=lambda: date.today().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        """Validate transaction data after initialization."""
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if not self.category:
            raise ValueError("Category is required")
        if isinstance(self.transaction_type, str):
            self.transaction_type = TransactionType(self.transaction_type)

    def to_dict(self) -> dict:
        """Convert transaction to a dictionary.

        Returns:
            Dictionary representation of the transaction.
        """
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "transaction_type": self.transaction_type.value,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create a Transaction from a dictionary.

        Args:
            data: Dictionary with transaction data.

        Returns:
            Transaction instance.

        Raises:
            ValueError: If required fields are missing.
        """
        return cls(
            amount=float(data["amount"]),
            category=data["category"],
            transaction_type=TransactionType(data["transaction_type"]),
            description=data.get("description", ""),
            date=data.get("date", date.today().isoformat()),
            id=data.get("id", str(uuid.uuid4()))
        )

    @staticmethod
    def get_default_categories(trans_type: TransactionType) -> list[str]:
        """Get default categories for a transaction type.

        Args:
            trans_type: The transaction type to get categories for.

        Returns:
            List of category names.
        """
        if trans_type == TransactionType.INCOME:
            return ["Salary", "Freelance", "Investments", "Gifts", "Other Income"]
        return [
            "Food & Dining", "Transportation", "Shopping",
            "Entertainment", "Bills & Utilities", "Health",
            "Education", "Travel", "Other Expense"
        ]


@dataclass
class Category:
    """Represents a spending category with budget tracking.

    Attributes:
        name: Category name.
        budget: Monthly budget limit for this category.
        color: Display color for charts (hex code).
    """

    name: str
    budget: float = 0.0
    color: str = "#3498db"

    def __post_init__(self) -> None:
        """Validate category data."""
        if not self.name:
            raise ValueError("Category name is required")
        if self.budget < 0:
            raise ValueError("Budget cannot be negative")
