-- 清空所有业务数据，保留表结构（并重置自增）。
-- 用法：在目标库上执行，例如：
--   mysql -u YOUR_USER -p YOUR_DATABASE < backend/clear_all_data.sql

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE User_Question_State;
TRUNCATE TABLE Question_Material_Link;
TRUNCATE TABLE Questions;
TRUNCATE TABLE Materials;
TRUNCATE TABLE Users;

SET FOREIGN_KEY_CHECKS = 1;
