"""Routes package - registers all application blueprints."""

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """Register all route blueprints with the application.

    Args:
        app: The Flask application instance.
    """
    from routes.auth import auth_bp
    from routes.challenges import challenges_bp
    from routes.leaderboard import leaderboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(leaderboard_bp)
