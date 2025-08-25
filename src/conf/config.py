from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:12345@localhost:5438/postgres"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "your_email@example.com"
    MAIL_PASSWORD: str = "your_email_password"
    MAIL_FROM: str = "your_email@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "your_mail_server"
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "Cloudinary_name"
    CLD_API_KEY: int = "Cloudinary_api_key"
    CLD_API_SECRET: str = "Cloudinary_api_secret"

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v):
        if v not in {"HS256", "HS512"}:
            raise ValueError("ALGORITHM must be HS256 or HS512")
        return v

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
