import os
import sys
import time
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


def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        discover_wallets_job,
        "interval",
        seconds=60,   # IMPORTANT: plus stable que minutes=1
        id="scan_job",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()

    print("🟢 Scheduler STARTED")

    return scheduler


def main():

    debug()

    init_db()

    # =========================
    # START SCHEDULER
    # =========================
    scheduler = start_scheduler()

    # =========================
    # BOT
    # =========================
    bot = create_bot()

    print("🚀 Smart Wallet Hunter lancé")

    # KEEP ALIVE LOOP (IMPORTANT RAILWAY)
    bot.run_polling(
        drop_pending_updates=True
    )

    # sécurité anti stop process
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()