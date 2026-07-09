import streamlit as st
from pipeline import process_workflow

st.set_page_config(page_title="AI Summarization Pipeline", page_icon="🤖", layout="centered")

st.title("AI Summarization Pipeline")
st.write("Paste your text below. The output format (PDF or TXT) is decided automatically based on what you ask for in the prompt.")

user_input = st.text_area(
    "Enter your text and instructions:",
    height=250,
    placeholder="Example: Summarize this article and give me a PDF suitable for printing..."
)

generate_clicked = st.button("Generate Summary", type="primary", disabled=not user_input.strip())

if generate_clicked:
    with st.spinner("Analyzing and summarizing..."):
        result = process_workflow(user_input)

    if result["success"]:
        st.success(f"Done. Detected format: {result['file_format'].upper()}")

        st.markdown("### Preview")
        st.markdown(result["summary"])

        output_path = result["output_filename"]
        mime_type = "application/pdf" if result["file_format"] == "pdf" else "text/plain"

        with open(output_path, "rb") as f:
            st.download_button(
                label=f"Download {output_path}",
                data=f.read(),
                file_name=output_path,
                mime=mime_type,
            )
    else:
        st.error(f"Something went wrong: {result['error']}")