"""ChatBot module with OpenAI API integration."""

from datetime import datetime
from openai import OpenAI, OpenAIError


class ChatBotError(Exception):
    """Custom exception for ChatBot-related errors."""

    pass


class ChatBot:
    """AI Chatbot powered by OpenAI's GPT models.

    Manages conversation history and communicates with the OpenAI API
    to generate contextual responses.

    Attributes:
        model: The OpenAI model to use for completions.
        client: The OpenAI API client instance.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo") -> None:
        """Initialize the ChatBot with API credentials.

        Args:
            api_key: OpenAI API key for authentication.
            model: Model identifier to use. Defaults to gpt-3.5-turbo.

        Raises:
            ChatBotError: If the API key is empty or invalid.
        """
        if not api_key:
            raise ChatBotError("API key cannot be empty")

        self.model = model
        self.client = OpenAI(api_key=api_key)
        self._conversation_history: list[dict[str, str]] = []
        self._system_prompt = (
            "You are a helpful, friendly AI assistant. "
            "Provide clear and concise responses."
        )

    def send_message(self, message: str) -> str:
        """Send a message and get a response from the AI.

        Args:
            message: The user's input message.

        Returns:
            The AI-generated response text.

        Raises:
            ChatBotError: If the API call fails or message is empty.
        """
        if not message.strip():
            raise ChatBotError("Message cannot be empty")

        self._conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })

        try:
            messages = [{"role": "system", "content": self._system_prompt}]
            messages.extend([
                {"role": msg["role"], "content": msg["content"]}
                for msg in self._conversation_history
            ])

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )

            assistant_message = response.choices[0].message.content

            self._conversation_history.append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat()
            })

            return assistant_message

        except OpenAIError as e:
            raise ChatBotError(f"OpenAI API error: {str(e)}") from e
        except Exception as e:
            raise ChatBotError(f"Unexpected error: {str(e)}") from e

    def get_conversation_history(self) -> list[dict]:
        """Retrieve the full conversation history.

        Returns:
            List of message dictionaries with role, content, and timestamp.
        """
        return self._conversation_history.copy()

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._conversation_history = []

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt for the chatbot.

        Args:
            prompt: New system prompt to guide AI behavior.
        """
        if prompt.strip():
            self._system_prompt = prompt
