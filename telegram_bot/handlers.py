from telegram.ext import CommandHandler


async def start(update, context):
    await update.message.reply_text("🚀 Bot actif")


async def status(update, context):
    await update.message.reply_text("🟢 OK")


def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))