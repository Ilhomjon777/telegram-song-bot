from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Men sizga qo'shiqni topib berishga yordam beraman. "
        "Iltimos, qidirayotgan qo'shiq nomini yozing."
    )

# Qo'shiq nomini qidirish va manzilni qaytarish
async def find_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    await update.message.reply_text(f"\"{query}\" qo'shig'ini qidiryapman...")

    # YouTube-dan qidirish va yuklab olish uchun
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            if 'entries' in result:
                result = result['entries'][0]  # Birinchi natijani olamiz
            download_url = result['url']
            title = result['title']

            await update.message.reply_text(
                f"Qo'shiq topildi: {title}\nMana yuklab olish uchun havola: {download_url}"
            )
    except Exception as e:
        await update.message.reply_text("Kechirasiz, qo'shiqni topishda xatolik yuz berdi.")

# Botni ishga tushirish
if name == 'main':
    application = ApplicationBuilder().token("1997127715:AAFk1qjeTNlV0zj8hrxIA8skIKZQuCkjKVc").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_song))

    print("Bot ishga tushdi!")
    application.run_polling()
