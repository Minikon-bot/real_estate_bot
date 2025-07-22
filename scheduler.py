import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parsers.otodom_parser import parse_otodom
from db import load_subscribers

def start_scheduler(application):
    scheduler = AsyncIOScheduler()

    async def job():
        logging.info("Запуск парсинга Otodom...")
        listings = parse_otodom()
        for chat_id in load_subscribers():
            for item in listings:
                try:
                    await application.bot.send_message(chat_id=chat_id, text=item)
                except Exception as e:
                    logging.warning(f"Ошибка при отправке в чат {chat_id}: {e}")
    
    scheduler.add_job(job, "interval", minutes=10)
    scheduler.start()
