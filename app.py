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

    # Lance le scheduler de scan
    start_scheduler()

    # Démarrage du bot Telegram
    # drop_pending_updates supprime automatiquement
    # les anciens messages et le webhook éventuel.
    app.run_polling(
        drop_pending_updates=True,
        close_loop=False,
    )


if __name__ == "__main__":
    main()