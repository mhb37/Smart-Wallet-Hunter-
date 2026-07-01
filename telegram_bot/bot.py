from telegram.ext import ApplicationBuilder

from telegram_bot.handlers import register_handlers


def build_bot(token):

    app = (
        ApplicationBuilder()
        .token(token)
        .build()
    )

    register_handlers(app)

    return app