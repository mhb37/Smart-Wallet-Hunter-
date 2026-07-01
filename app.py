import os
import sys
import asyncio
import logging

from telegram.ext import ApplicationBuilder

from scheduler.jobs import start_scheduler
from telegram_bot.handlers import register_handlers


# ========================
# LOGGING GLOBAL
# ========================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# ========================
# ANTI DOUBLE INSTANCE
# ========================
def kill_if_duplicate():
    """
    Empêche 2 bots Telegram (getUpdates conflict)
    """
    global_lock_file = "/tmp/smart_wallet_bot.lock"

    if os.path.exists(global_lock_file):
        logger.error("❌ Bot déjà en cours (lock file existant)")
        sys.exit(1)

    with open(global_lock_file, "w") as f:
        f.write(str(os.getpid()))

    logger.info("🔒 Lock acquis, instance unique OK")


def release_lock():
    try:
        os.remove("/tmp/smart_wallet_bot.lock")
    except:
        pass


# ========================
# MAIN
# ========================
async def main():
    kill_if_duplicate()

    logger.info("🚀 Smart Wallet Hunter lancé")

    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN manquant")

    app = ApplicationBuilder().token(TOKEN).build()

    # handlers
    register_handlers(app)

    # scheduler
    start_scheduler()

    logger.info("🟢 Bot prêt")

    try:
        await app.run_polling(close_loop=False)
    finally:
        release_lock()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(e)
        release_lock()