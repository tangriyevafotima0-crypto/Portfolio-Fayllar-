"""User model for the coding challenges platform."""

from datetime import datetime
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """Represents a registered user on the platform.

    Attributes:
        id: Unique identifier for the user.
        username: Display name chosen by the user.
        email: User's email address.
        password_hash: Hashed password for authentication.
        bio: Optional user biography.
        total_points: Accumulated points from solved challenges.
        challenges_solved: Number of challenges successfully completed.
        created_at: Timestamp of account creation.
    """

    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(256), nullable=False)
    bio: Optional[str] = db.Column(db.Text, default="")
    total_points: int = db.Column(db.Integer, default=0)
    challenges_solved: int = db.Column(db.Integer, default=0)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship("Submission", backref="author", lazy="dynamic")

    def set_password(self, password: str) -> None:
        """Hash and store the user's password.

        Args:
            password: Plain text password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash.

        Args:
            password: Plain text password to verify.

        Returns:
            True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def add_points(self, points: int) -> None:
        """Add points to the user's total score.

        Args:
            points: Number of points to add.
        """
        self.total_points += points
        self.challenges_solved += 1

    def get_stats(self) -> dict:
        """Get user statistics summary.

        Returns:
            Dictionary containing user stats.
        """
        return {
            "username": self.username,
            "total_points": self.total_points,
            "challenges_solved": self.challenges_solved,
            "member_since": self.created_at.strftime("%B %Y"),
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """Load a user by their ID for Flask-Login.

    Args:
        user_id: String representation of the user's ID.

    Returns:
        User instance or None if not found.
    """
    return User.query.get(int(user_id))
