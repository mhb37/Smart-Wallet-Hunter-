import os
import logging
from telegram.ext import ApplicationBuilder

from telegram_bot.handlers import register_handlers
from scheduler.jobs import start_scheduler

logging.basicConfig(level=logging.INFO)


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN missing")

    app = ApplicationBuilder().token(token).build()

    register_handlers(app)

    start_scheduler()

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()