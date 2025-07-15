from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID

def owner_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if user_id != OWNER_ID:
            return
        return await func(update, context)
    return wrapper