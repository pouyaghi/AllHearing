import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

from data.storage import save_message, init_db
from bot.handlers import register_handlers
from pipeline.batch_processor import process_batch_if_needed


# load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming Telegram messages
    """

    message = update.message

    if not message:
        return

    # ignore non-text messages
    if not message.text:
        return

    username = message.from_user.username or message.from_user.first_name
    text = message.text

    # save message
    message_count = save_message(username, text)

    # trigger batch processing
    process_batch_if_needed(message_count)


def main():

    # initialize database
    init_db()

    # create telegram application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # register command handlers
    register_handlers(app)

    # listen to text messages only
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()