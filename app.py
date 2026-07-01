import os
import logging

from telegram.ext import ApplicationBuilder

from telegram_bot.handlers import register_handlers
from scheduler.jobs import start_scheduler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():

    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN missing")

    app = (
        ApplicationBuilder()
        .token(token)
        .build()
    )

    register_handlers(app)

    # Supprime un éventuel ancien webhook
    app.bot.delete_webhook(drop_pending_updates=True)

    # Lance le scanner
    start_scheduler()

    # Telegram polling
    app.run_polling(
        drop_pending_updates=True,
        close_loop=False,
    )


if __name__ == "__main__":
    main()