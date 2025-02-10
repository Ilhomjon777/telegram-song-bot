import os
import yt_dlp
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# .env fayldan tokenni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # `.env` fayldan tokenni olish

# /start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! YouTube videolarini yuklab olish uchun havolasini yuboring."
    )

# YouTube video va audio yuklab olish
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    await update.message.reply_text(f"Yuklab olish boshlandi: {url}")

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        # Audio yuklash
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])
        audio_path = "audio.mp3"

        # Video yuklash
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])
        video_path = "video.mp4"

        # Telegram orqali foydalanuvchiga yuborish
        await update.message.reply_audio(audio=open(audio_path, 'rb'))
        await update.message.reply_video(video=open(video_path, 'rb'))

        # Yuklangan fayllarni o‘chirish
        os.remove(audio_path)
        os.remove(video_path)

    except Exception as e:
        await update.message.reply_text("Kechirasiz, yuklab olishda xatolik yuz berdi.")

# Asinxron botni ishga tushirish
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("Bot ishga tushdi!")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())  # Asinxron tarzda ishga tushirish

