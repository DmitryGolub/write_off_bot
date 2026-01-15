from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "postgresql+asyncpg://bot_user:bot_password@postgres/write_off_bot"

    class Config:
        env_file = ".env"


settings = Settings()
