import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler

from telegram_bot.bot import create_bot
from scheduler.jobs import discover_wallets_job
from storage.db import init_db


def debug():
    print("\n===== DEBUG =====")
    print("WORKDIR:", os.getcwd())
    print("FILES:", os.listdir("."))
    print("PYTHON PATH:", sys.path)
    print("================\n")


def main():

    debug()

    # INIT DATABASE
    init_db()

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        discover_wallets_job,
        "interval",
        minutes=1,
        id="scan_job",
        replace_existing=True
    )

    scheduler.start()

    bot = create_bot()

    print("🚀 Smart Wallet Hunter lancé")

    bot.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()