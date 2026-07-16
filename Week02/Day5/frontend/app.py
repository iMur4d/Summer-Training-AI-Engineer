import os
import re
import json
import streamlit as st

# Load vault path from storage if available
try:
    from backend.storage import VAULT_PATH
except ImportError:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    VAULT_PATH = os.path.join(BASE_DIR, "vault")

st.set_page_config(layout="wide", page_title="Obsidian Brain")

# Initialize language state (Streamlit UI only, notes remain in original language)
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

direction = "rtl" if st.session_state.lang == 'العربية' else "ltr"
text_align = "right" if st.session_state.lang == 'العربية' else "left"

st.markdown(f"""
<style>
    /* Completely eradicate Streamlit default UI constraints */
    header {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    
    .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }}
    
    iframe[title="streamlit_html"] {{
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
    }}
    
    .stApp {{
        background-color: #09090b !important;
        overflow: hidden !important;
        color: #c9d1d9;
    }}
    .css-1d391kg {{
        background-color: #09090b !important;
    }}
    
    h1, h2, h3, p, .rtl-text {{
        direction: {direction};
        text-align: {text_align};
    }}
</style>
""", unsafe_allow_html=True)

def parse_markdown_file(filepath):
    """Parses the markdown file, extracts metadata, and returns raw markdown content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from frontmatter
    title = "Untitled"
    title_match = re.search(r'title:\s*"(.*?)"', content)
    if title_match:
        title = title_match.group(1)
        
    # Extract date
    date = "Unknown Date"
    date_match = re.search(r'date:\s*(.*?)\n', content)
    if date_match:
        date = date_match.group(1).strip()
        
    # Extract tags
    tags = []
    tags_match = re.search(r'tags:\s*\[(.*?)\]', content)
    if tags_match:
        tags = [t.strip() for t in tags_match.group(1).split(',') if t.strip()]
        
    lobes = ['frontal', 'occipital', 'temporal', 'cerebellum']
    assigned_lobe = 'frontal'
    if tags:
        assigned_lobe = lobes[hash(tags[0]) % len(lobes)]
        
    # Remove YAML frontmatter from the raw content so it isn't rendered
    raw_content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL).strip()
        
    return {
        "id": os.path.basename(filepath),
        "title": title,
        "date": date,
        "tags": tags,
        "raw_content": raw_content,
        "lobe": assigned_lobe
    }

def load_notes():
    notes = []
    if os.path.exists(VAULT_PATH):
        for filename in os.listdir(VAULT_PATH):
            if filename.endswith(".md"):
                filepath = os.path.join(VAULT_PATH, filename)
                notes.append(parse_markdown_file(filepath))
    return notes

# Sidebar for Language Selection
with st.sidebar:
    selected_lang = st.radio("Language / اللغة", ['English', 'العربية'], index=0 if st.session_state.lang == 'English' else 1)
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    st.markdown("---")
    if st.session_state.lang == 'English':
        st.markdown("**Instructions:**\n- Drag to rotate the brain.\n- Scroll to zoom.\n- Click on any glowing node to read the note.")
    else:
        st.markdown("<div class='rtl-text'><b>التعليمات:</b><br>- اسحب لتدوير الدماغ.<br>- مرر للتكبير والتصغير.<br>- انقر على أي عقدة مضيئة لقراءة الملاحظة.</div>", unsafe_allow_html=True)


# Load real notes from Vault
vault_notes = load_notes()

# Prepare graph data
# As per v0.6.0 requirements, links/edges are intentionally empty to reflect current capabilities honestly.
graph_data = json.dumps({
    "nodes": vault_notes,
    "links": [],  # Empty layer ready for future semantic relationships
    "explore_text": "Explore Notes" if st.session_state.lang == 'English' else "استكشف الملاحظات"
})

# Read HTML template and modules
try:
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    with open(os.path.join(assets_dir, "brain_graph.html"), "r", encoding="utf-8") as f:
        html_template = f.read()
        
    with open(os.path.join(assets_dir, "styles.css"), "r", encoding="utf-8") as f:
        css_content = f.read()
        
    with open(os.path.join(assets_dir, "brain.js"), "r", encoding="utf-8") as f:
        js_content = f.read()

    # Inject modules first so placeholders are in the string
    html_code = html_template.replace("<!-- INJECT_CSS -->", f"<style>\n{css_content}\n</style>")
    html_code = html_code.replace("<!-- INJECT_JS -->", f"<script>\n{js_content}\n</script>")
    
    # Then inject data
    html_code = html_code.replace("{{ GRAPH_DATA }}", graph_data).replace("{{GRAPH_DATA}}", graph_data)
    
    # Give the canvas full width
    st.components.v1.html(html_code, height=800)
except FileNotFoundError as e:
    st.error(f"Missing template file: {e}")


