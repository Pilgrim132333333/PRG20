# 配置：DATABASE_URL、JWT、CORS 等
from pydantic import BaseSettings, AnyUrl
from typing import List

class Settings(BaseSettings):
    DATABASE_HOST: str = "192.168.56.1"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "team_dev"
    DATABASE_PASSWORD: str = "grp20"
    DATABASE_NAME: str = "study_resources"

    # 异步 SQLAlchemy 连接（推荐用于 AsyncSession）：
    DATABASE_URL="mysql+aiomysql://team_dev:grp20@192.168.56.1:3306/study_resources?charset=utf8mb4"

    # （可选）同步驱动示例：
    SYNC_DATABASE_URL="mysql+pymysql://team_dev:grp20@192.168.56.1:3306/study_resources?charset=utf8mb4"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()