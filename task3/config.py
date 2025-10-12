from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv(".env")  # take environment variables from .env file


class Settings(BaseSettings):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int = 3600
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str


    class Config:
        env_file = ".env"

settings = Settings()