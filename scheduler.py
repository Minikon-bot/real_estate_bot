import asyncio
import schedule
from bot import send_updates, ApplicationBuilder, TOKEN

async def run_scheduler():
    application = ApplicationBuilder().token(TOKEN).build()
    await application.initialize()
    await application.start()

    def job():
        asyncio.create_task(send_updates(application))

    schedule.every(15).minutes.do(job)

    try:
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

    await application.stop()
    await application.shutdown()

if __name__ == "__main__":
    asyncio.run(run_scheduler())
