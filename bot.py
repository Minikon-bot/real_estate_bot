import json
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

API_TOKEN = "ВАШ_ТОКЕН_БОТА"

WEBHOOK_HOST = "https://ВАШ_ДОМЕН"  # Например, https://mydomain.com
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

WEBHOOK_PORT = 8443  # Порт для входящих вебхуков
WEBHOOK_LISTEN = "0.0.0.0"

# Файл для хранения подписчиков
SUBSCRIBERS_FILE = Path("subscribers.json")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Загрузка подписчиков из файла
def load_subscribers():
    if SUBSCRIBERS_FILE.exists():
        with open(SUBSCRIBERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

# Сохранение подписчиков в файл
def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(subscribers), f)

subscribers = load_subscribers()

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        save_subscribers(subscribers)
        await message.answer("Вы подписались на обновления!")
        logging.info(f"Новый подписчик: {chat_id}")
    else:
        await message.answer("Вы уже подписаны на обновления.")

# Пример функции рассылки сообщений всем подписчикам
async def broadcast_message(text: str):
    for chat_id in list(subscribers):
        try:
            await bot.send_message(chat_id, text)
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение {chat_id}: {e}")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook установлен")

async def on_shutdown(dp):
    logging.info("Удаление webhook...")
    await bot.delete_webhook()
    logging.info("Webhook удалён")

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
    )
