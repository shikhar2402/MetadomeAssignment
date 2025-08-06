# Unstructured Text to Structured JSON Converter

## Solution Design Doc

### System Architecture

```
+-------------------+         REST API         +-------------------+         Ollama LLM API
|   Streamlit UI    | <---------------------> |    FastAPI Server | <---------------------> (local inference)
+-------------------+                         +-------------------+
        |                                            |
        |                                            |
   User uploads text & schema                   Backend validates, prompts LLM,
   selects model, triggers conversion           fixes output, validates JSON
        |                                            |
   Receives structured JSON, logs, etc.         Returns structured JSON
```

- **Frontend:** Streamlit app for file upload, schema preview, model selection, and result display.
- **Backend:** FastAPI app for prompt orchestration, LLM calls, output fixing, and schema validation.
- **LLM Layer:** Ollama runs local models (qwen2.5:7b, llama2:70b, etc.) for conversion and JSON fixing.

### Implementation Log

- **Initial Design:** CLI and web UI considered; Streamlit chosen for rapid prototyping and interactivity.
- **Backend:** FastAPI chosen for async REST API and easy integration with Python ecosystem.
- **LLM Selection:** Ollama used for local inference due to lack of OpenAI API credits.
- **Error Handling:** Added second LLM pass to fix invalid JSON outputs.
- **Validation:** Used `jsonschema` for strict schema validation.
- **Refactor:** Split into `frontend/` and `backend/` directories for clarity.
- **UI Improvements:** Added sidebar, previews, model info, log viewing, and download options.

## Overview

This project converts unstructured plain text (e.g., BibTeX) into structured JSON strictly following a provided JSON schema, using LLMs via Ollama.

## Directory Structure

```
meta/
  backend/
    main.py
  frontend/
    streamlit_app.py
  requirements.txt
  README.md
```

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Install and Run Ollama

- Download and install Ollama from [https://ollama.com/download](https://ollama.com/download)
- Pull required models (example for qwen2.5:7b):
  ```bash
  ollama pull qwen2.5:7b
  ollama pull llama2:70b
  ollama pull gpt-oss
  ollama pull deepseek-r1
  ollama pull llama3.1
  ```
- Start Ollama server:
  ```bash
  ollama serve
  ```

### 4. Run Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

### 5. Run Frontend (Streamlit)

```bash
streamlit run frontend/streamlit_app.py
```

### 6. Usage

- Open the Streamlit UI (usually at http://localhost:8501).
- Upload your unstructured text file and JSON schema file.
- Select the desired LLM model.
- Click "Convert" to get the structured JSON output.

## Limitations

- **Ollama-based LLMs:** We use Ollama for local LLM inference since we do not have credits for OpenAI GPT or other paid APIs.
- **Model Output:** LLMs may sometimes generate invalid JSON (comments, escape errors); we use a second LLM pass to fix and validate the output.
- **Schema Strictness:** The output is validated against your schema, but complex/nested schemas may require additional prompt engineering.
- **No Streaming/Async:** The system is synchronous and not optimized for high throughput or streaming.
- **Local Only:** All inference is local; no cloud APIs are used.

## requirements.txt

See below for required Python packages.
