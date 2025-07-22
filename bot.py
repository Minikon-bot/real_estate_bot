import json
import os
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from parser import check_new_ads

# Файл для хранения подписчиков
SUBSCRIBERS_FILE = "/tmp/subscribers.json"

# Инициализация файла подписчиков
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

# Удаление подписчика
def remove_subscriber(chat_id):
    subscribers = get_subscribers()
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(subscribers, f)

# Создание Flask-приложения
flask_app = Flask(__name__)

# Получение токена из переменной окружения
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения TOKEN не задана")

# Создание приложения Telegram
application = Application.builder().token(TOKEN).build()

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    add_subscriber(chat_id)
    await update.message.reply_text('Бот запущен! Вы подписаны на новые объявления.')
    # Запуск задачи проверки объявлений, если она еще не запущена
    if not context.job_queue.get_jobs_by_name("check_ads"):
        context.job_queue.run_repeating(check_new_ads_callback, interval=300, first=10, name="check_ads")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    remove_subscriber(chat_id)
    await update.message.reply_text('Вы отписаны от уведомлений.')

async def check_new_ads_callback(context: ContextTypes.DEFAULT_TYPE):
    new_ads = check_new_ads()
    if new_ads:
        subscribers = get_subscribers()
        print(f"Найдено {len(new_ads)} новых объявлений, отправка {len(subscribers)} подписчикам")
        for chat_id in subscribers:
            for ad in new_ads:
                try:
                    await context.bot.send_message(chat_id=chat_id, text=ad)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")

# Добавление обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("stop", stop))

# Настройка маршрута для вебхука
WEBHOOK_PATH = f"/{TOKEN}"

@flask_app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string, application.bot)
        if update:
            await application.process_update(update)
        return Response('ok', status=200)
    return Response('error', status=403)

@flask_app.route('/')
def health_check():
    return "Bot is running"

if __name__ == '__main__':
    # Настройка вебхука
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}"
    if not webhook_url:
        raise ValueError("Переменная окружения RENDER_EXTERNAL_URL не задана")
    application.bot.set_webhook(webhook_url)
    # Запуск Flask-приложения
    flask_app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))