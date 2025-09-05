import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Load FAQ knowledge base
with open("faq.json", "r", encoding="utf-8-sig") as f:
    faq = json.load(f)


# Normalize keys (case-insensitive matching)
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
    # Get your bot token (replace with your own)
    import os
    TOKEN = os.getenv("BOT_TOKEN")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot started polling...")
    app.run_polling()

if __name__ == "__main__":
    main()



