import streamlit as st
import requests
import json

st.set_page_config(page_title="Text to Structured JSON Converter", layout="wide")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Choose LLM model",
        ["qwen2.5:7b", "llama2:70b", "gpt-oss", "deepseek-r1", "llama3.1"],
        help="Select the LLM model to use for conversion."
    )
    st.markdown("""
    **Model Info**  
    - All models run locally via Ollama.
    - No OpenAI API credits required.
    - If unsure, use the default (`qwen2.5:7b`).
    """)

st.title("Unstructured Text to Structured JSON Converter")
st.markdown("Upload your unstructured text (e.g., BibTeX) and a JSON schema. The system will convert the text to structured JSON using your chosen LLM.")

col1, col2 = st.columns(2)
with col1:
    text_file = st.file_uploader("Upload unstructured text file", type=["txt"])
    if text_file:
        st.subheader("Text Preview")
        st.code(text_file.read().decode("utf-8"), language="text")
        text_file.seek(0)  # Reset for reading again

with col2:
    schema_file = st.file_uploader("Upload JSON schema file", type=["json"])

if st.button("Convert", use_container_width=True) and text_file and schema_file:
    text = text_file.read().decode("utf-8")
    schema = schema_file.read().decode("utf-8")
    with st.spinner("Converting... Please wait."):
        response = requests.post(
            "http://localhost:8000/convert",
            json={"text": text, "schema": schema, "model": model}
        )
        try:
            resp_json = response.json()
        except Exception:
            st.error(f"Error: Could not parse backend response: {response.text}")
        else:
            if response.status_code == 200 and "structured" in resp_json:
                st.success("Conversion successful! 🎉")
                st.subheader("Structured JSON Output")
                st.json(resp_json["structured"])
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(resp_json["structured"], indent=2),
                    file_name="output.json",
                    mime="application/json"
                )
                st.info(f"Model used: {resp_json.get('model_used', model)}")
                st.caption(f"Available models: {', '.join(resp_json.get('available_models', []))}")
            else:
                error_msg = response.text
                if isinstance(resp_json, dict):
                    error_msg = resp_json.get('error', response.text)
                st.error(f"Error: {error_msg}")
