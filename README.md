# Unstructured Text to Structured JSON Converter

## Overview

This project converts unstructured plain text into structured JSON strictly following a provided JSON schema, using the Ollama Qwen LLM.

## Components

- **Frontend:** Streamlit app (`streamlit_app.py`)
- **Backend:** FastAPI app (`backend.py`)
- **Model:** Ollama Qwen (run locally)

## How to Run

1. **Install dependencies:**

   ```bash
   pip install streamlit fastapi pydantic requests jsonschema uvicorn
   ```

2. **Start the Ollama Qwen model (if not already running):**

   ```bash
   ollama run qwen
   ```

   (Make sure Ollama is installed and running on your machine.)

3. **Start the FastAPI backend:**

   ```bash
   uvicorn backend:app --reload
   ```

   (Run this command in the directory containing `backend.py`.)

4. **Start the Streamlit frontend:**

   ```bash
   streamlit run streamlit_app.py
   ```

   (Run this command in the directory containing `streamlit_app.py`.)

5. **Usage:**

   - Open the Streamlit web UI (usually at http://localhost:8501).
   - Upload your unstructured text file and JSON schema file.
   - Click "Convert" to get the structured JSON output.

## Notes

- The backend validates the output against your schema.
- Ollama Qwen must be running and accessible at `http://localhost:11434`.
