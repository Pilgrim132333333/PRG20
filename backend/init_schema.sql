-- 1. 创建并使用 PGA 专属数据库
CREATE DATABASE IF NOT EXISTS pga_platform;
USE pga_platform;

-- 2. 物料表 (Materials)
CREATE TABLE Materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,  
    material_code VARCHAR(50) UNIQUE NOT NULL,   
    course_name VARCHAR(100) DEFAULT 'Programming and Algorithms',
    material_type ENUM('PPT', 'Lab', 'CW', 'Tutorial') NOT NULL, 
    week_number INT,                             
    title VARCHAR(200),                          
    file_path VARCHAR(255) NOT NULL              
);

-- 3. 题库表 (Questions)
CREATE TABLE Questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,  
    question_code VARCHAR(50) UNIQUE NOT NULL,   
    course_name VARCHAR(100) DEFAULT 'Programming and Algorithms',
    source_year VARCHAR(20),                     
    source_type ENUM('Sample Paper', 'CW', 'Lab Worksheet', 'Tutorial', 'Sample Paper'), 
    knowledge_point VARCHAR(100),                
    question_text TEXT NOT NULL,                 
    answer_text TEXT,                            
    image_path VARCHAR(255) DEFAULT NULL         
);

-- 4. 多对多关联表 (Question_Material_Link)
CREATE TABLE Question_Material_Link (
    question_id INT,                             
    material_id INT,                             
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES Materials(material_id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, material_id)       
);