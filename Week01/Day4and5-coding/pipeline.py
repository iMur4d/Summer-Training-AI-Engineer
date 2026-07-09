import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from google import genai
from google.genai import types
from markdown_it import MarkdownIt
from weasyprint import HTML

LOCAL_TZ = ZoneInfo("Asia/Riyadh")

def load_system_prompt(file_path="system_prompt.txt"):
    """Reads system instruction configuration from an external text file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    # Safe default fallback prompt
    return "Summarize the input text and output raw JSON containing 'summary' and 'file_format'."

def init_gemini_client():
    """Initializes the Gemini client using environmental variables and JSON config."""
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=800,
        response_mime_type="application/json",
        system_instruction=load_system_prompt()
    )
    return client, config

def log_run(user_input, response, summary_text, file_format, output_filename):
    """Generates a separate session log file for audit and tracking purposes."""
    now = datetime.now(LOCAL_TZ)
    log_filename = f"run_log_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_filename, "w", encoding="utf-8", errors="replace") as f:
        f.write(f"Timestamp: {now.isoformat()}\n")
        f.write(f"Format: {file_format} | Output: {output_filename}\n")
        f.write("=" * 40 + "\nUser Input:\n" + user_input + "\n")
        f.write("=" * 40 + "\nModel Summary:\n" + summary_text + "\n")
        f.write("=" * 40 + "\n" + "[RAW GEMINI API RESPONSE OBJECT]\n" )
        f.write(response.text + "\n")
    print(f"Log archived to {log_filename}")

def generate_txt(text):
    """Outputs the markdown text directly into a text file."""
    filename = "summarize.txt"
    with open(filename, "w", encoding="utf-8", errors="replace") as f:
        f.write(text)
    print(f"File created: {filename}")
    return filename

def detect_text_direction(text):
    """Evaluates text script property to determine logical layout direction."""
    alpha_chars = [ch for ch in text if ch.isalpha()]
    if not alpha_chars:
        return "ltr"
    
    arabic_chars = sum(1 for ch in alpha_chars if '\u0600' <= ch <= '\u06FF')
    return "rtl" if (arabic_chars / len(alpha_chars)) > 0.3 else "ltr"

def generate_pdf(text):
    """Renders formatted markdown string to an optimized A4 PDF layout."""
    filename = "summarize.pdf"
    direction = detect_text_direction(text)

    html_content = MarkdownIt("gfm-like").render(text)
    
    html_styled = f"""
    <!DOCTYPE html>
    <html lang="{"ar" if direction == "rtl" else "en"}" dir="{direction}">
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 2.5cm 2cm;
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #6c757d;
                }}
            }}
            body {{
                font-family: 'Noto Naskh Arabic', 'Noto Sans Arabic', 'DejaVu Sans', sans-serif;
                direction: {direction};
                text-align: {"right" if direction == "rtl" else "left"};
                color: #2c3e50;
                line-height: 1.8;
                font-size: 11pt;
            }}
            h1 {{ font-size: 22pt; color: #2c3e50; border-bottom: 2px solid #34495e; padding-bottom: 10px; margin-bottom: 20px; }}
            h2 {{ font-size: 15pt; color: #2980b9; margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #ecf0f1; padding-bottom: 5px; }}
            h3 {{ font-size: 12pt; color: #34495e; margin-top: 18px; }}
            p {{ margin-bottom: 12px; text-align: justify; }}
            ul, ol {{ margin-bottom: 18px; padding-inline-start: 22px; }}
            li {{ margin-bottom: 6px; }}
            blockquote {{ background-color: #f8f9fa; border-inline-start: 4px solid #2980b9; padding: 10px 15px; margin: 18px 0; color: #555; }}
            pre {{ background-color: #f8f9fa; border: 1px solid #e0e0e0; padding: 12px; border-radius: 6px; direction: ltr; text-align: left; font-family: 'DejaVu Sans Mono', monospace; font-size: 10pt; overflow-wrap: break-word; }}
            code {{ font-family: 'DejaVu Sans Mono', monospace; background-color: #eaeded; padding: 2px 5px; font-size: 10pt; }}
            table {{ width: 100%; margin: 18px 0; border-collapse: collapse; border: 1px solid #dee2e6; }}
            th {{ background-color: #2980b9; color: white; padding: 10px; }}
            td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    HTML(string=html_styled).write_pdf(filename)
    print(f"File created: {filename}")
    return filename

def process_workflow(user_input):
    """Executes the execution graph: Inference -> Extraction -> File Routing."""
    client, config = init_gemini_client()
    print("Executing analysis pipeline...")
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=user_input,
        config=config
    )
    
    try:
        data = json.loads(response.text)
        summary_text = data.get("summary", "")
        file_format = data.get("file_format", "txt").lower()
        
        output_filename = generate_pdf(summary_text) if file_format == "pdf" else generate_txt(summary_text)
        log_run(user_input, response, summary_text, file_format, output_filename)

 
        return {
            "success": True,
            "summary": summary_text,
            "file_format": file_format,
            "output_filename": output_filename,
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Invalid internal response payload structure.",
        }

if __name__ == "__main__":
    print("=== Production AI Pipeline CLI ===")
    user_text = input("Pipeline Input Context:\n> ").strip()
    if user_text:
        result = process_workflow(user_text)
        if result["success"]:
            print(f"\n[Execution Meta] Detected Target Format: {result['file_format'].upper()}")
            print(f"File created: {result['output_filename']}")
        else:
            print(f"Pipeline Execution Error: {result['error']}")