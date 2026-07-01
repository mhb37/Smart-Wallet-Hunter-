from telegram.ext import CommandHandler

from telegram_bot.commands import start, status


def register_handlers(app):

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("status", status)
    )