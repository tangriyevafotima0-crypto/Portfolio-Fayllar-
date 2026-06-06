"""Challenge model for storing coding problems."""

import json
import os
from datetime import datetime
from typing import Optional

from app import db


class Challenge(db.Model):
    """Represents a coding challenge on the platform.

    Attributes:
        id: Unique identifier for the challenge.
        title: Challenge title displayed to users.
        description: Full problem description with examples.
        difficulty: Difficulty level (easy, medium, hard).
        category: Problem category (arrays, strings, math, etc.).
        test_cases: JSON string of input/output test cases.
        starter_code: Optional starter code template.
        points: Points awarded for solving.
        times_solved: Number of successful submissions.
        created_at: Timestamp of challenge creation.
    """

    __tablename__ = "challenges"

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    difficulty: str = db.Column(db.String(20), nullable=False, default="easy")
    category: str = db.Column(db.String(50), nullable=False, default="general")
    test_cases: str = db.Column(db.Text, nullable=False)
    starter_code: Optional[str] = db.Column(db.Text, default="")
    points: int = db.Column(db.Integer, default=10)
    times_solved: int = db.Column(db.Integer, default=0)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship("Submission", backref="challenge", lazy="dynamic")

    def get_test_cases(self) -> list[dict]:
        """Parse and return test cases as a list of dictionaries.

        Returns:
            List of test case dictionaries with 'input' and 'expected' keys.
        """
        try:
            return json.loads(self.test_cases)
        except json.JSONDecodeError:
            return []

    def get_difficulty_color(self) -> str:
        """Get CSS color class for the difficulty level.

        Returns:
            CSS class name for the difficulty badge.
        """
        colors = {
            "easy": "text-green-500",
            "medium": "text-yellow-500",
            "hard": "text-red-500",
        }
        return colors.get(self.difficulty, "text-gray-500")

    def increment_solved(self) -> None:
        """Increment the solved counter for this challenge."""
        self.times_solved += 1

    @classmethod
    def load_from_json(cls, filepath: str) -> "Challenge":
        """Create a Challenge instance from a JSON file.

        Args:
            filepath: Path to the JSON challenge file.

        Returns:
            New Challenge instance populated from the file data.

        Raises:
            FileNotFoundError: If the challenge file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Challenge file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(
            title=data["title"],
            description=data["description"],
            difficulty=data["difficulty"],
            category=data.get("category", "general"),
            test_cases=json.dumps(data["test_cases"]),
            starter_code=data.get("starter_code", ""),
            points=data.get("points", 10),
        )

    def __repr__(self) -> str:
        return f"<Challenge {self.title} [{self.difficulty}]>"
