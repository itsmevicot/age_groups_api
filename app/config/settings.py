from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    environment: str
    port: int
    mongo_uri: str
    mongo_db_name: str


def get_settings() -> Settings:
    return Settings()
