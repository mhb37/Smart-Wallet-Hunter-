import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler

from telegram_bot.bot import create_bot
from scheduler.jobs import discover_wallets_job


# =========================
# DEBUG STARTUP
# =========================

print("\n===== STARTUP DEBUG =====")
print("WORKDIR:", os.getcwd())
print("FILES:", os.listdir("."))
print("PYTHON PATH:", sys.path)
print("========================\n")


# =========================
# ANTI DOUBLE INSTANCE (BASIC)
# =========================

def is_railway():
    return bool(os.getenv("RAILWAY_ENVIRONMENT"))


if is_railway():
    print("🚀 Railway detected -> single instance mode enforced")


# =========================
# MAIN
# =========================

def main():

    # Scheduler
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        discover_wallets_job,
        "interval",
        minutes=1,
        id="wallet_scan_job",
        replace_existing=True
    )

    scheduler.start()

    # Bot
    bot = create_bot()

    print("🚀 Smart Wallet Hunter lancé")

    bot.run_polling(
        drop_pending_updates=True  # IMPORTANT anti conflits Telegram
    )


if __name__ == "__main__":
    main()