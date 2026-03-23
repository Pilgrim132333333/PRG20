# 配置：DATABASE_URL、JWT、CORS 等
from urllib.parse import quote_plus

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
    DB_PORT: int | None = None  # 与 DB_HOST 同用时可覆盖端口
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

    def _port(self) -> int:
        return self.DB_PORT if self.DB_PORT is not None else self.DATABASE_PORT

    def _encoded_credentials(self) -> tuple[str, str]:
        """用户名/密码中的 @ : / ? # ! 等需 URL 编码，否则 pymysql 解析错误"""
        return quote_plus(self._user(), safe=""), quote_plus(self._password(), safe="")

    @property
    def DATABASE_URL(self) -> str:
        """异步连接（aiomysql）"""
        u, p = self._encoded_credentials()
        return f"mysql+aiomysql://{u}:{p}@{self._host()}:{self._port()}/{self._db_name()}?charset=utf8mb4"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """同步连接（pymysql）"""
        u, p = self._encoded_credentials()
        return f"mysql+pymysql://{u}:{p}@{self._host()}:{self._port()}/{self._db_name()}?charset=utf8mb4"


settings = Settings()