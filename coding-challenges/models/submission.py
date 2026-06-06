"""Submission model for tracking user code submissions."""

from datetime import datetime
from typing import Optional

from app import db


class Submission(db.Model):
    """Represents a code submission for a challenge.

    Attributes:
        id: Unique identifier for the submission.
        user_id: Foreign key to the submitting user.
        challenge_id: Foreign key to the attempted challenge.
        code: The submitted source code.
        language: Programming language of the submission.
        passed: Whether all test cases passed.
        tests_passed: Number of test cases that passed.
        tests_total: Total number of test cases.
        points_earned: Points awarded for this submission.
        execution_time: Time taken to execute in seconds.
        error_message: Error message if execution failed.
        created_at: Timestamp of submission.
    """

    __tablename__ = "submissions"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id: int = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False
    )
    code: str = db.Column(db.Text, nullable=False)
    language: str = db.Column(db.String(20), default="python")
    passed: bool = db.Column(db.Boolean, default=False)
    tests_passed: int = db.Column(db.Integer, default=0)
    tests_total: int = db.Column(db.Integer, default=0)
    points_earned: int = db.Column(db.Integer, default=0)
    execution_time: Optional[float] = db.Column(db.Float, default=0.0)
    error_message: Optional[str] = db.Column(db.Text, default="")
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def get_result_summary(self) -> dict:
        """Get a summary of the submission result.

        Returns:
            Dictionary with pass/fail status and details.
        """
        return {
            "passed": self.passed,
            "tests_passed": self.tests_passed,
            "tests_total": self.tests_total,
            "points_earned": self.points_earned,
            "execution_time": f"{self.execution_time:.3f}s" if self.execution_time else "N/A",
            "error": self.error_message or None,
        }

    def get_pass_rate(self) -> float:
        """Calculate the percentage of tests passed.

        Returns:
            Percentage as a float between 0 and 100.
        """
        if self.tests_total == 0:
            return 0.0
        return (self.tests_passed / self.tests_total) * 100

    def __repr__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"<Submission #{self.id} [{status}] by User {self.user_id}>"
