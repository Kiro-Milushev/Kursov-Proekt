"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import dotenv_values


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_VALUES = dotenv_values(PROJECT_ROOT / ".env")


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the backend."""

    cf_account_id: str
    cf_ai_api_key: str
    cf_model: str = "@cf/meta/llama-3.2-3b-instruct"
    request_timeout_seconds: float = 90.0

    @property
    def cloudflare_ai_url(self) -> str:
        """Build the Cloudflare AI inference endpoint URL."""

        return f"https://api.cloudflare.com/client/v4/accounts/{self.cf_account_id}/ai/run/{self.cf_model}"


def _read_float_env(name: str, default: float) -> float:
    """Read a float environment variable with a fallback default."""

    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return float(raw_value)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    account_id = DOTENV_VALUES.get("CF_ACCOUNT_ID") or os.getenv("CF_ACCOUNT_ID")
    api_key = DOTENV_VALUES.get("CF_AI_API_KEY") or os.getenv("CF_AI_API_KEY")

    return Settings(
        cf_account_id=account_id or "",
        cf_ai_api_key=api_key or "",
        cf_model=(DOTENV_VALUES.get("CF_MODEL") or os.getenv("CF_MODEL") or "@cf/meta/llama-3.2-3b-instruct"),
        request_timeout_seconds=_read_float_env("REQUEST_TIMEOUT_SECONDS", 90.0),
    )
