import os
import requests
from dotenv import load_dotenv

load_dotenv()

AIPIPE_URL = os.getenv("AIPIPE_URL")
AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")


def ask_llm(messages):
    """
    Send conversation history to AI Pipe
    and return only the assistant text.
    """

    if not AIPIPE_URL or not AIPIPE_TOKEN:
        raise RuntimeError(
            "Missing AIPIPE_URL or AIPIPE_TOKEN in .env"
        )

    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": messages,
        "temperature": 0.2
    }

    response = requests.post(
        AIPIPE_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]