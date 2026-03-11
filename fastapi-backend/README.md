# FastAPI 后端 + SQL 数据库 文件结构说明

## 项目目录树

```
fastapi-backend/
├── requirements.txt          # Python 依赖
├── venv/         # 不用管
│
└── app/
    ├── __init__.py           # 应用包标识
    ├── main.py               # FastAPI 入口，注册路由、CORS、生命周期
    ├── config.py             # 配置（数据库、JWT、CORS 等）
    ├── database.py           # 数据库连接、Session、建表
    │
    ├── models/               # 定义表结构，描述数据在数据库中长什么样子
    │   ├── __init__.py
    │   ├── user.py           # 用户表
    │   ├── course.py         # 课程表
    │   ├── question.py       # 题目表
    │   └── coursework.py     # 作业表、作业提交表
    │
    ├── schemas/              # 定义前端发来的请求和接口返回的数据长什么样
    │   ├── __init__.py
    │   ├── user.py           # 用户相关 Schema
    │   ├── course.py         # 课程相关 Schema
    │   ├── question.py       # 题目相关 Schema
    │   └── coursework.py     # 作业相关 Schema
    │
    ├── api/                  # API 层
    │   ├── __init__.py
    │   └── routes/
    │       ├── __init__.py
    │       ├── users.py      # 用户：注册、登录
    │       ├── courses.py    # 课程：增删改查
    │       ├── questions.py  # 题目：列表、详情、创建、筛选
    │       └── courseworks.py# 作业：列表、详情、创建
    │
    └── utils/                # 工具函数
        ├── __init__.py
        └── security.py       # 密码哈希、JWT 等
```

---

## 各文件功能说明

### 根目录

| 文件 | 作用 |
|------|------|
| `requirements.txt` | 列出项目依赖（FastAPI、SQLAlchemy、uvicorn、pydantic 等） |
| `FILE_STRUCTURE.md` | 记录项目结构及各文件职责（本文件） |

---

### `app/` 应用主包

| 文件 | 作用 |
|------|------|
| `__init__.py` | 将 `app` 标记为 Python 包 |
| `main.py` | **应用入口**：创建 FastAPI 实例、配置 CORS、注册路由、定义启动/关闭生命周期 |
| `config.py` | **配置管理**：数据库 URL、JWT 密钥、CORS 允许来源等，支持 `.env` |
| `database.py` | **数据库层**：创建异步引擎、Session 工厂、`get_db` 依赖、`init_db` 建表逻辑 |

---

### `app/models/` 数据模型

| 文件 | 作用 |
|------|------|
| `user.py` | 用户模型：用户名、邮箱、密码哈希、角色（教师/学生） |
| `course.py` | 课程模型：课程名、代码、年份等 |
| `question.py` | 题目模型：标题、内容、语言、难度、知识点、答案等 |
| `coursework.py` | 作业模型 + 作业提交模型：作业信息与学生提交记录 |

---

### `app/schemas/` 请求/响应结构

| 文件 | 作用 |
|------|------|
| `user.py` | 用户注册、登录、响应的数据结构（Create/Login/Response） |
| `course.py` | 课程创建与响应的数据结构 |
| `question.py` | 题目创建、列表、响应的数据结构 |
| `coursework.py` | 作业创建与响应的数据结构 |

---

### `app/api/routes/` API 路由

| 文件 | 作用 |
|------|------|
| `users.py` | 用户相关 API：注册、登录 |
| `courses.py` | 课程相关 API：列表、详情、创建 |
| `questions.py` | 题目相关 API：列表（支持筛选）、详情、创建 |
| `courseworks.py` | 作业相关 API：列表、详情、创建 |

---

### `app/utils/` 工具

| 文件 | 作用 |
|------|------|
| `security.py` | 密码加密（bcrypt）、密码校验、JWT 生成/验证等安全相关函数 |
