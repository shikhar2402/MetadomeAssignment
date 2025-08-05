from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import requests
import jsonschema

app = FastAPI()

class ConvertRequest(BaseModel):
    text: str
    schema: str

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
    print("calling")
    # Call Ollama Qwen model (assuming Ollama is running locally)
    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )
    result = ollama_response.json()
    # Save the raw model result to a local file for inspection
    with open("ollama_raw_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    # Extract JSON object from the model's response, even if surrounded by text or markdown
    try:
        print("result", result)
        response_text = result["response"]
        # Find the first '{' and the last '}' for the JSON object
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON object found in model response.")
        json_str = response_text[start:end]
        print("json str" , json_str)
        structured = json.loads(json_str)
        schema_obj = json.loads(req.schema)
        jsonschema.validate(instance=structured, schema=schema_obj)
    except Exception as e:
        return {"error": f"Failed to parse or validate model output: {str(e)}\n\nModel output: {result.get('response', '')}"}, 400
    return {"structured": structured}
