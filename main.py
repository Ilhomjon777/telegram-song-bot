import os
import yt_dlp
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# .env fayldan tokenni yuklash
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! YouTube videolarini audio yoki video shaklida yuklab olish uchun havolasini yuboring."
    )

# YouTube audio va videosini yuklab olish
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    await update.message.reply_text(f"Yuklab olish boshlandi: {url}")

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }

    video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])
        audio_path = "audio.mp3"

        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])
        video_path = "video.mp4"

        await update.message.reply_audio(audio=open(audio_path, 'rb'))
        await update.message.reply_video(video=open(video_path, 'rb'))

        os.remove(audio_path)
        os.remove(video_path)

    except Exception as e:
        await update.message.reply_text("Kechirasiz, yuklab olishda xatolik yuz berdi.")

# Botni ishga tushirish
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("Bot ishga tushdi!")
    await application.run_polling()

# Asinxron kodni to‘g‘ri ishga tushirish
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
