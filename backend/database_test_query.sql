USE pga_platform;

-- =========================================================
-- DEMO STEP 1: Show the full question bank
-- This displays all questions currently stored in the database.
-- =========================================================
SELECT 
    question_code, 
    knowledge_point, 
    question_text, 
    language 
FROM Questions;

-- =========================================================
-- DEMO STEP 2: Retrieve ONLY AI-related questions
-- Filtering questions where the question_code contains 'AI'.
-- =========================================================
SELECT 
    question_code, 
    knowledge_point, 
    question_text 
FROM Questions 
WHERE question_code LIKE '%AI%';

-- =========================================================
-- DEMO STEP 3: Delete a specific question ('PGA-AI-Q10')
-- Demonstrating the DELETE operation. (Note: Any user states 
-- or materials linked to this question will be auto-deleted 
-- due to our ON DELETE CASCADE architecture).
-- =========================================================
DELETE FROM Questions 
WHERE question_code = 'PGA-AI-Q10';

-- Verify the deletion was successful
SELECT * FROM Questions 
WHERE question_code = 'PGA-AI-Q10';

-- =========================================================
-- DEMO STEP 4: Add a new AI question
-- Demonstrating the INSERT operation with a brand new question.
-- =========================================================
INSERT INTO Questions (
    question_code, 
    course_name, 
    source_type, 
    knowledge_point, 
    question_text, 
    answer_text, 
    language
) VALUES (
    'PGA-AI-Q11', 
    'Programming and Algorithms', 
    'Tutorial', 
    'AI Assisted Programming', 
    'Explain the concept of Vibe Coding and how to effectively utilize AI tools like Cursor or Claude in software development.', 
    'Vibe Coding relies on natural language prompting to guide AI models in generating, refactoring, and debugging code...', 
    'C'
);

-- =========================================================
-- DEMO STEP 5: Show the newly added question
-- Fetching the exact question we just created to prove it's there.
-- =========================================================
SELECT 
    question_code, 
    knowledge_point, 
    question_text 
FROM Questions 
WHERE question_code = 'PGA-AI-Q11';