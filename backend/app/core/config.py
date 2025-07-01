from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: str = "3306"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "chatbot"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "password"

    OLLAMA_URL: str = "http://ollama:11434"

    SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

settings = Settings()