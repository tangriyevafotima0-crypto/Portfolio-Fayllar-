"""Flask web application for the AI Chatbot."""

from flask import Flask, render_template, request, jsonify, session
from config import Config
from chatbot import ChatBot, ChatBotError


app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

chatbots: dict[str, ChatBot] = {}


def get_chatbot(session_id: str) -> ChatBot:
    """Get or create a ChatBot instance for the given session.

    Args:
        session_id: Unique session identifier.

    Returns:
        ChatBot instance associated with the session.

    Raises:
        ChatBotError: If configuration is invalid.
    """
    if session_id not in chatbots:
        Config.validate()
        chatbots[session_id] = ChatBot(
            api_key=Config.OPENAI_API_KEY,
            model=Config.MODEL_NAME
        )
    return chatbots[session_id]


@app.route("/")
def index() -> str:
    """Render the main chat interface."""
    if "session_id" not in session:
        import uuid
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat message API endpoint.

    Expects JSON body with 'message' field.
    Returns JSON with 'response' or 'error' field.
    """
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    message = data["message"].strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        session_id = session.get("session_id", "default")
        bot = get_chatbot(session_id)
        response = bot.send_message(message)
        return jsonify({"response": response})
    except ChatBotError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def history():
    """Get conversation history for the current session."""
    session_id = session.get("session_id", "default")
    if session_id in chatbots:
        return jsonify({"history": chatbots[session_id].get_conversation_history()})
    return jsonify({"history": []})


@app.route("/api/clear", methods=["POST"])
def clear():
    """Clear conversation history for the current session."""
    session_id = session.get("session_id", "default")
    if session_id in chatbots:
        chatbots[session_id].clear_history()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
