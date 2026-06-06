# AI Chatbot

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange?logo=openai)
![License](https://img.shields.io/badge/License-MIT-yellow)

A modern web-based AI chatbot powered by OpenAI's GPT-3.5 Turbo. Features a sleek dark-themed interface with real-time message streaming, conversation history, and session management.

## Features

- Real-time AI responses using OpenAI GPT-3.5 Turbo
- Clean, modern dark-themed chat interface
- Conversation history with session persistence
- Typing indicators for better UX
- Clear chat functionality
- Responsive design for mobile and desktop
- RESTful API endpoints for chat operations

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Backend language |
| Flask 3.0 | Web framework |
| OpenAI API | AI/ML responses |
| HTML/CSS/JS | Frontend interface |
| Fetch API | Async communication |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/ai-chatbot.git
cd ai-chatbot
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
# Edit .env and add your OpenAI API key
```

5. Run the application:
```bash
python app.py
```

6. Open http://localhost:5000 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main chat interface |
| POST | `/api/chat` | Send a message |
| GET | `/api/history` | Get conversation history |
| POST | `/api/clear` | Clear chat history |

## Project Structure

```
ai-chatbot/
├── app.py              # Flask application and routes
├── chatbot.py          # ChatBot class with OpenAI integration
├── config.py           # Configuration management
├── templates/
│   ├── base.html       # Base template
│   └── index.html      # Chat interface
├── static/
│   ├── css/style.css   # UI styling
│   └── js/script.js    # Frontend logic
├── tests/
│   └── test_chatbot.py # Unit tests
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
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
