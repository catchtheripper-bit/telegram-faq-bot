from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import os

# Load knowledge base
def load_kb():
    with open("faq.json", "r") as f:
        return json.load(f)

knowledge = load_kb()

def start(update, context):
    update.message.reply_text("Welcome to the Knowledge Bot! Type a keyword like 'rules' or 'contact' to get started.")

def reply(update, context):
    global knowledge
    user_text = update.message.text.lower().strip()

    if user_text in knowledge:
        update.message.reply_text(knowledge[user_text])
    else:
        update.message.reply_text("Sorry, I don't have an answer for that.")

def main():
    TOKEN = os.getenv("TOKEN")  # Railway/Render will use environment variable
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()