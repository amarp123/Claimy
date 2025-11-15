import google.generativeai as genai
import json

# Your Gemini API Key — replace with your key
GEMINI_API_KEY = "AIzaSyAUag3TLW0Se9XD---oq5ed09zx1TAyVlw"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_insurance_text(text: str):
    prompt = f"""
You are an insurance verification AI.
Analyze the extracted hospital insurance document text.

TEXT:
{text}

Return ONLY a valid JSON with these fields:

{{
  "patient_name": "",
  "hospital_name": "",
  "diagnosis": "",
  "total_bill": "",
  "treatment_date": "",
  "is_valid_document": "yes/no",
  "fraud_score": 0
}}

Rules:
- fraud_score must be a number between 0–100
- is_valid_document must be "yes" or "no"
- Return ONLY JSON, no explanation
    """

    response = model.generate_content(prompt)

    raw = response.text.strip()

    try:
        return json.loads(raw)
    except:
        # If Gemini wraps JSON in ```json blocks
        cleaned = raw.replace("```json", "").replace("```", "")
        return json.loads(cleaned)
