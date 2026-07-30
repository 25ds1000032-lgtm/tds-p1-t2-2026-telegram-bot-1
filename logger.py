import json
from datetime import datetime

LOG_FILE = "run.jsonl"


def log_run(chat_id, user_id, question, answer, status="success"):
    """
    Append one interaction to run.jsonl
    """

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "chat_id": chat_id,
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "status": status,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record