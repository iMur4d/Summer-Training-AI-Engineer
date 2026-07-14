import os
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

# Load environment variables in case they aren't loaded yet
load_dotenv()

# Initialize module-level configurations
API_KEY = os.getenv("GEMINI_API_KEY")
_raw_model = os.getenv("GEMINI_MODEL", "")
MODEL_NAME = _raw_model.strip() if _raw_model.strip() else "gemma-4-26b-a4b-it"

_CLIENT = None
_SYSTEM_INSTRUCTION = ""

def _init_llm():
    """Initializes the Gemini client and loads the system prompt once at startup."""
    global _CLIENT, _SYSTEM_INSTRUCTION
    
    prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.txt")
    try:
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                _SYSTEM_INSTRUCTION = f.read().strip()
        else:
            print(f"WARNING: system_prompt.txt not found at {prompt_path}.")
    except Exception as e:
        print(f"WARNING: Failed to read system_prompt.txt: {e}")

    if API_KEY:
        try:
            _CLIENT = genai.Client(api_key=API_KEY)
        except Exception as e:
            print(f"WARNING: Failed to initialize genai.Client: {e}")

# Call initialization on module load
_init_llm()

def generate_response(text: str) -> str:
    """
    Sends the user input text to the Gemini API using the configured model.
    Returns the LLM's response or a graceful error message on failure.
    """
    if not _CLIENT:
        return "Error: GEMINI_API_KEY is not set or client failed to initialize."
        
    print(f"DEBUG: Using model '{MODEL_NAME}' for generation.")
    
    try:
        # Configure model request
        config = types.GenerateContentConfig(
            system_instruction=_SYSTEM_INSTRUCTION if _SYSTEM_INSTRUCTION else None,
            temperature=0.2
        )
        
        # Call the models generate_content API
        response = _CLIENT.models.generate_content(
            model=MODEL_NAME,
            contents=text,
            config=config
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
