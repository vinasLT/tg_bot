import os

from dotenv import load_dotenv

load_dotenv()

API_SERVICE_URL=os.getenv('API_SERVICE_URL')
API_BOT_TOKEN=os.getenv('API_BOT_TOKEN')
SECRET_ADMIN_KEY=os.getenv('SECRET_ADMIN_KEY')

