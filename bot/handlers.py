import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

from data.storage import get_users, get_messages_by_user
from analysis.analyzer import analyze_user_messages


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

    profile_text = json.dumps(profile, indent=2, ensure_ascii=False)

    await query.edit_message_text(f"Profile for {username}:\n{profile_text}")


def register_handlers(app):
    app.add_handler(CommandHandler("people", people))
    app.add_handler(CallbackQueryHandler(user_selected))