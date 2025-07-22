import asyncio
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from parser import check_new_ads

# Файл для хранения подписчиков
SUBSCRIBERS_FILE = "subscribers.json"

# Инициализация файла подписчиков, если он не существует
def init_subscribers_file():
    if not os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump([], f)

# Чтение списка подписчиков
def get_subscribers():
    init_subscribers_file()
    with open(SUBSCRIBERS_FILE, 'r') as f:
        return json.load(f)

# Добавление нового подписчика
def add_subscriber(chat_id):
    subscribers = get_subscribers()
    if chat_id not in subscribers:
        subscribers.append(chat_id)
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(subscribers, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    add_subscriber(chat_id)
    await update.message.reply_text('Бот запущен! Вы подписаны на новые объявления.')
    # Запускаем задачу проверки объявлений, если она еще не запущена
    if not context.job_queue.get_jobs_by_name("check_ads"):
        context.job_queue.run_repeating(check_new_ads_callback, interval=300, first=10, name="check_ads")

async def check_new_ads_callback(context: ContextTypes.DEFAULT_TYPE):
    new_ads = check_new_ads()  # Предполагается, что возвращает список строк
    if new_ads:
        subscribers = get_subscribers()
        for chat_id in subscribers:
            for ad in new_ads:
                try:
                    await context.bot.send_message(chat_id=chat_id, text=ad)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")

async def main():
    # Предполагается, что TOKEN задан в переменной окружения
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("Переменная окружения TOKEN не задана")
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())