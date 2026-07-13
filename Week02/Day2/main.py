import os
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN is not set in the environment or .env file.")
    sys.exit(1)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Print the received message to the console
    user = update.effective_user
    username = user.username or f"{user.first_name} {user.last_name or ''}".strip()
    message_text = update.message.text
    
    print(f"Received message from @{username}: {message_text}")
    
    # Reply with a simple confirmation message
    await update.message.reply_text("Received your thought!")

def main():
    print("Starting AI Thought Refinement Assistant Bot (v0.1.0)...")
    
    # Create the Telegram Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register the message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start polling for updates
    application.run_polling()

if __name__ == "__main__":
    main()
