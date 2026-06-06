"""Main routes for the Quiz Platform homepage and dashboard."""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Quiz, Result

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Display the landing page with featured quizzes."""
    recent_quizzes = Quiz.query.order_by(Quiz.created_at.desc()).limit(6).all()
    total_quizzes = Quiz.query.count()
    return render_template(
        "index.html",
        quizzes=recent_quizzes,
        total_quizzes=total_quizzes
    )


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Display user dashboard with statistics and history.

    Shows:
        - Total quizzes taken
        - Average score
        - Recent results
        - Category breakdown
    """
    results = Result.query.filter_by(user_id=current_user.id).order_by(
        Result.completed_at.desc()
    ).all()

    total_taken = len(results)
    avg_score = current_user.get_average_score()
    recent_results = results[:5]

    best_score = max((r.score for r in results), default=0)

    return render_template(
        "dashboard.html",
        total_taken=total_taken,
        avg_score=avg_score,
        best_score=best_score,
        recent_results=recent_results
    )
