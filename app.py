import os
import logging

from telegram_bot.bot import build_bot
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
        raise ValueError("BOT_TOKEN missing")

    # démarre le scanner
    start_scheduler()

    # construit le bot
    app = build_bot(token)

    logger.info("🟢 Bot running")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()