import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram bot token
TOKEN = "1997127715:AAFk1qjeTNlV0zj8hrxIA8skIKZQuCkjKVc"

# Start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! YouTube'dan video yuklab olish uchun link yuboring."
    )

# YouTube videoni yuklab olish
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    await update.message.reply_text(f"Video yuklab olinmoqda: {url}")

    video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info)

        # Agar fayl juda katta bo'lsa, yuborishdan oldin tekshiramiz
        if os.path.getsize(video_filename) > 50 * 1024 * 1024:
            await update.message.reply_text("Kechirasiz, video hajmi Telegram cheklovidan oshib ketdi.")
            os.remove(video_filename)
            return

        # Videoni foydalanuvchiga yuborish
        await update.message.reply_video(video=open(video_filename, 'rb'))

        # Yuklangan faylni o‘chirish
        os.remove(video_filename)

    except Exception as e:
        await update.message.reply_text("Kechirasiz, video topishda yoki yuklab olishda xatolik yuz berdi.")

# Botni ishga tushirish
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot ishga tushdi!")
    application.run_polling()
