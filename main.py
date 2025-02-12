import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /start komandasi
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men qo‘shiq nomini qabul qilaman va YouTube’dan videoni topib beraman. Qo‘shiq nomini yuboring.")

# Qo‘shiq nomini qabul qilish va videoni qidirish
async def search_video(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    await update.message.reply_text(f"Sizning so‘rovingiz: {query}. Qidirilmoqda...")

    try:
        # YouTube'da qidirish
        ydl_opts = {
            'quiet': True,
            'default_search': 'ytsearch1',  # 1 ta natija qaytaradi
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

        if 'entries' not in info or len(info['entries']) == 0:
            await update.message.reply_text("Kechirasiz, video topilmadi.")
            return

        video_url = info['entries'][0]['url']  # Topilgan video URL
        video_title = info['entries'][0]['title']

        await update.message.reply_text(f"✅ Video topildi: {video_title}\n{video_url}")

    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        await update.message.reply_text("Kechirasiz, videoni topa olmadim.")

# Xatolikni qaytarish
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

# Asosiy funksiya
def main() -> None:
    # Telegram bot tokeni
    token = "7419683942:AAE8pq7deHIRf8O-YwJpNQHVQkuz_oqwSSA"

    # Bot uchun Application yaratish
    app = Application.builder().token(token).build()

    # Handlerlarni qo‘shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_video))
    app.add_error_handler(error)

    # Botni ishga tushirish
    app.run_polling()

if __name__ == '__main__':
    main()
