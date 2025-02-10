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
    await update.message.reply_text(f"⏳ Yuklab olish boshlandi: {url}")

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.mp3',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }

    video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        # Audio yuklab olish
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])

        # Video yuklab olish
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])

        # Foydalanuvchiga fayllarni jo‘natish
        await update.message.reply_audio(audio=open("audio.mp3", 'rb'))
        await update.message.reply_video(video=open("video.mp4", 'rb'))

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")

    finally:
        # Fayllarni o‘chirish
        if os.path.exists("audio.mp3"):
            os.remove("audio.mp3")
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

# Botni ishga tushirish
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("✅ Bot ishga tushdi!")
    await application.run_polling()

# Asinxron kodni to‘g‘ri ishga tushirish
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
