from telegram_bot.bot import create_bot


def main():

    bot = create_bot()

    print("🚀 Smart Wallet Hunter lancé")

    bot.run_polling()


if __name__ == "__main__":
    main()