import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from pytube import YouTube

# Bot tokenini shu yerga kiriting
TOKEN = "1997127715:AAFk1qjeTNlV0zj8hrxIA8skIKZQuCkjKVc"

# Bot va dispatcher obyektlarini yaratamiz
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Salom! YouTube videolarini yuklab beruvchi bot. Menga YouTube link yuboring.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text
    try:
        await message.reply("⏳ Video yuklanmoqda, biroz kuting...")
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension="mp4").first()
        file_path = video.download()
        
        # Telegramga yuklash
        with open(file_path, "rb") as video_file:
            await bot.send_video(message.chat.id, video_file, caption=f"{yt.title}\n\n@YourBotUsername")
        
        # Faylni o‘chiramiz
        os.remove(file_path)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
