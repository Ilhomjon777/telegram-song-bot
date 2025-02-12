import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
import requests

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /start komandasi
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Salom! Men qo\'shiq nomini qabul qilaman va YouTube\'dan videoni topib beraman. Qo\'shiq nomini yuboring.')

# Qo'shiq nomini qabul qilish va videoni qidirish
def search_video(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    update.message.reply_text(f'Sizning so\'rovingiz: {query}. Qidirilmoqda...')

    try:
        # YouTube'dan videoni qidirish
        yt = YouTube(f"https://www.youtube.com/results?search_query={query}")
        video_url = yt.watch_url

        # Videoni yuklab olish
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(filename='video.mp4')

        # Videoni Telegramga yuborish
        update.message.reply_video(video=open('video.mp4', 'rb'))
        os.remove('video.mp4')  # Faylni o'chirish

    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        update.message.reply_text('Kechirasiz, videoni topa olmadim.')

# Xatolikni qaytarish
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

# Asosiy funksiya
def main() -> None:
    # Telegram bot tokeni
    token = "8100475091:AAHczc0rGkOBEBkm7iqMP7Espv11J4ZAxFA"

    # Updater va Dispatcher
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # CommandHandler va MessageHandler
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search_video))

    # Xatolikni qaytarish
    dispatcher.add_error_handler(error)

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
