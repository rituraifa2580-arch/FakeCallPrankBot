import os
import tempfile
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

WELCOME = """
🌙 Welcome to Soul Downloader!

TikTok | Facebook | YouTube

একটি অনুমোদিত ভিডিও লিংক পাঠাও।
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("https://", "http://")):
        await update.message.reply_text("সঠিক লিংক পাঠাও।")
        return

    status = await update.message.reply_text("⏳ লিংক পরীক্ষা করছি...")

    try:
        with tempfile.TemporaryDirectory() as folder:
            options = {
                "format": "best[ext=mp4]/best",
                "outtmpl": f"{folder}/video.%(ext)s",
                "noplaylist": True,
                "max_filesize": 49 * 1024 * 1024,
                "quiet": True,
            }

            def get_video():
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    return ydl.prepare_filename(info)

            path = await asyncio.to_thread(get_video)

            if not os.path.exists(path):
                raise Exception("ভিডিও পাওয়া যায়নি।")

            await status.edit_text("📤 Telegram-এ পাঠাচ্ছি...")

            with open(path, "rb") as video:
                await update.message.reply_video(
                    video=video,
                    caption="🌙 Soul Downloader"
                )

            await status.delete()

    except Exception:
        await status.edit_text(
            "❌ ডাউনলোড করা যায়নি। লিংকটি পরীক্ষা করো "
            "অথবা সাইটটি ডাউনলোড অনুমোদন করে কি না দেখো।"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()

if __name__ == "__main__":
    main()
