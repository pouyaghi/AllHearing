import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"


def analyze_user_messages(username, messages):

    messages_text = "\n".join(messages)

    prompt = f"""
You are analyzing a Telegram user based ONLY on their messages.

Username: {username}

Rules:
- Only infer attributes supported by the messages.
- Do NOT invent information.
- If something cannot be inferred, omit it.
- Return ONLY a valid JSON dictionary.

Messages:
{messages_text}
"""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=data
    )

    if response.status_code != 200:
        return {"error": f"Gemini API error: {response.status_code}"}

    try:
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        profile = json.loads(text)

        return profile

    except Exception:
        return {
            "error": "Failed to parse Gemini response",
            "raw": response.text
        }