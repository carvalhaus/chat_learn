from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: str = "3306"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "chatbot"

settings = Settings()