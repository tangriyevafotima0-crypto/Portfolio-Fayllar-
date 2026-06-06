"""Pytest configuration and shared fixtures."""

import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from config import TestConfig


@pytest.fixture
def app():
    """Create application for testing.

    Yields:
        Flask application configured for testing.
    """
    application = create_app(TestConfig)

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client.

    Args:
        app: The Flask test application.

    Returns:
        Flask test client instance.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a CLI test runner.

    Args:
        app: The Flask test application.

    Returns:
        Flask CLI test runner instance.
    """
    return app.test_cli_runner()
