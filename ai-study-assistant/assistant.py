"""StudyAssistant class for AI-powered study interactions using LangChain."""

from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from config import Config


class StudyAssistant:
    """AI-powered study assistant using LangChain and OpenAI.

    Provides conversational study help, summarization, and
    study plan generation capabilities.

    Attributes:
        llm: The language model instance.
        memory: Conversation memory for context retention.
        config: Application configuration.
    """

    def __init__(self, api_key: str = "", model: str = "gpt-3.5-turbo") -> None:
        """Initialize the StudyAssistant with API credentials.

        Args:
            api_key: OpenAI API key. Falls back to config if empty.
            model: Name of the model to use.
        """
        self.config = Config()
        effective_key = api_key or self.config.OPENAI_API_KEY

        if not effective_key:
            raise ValueError(
                "OpenAI API key is required. Set it in .env or pass directly."
            )

        self.llm = ChatOpenAI(
            openai_api_key=effective_key,
            model_name=model,
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
        )

        self.memory = ConversationBufferWindowMemory(
            k=10, return_messages=True
        )

    def ask_question(self, context: str, question: str) -> str:
        """Ask a question about provided study material.

        Uses the context as reference material and answers
        the question based on that content.

        Args:
            context: The study material or text to reference.
            question: The question to answer about the material.

        Returns:
            AI-generated answer as a string.

        Raises:
            ValueError: If context or question is empty.
        """
        if not context.strip():
            raise ValueError("Context material cannot be empty.")
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a helpful study assistant. Answer questions based on "
                "the provided study material. Be clear, concise, and educational. "
                "If the answer is not in the material, say so honestly."
            ),
            HumanMessagePromptTemplate.from_template(
                "Study Material:\n{context}\n\nQuestion: {question}"
            ),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(context=context, question=question)

        return response.strip()

    def summarize(self, text: str, max_length: int = 200) -> str:
        """Summarize a piece of text to the specified length.

        Args:
            text: The text to summarize.
            max_length: Approximate maximum length in words.

        Returns:
            Condensed summary of the text.

        Raises:
            ValueError: If the text is empty.
        """
        if not text.strip():
            raise ValueError("Text to summarize cannot be empty.")

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert at creating clear, concise summaries. "
                "Capture the key points and main ideas."
            ),
            HumanMessagePromptTemplate.from_template(
                "Summarize the following text in approximately {max_length} words. "
                "Focus on the most important concepts and takeaways.\n\n"
                "Text:\n{text}"
            ),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(text=text, max_length=str(max_length))

        return response.strip()

    def get_study_plan(self, topic: str, days: int) -> dict:
        """Generate a structured study plan for a topic.

        Creates a day-by-day study plan with specific goals,
        resources, and activities for each day.

        Args:
            topic: The subject or topic to study.
            days: Number of days for the study plan.

        Returns:
            Dictionary containing the study plan with daily goals.

        Raises:
            ValueError: If topic is empty or days is invalid.
        """
        if not topic.strip():
            raise ValueError("Topic cannot be empty.")
        if days < 1 or days > 90:
            raise ValueError("Days must be between 1 and 90.")

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert study planner. Create detailed, actionable "
                "study plans that break complex topics into manageable daily goals."
            ),
            HumanMessagePromptTemplate.from_template(
                "Create a {days}-day study plan for learning: {topic}\n\n"
                "For each day, provide:\n"
                "- A clear learning objective\n"
                "- Specific topics to cover\n"
                "- Suggested activity or exercise\n"
                "- Estimated time needed\n\n"
                "Format as a structured plan."
            ),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(topic=topic, days=str(days))

        study_plan = {
            "topic": topic,
            "duration_days": days,
            "plan": response.strip(),
            "generated": True,
        }

        return study_plan

    def explain_concept(self, concept: str, level: str = "intermediate") -> str:
        """Explain a concept at the specified difficulty level.

        Args:
            concept: The concept to explain.
            level: Difficulty level (beginner, intermediate, advanced).

        Returns:
            Explanation tailored to the specified level.
        """
        if not concept.strip():
            raise ValueError("Concept cannot be empty.")

        level_instructions = {
            "beginner": "Explain like I'm 10 years old. Use simple words and analogies.",
            "intermediate": "Explain clearly with examples. Assume basic knowledge.",
            "advanced": "Provide in-depth explanation with technical details.",
        }

        instruction = level_instructions.get(level, level_instructions["intermediate"])

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a knowledgeable tutor. {instruction}"
            ),
            HumanMessagePromptTemplate.from_template(
                "Explain this concept: {concept}"
            ),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(concept=concept, instruction=instruction)

        return response.strip()
