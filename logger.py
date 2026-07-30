import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = "run.jsonl"


def log_run(user_id, question, answer):
    """
    Append one interaction to run.jsonl
    """

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "question": question,
        "answer": answer
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            json.dumps(record, ensure_ascii=False)
            + "\n"
        )

    return record