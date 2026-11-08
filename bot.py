import os
import time
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")
last_call = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Welcome to Fake Call Prank Bot!\n\n"
        "আমাকে দিয়ে মজার Fake Call Prank করতে পারো।\n\n"
        "/call - Fake incoming call\n"
        "/help - Help"
    )

async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()

    if now - last_call.get(user_id, 0) < 15:
        await update.message.reply_text("⏳ একটু অপেক্ষা করো!")
        return

    last_call[user_id] = now
    caller = " ".join(context.args) or "Unknown Caller"

    keyboard = [
        [
            InlineKeyboardButton("📞 Answer", callback_data="answer"),
            InlineKeyboardButton("❌ Decline", callback_data="decline"),
        ]
    ]

    await update.message.reply_text(
        f"📲 INCOMING CALL — PRANK SIMULATION\n\n"
        f"👤 Caller: {caller}\n"
        f"🔔 Ring Ring... Ring Ring...\n\n"
        f"এটি শুধু Telegram-এর মজার Simulation!",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "answer":
        message = "😂 হ্যালো! এটা একটা প্র্যাঙ্ক কল!"
    else:
        message = "📵 তুমি কলটি কেটে দিয়েছ!"

    await query.edit_message_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Fake Call Prank Bot\n\n"
        "/start - Start bot\n"
        "/call - Make a fake call\n"
        "/call Friend - Caller name সহ prank"
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN সেট করা নেই!")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("call", call))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(buttons))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
