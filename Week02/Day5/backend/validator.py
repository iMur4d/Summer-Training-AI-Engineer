import json
from typing import Tuple, Optional, Any, Dict

def parse_and_validate(raw_text: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Parses raw text into JSON and strictly validates the schema.
    
    Returns:
        is_valid (bool): True if parsing and validation succeed.
        data (dict): The parsed and validated dictionary. None if invalid.
        message (str): A message explaining the validation failure, or the raw text if 
                       it's assumed to be a valid refusal message from the LLM.
    """
    # 1. Clean the text (strip backticks if wrapped in a markdown code block)
    clean_text = raw_text.strip("` \n")
    if clean_text.startswith("json"):
        clean_text = clean_text[4:].strip()
        
    # 2. Parse JSON
    try:
        data = json.loads(clean_text)
    except json.JSONDecodeError:
        # If it's not valid JSON, we assume it's a plain text refusal message from the LLM
        # (e.g. "I can only help you organize and refine your own thoughts.")
        # We return it as the message so the orchestrator can relay it.
        return False, None, raw_text.strip()
        
    # 3. Validate it's a dictionary
    if not isinstance(data, dict):
        return False, None, "Error: The model output is not a JSON object."
        
    # 4. Strict field validation
    required_strings = ["title", "summary", "thought_type"]
    required_lists = ["key_points", "tags", "open_questions"]
    
    for field in required_strings:
        if field not in data:
            return False, None, f"Error: Missing required string field '{field}'."
        if not isinstance(data[field], str):
            return False, None, f"Error: Field '{field}' must be a string."
            
    allowed_thought_types = {"Concept", "Task", "Question", "Observation", "Insight", "Research Idea"}
    if data["thought_type"] not in allowed_thought_types:
        return False, None, f"Error: '{data['thought_type']}' is not a valid thought_type."
            
    for field in required_lists:
        if field not in data:
            return False, None, f"Error: Missing required list field '{field}'."
        if not isinstance(data[field], list):
            return False, None, f"Error: Field '{field}' must be a list."
        # Ensure all items in the list are strings
        for item in data[field]:
            if not isinstance(item, str):
                return False, None, f"Error: All items in '{field}' must be strings."
                
    # Everything is valid!
    return True, data, ""
