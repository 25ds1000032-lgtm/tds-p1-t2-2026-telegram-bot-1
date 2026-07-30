import os
import re
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from llm import ask_llm
from formatter import format_response
from logger import log_run
from memory import add_message, get_history
from dataset import download_file, analyze_dataset


# -------------------------------------------------
# Load environment variables
# -------------------------------------------------

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found in .env"
    )


# -------------------------------------------------
# System Prompt
# -------------------------------------------------

SYSTEM_PROMPT = """
You are an expert data analyst.

Answer the user's LAST message.

Use previous conversation only as context.

Give accurate and useful answers.

Do not use markdown unless requested.
"""


# -------------------------------------------------
# URL Detection
# -------------------------------------------------

def extract_url(text):

    match = re.search(
        r"https?://\S+",
        text
    )

    if match:
        return match.group(0)

    return None


# -------------------------------------------------
# Telegram Message Handler
# -------------------------------------------------

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id

    user_text = update.message.text


    # Save user message
    add_message(
        chat_id,
        "user",
        user_text
    )


    # Get conversation history
    history = get_history(chat_id)


    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        *history,
    ]


    dataset_url = extract_url(
        user_text
    )


    try:

        # -----------------------------------------
        # Dataset analysis path
        # -----------------------------------------

        if dataset_url:

            file_path = download_file(
                dataset_url
            )

            dataset_info = analyze_dataset(
                file_path
            )

            messages.append(
                {
                    "role": "user",
                    "content":
                    f"""
                    The user provided a dataset.

                    Dataset analysis:

                    {dataset_info}

                    Explain the important insights.
                    """
                }
            )


        # -----------------------------------------
        # AI Pipe response
        # -----------------------------------------

        answer = ask_llm(
            messages
        )


    except Exception as e:

        answer = f"Error: {str(e)}"



    # Save assistant message
    add_message(
        chat_id,
        "assistant",
        answer
    )


    # Log interaction
    log_run(
        chat_id,
        user_text,
        answer
    )


    # JSON-only output
    final_response = format_response(
        answer
    )


    await update.message.reply_text(
        final_response
    )


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    app = ApplicationBuilder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )


    print(
        "Bot is running..."
    )


    app.run_polling()



if __name__ == "__main__":
    main()