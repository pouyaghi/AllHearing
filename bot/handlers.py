import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

from data.storage import get_users, get_messages_by_user
from analysis.analyzer import analyze_user_messages


def format_profile(username, profile):
    if "error" in profile:
        return f"⚠️ Error analyzing user:\n{profile['error']}"

    message = f"👤 Profile for {username}\n\n"

    for key, values in profile.items():

        # skip simple fields like name
        if isinstance(values, str):
            continue

        if not values:
            continue

        title = key.replace("_", " ").title()
        message += f"📌 {title}\n"

        for v in values:
            message += f"• {v}\n"

        message += "\n"

    return message.strip()


async def people(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_users()

    if not users:
        await update.message.reply_text("No users stored yet.")
        return

    buttons = [[InlineKeyboardButton(u, callback_data=u)] for u in users]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text("Select a user:", reply_markup=keyboard)


async def user_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    username = query.data
    messages = get_messages_by_user(username)

    if not messages:
        await query.edit_message_text("No messages found for this user.")
        return

    profile = analyze_user_messages(username, messages)

    # convert JSON profile into readable text
    formatted_profile = format_profile(username, profile)

    await query.edit_message_text(formatted_profile)


def register_handlers(app):
    app.add_handler(CommandHandler("people", people))
    app.add_handler(CallbackQueryHandler(user_selected))