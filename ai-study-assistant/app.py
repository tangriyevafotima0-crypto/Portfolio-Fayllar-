"""AI Study Assistant - Streamlit application for AI-powered studying.

Features:
- Chat with study material
- Generate quizzes from text
- Create flashcards
- Get personalized study plans
"""

import streamlit as st

from config import Config
from assistant import StudyAssistant
from quiz_generator import QuizGenerator
from flashcard_generator import FlashcardGenerator
from utils import validate_api_key, count_words


def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon="📚",
        layout="wide",
    )

    st.title("📚 AI Study Assistant")
    st.markdown("Your personal AI-powered study companion")

    api_key = setup_sidebar()

    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to get started.")
        st.info("Get your API key at https://platform.openai.com/api-keys")
        return

    page = st.session_state.get("current_page", "Chat")

    if page == "Chat":
        render_chat_page(api_key)
    elif page == "Quiz":
        render_quiz_page(api_key)
    elif page == "Flashcards":
        render_flashcard_page(api_key)
    elif page == "Study Plan":
        render_study_plan_page(api_key)


def setup_sidebar() -> str:
    """Set up the sidebar with navigation and API key input.

    Returns:
        The API key entered by the user.
    """
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable AI features.",
        )

        st.divider()
        st.header("Navigation")

        pages = ["Chat", "Quiz", "Flashcards", "Study Plan"]
        for page in pages:
            if st.button(page, use_container_width=True):
                st.session_state["current_page"] = page

        st.divider()
        st.markdown("---")
        st.caption("Built with Streamlit + LangChain")

    return api_key


def render_chat_page(api_key: str) -> None:
    """Render the chat with study material page.

    Args:
        api_key: OpenAI API key for the assistant.
    """
    st.header("💬 Chat with Study Material")
    st.markdown("Paste your study material and ask questions about it.")

    context = st.text_area(
        "Study Material",
        height=200,
        placeholder="Paste your notes, textbook excerpt, or any study material here...",
    )

    if context:
        word_count = count_words(context)
        st.caption(f"Material loaded: {word_count} words")

    question = st.text_input(
        "Ask a question",
        placeholder="What are the main concepts in this material?",
    )

    if st.button("Ask", type="primary") and context and question:
        with st.spinner("Thinking..."):
            try:
                assistant = StudyAssistant(api_key=api_key)
                answer = assistant.ask_question(context, question)
                st.markdown("### Answer")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if context and st.button("Summarize Material"):
        with st.spinner("Summarizing..."):
            try:
                assistant = StudyAssistant(api_key=api_key)
                summary = assistant.summarize(context)
                st.markdown("### Summary")
                st.markdown(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")


def render_quiz_page(api_key: str) -> None:
    """Render the quiz generation page.

    Args:
        api_key: OpenAI API key for quiz generation.
    """
    st.header("📝 Generate Quiz")
    st.markdown("Create a quiz from any study material.")

    text = st.text_area(
        "Source Material",
        height=200,
        placeholder="Paste the text you want to be quizzed on...",
    )

    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of questions", 1, 10, 5)
    with col2:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])

    if st.button("Generate Quiz", type="primary") and text:
        with st.spinner("Generating quiz..."):
            try:
                generator = QuizGenerator(api_key=api_key)
                questions = generator.generate_quiz(text, num_questions, difficulty)

                st.session_state["quiz_questions"] = questions
                st.session_state["quiz_answers"] = {}
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")

    if "quiz_questions" in st.session_state:
        display_quiz(st.session_state["quiz_questions"])


def display_quiz(questions: list[dict]) -> None:
    """Display quiz questions with answer selection.

    Args:
        questions: List of question dictionaries.
    """
    st.markdown("---")
    score = 0

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i + 1}: {q['question']}**")
        answer = st.radio(
            f"Select answer for Q{i + 1}:",
            q["options"],
            key=f"q_{i}",
            label_visibility="collapsed",
        )

        if answer:
            selected_idx = q["options"].index(answer)
            if selected_idx == q["correct_answer"]:
                score += 1

    if st.button("Check Answers"):
        st.markdown(f"### Score: {score}/{len(questions)}")
        for i, q in enumerate(questions):
            correct = q["options"][q["correct_answer"]]
            st.markdown(f"Q{i + 1}: Correct answer - **{correct}**")
            if q.get("explanation"):
                st.caption(q["explanation"])


def render_flashcard_page(api_key: str) -> None:
    """Render the flashcard generation page.

    Args:
        api_key: OpenAI API key for flashcard generation.
    """
    st.header("🗂️ Generate Flashcards")
    st.markdown("Create flashcards for active recall study.")

    text = st.text_area(
        "Source Material",
        height=200,
        placeholder="Paste text to create flashcards from...",
    )

    num_cards = st.slider("Number of flashcards", 3, 20, 10)

    if st.button("Generate Flashcards", type="primary") and text:
        with st.spinner("Creating flashcards..."):
            try:
                generator = FlashcardGenerator(api_key=api_key)
                cards = generator.generate_flashcards(text, num_cards)
                st.session_state["flashcards"] = cards
                st.session_state["card_index"] = 0
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if "flashcards" in st.session_state:
        display_flashcards(st.session_state["flashcards"])


def display_flashcards(cards: list[dict]) -> None:
    """Display flashcards with flip functionality.

    Args:
        cards: List of flashcard dictionaries.
    """
    idx = st.session_state.get("card_index", 0)

    if not cards:
        return

    card = cards[idx % len(cards)]

    st.markdown("---")
    st.markdown(f"**Card {idx + 1} of {len(cards)}** | Category: {card.get('category', 'General')}")

    st.markdown(f"### {card['front']}")

    if st.button("Show Answer"):
        st.markdown(f"**{card['back']}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous") and idx > 0:
            st.session_state["card_index"] = idx - 1
    with col2:
        if st.button("Next") and idx < len(cards) - 1:
            st.session_state["card_index"] = idx + 1


def render_study_plan_page(api_key: str) -> None:
    """Render the study plan generation page.

    Args:
        api_key: OpenAI API key for plan generation.
    """
    st.header("📅 Study Plan Generator")
    st.markdown("Get a personalized study plan for any topic.")

    topic = st.text_input(
        "What do you want to study?",
        placeholder="e.g., Python Data Structures, Machine Learning Basics",
    )

    days = st.slider("How many days?", 1, 30, 7)

    if st.button("Generate Study Plan", type="primary") and topic:
        with st.spinner("Creating your study plan..."):
            try:
                assistant = StudyAssistant(api_key=api_key)
                plan = assistant.get_study_plan(topic, days)

                st.markdown(f"### Study Plan: {plan['topic']}")
                st.markdown(f"*Duration: {plan['duration_days']} days*")
                st.markdown("---")
                st.markdown(plan["plan"])
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
