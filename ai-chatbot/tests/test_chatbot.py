"""Tests for the ChatBot class."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import ChatBot, ChatBotError


class TestChatBotInit:
    """Tests for ChatBot initialization."""

    def test_init_with_valid_key(self) -> None:
        """Test successful initialization with a valid API key."""
        bot = ChatBot(api_key="test-key-123")
        assert bot.model == "gpt-3.5-turbo"

    def test_init_with_custom_model(self) -> None:
        """Test initialization with a custom model."""
        bot = ChatBot(api_key="test-key", model="gpt-4")
        assert bot.model == "gpt-4"

    def test_init_with_empty_key_raises_error(self) -> None:
        """Test that empty API key raises ChatBotError."""
        with pytest.raises(ChatBotError, match="API key cannot be empty"):
            ChatBot(api_key="")

    def test_init_history_is_empty(self) -> None:
        """Test that conversation history starts empty."""
        bot = ChatBot(api_key="test-key")
        assert bot.get_conversation_history() == []


class TestChatBotMessages:
    """Tests for message sending and history."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.bot = ChatBot(api_key="test-key-123")

    def test_send_empty_message_raises_error(self) -> None:
        """Test that sending an empty message raises an error."""
        with pytest.raises(ChatBotError, match="Message cannot be empty"):
            self.bot.send_message("")

    def test_send_whitespace_message_raises_error(self) -> None:
        """Test that whitespace-only message raises an error."""
        with pytest.raises(ChatBotError, match="Message cannot be empty"):
            self.bot.send_message("   ")

    def test_clear_history(self) -> None:
        """Test clearing conversation history."""
        self.bot._conversation_history = [
            {"role": "user", "content": "hello", "timestamp": "2024-01-01"}
        ]
        self.bot.clear_history()
        assert self.bot.get_conversation_history() == []

    def test_get_history_returns_copy(self) -> None:
        """Test that get_conversation_history returns a copy."""
        history = self.bot.get_conversation_history()
        history.append({"role": "user", "content": "test"})
        assert self.bot.get_conversation_history() == []

    def test_set_system_prompt(self) -> None:
        """Test updating the system prompt."""
        self.bot.set_system_prompt("You are a pirate.")
        assert self.bot._system_prompt == "You are a pirate."

    def test_set_empty_system_prompt_ignored(self) -> None:
        """Test that empty system prompt is ignored."""
        original = self.bot._system_prompt
        self.bot.set_system_prompt("   ")
        assert self.bot._system_prompt == original
