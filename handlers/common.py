from telegram import Update
from telegram.ext import ContextTypes
from utils.auth import owner_only

@owner_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу вести учет долгов.\n\n"
        "Команды:\n"
        "/borrow Имя Сумма - я занял у человека\n"
        "/lend Имя Сумма - я дал взаймы\n"
        "/pay Имя Сумма - я вернул долг\n"
        "/returned Имя Сумма - мне вернули долг\n"
        "/show - показать все долги"
    )

@owner_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Управление долгами:\n\n"
        "• /borrow Канат 5000 - вы заняли у Каната 5000 (ваш долг)\n"
        "• /lend Асет 3000 - вы дали взаймы Асету 3000 (вам должны)\n"
        "• /pay Канат 2000 - вы вернули Канату 2000\n"
        "• /returned Асет 1000 - Асет вернул вам 1000\n"
        "• /show - посмотреть все долги\n\n"
        "Отрицательная сумма = вы должны\n"
        "Положительная сумма = вам должны"
    )