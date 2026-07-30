import os
import json
from dotenv import load_dotenv

load_dotenv()

LOG_URL = os.getenv("LOG_URL")


def format_response(answer):
    """
    Convert assistant reply into required JSON format.
    """

    response = {
        "answer": answer,
        "log_url": LOG_URL
    }

    return json.dumps(
        response,
        ensure_ascii=False
    )