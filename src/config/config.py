from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    postgres_user: str = "login"
    postgres_password: str = "password"
    postgres_db: str = "dbname"
    database_url: str = "db_url"

    openai_api_key: str = "openai_api_key"


settings = Settings()
