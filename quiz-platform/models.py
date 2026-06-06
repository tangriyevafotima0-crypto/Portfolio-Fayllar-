"""Database models for the Quiz Platform."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and quiz participation.

    Attributes:
        id: Unique user identifier.
        username: Display name for the user.
        email: User's email address.
        password_hash: Hashed password for security.
        created_at: Account creation timestamp.
        results: Related quiz results.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship("Result", backref="user", lazy="dynamic")

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.

        Args:
            password: Plain text password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash.

        Args:
            password: Plain text password to verify.

        Returns:
            True if password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def get_average_score(self) -> float:
        """Calculate the user's average quiz score.

        Returns:
            Average score as a percentage, or 0 if no results.
        """
        results = self.results.all()
        if not results:
            return 0.0
        total = sum(r.score for r in results)
        return round(total / len(results), 1)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Quiz(db.Model):
    """Quiz model containing questions and metadata.

    Attributes:
        id: Unique quiz identifier.
        title: Quiz title.
        description: Brief description of the quiz.
        category: Quiz category for filtering.
        created_at: Creation timestamp.
        questions: Related questions.
    """

    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default="General")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship("Question", backref="quiz", lazy="dynamic",
                                cascade="all, delete-orphan")
    results = db.relationship("Result", backref="quiz", lazy="dynamic")

    def get_question_count(self) -> int:
        """Get the number of questions in this quiz.

        Returns:
            Total number of questions.
        """
        return self.questions.count()

    def __repr__(self) -> str:
        return f"<Quiz {self.title}>"


class Question(db.Model):
    """Individual question within a quiz.

    Attributes:
        id: Unique question identifier.
        quiz_id: Foreign key to parent quiz.
        text: The question text.
        option_a: First answer option.
        option_b: Second answer option.
        option_c: Third answer option.
        option_d: Fourth answer option.
        correct_answer: Letter of the correct option (a/b/c/d).
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

    def check_answer(self, answer: str) -> bool:
        """Check if the provided answer is correct.

        Args:
            answer: The user's answer (a, b, c, or d).

        Returns:
            True if the answer is correct.
        """
        return answer.lower() == self.correct_answer.lower()

    def __repr__(self) -> str:
        return f"<Question {self.id}: {self.text[:30]}>"


class Result(db.Model):
    """Quiz result tracking user performance.

    Attributes:
        id: Unique result identifier.
        user_id: Foreign key to the user.
        quiz_id: Foreign key to the quiz.
        score: Percentage score achieved.
        total_questions: Number of questions in the quiz.
        correct_answers: Number of correct answers.
        completed_at: Timestamp when the quiz was completed.
    """

    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score = db.Column(db.Float, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Result user={self.user_id} quiz={self.quiz_id} score={self.score}%>"
