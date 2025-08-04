import subprocess
import json
from config import REQUIRED_FIELDS

def extract_fields_with_mistral(email_body: str):
    prompt = f"""
You are an assistant that extracts structured data from emails.

Required fields:
{', '.join(REQUIRED_FIELDS)}

Return the result **only** as valid JSON,  without comments, explanations or notes. Use `null` if anything is missing.
At the end, include a key "Missing Fields" which is a list of missing field names.

Instructions:
- Do not include any comments or explanations in the JSON.
- Return ONLY a valid JSON object (no comments or explanation).
- If a date like "this Monday" or "next week" is used, treat it as missing. Don't try to guess.
- Use null for any missing field.
- Add a "Missing Fields" list.

Example:
{{
  "Trainer Name": "Ashiya",
  "Session Topic": "Docker",
  "Date": "2024-08-10",
  "Time": "10:00 AM",
  "Duration": "90 minutes",
  "Mode": "Online",
  "Missing Fields": []
}}

Email:
\"\"\"
{email_body}
\"\"\"
"""

    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        capture_output=True,
        text=True
    )

    try:
        response = result.stdout.strip()

        # Optional debug log
        print("🧠 Mistral raw output:\n", response)

        # Try to extract the first JSON block
        start = response.find('{')
        end = response.rfind('}') + 1
        json_str = response[start:end]

        json_data = json.loads(json_str)
        return json_data
    except Exception as e:
        print(f"[Mistral Error] {e}")
        return None
