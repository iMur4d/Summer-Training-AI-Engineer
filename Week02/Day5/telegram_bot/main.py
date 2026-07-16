import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from backend.llm import generate_response
from backend.validator import parse_and_validate
from backend.markdown_generator import generate_markdown
from backend.storage import save_note

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN is not set in the environment or .env file.")
    sys.exit(1)

# In-memory dictionary to hold pending structured notes
PENDING_NOTES = {}

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
        # Construct the preview message
        title = data.get("title", "Untitled")
        thought_type = data.get("thought_type", "Observation")
        summary = data.get("summary", "")
        
        # Build key points string
        key_points = "\n".join([f"- {kp}" for kp in data.get("key_points", [])])
        
        # Build open questions string if they exist
        open_questions = data.get("open_questions", [])
        valid_oqs = [oq for oq in open_questions if oq.lower() != "none"]
        oq_text = "\n".join([f"- {oq}" for oq in valid_oqs]) if valid_oqs else "None"
        
        tags = ", ".join(data.get("tags", []))
        
        preview_text = (
            f"🧠 KNOWLEDGE EXTRACTED\n\n"
            f"Title: {title}\n"
            f"Type: {thought_type}\n\n"
            f"Summary:\n{summary}\n\n"
            f"Key Points:\n{key_points}\n\n"
            f"Open Questions:\n{oq_text}\n\n"
            f"Tags: {tags}\n\n"
            f"Would you like to save this note?"
        )
        
        # Store in pending state (overwrites any existing pending note for this user)
        PENDING_NOTES[user.id] = data
        
        # Create Inline Keyboard
        keyboard = [
            [
                InlineKeyboardButton("✅ Save", callback_data="save"),
                InlineKeyboardButton("❌ Discard", callback_data="discard"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(preview_text, reply_markup=reply_markup)
    else:
        # If invalid (e.g., refusal message, schema error), fallback to the provided message
        await update.message.reply_text(fallback_msg)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # Answer the query to stop the loading animation on the button
    await query.answer()
    
    user_id = query.from_user.id
    
    # Verify the user has a pending note
    if user_id not in PENDING_NOTES:
        await query.edit_message_text("⚠️ This note has expired or was already processed.")
        return
        
    data = PENDING_NOTES[user_id]
    action = query.data
    
    if action == "save":
        # Generate markdown
        markdown_text = generate_markdown(data)
        
        # Save the note to local storage
        title = data.get("title", "Untitled")
        thought_type = data.get("thought_type", "Observation")
        success, result = save_note(title, markdown_text)
        
        if success:
            final_response = f"✅ Saved [{thought_type}]: {title}"
        else:
            final_response = f"⚠️ Couldn't save your note: {result}"
            
        await query.edit_message_text(final_response)
        
    elif action == "discard":
        await query.edit_message_text("❌ Note discarded.")
        
    # Always clear the pending state after handling the callback
    del PENDING_NOTES[user_id]

def main():
    print("Starting AI Thought Refinement Assistant Bot (v1.0.0)...")
    
    # Create the Telegram Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Start polling for updates
    application.run_polling()

if __name__ == "__main__":
    main()
