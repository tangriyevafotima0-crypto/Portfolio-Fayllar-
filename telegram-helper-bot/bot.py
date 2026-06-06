"""
Telegram Helper Bot
A fun bot with quiz questions, random facts, and motivational quotes
Uses python-telegram-bot library
"""

import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging so we can see errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Quiz questions - each has a question, options, and correct answer
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of Japan?",
        "options": ["A) Seoul", "B) Tokyo", "C) Beijing", "D) Bangkok"],
        "answer": "B) Tokyo"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A) Venus", "B) Jupiter", "C) Mars", "D) Saturn"],
        "answer": "C) Mars"
    },
    {
        "question": "What programming language is known for its snake logo?",
        "options": ["A) Java", "B) C++", "C) Python", "D) Ruby"],
        "answer": "C) Python"
    },
    {
        "question": "How many bits are in one byte?",
        "options": ["A) 4", "B) 8", "C) 16", "D) 32"],
        "answer": "B) 8"
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
        "answer": "D) Pacific"
    }
]

# Fun facts list
FUN_FACTS = [
    "Honey never spoils. Archaeologists have found 3000-year-old honey that was still edible!",
    "A group of flamingos is called a 'flamboyance'.",
    "The first computer programmer was Ada Lovelace, who wrote programs in the 1840s.",
    "Octopuses have three hearts and blue blood.",
    "The first 1 GB hard drive weighed about 550 pounds and cost $40,000 in 1980.",
    "Bananas are berries, but strawberries are not.",
    "The entire internet weighs about the same as a strawberry (in electrons).",
    "There are more possible chess games than atoms in the observable universe."
]

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "The best way to predict the future is to create it. - Peter Drucker",
    "Code is like humor. When you have to explain it, it is bad. - Cory House",
    "Every expert was once a beginner. Keep going!",
    "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "The more I practice, the luckier I get. - Gary Player"
]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - greet the user"""
    user_name = update.effective_user.first_name
    welcome_message = (
        f"Hello {user_name}! Welcome to Helper Bot! 🤖\n\n"
        "Here is what I can do:\n"
        "/quiz - Get a random quiz question\n"
        "/fact - Learn a random fun fact\n"
        "/motivate - Get a motivational quote\n"
        "/help - Show all commands"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command - show available commands"""
    help_text = (
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/quiz - Get a random quiz question\n"
        "/fact - Get a random fun fact\n"
        "/motivate - Get a motivational quote\n"
    )
    await update.message.reply_text(help_text)


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /quiz command - send a random quiz question"""
    question = random.choice(QUIZ_QUESTIONS)
    options_text = "\n".join(question["options"])
    quiz_text = (
        f"🧠 Quiz Time!\n\n"
        f"{question['question']}\n\n"
        f"{options_text}\n\n"
        f"(Answer: {question['answer']})"
    )
    await update.message.reply_text(quiz_text)


async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /fact command - send a random fun fact"""
    fact = random.choice(FUN_FACTS)
    await update.message.reply_text(f"💡 Fun Fact:\n\n{fact}")


async def motivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /motivate command - send a motivational quote"""
    quote = random.choice(MOTIVATIONAL_QUOTES)
    await update.message.reply_text(f"✨ Motivation:\n\n{quote}")


def main():
    """Set up the bot and start polling for messages"""
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        print("Error: BOT_TOKEN not found in .env file")
        print("Please create a .env file with your bot token")
        print("See .env.example for reference")
        return

    # Create the bot application
    try:
        app = Application.builder().token(bot_token).build()
    except Exception as e:
        print(f"Error creating bot: {e}")
        return

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler("fact", fact_command))
    app.add_handler(CommandHandler("motivate", motivate_command))

    # Start the bot
    print("Bot is running! Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
