# Quiz Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

A full-stack multi-user quiz platform built with Flask. Users can register, browse quizzes by category, take timed quizzes, view scores, and track their progress on a personal dashboard.

## Features

- User registration and authentication with secure password hashing
- Quiz browsing with category-based filtering
- Multiple-choice quiz engine with instant scoring
- Personal dashboard with statistics:
  - Total quizzes taken
  - Average score
  - Best score
  - Recent activity history
- Responsive design for mobile and desktop
- Flash messages for user feedback
- Paginated quiz listing

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Backend language |
| Flask 3.0 | Web framework |
| Flask-SQLAlchemy | ORM / Database |
| Flask-Login | User session management |
| SQLite | Database engine |
| Werkzeug | Password hashing |
| Jinja2 | Template engine |
| HTML/CSS | Frontend |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/quiz-platform.git
cd quiz-platform
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python app.py
```

6. Open http://localhost:5001 in your browser.

## Project Structure

```
quiz-platform/
├── app.py                  # App factory
├── config.py               # Configuration
├── models.py               # SQLAlchemy models
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── main.py             # Main pages
│   └── quiz.py             # Quiz operations
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Landing page
│   ├── dashboard.html      # User dashboard
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── quiz/
│       ├── list.html
│       ├── take.html
│       └── results.html
├── static/
│   └── css/style.css
├── tests/
│   ├── conftest.py         # Test fixtures
│   └── test_models.py      # Model tests
├── .env.example
├── requirements.txt
└── README.md
```

## Screenshots

> Screenshots will be added after deployment.

## Running Tests

```bash
python -m pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is part of my development portfolio.
