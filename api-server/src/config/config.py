from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    database: str

    model_config = SettingsConfigDict(env_file=".env")
