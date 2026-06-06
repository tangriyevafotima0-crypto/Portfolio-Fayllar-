# Telegram Helper Bot

A fun Telegram bot that sends quiz questions, random facts, and motivational quotes.

## Setup Instructions

### 1. Create a Bot with BotFather

1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow the prompts
3. Choose a name and username for your bot
4. Copy the API token BotFather gives you

### 2. Configure the Bot

1. Copy `.env.example` to `.env`
2. Replace `your_telegram_bot_token_here` with your actual token

### 3. Install and Run

```bash
pip install -r requirements.txt
python bot.py
```

## Commands

- `/start` - Welcome message and command list
- `/help` - Show available commands
- `/quiz` - Get a random quiz question with answer
- `/fact` - Learn a random fun fact
- `/motivate` - Get a motivational quote
