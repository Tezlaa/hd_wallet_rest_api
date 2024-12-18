
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AnyHttpUrl,
    PostgresDsn,
)


class Settings(BaseSettings):
    DEBUG: bool = True
    API_STR: str = "/api/v1"

    # BSC settings
    BSC_RPC_URL: AnyHttpUrl
    MASTER_PRIVATE_KEY: str
    BSC_CHAIN_ID: int

    # Database settings
    POSTGRES_HOST: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    SQLALCHEMY_DATABASE_URI: PostgresDsn | str | None = None

    @property
    def sqlalchemy_database_uri(self) -> str:  # by default using asyncpg
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI.replace("postgresql", "postgresql+asyncpg")

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"{self.POSTGRES_DB or ''}",
        ).unicode_string()

    model_config = SettingsConfigDict(case_sensitive=True)
