# 配置：DATABASE_URL、JWT、CORS 等
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """支持 DB_*（本机 pga_platform）或 DATABASE_*（远程）"""
    model_config = ConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = "pga_platform"

    DB_HOST: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None

    # 材料文件根目录，例如 /path/to/Workspace/backend/static
    STATIC_FILES_ROOT: str | None = None

    def _host(self) -> str:
        return self.DB_HOST or self.DATABASE_HOST

    def _user(self) -> str:
        return self.DB_USER or self.DATABASE_USER

    def _password(self) -> str:
        return self.DB_PASSWORD or self.DATABASE_PASSWORD

    def _db_name(self) -> str:
        return self.DB_NAME or self.DATABASE_NAME

    @property
    def DATABASE_URL(self) -> str:
        """异步连接（aiomysql）"""
        return f"mysql+aiomysql://{self._user()}:{self._password()}@{self._host()}:{self.DATABASE_PORT}/{self._db_name()}?charset=utf8mb4"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """同步连接（pymysql）"""
        return f"mysql+pymysql://{self._user()}:{self._password()}@{self._host()}:{self.DATABASE_PORT}/{self._db_name()}?charset=utf8mb4"


settings = Settings()