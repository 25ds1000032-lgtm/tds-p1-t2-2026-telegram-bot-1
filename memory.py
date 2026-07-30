conversation_history = {}

MAX_HISTORY = 8


def add_message(chat_id, role, content):
    history = conversation_history.setdefault(chat_id, [])

    history.append(
        {
            "role": role,
            "content": content,
        }
    )

    if len(history) > MAX_HISTORY:
        conversation_history[chat_id] = history[-MAX_HISTORY:]


def get_history(chat_id):
    return conversation_history.get(chat_id, [])