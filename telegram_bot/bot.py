from telegram_bot.bot import build_bot

app = build_bot(token)
app.run_polling(drop_pending_updates=True)