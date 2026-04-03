from functools import lru_cache

from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "POS System API"
    app_env: str = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"

    secret_key: str
    access_token_expire_minutes: int = 1440

    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str
    db_ssl_ca: str | None = None
    db_echo: bool = False

    auth_secret_key: str
    auth_access_token_expire_minutes: int = 480
    auth_issuer: str = "pos-backend"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlalchemy_database_uri(self) -> str:
        return URL.create(
            drivername="mysql+pymysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()