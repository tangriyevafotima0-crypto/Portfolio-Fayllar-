# Code Challenges Platform

A Flask-based coding challenge platform where users can solve programming problems, submit solutions, and compete on a global leaderboard.

## Features

- **Challenge Library** - Browse and filter challenges by difficulty and category
- **Code Submission** - Write and submit Python solutions with instant feedback
- **Automated Testing** - Solutions are validated against predefined test cases
- **Scoring System** - Earn points based on difficulty, pass rate, and execution speed
- **Leaderboard** - Compete with other users for the top spot
- **User Profiles** - Track your progress, view submission history

## Tech Stack

- **Backend**: Flask 3.0 with Blueprints for modular routing
- **Database**: SQLAlchemy ORM with SQLite (configurable)
- **Authentication**: Flask-Login with secure password hashing
- **Frontend**: Custom dark-theme UI optimized for coding
- **Testing**: Pytest with fixtures and test isolation

## Project Structure

```
coding-challenges/
├── app.py              # Application factory
├── config.py           # Configuration classes
├── models/
│   ├── user.py         # User model with authentication
│   ├── challenge.py    # Challenge model with test cases
│   └── submission.py   # Submission tracking model
├── routes/
│   ├── auth.py         # Registration, login, profile
│   ├── challenges.py   # Challenge listing and submission
│   └── leaderboard.py  # Rankings and statistics
├── services/
│   ├── code_runner.py  # Safe code execution engine
│   └── scorer.py       # Points calculation logic
├── templates/          # Jinja2 HTML templates
├── static/             # CSS and JavaScript assets
├── challenges/         # Sample challenge data (JSON)
├── tests/              # Pytest test suite
├── requirements.txt    # Python dependencies
└── .env.example        # Environment variable template
```

## Installation

```bash
# Clone the repository
cd coding-challenges

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run the application
python app.py
```

## Running Tests

```bash
pytest tests/ -v
```

## API Design

The application uses Flask Blueprints for clean route organization:

- `/auth/` - Authentication (register, login, logout, profile)
- `/challenges` - Challenge listing and submission
- `/challenges/<id>` - Individual challenge view
- `/leaderboard/` - Global rankings

## Code Runner Safety

The `CodeRunner` service executes user-submitted code in a restricted namespace. It captures output, enforces time limits, and catches exceptions gracefully.

## Scoring Algorithm

Points are calculated based on:
- **Base points**: Determined by difficulty (Easy: 10, Medium: 25, Hard: 50)
- **Pass ratio**: Full credit for all tests, partial for >50%, zero otherwise
- **Speed bonus**: 10% bonus for sub-second execution
- **Streak bonus**: Extra points for consecutive solves

## Contributing

1. Add new challenges as JSON files in the `challenges/` directory
2. Follow the existing test case format
3. Run the test suite before submitting changes

## License

MIT License - Built as a learning project.
