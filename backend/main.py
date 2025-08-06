from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import requests
import jsonschema
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

AVAILABLE_MODELS = [
    "llama2:70b",
    "gpt-oss",
    "deepseek-r1",
    "llama3.1",
    "qwen2.5:7b"
]

class ConvertRequest(BaseModel):
    text: str
    schema: str
    model: str = "qwen2.5:7b"  # Optional, default to qwen2.5:7b

@app.post("/convert")
async def convert(req: ConvertRequest):
    # Prepare prompt for Ollama Qwen
    prompt = (
        "Convert the following text to a JSON object that strictly follows this JSON schema. "
        "Do not include any extra fields or fields which are not present in the text. Output only the JSON object.\n\n"
        "Schema:\n"
        f"{req.schema}\n\n"
        "Text:\n"
        f"{req.text}\n"
    )
    logging.info("Calling Ollama model: %s", req.model)
    # Use requested model if available, else fallback to default
    model_name = req.model if req.model in AVAILABLE_MODELS else "qwen2.5:7b"
    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )
    result = ollama_response.json()
    try:
        response_text = result["response"]
        # Find the first '{' and the last '}' for the JSON object
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON object found in model response.")
        json_str = response_text[start:end]
        logging.info("Extracted JSON string from model response.")
        # LLM layer to fix invalid JSON
        fix_prompt = (
            "Fix the following string so that it is valid JSON. "
            "Remove any comments, invalid escape sequences, and ensure all keys and values are properly quoted. "
            "Output only the corrected JSON string.\n\n"
            f"{json_str}\n"
        )
        fix_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": fix_prompt,
                "stream": False
            }
        )
        fixed_json_str = fix_response.json()["response"]
        # Find the first '{' and last '}' again in case LLM adds text
        start_fixed = fixed_json_str.find('{')
        end_fixed = fixed_json_str.rfind('}') + 1
        if start_fixed == -1 or end_fixed == -1:
            raise ValueError("No valid JSON object found after LLM fix.")
        fixed_json_str = fixed_json_str[start_fixed:end_fixed]
        logging.info("Fixed JSON string using LLM.")
        structured = json.loads(fixed_json_str)
    except Exception as e:
        logging.error("Failed to parse or validate model output: %s", str(e))
        return {"error": f"Failed to parse or validate model output: {str(e)}\n\nModel output: {result.get('response', '')}"}, 400
    return {"structured": structured, "model_used": model_name, "available_models": AVAILABLE_MODELS}
