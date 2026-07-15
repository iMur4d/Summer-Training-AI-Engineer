import os
import json
import traceback

# Import modules from the current directory
try:
    from storage import save_note, get_unique_filepath, VAULT_PATH
except ImportError:
    pass
    
try:
    from markdown_generator import generate_markdown
except ImportError:
    pass

try:
    from validator import parse_and_validate
except ImportError:
    pass

def run_test_1():
    print("=== TEST 1: Storage Collision Fix ===")
    title = "Test Collision Title"
    content = "This is test content."
    
    # Clean up old files if they exist for a fresh test
    from storage import generate_safe_slug
    slug = generate_safe_slug(title)
    
    for i in ["", "-1", "-2", "-3"]:
        fp = os.path.join(VAULT_PATH, f"{slug}{i}.md")
        if os.path.exists(fp):
            os.remove(fp)

    results = []
    for _ in range(3):
        success, filepath = save_note(title, content)
        results.append((success, filepath))
        
    print("Calls made: 3")
    all_exist = True
    for idx, (success, fp) in enumerate(results):
        exists = os.path.exists(fp)
        print(f"Call {idx+1}: success={success}, filepath='{os.path.basename(fp)}', exists={exists}")
        if not exists:
            all_exist = False
            
    if all_exist and len(set(fp for _, fp in results)) == 3:
        print("RESULT: PASS - All 3 files generated unique names and exist.\n")
    else:
        print("RESULT: FAIL - Files were not unique or did not exist.\n")

def run_test_2():
    print("=== TEST 2: YAML Frontmatter Fix ===")
    data = {
        "title": "Debugging: The Art of Fixing Code",
        "summary": "Summary",
        "key_points": ["a", "b"],
        "tags": ["test", "yaml"],
        "open_questions": []
    }
    
    md = generate_markdown(data)
    print("Generated Markdown:")
    print("-------------------")
    print(md)
    print("-------------------")
    
    # Extract frontmatter
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) >= 3:
            frontmatter_str = parts[1].strip()
            print("Frontmatter block extracted successfully.")
            
            try:
                import yaml
                parsed = yaml.safe_load(frontmatter_str)
                print(f"Parsed YAML title: {parsed.get('title')}")
                if parsed.get('title') == "Debugging: The Art of Fixing Code":
                    print("RESULT: PASS - YAML parsed correctly and title matches.\n")
                else:
                    print("RESULT: FAIL - YAML parsed but title mismatch.\n")
            except ImportError:
                print("PyYAML not installed. Falling back to string check.")
                if 'title: "Debugging: The Art of Fixing Code"' in frontmatter_str:
                    print("RESULT: PASS - Found properly quoted title in frontmatter.\n")
                else:
                    print("RESULT: FAIL - Title not properly quoted.\n")
            except Exception as e:
                print(f"RESULT: FAIL - YAML parser threw an error: {e}\n")
        else:
            print("RESULT: FAIL - Could not split frontmatter.\n")
    else:
        print("RESULT: FAIL - Markdown doesn't start with ---\n")

def run_test_3():
    print("=== TEST 3: Validator Case-Sensitivity Fix ===")
    json_str = json.dumps({
        "title": "Valid Title",
        "summary": "Valid Summary",
        "key_points": ["Point 1"],
        "tags": ["Tag1"],
        "open_questions": []
    })
    
    print(f"Input JSON: {json_str}")
    is_valid, data, msg = parse_and_validate(json_str)
    
    print(f"is_valid: {is_valid}")
    print(f"Error Message: '{msg}'")
    
    if is_valid and data.get("title") == "Valid Title":
        print("RESULT: PASS - Validator successfully accepted lowercase 'title'.\n")
    else:
        print("RESULT: FAIL - Validator rejected the valid input.\n")

if __name__ == "__main__":
    try:
        run_test_1()
        run_test_2()
        run_test_3()
    except Exception as e:
        print(f"Test script failed with exception: {e}")
        traceback.print_exc()
