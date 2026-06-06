# AI Study Assistant

An AI-powered study tool built with Streamlit and LangChain that helps students learn more effectively through interactive features.

## Features

### Chat with Study Material
Paste any text (notes, textbook excerpts, articles) and ask questions about it. The AI provides accurate answers based on the provided content.

### Quiz Generation
Automatically generate multiple-choice quizzes from study material. Choose difficulty and number of questions. Get instant feedback with explanations.

### Flashcard Creator
Turn study text into flashcards for active recall practice. Cards are categorized by topic for organized review sessions.

### Study Plan Generator
Input any topic and timeframe to receive a structured, day-by-day study plan with specific goals, activities, and time estimates.

## Tech Stack

- **Frontend**: Streamlit 1.29
- **AI/LLM**: LangChain 0.0.350 + OpenAI GPT-3.5 Turbo
- **Configuration**: python-dotenv for environment management
- **Testing**: Pytest with unit tests for core logic

## Project Structure

```
ai-study-assistant/
├── app.py                  # Streamlit main application
├── assistant.py            # StudyAssistant class (LangChain)
├── quiz_generator.py       # QuizGenerator class
├── flashcard_generator.py  # FlashcardGenerator class
├── utils.py                # Text processing utilities
├── config.py               # Configuration management
├── tests/
│   ├── test_utils.py       # Tests for utility functions
│   └── test_quiz_generator.py  # Tests for quiz generation
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md
```

## Installation

```bash
cd ai-study-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OpenAI API key to .env

# Run the application
streamlit run app.py
```

## Usage

1. Launch the app with `streamlit run app.py`
2. Enter your OpenAI API key in the sidebar
3. Choose a feature from the navigation menu
4. Paste your study material and interact with the AI

## Running Tests

```bash
pytest tests/ -v
```

## Architecture

The application follows a modular design:

- **StudyAssistant**: Core class handling Q&A, summarization, and study plans
- **QuizGenerator**: Specialized class for generating validated quiz questions
- **FlashcardGenerator**: Creates structured flashcards with categories
- **Utils**: Shared text processing functions (cleaning, chunking, validation)

Each AI class uses LangChain's prompt templates and chains for structured interactions with the language model.

## Requirements

- Python 3.10+
- OpenAI API key (GPT-3.5 Turbo or better)
- Internet connection for API calls

## License

MIT License - Built as a learning project.
