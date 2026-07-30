from llm import ask_llm


messages = [
    {
        "role": "user",
        "content": "Say hello in one sentence"
    }
]


reply = ask_llm(messages)

print(reply)