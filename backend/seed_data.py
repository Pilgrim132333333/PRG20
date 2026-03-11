import pymysql
import csv
import os

# ==========================================
# 1. 数据库连接配置
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '041121Grp',  # 
    'database': 'pga_platform',
    'charset': 'utf8mb4'
}

def get_full_path(material_type, filename):
    """自动给文件名加上正确的文件夹前缀"""
    if material_type == 'PPT':
        return f"/static/lectures/{filename}"
    elif material_type == 'Tutorial':
        return f"/static/tutorials/{filename}"
    elif material_type == 'Lab':
        return f"/static/labs/{filename}"
    elif material_type == 'CW':
        return f"/static/courseworks/{filename}"
    return f"/static/others/{filename}"

def run_seed():
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # ==========================================
            # 2. 读取并导入 materials.csv
            # ==========================================
            print("⏳ 正在导入物料表 (Materials)...")
            with open('database_templates/materials.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    full_path = get_full_path(row['material_type'], row['file_path'])
                    sql = """
                        INSERT IGNORE INTO Materials 
                        (material_code, material_type, week_number, title, file_path) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        row['material_code'].strip(),  # strip() 顺便帮你去掉可能不小心多打的空格
                        row['material_type'].strip(), 
                        row['week_number'].strip(), 
                        row['title'].strip(), 
                        full_path.strip()
                    ))

            # ==========================================
            # 3. 读取并导入 questions.csv
            # ==========================================
            print("⏳ 正在导入题库表 (Questions)...")
            with open('database_templates/questions.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    img_path = row['image_path'] if row.get('image_path', '').strip() else None
                    sql = """
                        INSERT IGNORE INTO Questions 
                        (question_code, source_year, source_type, knowledge_point, question_text, answer_text, image_path) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        row['question_code'].strip(), 
                        row['source_year'].strip(), 
                        row['source_type'].strip(), 
                        row['knowledge_point'].strip(), 
                        row['question_text'].strip(), 
                        row['answer_text'].strip(), 
                        img_path
                    ))

            # ==========================================
            # 4. 读取并导入 links.csv
            # ==========================================
            print("⏳ 正在建立多对多关联 (Links)...")
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
            print("🎉 大功告成！所有数据已完美写入数据库！")

    except Exception as e:
        print(f"❌ 数据库操作出错: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    run_seed()