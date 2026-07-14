import os
import re
from typing import Tuple
from dotenv import load_dotenv

# Load environment variables in case they aren't loaded yet
load_dotenv()

# Get the vault path from the environment, defaulting to './vault'
_raw_vault = os.getenv("VAULT_PATH", "./vault").strip()
VAULT_PATH = _raw_vault if _raw_vault else "./vault"

def generate_safe_slug(title: str) -> str:
    """
    Converts a title string into a safe, collision-resistant filename slug.
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower().replace(" ", "-")
    # Remove any non-alphanumeric or hyphen characters
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug).strip('-')
    
    return slug if slug else "untitled"

def get_unique_filepath(vault_path: str, slug: str) -> str:
    """
    Generates a unique filepath by appending a counter if the file already exists.
    Known limitation: theoretical race condition between exists() and write().
    """
    base_filepath = os.path.join(vault_path, f"{slug}.md")
    if not os.path.exists(base_filepath):
        return base_filepath
        
    counter = 1
    while True:
        filepath = os.path.join(vault_path, f"{slug}-{counter}.md")
        if not os.path.exists(filepath):
            return filepath
        counter += 1

def save_note(title: str, markdown_content: str) -> Tuple[bool, str]:
    """
    Saves the markdown string to the local vault directory.
    
    Returns:
        (success: bool, result_or_error_msg: str)
    """
    try:
        # Create vault directory if it doesn't exist
        os.makedirs(VAULT_PATH, exist_ok=True)
        
        # Generate safe filename and find unique path
        slug = generate_safe_slug(title)
        filepath = get_unique_filepath(VAULT_PATH, slug)
        
        # Write content to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        return True, filepath
    except PermissionError:
        return False, f"Permission denied to write to '{VAULT_PATH}'."
    except OSError as e:
        return False, f"OS error occurred while saving: {e}"
    except Exception as e:
        return False, f"Unexpected error while saving: {e}"
