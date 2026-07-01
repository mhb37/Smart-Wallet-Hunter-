import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler

from telegram_bot.bot import create_bot
from scheduler.jobs import discover_wallets_job


def debug_environment():
    print("\n===== DEBUG ENVIRONMENT =====")
    print("WORKING DIR:", os.getcwd())
    print("FILES:", os.listdir("."))
    print("PYTHON PATH:", sys.path)
    print("============================\n")


def main():

    # Debug Railway (très important pour ton erreur actuelle)
    debug_environment()

    # Scheduler
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        discover_wallets_job,
        "interval",
        minutes=1  # test rapide
    )

    scheduler.start()

    # Telegram bot
    bot = create_bot()

    print("🚀 Smart Wallet Hunter lancé")

    bot.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()