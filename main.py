from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

# Start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Men sizga qo'shiqning videoni topib berishga yordam beraman. "
        "Iltimos, qidirayotgan qo'shiq nomini yozing."
    )

# Qo'shiq nomini qidirish va videoni yuklab olish
async def find_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    await update.message.reply_text(f"\"{query}\" qo'shig'ining videosini qidiryapman...")

    # YouTube-dan qidirish va yuklab olish uchun
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'outtmpl': 'video.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=True)
            if 'entries' in result:
                result = result['entries'][0]  # Birinchi natijani olamiz
            video_path = f"video.{result['ext']}"
            title = result['title']

            await update.message.reply_text(f"Qo'shiq topildi: {title}. Yuklab olinmoqda...")
            await update.message.reply_video(video=open(video_path, 'rb'))
            os.remove(video_path)  # Faylni o‘chirib tashlash

    except Exception as e:
        await update.message.reply_text("Kechirasiz, video topishda yoki yuklab olishda xatolik yuz berdi.")

# Botni ishga tushirish
if __name__ == "__main__":  # ✅ To‘g‘ri yozilgan
    application = ApplicationBuilder().token("1997127715:AAFk1qjeTNlV0zj8hrxIA8skIKZQuCkjKVc").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_song))

    print("Bot ishga tushdi!")
    application.run_polling()
