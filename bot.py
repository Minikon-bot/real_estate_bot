import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from parser import check_new_ads
from config import TOKEN, CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот запущен! Подписка на новые объявления активирована.')
    context.job_queue.run_repeating(check_new_ads_callback, interval=300, first=10, context=update.message.chat_id)

async def check_new_ads_callback(context: ContextTypes.DEFAULT_TYPE):
    new_ads = check_new_ads()  # Предполагается, что функция возвращает список строк
    chat_id = context.job.context
    if new_ads:
        for ad in new_ads:
            await context.bot.send_message(chat_id=chat_id, text=ad)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())