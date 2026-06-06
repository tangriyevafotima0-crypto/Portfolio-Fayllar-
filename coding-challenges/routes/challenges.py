"""Challenge routes for browsing, viewing, and submitting solutions."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models.challenge import Challenge
from models.submission import Submission
from services.code_runner import CodeRunner
from services.scorer import Scorer

challenges_bp = Blueprint("challenges", __name__)


@challenges_bp.route("/")
def index():
    """Display the home page with featured challenges."""
    featured = Challenge.query.order_by(Challenge.times_solved.desc()).limit(6).all()
    return render_template("index.html", featured_challenges=featured)


@challenges_bp.route("/challenges")
def list_challenges():
    """Display all challenges with optional filtering.

    Query Parameters:
        difficulty: Filter by difficulty level (easy, medium, hard).
        category: Filter by problem category.
    """
    difficulty = request.args.get("difficulty")
    category = request.args.get("category")

    query = Challenge.query

    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if category:
        query = query.filter_by(category=category)

    challenges = query.order_by(Challenge.created_at.desc()).all()

    categories = db.session.query(Challenge.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template(
        "challenges/list.html",
        challenges=challenges,
        categories=categories,
        current_difficulty=difficulty,
        current_category=category,
    )


@challenges_bp.route("/challenges/<int:challenge_id>")
def detail(challenge_id: int):
    """Display a single challenge with problem description.

    Args:
        challenge_id: ID of the challenge to display.
    """
    challenge = Challenge.query.get_or_404(challenge_id)
    user_submissions = []

    if current_user.is_authenticated:
        user_submissions = (
            Submission.query.filter_by(
                user_id=current_user.id, challenge_id=challenge_id
            )
            .order_by(Submission.created_at.desc())
            .limit(5)
            .all()
        )

    return render_template(
        "challenges/detail.html",
        challenge=challenge,
        submissions=user_submissions,
    )


@challenges_bp.route("/challenges/<int:challenge_id>/submit", methods=["POST"])
@login_required
def submit_solution(challenge_id: int):
    """Process a code submission for a challenge.

    Runs the submitted code against test cases and records the result.

    Args:
        challenge_id: ID of the challenge being attempted.
    """
    challenge = Challenge.query.get_or_404(challenge_id)
    code = request.form.get("code", "").strip()

    if not code:
        flash("Please submit some code.", "error")
        return redirect(url_for("challenges.detail", challenge_id=challenge_id))

    if len(code) > 10000:
        flash("Code exceeds maximum length of 10,000 characters.", "error")
        return redirect(url_for("challenges.detail", challenge_id=challenge_id))

    runner = CodeRunner(timeout=5)
    test_cases = challenge.get_test_cases()
    result = runner.run_tests(code, test_cases)

    scorer = Scorer()
    points = scorer.calculate_points(
        difficulty=challenge.difficulty,
        tests_passed=result["tests_passed"],
        tests_total=result["tests_total"],
    )

    submission = Submission(
        user_id=current_user.id,
        challenge_id=challenge_id,
        code=code,
        passed=result["all_passed"],
        tests_passed=result["tests_passed"],
        tests_total=result["tests_total"],
        points_earned=points,
        execution_time=result.get("execution_time", 0.0),
        error_message=result.get("error", ""),
    )

    db.session.add(submission)

    if result["all_passed"]:
        current_user.add_points(points)
        challenge.increment_solved()
        flash(f"All tests passed! You earned {points} points!", "success")
    else:
        flash(
            f"Passed {result['tests_passed']}/{result['tests_total']} tests.",
            "warning",
        )

    db.session.commit()

    return render_template(
        "challenges/result.html",
        challenge=challenge,
        submission=submission,
        result=result,
    )
