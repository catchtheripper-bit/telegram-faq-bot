import json
import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Load FAQ knowledge base
with open("faq.json", "r", encoding="utf-8-sig") as f:
    faq = json.load(f)

# Normalize keys for case-insensitive lookup
faq = {k.lower(): v for k, v in faq.items()}


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I’m your FAQ Bot. Ask me anything!")


# Handle messages
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower().strip()
    response = faq.get(user_message, "Sorry, I don’t know the answer to that.")
    await update.message.reply_text(response)


def main() -> None:
    TOKEN = os.getenv("TOKEN")
    PORT = int(os.environ.get("PORT", 8080))
    HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

    if not TOKEN or not HOSTNAME:
        raise RuntimeError("BOT_TOKEN or RENDER_EXTERNAL_HOSTNAME not set!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Start webhook server
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{HOSTNAME}/{TOKEN}",
    )


if __name__ == "__main__":
    main()
