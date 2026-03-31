# AI Programming Question Bank（Group 20 · Project 15）

面向编程与算法课程的教学辅助平台：题库浏览、材料下载、作业与课程信息、以及基于大模型的学习助手（OpenAI 兼容接口）。前端为静态 HTML（Tailwind CDN），后端为 FastAPI + MySQL。

## 小组成员

- Bingzhuo Wang  
- Ziheng Meng  
- Yunuo Shao  
- Zigeng Guo  
- Wenqi Huang  
- Junjie Chen  

## 技术栈

| 层级 | 说明 |
|------|------|
| 前端 | `vue-frontend/`：多页 HTML（登录、注册、学生端等），通过 `fetch` 调用 REST API |
| 后端 | `fastapi-backend/`：FastAPI、SQLAlchemy（同步 Session + MySQL）、bcrypt 密码 |
| 数据库 | MySQL 8（建议 `utf8mb4`），表结构见 `backend/init_schema.sql` |
| AI | 兼容 OpenAI Chat Completions（默认 DeepSeek，可在 `.env` 中改为 OpenAI 等） |

## 仓库结构

```
Workspace/
├── .env                    # 本地环境变量（勿提交密钥；见下方说明）
├── fastapi-backend/        # FastAPI 应用
│   ├── app/
│   │   ├── main.py         # 路由挂载：questions / courseworks / materials / auth / ai
│   │   ├── config.py       # DB_*、AI_* 等配置
│   │   └── ...
│   └── requirements.txt
├── backend/                # 数据库脚本与种子数据
│   ├── init_schema.sql     # 建库建表（新环境）
│   ├── clear_all_data.sql  # 仅清空数据、保留表结构
│   ├── seed_data.py        # 从 CSV 导入示例数据
│   ├── database_templates/ # materials.csv、questions.csv、links.csv 等
│   └── static/             # 材料文件目录（与库中 file_path 对应）
└── vue-frontend/           # 静态页面（需本地 HTTP 服务打开，避免 file:// 跨域问题）
```

## 环境要求

- Python 3.10+（推荐 3.12）
- MySQL 8
- 可选：`python-dotenv`（`seed_data.py` 读取项目根目录 `.env`）

## 配置说明

在**仓库根目录**创建或编辑 `.env`（`fastapi-backend/app/config.py` 会读取 `Workspace/.env` 或 `fastapi-backend/.env`）。

**数据库（二选一，优先 `DB_*`）：**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=pga_platform
```

也可使用 `DATABASE_HOST`、`DATABASE_USER` 等一组变量（与 FastAPI 配置一致）。

**AI 助手（可选）：**

```env
AI_API_KEY=你的密钥
AI_API_BASE=https://api.deepseek.com
AI_MODEL=deepseek-chat
```

不要将真实密钥提交到 Git。若密码含特殊字符，可用双引号包裹；后端会对账号密码做 URL 编码。

## 数据库初始化

1. 在 MySQL 中执行 `backend/init_schema.sql`（会创建库 `pga_platform`；若库已存在可只执行建表部分）。
2. （可选）导入示例数据：

   ```bash
   cd "/path/to/Workspace"
   pip install pymysql cryptography python-dotenv
   python backend/seed_data.py
   ```

3. 若仅需**清空数据、保留表结构**：

   ```bash
   mysql -u USER -p DATABASE_NAME < backend/clear_all_data.sql
   ```

## 启动后端

```bash
cd fastapi-backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

默认 API 根路径：`http://127.0.0.1:8000`，业务接口前缀为 `/api`（例如 `/api/auth/login`、`/api/questions`）。

## 启动前端

前端页面通过 `API_BASE = 'http://127.0.0.1:8000/api'` 访问后端；请用**本地 HTTP 服务**打开页面，不要直接用 `file://`。

```bash
cd vue-frontend
python -m http.server 5173
```