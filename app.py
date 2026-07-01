import os
import logging

from telegram.ext import ApplicationBuilder

from telegram_bot.handlers import register_handlers
from scheduler.jobs import start_scheduler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def main():

    logger.info("🚀 Smart Wallet Hunter starting...")

    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError(
            "BOT_TOKEN missing. Configure Railway Variables."
        )

    app = ApplicationBuilder() \
        .token(token) \
        .build()

    # Telegram commands
    register_handlers(app)

    # Background scanner
    start_scheduler()

    logger.info("🟢 Bot running")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()