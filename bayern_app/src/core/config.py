from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Указываем, какие переменные мы ЖДЕМ из файла .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Динамически собираем URL для подключения к базе
    @property
    def DATABASE_URL(self) -> str:
        # Формат: postgresql://user:password@host:port/database_name
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Говорим Pydantic, откуда брать данные
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Создаем объект настроек, который будем импортировать в другие файлы
settings = Settings()