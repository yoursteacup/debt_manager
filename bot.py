import logging
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers.common import start, help_command
from handlers.debt import borrow, lend, pay, returned, show, history

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("borrow", borrow))
    application.add_handler(CommandHandler("lend", lend))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(CommandHandler("returned", returned))
    application.add_handler(CommandHandler("show", show))
    application.add_handler(CommandHandler("history", history))
    
    logger.info("Bot started with long polling")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    from telegram import Update
    main()