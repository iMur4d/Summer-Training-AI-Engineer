import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from llm import generate_response
from validator import parse_and_validate
from markdown_generator import generate_markdown

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
    
    # Send user message to LLM asynchronously
    raw_response = await asyncio.to_thread(generate_response, message_text)
    
    # Validate the raw response
    is_valid, data, fallback_msg = parse_and_validate(raw_response)
    
    if is_valid:
        # Generate markdown if valid
        final_response = generate_markdown(data)
    else:
        # If invalid (e.g., refusal message, schema error), fallback to the provided message
        # Prepared for retry logic in future versions: if not is_valid and retries < MAX...
        final_response = fallback_msg
    
    # Reply with the final response
    await update.message.reply_text(final_response)

def main():
    print("Starting AI Thought Refinement Assistant Bot (v0.4.0)...")
    
    # Create the Telegram Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register the message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start polling for updates
    application.run_polling()

if __name__ == "__main__":
    main()
