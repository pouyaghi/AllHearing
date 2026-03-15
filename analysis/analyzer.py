import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"


def analyze_user_messages(username, messages):

    messages_text = "\n".join(messages)

    prompt = f"""
Analyze the following Telegram messages written by the user '{username}'.

Your task:
Infer anything that can reasonably be understood about this person from their messages.

Examples of possible attributes:
- personality traits
- interests
- communication style
- social tendencies
- plans or intentions
- habits

Rules:
- Only include attributes supported by the messages.
- If something is unknown, do not invent it.
- Do not guess names or facts not mentioned.
- Return ONLY valid JSON.
- Do NOT wrap the JSON in markdown.
- Do NOT use ```json blocks.

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
    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        return {"error": f"Gemini API error: {response.status_code}", "raw": response.text}

    try:
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # remove markdown code blocks if Gemini added them
        text = text.replace("```json", "").replace("```", "").strip()

        profile = json.loads(text)

        return profile

    except Exception:
        return {
            "error": "Failed to parse Gemini response",
            "raw": text if 'text' in locals() else response.text
        }
    

def analyze_conversation(messages):

    conversation = ""

    for user, text in messages:
        conversation += f"{user}: {text}\n"

    prompt = f"""
You are analyzing a conversation to infer facts about people.

IMPORTANT RULES:
- Do not assume someone likes something unless they explicitly say they like it.
- If someone answers a question like "what food do you hate?" and says "lasagna",
  that means they DISLIKE lasagna.
- Use conversation context to understand questions and answers.
- Never infer the opposite meaning.

Conversation:
{conversation}

Create a profile for each participant.

Return ONLY valid JSON.
Do not use markdown formatting.
Only include attributes that are strongly supported by the conversation.
"""

    # your existing Gemini request code here