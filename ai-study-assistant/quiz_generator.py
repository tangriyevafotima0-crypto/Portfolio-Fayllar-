"""Quiz generation module for creating study quizzes from text content."""

import json
import re
from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from config import Config
from utils import clean_text, count_words


class QuizGenerator:
    """Generates multiple-choice quizzes from study material.

    Uses AI to analyze text content and create relevant quiz
    questions with answer options and explanations.

    Attributes:
        llm: The language model for quiz generation.
        config: Application configuration.
    """

    def __init__(self, api_key: str = "") -> None:
        """Initialize the QuizGenerator.

        Args:
            api_key: OpenAI API key. Falls back to config if empty.
        """
        self.config = Config()
        effective_key = api_key or self.config.OPENAI_API_KEY

        self.llm = ChatOpenAI(
            openai_api_key=effective_key,
            model_name=self.config.MODEL_NAME,
            temperature=0.5,
            max_tokens=self.config.MAX_TOKENS,
        )

    def generate_quiz(
        self,
        text: str,
        num_questions: int = 5,
        difficulty: str = "medium",
    ) -> list[dict]:
        """Generate a quiz from the provided study material.

        Args:
            text: The source text to generate questions from.
            num_questions: Number of questions to generate (1-20).
            difficulty: Quiz difficulty (easy, medium, hard).

        Returns:
            List of question dictionaries containing:
                - question: The question text
                - options: List of 4 answer choices
                - correct_answer: Index of the correct option (0-3)
                - explanation: Why the answer is correct

        Raises:
            ValueError: If text is empty or num_questions is invalid.
        """
        if not text.strip():
            raise ValueError("Source text cannot be empty.")
        if num_questions < 1 or num_questions > 20:
            raise ValueError("Number of questions must be between 1 and 20.")

        cleaned_text = clean_text(text)
        word_count = count_words(cleaned_text)

        actual_questions = min(num_questions, max(1, word_count // 50))

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert quiz creator. Generate multiple-choice questions "
                "that test understanding of the provided material. "
                "Return ONLY valid JSON - an array of question objects."
            ),
            HumanMessagePromptTemplate.from_template(
                "Create {num_questions} {difficulty}-difficulty multiple choice questions "
                "from this text:\n\n{text}\n\n"
                "Return a JSON array where each object has:\n"
                '- "question": the question text\n'
                '- "options": array of 4 answer choices\n'
                '- "correct_answer": index (0-3) of correct option\n'
                '- "explanation": brief explanation of why the answer is correct\n\n'
                "Return ONLY the JSON array, no other text."
            ),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            text=cleaned_text[:3000],
            num_questions=str(actual_questions),
            difficulty=difficulty,
        )

        questions = self._parse_quiz_response(response)
        return questions

    def _parse_quiz_response(self, response: str) -> list[dict]:
        """Parse the AI response into structured quiz data.

        Args:
            response: Raw AI response text.

        Returns:
            List of validated question dictionaries.
        """
        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                questions = json.loads(json_match.group())
            else:
                questions = json.loads(response)
        except json.JSONDecodeError:
            return self._create_fallback_quiz()

        validated = []
        for q in questions:
            if self._validate_question(q):
                validated.append({
                    "question": q["question"],
                    "options": q["options"][:4],
                    "correct_answer": int(q["correct_answer"]),
                    "explanation": q.get("explanation", ""),
                })

        return validated if validated else self._create_fallback_quiz()

    def _validate_question(self, question: dict) -> bool:
        """Validate a question dictionary has required fields.

        Args:
            question: Question dictionary to validate.

        Returns:
            True if the question is valid, False otherwise.
        """
        required_fields = ["question", "options", "correct_answer"]
        if not all(field in question for field in required_fields):
            return False
        if not isinstance(question["options"], list) or len(question["options"]) < 2:
            return False
        if not isinstance(question["correct_answer"], int):
            return False
        return True

    def _create_fallback_quiz(self) -> list[dict]:
        """Create a fallback quiz when parsing fails.

        Returns:
            A simple default quiz question.
        """
        return [{
            "question": "Quiz generation encountered an issue. Please try again.",
            "options": ["Try again", "Modify text", "Reduce questions", "Contact support"],
            "correct_answer": 0,
            "explanation": "Please try regenerating the quiz.",
        }]
