from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "TaskFlow API"
    ENVIRONMENT: str = Field("development", alias="APP_ENV")
    DB_USER: str = Field(..., alias="POSTGRES_USER")
    DB_PASSWORD: str = Field(..., alias="POSTGRES_PASSWORD")
    DB_HOST: str = Field("localhost", alias="POSTGRES_HOST")
    DB_PORT: int = Field(5432, alias="POSTGRES_PORT")
    DB_NAME: str = Field(..., alias="POSTGRES_DB")
    DATABASE_URL: str | None = None
    TEST_DATABASE_URL: str | None = Field(None, alias="TEST_DATABASE_URL")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def build_database_url(cls, value, info):
        if value:
            return value

        data = info.data
        user = data.get("DB_USER")
        password = data.get("DB_PASSWORD")
        host = data.get("DB_HOST")
        port = data.get("DB_PORT")
        name = data.get("DB_NAME")

        if not all([user, password, host, port, name]):
            raise ValueError("Missing PostgreSQL database configuration")

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    @property
    def test_database_url(self) -> str:
        """Return TEST_DATABASE_URL if explicitly configured, otherwise fallback to DATABASE_URL."""
        return self.TEST_DATABASE_URL or self.DATABASE_URL or ""


settings = Settings()
