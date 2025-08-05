import streamlit as st
import requests
import json

st.title("Unstructured Text to Structured JSON Converter")

st.markdown("Upload your unstructured text and JSON schema. The system will convert the text to structured JSON using the schema.")

text_file = st.file_uploader("Upload unstructured text file", type=["txt"])
schema_file = st.file_uploader("Upload JSON schema file", type=["json"])

if st.button("Convert") and text_file and schema_file:
    text = text_file.read().decode("utf-8")
    schema = schema_file.read().decode("utf-8")
    with st.spinner("Converting..."):
        response = requests.post(
            "http://localhost:8000/convert",
            json={"text": text, "schema": schema}
        )
        try:
            resp_json = response.json()
        except Exception:
            st.error(f"Error: Could not parse backend response: {response.text}")
        else:
            if response.status_code == 200 and "structured" in resp_json:
                st.success("Conversion successful!")
                st.json(resp_json["structured"])
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(resp_json["structured"], indent=2),
                    file_name="output.json",
                    mime="application/json"
                )
            else:
                # Show backend error details if available
                error_msg = response.text
                if isinstance(resp_json, dict):
                    # If backend returned a list (e.g., [{"error": "...", 400}]), handle that
                    if isinstance(resp_json, list) and len(resp_json) > 0 and isinstance(resp_json[0], dict):
                        error_msg = resp_json[0].get('error', response.text)
                    else:
                        error_msg = resp_json.get('error', response.text)
                st.error(f"Error: {error_msg}")
