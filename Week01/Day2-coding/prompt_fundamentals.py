import os
from datetime import datetime  # used to timestamp the log filename so each run creates a separate file
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Promopt examples for testing the chatbot:
# 1 - basic_prompt = "write a excuse message"
# 2 - Improved_prompt = "You are a professional employee. Write a short excuse message to your manager."
# 3 - Detailed_prompt = "You are a professional employee. Write an excuse message to your manager, explaining that you will be late to work because of a family emergency, and you will make up for the lost time by working extra hours this week."
# 4 - Creative_prompt = "You are a professional employee. Write an excuse message to your manager, explaining that you will be late to work because of a family emergency, and you will make up for the lost time by working extra hours this week. You need to be more empathetic and talking like you harry up with some mistaypes that represnt your anixity."
# 5 - const_prompt = "You are a professional employee. Write an excuse message to your manager, explaining that you will be late to work because of a family emergency, and you will make up for the lost time by working extra hours this week. Addionly, you need to make it only with 50 words, and it should be polite and professional witout be anxious."

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

config = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=300,
)

client = genai.Client(api_key=gemini_key)

print("Welcome to the Gemini Chatbot!")
print("Type 'q' to end the conversation.")

history = []

# Create a unique filename using the current date and time,
log_filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "q":
        print("Goodbye!")
        break

    history.append(f"You: {user_input}")
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=history,
        config=config
    )

    bot_response = response.text
    history.append(f"Bot: {bot_response}")

    print("---")
    print(f"Bot: {bot_response}")
    print("---")

    # Append this turn (prompt + response) to the log file as evidence,
    with open(log_filename, "a", encoding="utf-8", errors="replace") as f:
        f.write(f"You: {user_input}\n")
        f.write(f"Bot: {bot_response}\n")
        f.write("-" * 40 + "\n")

print(f"\nConversation saved to {log_filename}")