from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import listing_exists, add_listing, get_users
from parsers import fetch_all
from aiogram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def check_new_listings():
    ads = await fetch_all()
    for ad in ads:
        if not await listing_exists(ad["hash"]):
            await add_listing(ad)
            for tg_id in await get_users():
                text = f"**{ad['title']}**\nЦена: {ad['price']}\nЛокация: {ad['location']}\n{ad['description']}\n[Ссылка]({ad['url']})"
                await bot.send_message(tg_id, text, parse_mode="Markdown")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_new_listings, "interval", minutes=5)
    scheduler.start()
