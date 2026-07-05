import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

config = types.GenerateContentConfig(
    temperature= 0.8, #higher temperature
    max_output_tokens= 300,
    top_p= 0.9,
    system_instruction= "You are a friendly and detailed chatbot. Continue the conversation based on the previous history."
    )

client =genai.Client(api_key=gemini_key)


print("Welcome to the Gemini Chatbot!")
print("Type 'q' to end the conversation.")

history = []
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