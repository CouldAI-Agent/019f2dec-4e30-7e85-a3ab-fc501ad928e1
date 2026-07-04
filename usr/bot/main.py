import os
import sqlite3
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Basic configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8989477327:AAE-fUFGzOSlyJFzDYQoOxcAvLlUaqAUKR0")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7102287946"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Database
def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, is_premium INTEGER DEFAULT 0, premium_until TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, link TEXT, required_subs INTEGER, current_subs INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS anime (code INTEGER, file_id TEXT, description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

init_db()

class AnimeState(StatesGroup):
    waiting_for_code = State()
    waiting_for_file = State()
    waiting_for_desc = State()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (message.from_user.id,))
    conn.commit()
    conn.close()

    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanal qo'shish", callback_data="add_channel"),
             InlineKeyboardButton(text="🎬 Anime qo'shish", callback_data="add_anime")]
        ])
        await message.answer("Assalomu alaykum, Admin! Admin paneliga xush kelibsiz.", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Obuna bo'lish", url="https://t.me/example"),
             InlineKeyboardButton(text="Tekshirish", callback_data="check_sub")],
            [InlineKeyboardButton(text="Premium ⭐", callback_data="premium")]
        ])
        await message.answer("Barcha kanallarga obuna bo'ling.", reply_markup=keyboard)

@dp.callback_query(F.data == "check_sub")
async def check_sub_cb(call: types.CallbackQuery):
    await call.message.answer("✅ Obuna tasdiqlandi.\n\nEndi kino kodini yuboring.")
    await call.answer()

@dp.callback_query(F.data == "premium")
async def premium_cb(call: types.CallbackQuery):
    await call.message.answer("Premium sotib olish uchun admin bilan bog'laning.\n\n@Rustamjon_001")
    await call.answer()

@dp.message(F.text.regexp(r'^\d+$'))
async def send_anime(message: types.Message):
    code = int(message.text)
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, description FROM anime WHERE code=?", (code,))
    results = cursor.fetchall()
    conn.close()

    if results:
        for file_id, desc in results:
            await message.answer_video(video=file_id, caption=desc)
    else:
        await message.answer("Kechirasiz, bunday kodli anime topilmadi.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
