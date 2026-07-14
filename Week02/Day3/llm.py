import os
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv

# Load environment variables in case they aren't loaded yet
load_dotenv()


def generate_response(text: str) -> str:
    """
    Sends the user input text to the Gemini API using the configured model.
    Returns the LLM's response or a graceful error message on failure.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is not set in the environment or .env file."
    
    # Retrieve and sanitize the model name at runtime, fallback to default if empty/whitespace
    raw_model = os.getenv("GEMINI_MODEL")
    model_name = raw_model.strip() if (raw_model and raw_model.strip()) else "gemma-4-26b-a4b-it"
    
    print(f"DEBUG: Using model '{model_name}' for generation.")
    
    try:
        # Initialize client with the current API key
        client = genai.Client(api_key=api_key)
        
        # Call the models generate_content API
        response = client.models.generate_content(
            model=model_name,
            contents=text
        )
        
        # If response is empty or response.text is not populated
        if not response or not response.text:
            return "Error: Received empty response from the language model."
            
        return response.text
        
    except APIError as e:
        print(f"Gemini API Error: {e}")
        return f"Error: Gemini API request failed. Details: {e.message or str(e)}"
    except Exception as e:
        print(f"Unexpected error during LLM generation: {e}")
        return f"Error: An unexpected error occurred: {str(e)}"
