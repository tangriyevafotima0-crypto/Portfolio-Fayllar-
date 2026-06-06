"""Quiz routes for browsing, taking, and managing quizzes."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Quiz, Question, Result

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


@quiz_bp.route("/list")
def quiz_list():
    """Display all available quizzes with filtering options."""
    category = request.args.get("category", "")
    page = request.args.get("page", 1, type=int)

    query = Quiz.query
    if category:
        query = query.filter_by(category=category)

    quizzes = query.order_by(Quiz.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    categories = db.session.query(Quiz.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template(
        "quiz/list.html",
        quizzes=quizzes,
        categories=categories,
        current_category=category
    )


@quiz_bp.route("/take/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def take_quiz(quiz_id: int):
    """Handle quiz-taking flow.

    GET: Display quiz questions.
    POST: Process answers and calculate score.

    Args:
        quiz_id: The ID of the quiz to take.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.all()

    if not questions:
        flash("This quiz has no questions yet.", "warning")
        return redirect(url_for("quiz.quiz_list"))

    if request.method == "POST":
        correct = 0
        total = len(questions)

        for question in questions:
            answer = request.form.get(f"question_{question.id}", "")
            if question.check_answer(answer):
                correct += 1

        score = round((correct / total) * 100, 1) if total > 0 else 0

        result = Result(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score,
            total_questions=total,
            correct_answers=correct
        )
        db.session.add(result)
        db.session.commit()

        return render_template(
            "quiz/results.html",
            quiz=quiz,
            score=score,
            correct=correct,
            total=total
        )

    return render_template("quiz/take.html", quiz=quiz, questions=questions)


@quiz_bp.route("/results")
@login_required
def my_results():
    """Display the current user's quiz result history."""
    results = Result.query.filter_by(user_id=current_user.id).order_by(
        Result.completed_at.desc()
    ).all()
    return render_template("quiz/results.html", results=results, show_history=True)
