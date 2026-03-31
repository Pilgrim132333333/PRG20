# Settings: DATABASE_URL, JWT, CORS, AI, etc.
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings

# app/config.py -> fastapi-backend/ -> Workspace/
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_WORKSPACE_DIR = _BACKEND_DIR.parent
_ENV_FILES = tuple(
    str(p)
    for p in (_WORKSPACE_DIR / ".env", _BACKEND_DIR / ".env")
    if p.is_file()
)


class Settings(BaseSettings):
    """Supports DB_* (local pga_platform) or DATABASE_* (remote) credential groups."""
    model_config = ConfigDict(
        env_file=_ENV_FILES if _ENV_FILES else (".env",),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DB_PORT: int | None = None  # Overrides port when used together with DB_HOST
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = "pga_platform"

    DB_HOST: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None

    # Root directory for served material files, e.g. /path/to/Workspace/backend/static
    STATIC_FILES_ROOT: str | None = None

    # AI assistant: OpenAI-compatible POST {AI_API_BASE}/chat/completions
    # DeepSeek (default): set AI_API_KEY in Workspace/.env — never commit keys.
    # OpenAI: AI_API_BASE=https://api.openai.com/v1  AI_MODEL=gpt-4o-mini
    AI_API_KEY: str = ""
    AI_API_BASE: str = "https://api.deepseek.com"
    AI_MODEL: str = "deepseek-chat"
    AI_TEMPERATURE: float = 0.35
    AI_TIMEOUT_SECONDS: float = 120.0

    @field_validator("AI_API_KEY", mode="before")
    @classmethod
    def _strip_ai_api_key(cls, v):
        if v is None:
            return ""
        return str(v).strip()

    def _host(self) -> str:
        return self.DB_HOST or self.DATABASE_HOST

    def _user(self) -> str:
        return self.DB_USER or self.DATABASE_USER

    def _password(self) -> str:
        return self.DB_PASSWORD or self.DATABASE_PASSWORD

    def _db_name(self) -> str:
        return self.DB_NAME or self.DATABASE_NAME

    def _port(self) -> int:
        return self.DB_PORT if self.DB_PORT is not None else self.DATABASE_PORT

    def _encoded_credentials(self) -> tuple[str, str]:
        """URL-encode username and password to handle special characters (@, :, /, etc.)."""
        return quote_plus(self._user(), safe=""), quote_plus(self._password(), safe="")

    @property
    def DATABASE_URL(self) -> str:
        """Async connection string (aiomysql)."""
        u, p = self._encoded_credentials()
        return f"mysql+aiomysql://{u}:{p}@{self._host()}:{self._port()}/{self._db_name()}?charset=utf8mb4"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Synchronous connection string (pymysql)."""
        u, p = self._encoded_credentials()
        return f"mysql+pymysql://{u}:{p}@{self._host()}:{self._port()}/{self._db_name()}?charset=utf8mb4"


settings = Settings()
