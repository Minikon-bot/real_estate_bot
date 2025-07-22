import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import add_subscriber, load_subscribers
from parser import parse_otodom
import asyncio

TOKEN = "ВАШ_ТОКЕН_БОТА"  # ВАЖНО: Замените на свой токен

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_subscriber(chat_id)
    await update.message.reply_text(
        "Вы подписались на обновления объявлений. Буду присылать новые предложения."
    )

async def send_updates(application):
    subscribers = load_subscribers()
    offers = parse_otodom()
    if not offers:
        return
    message = "\n\n".join(offers)
    for chat_id in subscribers:
        try:
            await application.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения {chat_id}: {e}")

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Планировщик с asyncio (пример: обновлять каждые 15 минут)
    import asyncio
    import schedule

    def job():
        asyncio.create_task(send_updates(application))

    schedule.every(15).minutes.do(job)

    try:
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

    await application.updater.stop()
    await application.stop()
    await application.shutdown()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
