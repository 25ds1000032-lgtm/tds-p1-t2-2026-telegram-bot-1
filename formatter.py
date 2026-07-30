import json
import os
from dotenv import load_dotenv

load_dotenv()

LOG_URL = os.getenv("LOG_URL")

if not LOG_URL:
    raise RuntimeError("LOG_URL missing in .env")


def format_response(llm_output):
    """
    Ensure the final Telegram reply is exactly one JSON object.
    """

    try:
        data = json.loads(llm_output)

        if not isinstance(data, dict):
            raise ValueError()

        if "answer" not in data:
            data = {
                "answer": data
            }

    except Exception:

        data = {
            "answer": llm_output
        }

    data["log_url"] = LOG_URL

    return json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":")
    )