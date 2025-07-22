import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from db import init_db, add_user
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer("Привет! Я буду присылать новые объявления квартир по всей Польше. Фильтры можно будет настраивать в следующих обновлениях.")

async def main():
    await init_db()
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
