#!/usr/bin/env python3
"""
检测 MySQL 是否可连接（读取项目根目录 .env 中的 DB_* / DATABASE_*）。
在 fastapi-backend 目录执行: python check_db.py
"""
from sqlalchemy import text

from app.config import settings
from app.database import engine


def main() -> None:
    host = settings._host()
    dbn = settings._db_name()
    user = settings._user()
    print(f"尝试连接: {user}@{host}:{settings._port()}/{dbn}")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("OK：数据库连接成功。")
    except Exception as e:
        print("失败：", e)
        print("\n请检查：")
        print("1) 本机 MySQL 已启动；2) 已创建数据库", dbn)
        print("3) Workspace/.env 中 DB_USER / DB_PASSWORD / DB_NAME 与 MySQL 一致")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
