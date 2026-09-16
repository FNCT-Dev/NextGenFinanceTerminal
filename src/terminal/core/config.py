from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Non-secret application settings loaded from environment for development."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="NEXTGEN_", extra="ignore")

    app_name: str = "NextGen Finance Terminal"
    log_level: str = "INFO"
    alpaca_api_key: str | None = Field(default=None, repr=False)
    alpaca_api_secret: str | None = Field(default=None, repr=False)
    tiingo_api_key: str | None = Field(default=None, repr=False)
