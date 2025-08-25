from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_BOT_TOKEN: str
    SECRET_ADMIN_KEY: str

    RPC_CARFAX_URL: str = "localhost:50052"
    RPC_API_URL: str = "localhost:50051"

    SOURCE: str = 'telegram_bot'

    DEBUG: bool = True

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "testpass"

    class Config:
        env_file = ".env"

settings = Settings()
