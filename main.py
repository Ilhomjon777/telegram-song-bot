import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pytube import Search, YouTube

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
        search = Search(query)
        if not search.results:
            await update.message.reply_text("Kechirasiz, video topilmadi.")
            return

        video_url = search.results[0].watch_url
        yt = YouTube(video_url)

        # Videoni yuklab olish
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        file_path = "video.mp4"
        video.download(filename=file_path)

        # Videoni Telegramga yuborish
        await update.message.reply_video(video=open(file_path, 'rb'))

        # Yuklangan faylni o‘chirish
        os.remove(file_path)

    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        await update.message.reply_text("Kechirasiz, videoni topa olmadim.")

# Xatolikni qaytarish
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

# Asosiy funksiya
def main() -> None:
    # Telegram bot tokeni
    token = "8164698280:AAE06xC_aS-quAU-ObB-UEJaC3oT4hagtcI"

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

