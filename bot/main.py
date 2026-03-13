import os
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

from data.storage import save_message
from bot.handlers import register_handlers

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def message_listener(update, context):
    """Store every message from users."""
    if update.message and update.message.text:
        username = update.message.from_user.username or update.message.from_user.first_name
        text = update.message.text

        save_message(username, text)


def main():
    app = Application.builder().token(TOKEN).build()

    # Store every message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_listener))

    # Register commands
    register_handlers(app)

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()