"""Tests for the DatabaseManager class."""

import pytest
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from models import Transaction, TransactionType


@pytest.fixture
def temp_db():
    """Create a temporary database manager for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = DatabaseManager(data_dir=tmpdir, filename="test_data.json")
        yield db


class TestDatabaseManager:
    """Tests for DatabaseManager operations."""

    def test_add_transaction(self, temp_db) -> None:
        """Test adding a transaction."""
        t = Transaction(
            amount=50.0,
            category="Food",
            transaction_type=TransactionType.EXPENSE
        )
        temp_db.add_transaction(t)

        transactions = temp_db.get_all_transactions()
        assert len(transactions) == 1
        assert transactions[0].amount == 50.0

    def test_get_empty_transactions(self, temp_db) -> None:
        """Test getting transactions from empty database."""
        transactions = temp_db.get_all_transactions()
        assert transactions == []

    def test_get_transactions_by_type(self, temp_db) -> None:
        """Test filtering transactions by type."""
        temp_db.add_transaction(Transaction(
            amount=100, category="Salary", transaction_type=TransactionType.INCOME
        ))
        temp_db.add_transaction(Transaction(
            amount=20, category="Food", transaction_type=TransactionType.EXPENSE
        ))

        incomes = temp_db.get_transactions_by_type(TransactionType.INCOME)
        assert len(incomes) == 1
        assert incomes[0].category == "Salary"

    def test_delete_transaction(self, temp_db) -> None:
        """Test deleting a transaction."""
        t = Transaction(
            amount=30, category="Shopping", transaction_type=TransactionType.EXPENSE
        )
        temp_db.add_transaction(t)

        result = temp_db.delete_transaction(t.id)
        assert result is True
        assert len(temp_db.get_all_transactions()) == 0

    def test_delete_nonexistent_transaction(self, temp_db) -> None:
        """Test deleting a transaction that doesn't exist."""
        result = temp_db.delete_transaction("fake-id-12345")
        assert result is False

    def test_export_to_csv(self, temp_db) -> None:
        """Test exporting transactions to CSV."""
        temp_db.add_transaction(Transaction(
            amount=100, category="Salary", transaction_type=TransactionType.INCOME
        ))
        csv_data = temp_db.export_to_csv()
        assert csv_data is not None
        assert "Salary" in csv_data
        assert "100" in csv_data

    def test_export_empty_returns_none(self, temp_db) -> None:
        """Test exporting empty database returns None."""
        assert temp_db.export_to_csv() is None
