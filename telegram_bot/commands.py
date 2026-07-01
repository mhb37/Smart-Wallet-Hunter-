async def start(update, context):
    await update.message.reply_text(
        "🚀 Smart Wallet Hunter est en ligne !"
    )


async def status(update, context):
    await update.message.reply_text(
        "✅ Statut : opérationnel"
    )


async def help_command(update, context):
    await update.message.reply_text(
        """
Commandes disponibles :

/start
/status
/help
/top
/stats
"""
    )