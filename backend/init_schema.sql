CREATE DATABASE pga_platform;
USE pga_platform;

-- 1. 物料表
CREATE TABLE Materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,  
    material_code VARCHAR(50) UNIQUE NOT NULL,   
    course_name VARCHAR(100) DEFAULT 'Programming and Algorithms',
    material_type ENUM('PPT', 'Lab', 'CW', 'Tutorial', 'Lab Worksheet') NOT NULL, 
    week_number INT,                             
    title VARCHAR(200),                          
    file_path VARCHAR(255) NOT NULL              
);

-- 2. 题库表 
CREATE TABLE Questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,  
    question_code VARCHAR(50) UNIQUE NOT NULL,   
    course_name VARCHAR(100) DEFAULT 'Programming and Algorithms',
    source_year VARCHAR(20),                     
    source_type ENUM('Sample Paper', 'CW', 'Lab Worksheet', 'Tutorial'),
    knowledge_point VARCHAR(100),                
    question_text TEXT NOT NULL,                 
    answer_text TEXT,                            
    image_path VARCHAR(255) DEFAULT NULL,
    language ENUM('C', 'Java') DEFAULT 'C'
);

-- 3. 关联表
CREATE TABLE Question_Material_Link (
    question_id INT,                             
    material_id INT,                             
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES Materials(material_id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, material_id)       
);

-- 4. 用户表 (Users) 
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,    
    email VARCHAR(100) UNIQUE NOT NULL,      
    password_hash VARCHAR(255) NOT NULL,   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 用户-题目状态表 (User_Question_State)
CREATE TABLE User_Question_State (
    user_id INT,
    question_id INT,
    is_favourite TINYINT(1) DEFAULT 0,
    is_completed TINYINT(1) DEFAULT 0,
    PRIMARY KEY (user_id, question_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
);
