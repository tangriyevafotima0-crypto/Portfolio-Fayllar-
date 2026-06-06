"""Leaderboard routes for rankings and statistics."""

from flask import Blueprint, render_template, request

from models.user import User
from models.challenge import Challenge
from models.submission import Submission
from app import db

leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@leaderboard_bp.route("/")
def global_leaderboard():
    """Display the global leaderboard ranked by total points.

    Query Parameters:
        page: Page number for pagination (default: 1).
    """
    page = request.args.get("page", 1, type=int)
    per_page = 20

    users = (
        User.query.filter(User.total_points > 0)
        .order_by(User.total_points.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return render_template("leaderboard.html", users=users, page=page)


@leaderboard_bp.route("/challenge/<int:challenge_id>")
def challenge_stats(challenge_id: int):
    """Display statistics and top solvers for a specific challenge.

    Args:
        challenge_id: ID of the challenge to show stats for.
    """
    challenge = Challenge.query.get_or_404(challenge_id)

    top_submissions = (
        Submission.query.filter_by(challenge_id=challenge_id, passed=True)
        .order_by(Submission.execution_time.asc())
        .limit(10)
        .all()
    )

    total_attempts = Submission.query.filter_by(challenge_id=challenge_id).count()
    successful_attempts = Submission.query.filter_by(
        challenge_id=challenge_id, passed=True
    ).count()

    success_rate = (
        (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0
    )

    stats = {
        "total_attempts": total_attempts,
        "successful_attempts": successful_attempts,
        "success_rate": round(success_rate, 1),
    }

    return render_template(
        "leaderboard.html",
        challenge=challenge,
        top_submissions=top_submissions,
        stats=stats,
    )
