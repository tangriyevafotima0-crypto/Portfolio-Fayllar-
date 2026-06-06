"""Flashcard generation module for creating study flashcards from text."""

import json
import re
from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from config import Config
from utils import clean_text, count_words


class FlashcardGenerator:
    """Generates study flashcards from text content using AI.

    Creates front/back flashcard pairs that help with active
    recall and spaced repetition study techniques.

    Attributes:
        llm: The language model for flashcard generation.
        config: Application configuration.
    """

    def __init__(self, api_key: str = "") -> None:
        """Initialize the FlashcardGenerator.

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

    def generate_flashcards(
        self, text: str, num_cards: int = 10
    ) -> list[dict]:
        """Generate flashcards from the provided study material.

        Args:
            text: Source text to create flashcards from.
            num_cards: Number of flashcards to generate (1-30).

        Returns:
            List of flashcard dictionaries with 'front' and 'back' keys.

        Raises:
            ValueError: If text is empty or num_cards is invalid.
        """
        if not text.strip():
            raise ValueError("Source text cannot be empty.")
        if num_cards < 1 or num_cards > 30:
            raise ValueError("Number of cards must be between 1 and 30.")

        cleaned_text = clean_text(text)
        word_count = count_words(cleaned_text)
        actual_cards = min(num_cards, max(1, word_count // 30))

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert at creating effective study flashcards. "
                "Create cards that test key concepts, definitions, and relationships. "
                "Return ONLY valid JSON."
            ),
            HumanMessagePromptTemplate.from_template(
                "Create {num_cards} flashcards from this text:\n\n{text}\n\n"
                "Return a JSON array where each object has:\n"
                '- "front": a question or term (concise)\n'
                '- "back": the answer or definition (clear and complete)\n'
                '- "category": topic category for the card\n\n'
                "Return ONLY the JSON array."
            ),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(text=cleaned_text[:3000], num_cards=str(actual_cards))

        return self._parse_flashcard_response(response)

    def _parse_flashcard_response(self, response: str) -> list[dict]:
        """Parse AI response into structured flashcard data.

        Args:
            response: Raw AI response string.

        Returns:
            List of validated flashcard dictionaries.
        """
        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                cards = json.loads(json_match.group())
            else:
                cards = json.loads(response)
        except json.JSONDecodeError:
            return [{"front": "Error generating flashcards", "back": "Please try again", "category": "error"}]

        validated = []
        for card in cards:
            if "front" in card and "back" in card:
                validated.append({
                    "front": card["front"],
                    "back": card["back"],
                    "category": card.get("category", "General"),
                })

        return validated if validated else [
            {"front": "No cards generated", "back": "Please try different text", "category": "error"}
        ]
