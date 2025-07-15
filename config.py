import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = 'sqlite:///data/debts.db'
OWNER_ID = 619277920