import os

from dotenv import load_dotenv

load_dotenv()

API_SERVICE_URL=os.getenv('API_SERVICE_URL')
API_BOT_TOKEN=os.getenv('API_BOT_TOKEN')
SECRET_ADMIN_KEY=os.getenv('SECRET_ADMIN_KEY')
CARFAX_SERVICE_URL=os.getenv('CARFAX_SERVICE_URL')

SOURCE = 'telegram_bot'

DB_HOST = os.getenv("BOT_DB_HOST")
DB_PORT = os.getenv("BOT_DB_PORT")
DB_USER = os.getenv("BOT_DB_USER")
DB_PASSWORD = os.getenv("BOT_DB_PASS")
DB_NAME = os.getenv("BOT_DB_NAME")
