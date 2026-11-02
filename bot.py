import os, asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN .env faylida ko‘rsatilmagan")
if not WEBAPP_URL or not WEBAPP_URL.startswith("https://"):
    raise RuntimeError("WEBAPP_URL haqiqiy HTTPS manzil bo‘lishi kerak")

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎮 O‘yinlarni ochish", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True
    )
    await message.answer(
        "🌈 Salom! Kichkintoylar o‘yin olamiga xush kelibsiz!\n\n"
        "Bu yerda 50 ta bepul, qiziqarli va xavfsiz mini-o‘yin bor. "
        "O‘yinlardan birini tanlang va maroqli vaqt o‘tkazing!",
        reply_markup=keyboard
    )

@dp.message(F.text == "ℹ️ Yordam")
async def help_message(message: Message):
    await message.answer("🎮 O‘yinlarni ochish tugmasini bosing. Barcha o‘yinlar bepul!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
