import os

from dotenv import load_dotenv

load_dotenv()

API_SERVICE_URL=os.getenv('API_SERVICE_URL')
API_BOT_TOKEN=os.getenv('API_BOT_TOKEN')
SECRET_ADMIN_KEY=os.getenv('SECRET_ADMIN_KEY')
CARFAX_SERVICE_URL=os.getenv('CARFAX_SERVICE_URL')
PAYMENT_SERVICE_URL=os.getenv('PAYMENT_SERVICE_URL')

SOURCE = 'telegram_bot'

DEBUG = os.getenv("DEBUG", "true").lower() == "true"

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
