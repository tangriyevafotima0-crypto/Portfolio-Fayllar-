"""Database manager for JSON/CSV persistence of transactions."""

import json
import csv
import io
from pathlib import Path
from typing import Optional
from models import Transaction, TransactionType


class DatabaseError(Exception):
    """Custom exception for database operations."""

    pass


class DatabaseManager:
    """Manages transaction data persistence using JSON and CSV formats.

    Provides CRUD operations for transactions with file-based storage.

    Attributes:
        data_file: Path to the JSON data file.
    """

    def __init__(self, data_dir: str = "data", filename: str = "transactions.json") -> None:
        """Initialize the database manager.

        Args:
            data_dir: Directory for storing data files.
            filename: Name of the JSON data file.
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the data file if it doesn't exist."""
        if not self.data_file.exists():
            self._save_data([])

    def _load_data(self) -> list[dict]:
        """Load raw transaction data from the JSON file.

        Returns:
            List of transaction dictionaries.

        Raises:
            DatabaseError: If file reading fails.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        except OSError as e:
            raise DatabaseError(f"Failed to read data file: {e}") from e

    def _save_data(self, data: list[dict]) -> None:
        """Save transaction data to the JSON file.

        Args:
            data: List of transaction dictionaries.

        Raises:
            DatabaseError: If file writing fails.
        """
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise DatabaseError(f"Failed to save data: {e}") from e

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to the database.

        Args:
            transaction: Transaction instance to add.

        Raises:
            DatabaseError: If saving fails.
        """
        data = self._load_data()
        data.append(transaction.to_dict())
        self._save_data(data)

    def get_all_transactions(self) -> list[Transaction]:
        """Retrieve all transactions from the database.

        Returns:
            List of Transaction objects sorted by date (newest first).
        """
        data = self._load_data()
        transactions = []
        for item in data:
            try:
                transactions.append(Transaction.from_dict(item))
            except (ValueError, KeyError):
                continue
        return sorted(transactions, key=lambda t: t.date, reverse=True)

    def get_transactions_by_type(self, trans_type: TransactionType) -> list[Transaction]:
        """Get transactions filtered by type.

        Args:
            trans_type: TransactionType to filter by.

        Returns:
            List of matching transactions.
        """
        all_transactions = self.get_all_transactions()
        return [t for t in all_transactions if t.transaction_type == trans_type]

    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction by ID.

        Args:
            transaction_id: Unique ID of the transaction to delete.

        Returns:
            True if deleted, False if not found.
        """
        data = self._load_data()
        original_count = len(data)
        data = [t for t in data if t.get("id") != transaction_id]

        if len(data) < original_count:
            self._save_data(data)
            return True
        return False

    def export_to_csv(self) -> Optional[str]:
        """Export all transactions to CSV format.

        Returns:
            CSV string of all transactions, or None if empty.
        """
        transactions = self.get_all_transactions()
        if not transactions:
            return None

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["date", "type", "category", "amount", "description"])

        for t in transactions:
            writer.writerow([
                t.date,
                t.transaction_type.value,
                t.category,
                t.amount,
                t.description
            ])

        return output.getvalue()

    def import_from_csv(self, csv_content: str) -> int:
        """Import transactions from CSV content.

        Args:
            csv_content: CSV string with transaction data.

        Returns:
            Number of successfully imported transactions.

        Raises:
            DatabaseError: If import fails.
        """
        reader = csv.DictReader(io.StringIO(csv_content))
        imported = 0

        for row in reader:
            try:
                transaction = Transaction(
                    amount=float(row["amount"]),
                    category=row["category"],
                    transaction_type=TransactionType(row["type"]),
                    description=row.get("description", ""),
                    date=row.get("date", "")
                )
                self.add_transaction(transaction)
                imported += 1
            except (ValueError, KeyError) as e:
                continue

        return imported
