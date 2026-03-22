import pymysql
import csv

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '041121Grp', 
    'database': 'pga_platform',
    'charset': 'utf8mb4'
}

def get_full_path(material_type, filename):
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
            print("⏳ 正在导入物料表 (Materials)...")
            with open('database_templates/materials.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    path = get_full_path(row['material_type'], row['file_path'])
                    sql = "INSERT IGNORE INTO Materials (material_code, material_type, week_number, title, file_path) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (row['material_code'].strip(), row['material_type'].strip(), row['week_number'].strip(), row['title'].strip(), path))

            print("⏳ 正在导入题库表 (Questions)...")
            with open('database_templates/questions.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    img_path = row['image_path'] if row.get('image_path', '').strip() else None
                    lang = row.get('language', 'C').strip()
                    
                    sql = """
                        INSERT IGNORE INTO Questions 
                        (question_code, source_year, source_type, knowledge_point, question_text, answer_text, image_path, language) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        row['question_code'].strip(), row['source_year'].strip(), row['source_type'].strip(),
                        row['knowledge_point'].strip(), row['question_text'].strip(), row['answer_text'].strip(),
                        img_path, lang
                    ))

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

            print("⏳ 正在导入用户表 (Users)...")
            try:
                with open('database_templates/users.csv', 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sql = "INSERT IGNORE INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (
                            row['username'].strip(), 
                            row['email'].strip(), 
                            row['password_hash'].strip()
                        ))
            except FileNotFoundError:
                print("⚠️ 未找到 users.csv")

            print("⏳ 正在导入用户状态表 (User_Question_State)...")
            try:
                with open('database_templates/user_question_state.csv', 'r', encoding='utf-8-sig') as f:
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
                        cursor.execute(sql, (
                            row['username'].strip(), 
                            row['question_code'].strip(),
                            row['is_favourite'].strip(),
                            row['is_completed'].strip()
                        ))
            except FileNotFoundError:
                print("⚠️ 未找到 user_question_state.csv")

            connection.commit()
            print("🎉 数据同步成功！")

    except Exception as e:
        print(f"❌ 出错了: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    run_seed()
