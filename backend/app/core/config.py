from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "PayBD API"
    debug: bool = False
    database_url: str = Field(..., env="DATABASE_URL")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    access_token_expire_minutes: int = Field(default=15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    redis_url: str = Field(default="redis://localhost:6379/0")
    smtp_host: str = Field(default="localhost")
    smtp_port: int = Field(default=1025)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
