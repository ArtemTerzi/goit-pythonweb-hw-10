from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
