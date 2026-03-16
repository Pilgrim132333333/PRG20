import pymysql
import csv

# ==========================================
# 1. 数据库连接配置 (请确保密码正确)
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '041121Grp', 
    'database': 'pga_platform',
    'charset': 'utf8mb4'
}

def get_full_path(material_type, filename):
    """自动拼接相对路径"""
    paths = {
        'PPT': f"/static/lectures/{filename}",
        'Tutorial': f"/static/tutorials/{filename}",
        'Lab Worksheet': f"/static/labs/{filename}",
        'CW': f"/static/courseworks/{filename}"
    }
    return paths.get(material_type, f"/static/others/{filename}")

def run_seed():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # --- 导入物料 ---
            print("⏳ 正在导入物料表 (Materials)...")
            with open('database_templates/materials.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    path = get_full_path(row['material_type'], row['file_path'])
                    sql = "INSERT IGNORE INTO Materials (material_code, material_type, week_number, title, file_path) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (row['material_code'].strip(), row['material_type'].strip(), row['week_number'].strip(), row['title'].strip(), path))

            # --- 导入题库 (已更新 language 和 favourite) ---
            print("⏳ 正在导入题库表 (Questions)...")
            with open('database_templates/questions.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    img_path = row['image_path'] if row.get('image_path', '').strip() else None
                    # 获取编程语言，默认 C；获取收藏状态，默认 0
                    lang = row.get('language', 'C').strip()
                    fav = row.get('favourite', '0').strip()
                    
                    sql = """
                        INSERT IGNORE INTO Questions 
                        (question_code, source_year, source_type, knowledge_point, question_text, answer_text, image_path, language, favourite) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        row['question_code'].strip(), row['source_year'].strip(), row['source_type'].strip(),
                        row['knowledge_point'].strip(), row['question_text'].strip(), row['answer_text'].strip(),
                        img_path, lang, fav
                    ))

            # --- 建立关联 ---
            print("⏳ 正在建立关联 (Links)...")
            with open('database_templates/links.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sql = """
                        INSERT IGNORE INTO Question_Material_Link (question_id, material_id)
                        VALUES (
                            (SELECT question_id FROM Questions WHERE question_code = %s),
                            (SELECT material_id FROM Materials WHERE material_code = %s)
                        )
                    """
                    cursor.execute(sql, (row['question_code'].strip(), row['material_code'].strip()))

            connection.commit()
            print("🎉 数据同步成功！")

    except Exception as e:
        print(f"❌ 出错了: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    run_seed()