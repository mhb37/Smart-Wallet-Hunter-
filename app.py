from apscheduler.schedulers.background import BackgroundScheduler

from telegram_bot.bot import create_bot
from scheduler.jobs import discover_wallets_job


def main():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        discover_wallets_job,
        "interval",
        minutes=1
    )

    scheduler.start()

    bot = create_bot()

    print("🚀 Smart Wallet Hunter lancé")

    bot.run_polling()


if __name__ == "__main__":
    main()