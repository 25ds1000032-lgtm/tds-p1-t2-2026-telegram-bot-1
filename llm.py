from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")

client = OpenAI(
    api_key=AIPIPE_TOKEN,
    base_url="https://aipipe.org/openai/v1",
)

SYSTEM_PROMPT = """
You are an expert data analyst.

Solve the user's LAST request.

If the user specifies a JSON format,
return ONLY that JSON.

Never use markdown.

Never add explanations.

Use previous conversation as context.
"""


def ask_llm(messages):

    try:

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *messages,
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM Error: {e}"