from telegram.ext import ApplicationBuilder, CommandHandler

from config import TELEGRAM_TOKEN
from telegram_bot.commands import (
    start,
    status,
    help_command
)


def create_bot():

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help_command))

    return app