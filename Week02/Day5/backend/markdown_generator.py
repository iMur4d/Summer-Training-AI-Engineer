from datetime import datetime

def generate_markdown(data: dict) -> str:
    """
    Converts the validated dictionary data into the required Markdown structure.
    Assumes the dictionary is fully validated.
    """
    # Use current local time in a nice format for Obsidian (YYYY-MM-DD HH:MM)
    now_formatted = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Format tags for YAML (no # prefix)
    tags_yaml = f"[{', '.join(data.get('tags', []))}]"
    
    # Format key points
    key_points_md = "\n".join([f"- {kp}" for kp in data.get("key_points", [])])
    
    # Format open questions
    oq_list = data.get("open_questions", [])
    valid_oqs = [oq for oq in oq_list if oq.lower() != "none"]
    
    if not valid_oqs:
        open_questions_md = "None"
    else:
        open_questions_md = "\n".join([f"- {oq}" for oq in valid_oqs])
            
    md = f"""---
title: "{data.get('title', '')}"
date: {now_formatted}
thought_type: "{data.get('thought_type', 'Observation')}"
tags: {tags_yaml}
---

# {data.get('title', '')}
*Type: {data.get('thought_type', 'Observation')}*

## Summary
{data.get('summary', '')}

## Key Points
{key_points_md}

## Open Questions
{open_questions_md}"""

    return md
