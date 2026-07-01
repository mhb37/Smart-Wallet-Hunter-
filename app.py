import os
import sys
import time
from apscheduler.schedulers.background import BackgroundScheduler

from telegram_bot.bot import create_bot
from scheduler.jobs import discover_wallets_job
from storage.db import init_db

from analysis.graph import load_graph, save_graph


# =========================
# DEBUG
# =========================
def debug():
    print("\n===== DEBUG =====")
    print("WORKDIR:", os.getcwd())
    print("FILES:", os.listdir("."))
    print("PYTHON PATH:", sys.path)
    print("================\n")


# =========================
# SCHEDULER
# =========================
def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        discover_wallets_job,
        trigger="interval",
        seconds=60,  # stable sur Railway
        id="wallet_scan",
        max_instances=1,
        replace_existing=True
    )

    scheduler.start()

    print("🟢 Scheduler STARTED")

    return scheduler


# =========================
# MAIN
# =========================
def main():

    debug()

    # DB init
    init_db()

    # GRAPH LOAD (V6.1 FIX)
    load_graph()

    # BOT
    bot = create_bot()

    # SCHEDULER
    scheduler = start_scheduler()

    print("🚀 Smart Wallet Hunter lancé")

    try:
        # Telegram bot loop
        bot.run_polling(drop_pending_updates=True)

    except Exception as e:
        print("❌ BOT ERROR:", e)

    finally:
        # sauvegarde graph à l’arrêt
        print("💾 Saving graph...")
        save_graph()

        print("🛑 Shutdown complete")


# =========================
# KEEP ALIVE (RAILWAY SAFE)
# =========================
if __name__ == "__main__":

    main()

    # sécurité anti stop process Railway
    while True:
        time.sleep(60)