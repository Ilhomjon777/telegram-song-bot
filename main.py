import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from pytube import YouTube

# Railway Environment Variables dan TOKEN ni olish
TOKEN = os.getenv("TOKEN")

# Bot va dispatcher obyektlarini yaratamiz
bot = Bot(token=TOKEN)
dp = Dispatcher()

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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
