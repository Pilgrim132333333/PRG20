import csv
import os
from pathlib import Path

import pymysql

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# 本脚本在 backend/；项目根目录为上一级（与 fastapi-backend 共用 Workspace/.env）
BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent

if load_dotenv:
    load_dotenv(ROOT_DIR / ".env")


def _env(key: str, default: str = "") -> str:
    v = os.getenv(key)
    if v is None:
        return default
    v = v.strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        v = v[1:-1]
    return v


def get_db_config() -> dict:
    """与 fastapi-backend/app/config.py 一致：优先 DB_*，否则 DATABASE_*"""
    host = _env("DB_HOST") or _env("DATABASE_HOST", "localhost")
    port = int(_env("DB_PORT") or _env("DATABASE_PORT") or "3306")
    user = _env("DB_USER") or _env("DATABASE_USER", "root")
    password = _env("DB_PASSWORD") or _env("DATABASE_PASSWORD", "")
    database = _env("DB_NAME") or _env("DATABASE_NAME", "pga_platform")
    charset = _env("DB_CHARSET", "utf8mb4")
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "charset": charset,
    }


def csv_path(name: str) -> Path:
    return BACKEND_DIR / "database_templates" / name


def get_full_path(material_type, filename):
    paths = {
        "PPT": f"/static/lectures/{filename}",
        "Tutorial": f"/static/tutorials/{filename}",
        "Lab Worksheet": f"/static/labs/{filename}",
        "CW": f"/static/courseworks/{filename}",
    }
    return paths.get(material_type, f"/static/others/{filename}")


def ensure_user_tables(cursor) -> None:
    """
    若库是旧版只建了 Materials/Questions/Link，会缺少 Users、User_Question_State。
    与 backend/init_schema.sql 中定义一致。
    """
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS User_Question_State (
            user_id INT NOT NULL,
            question_id INT NOT NULL,
            is_favourite TINYINT(1) DEFAULT 0,
            is_completed TINYINT(1) DEFAULT 0,
            PRIMARY KEY (user_id, question_id),
            CONSTRAINT fk_seed_uqs_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            CONSTRAINT fk_seed_uqs_q FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )


def run_seed():
    db = get_db_config()
    print(f"📡 连接 MySQL: {db['user']}@{db['host']}:{db['port']}/{db['database']}")
    connection = pymysql.connect(**db)
    try:
        with connection.cursor() as cursor:
            print("⏳ 正在导入物料表 (Materials)...")
            with open(csv_path("materials.csv"), "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    path = get_full_path(row["material_type"], row["file_path"])
                    sql = "INSERT IGNORE INTO Materials (material_code, material_type, week_number, title, file_path) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(
                        sql,
                        (
                            row["material_code"].strip(),
                            row["material_type"].strip(),
                            row["week_number"].strip(),
                            row["title"].strip(),
                            path,
                        ),
                    )

            print("⏳ 正在导入题库表 (Questions)...")
            with open(csv_path("questions.csv"), "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    img_path = row["image_path"] if row.get("image_path", "").strip() else None
                    lang = row.get("language", "C").strip()

                    sql = """
                        INSERT IGNORE INTO Questions 
                        (question_code, source_year, source_type, knowledge_point, question_text, answer_text, image_path, language) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        sql,
                        (
                            row["question_code"].strip(),
                            row["source_year"].strip(),
                            row["source_type"].strip(),
                            row["knowledge_point"].strip(),
                            row["question_text"].strip(),
                            row["answer_text"].strip(),
                            img_path,
                            lang,
                        ),
                    )

            print("⏳ 正在建立关联 (Links)...")
            with open(csv_path("links.csv"), "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sql = """
                        INSERT IGNORE INTO Question_Material_Link (question_id, material_id)
                        VALUES (
                            (SELECT question_id FROM Questions WHERE question_code = %s),
                            (SELECT material_id FROM Materials WHERE material_code = %s)
                        )
                    """
                    cursor.execute(sql, (row["question_code"].strip(), row["material_code"].strip()))

            print("⏳ 检查/创建 Users、User_Question_State 表（依赖 Questions 已存在）...")
            ensure_user_tables(cursor)

            print("⏳ 正在导入用户表 (Users)...")
            try:
                with open(csv_path("users.csv"), "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sql = "INSERT IGNORE INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
                        cursor.execute(
                            sql,
                            (
                                row["username"].strip(),
                                row["email"].strip(),
                                row["password_hash"].strip(),
                            ),
                        )
            except FileNotFoundError:
                print("⚠️ 未找到 users.csv")

            print("⏳ 正在导入用户状态表 (User_Question_State)...")
            try:
                with open(csv_path("user_question_state.csv"), "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sql = """
                            INSERT IGNORE INTO User_Question_State (user_id, question_id, is_favourite, is_completed)
                            VALUES (
                                (SELECT user_id FROM Users WHERE username = %s),
                                (SELECT question_id FROM Questions WHERE question_code = %s),
                                %s, %s
                            )
                        """
                        cursor.execute(
                            sql,
                            (
                                row["username"].strip(),
                                row["question_code"].strip(),
                                row["is_favourite"].strip(),
                                row["is_completed"].strip(),
                            ),
                        )
            except FileNotFoundError:
                print("⚠️ 未找到 user_question_state.csv")

            connection.commit()
            print("🎉 数据同步成功！")

    except Exception as e:
        print(f"❌ 出错了: {e}")
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    run_seed()
