# AI Programming Question Bank (Group 20 · Project 15)

A teaching-support platform for the Programming and Algorithms course: browse questions, download materials, view coursework and course info, and interact with an AI study assistant (OpenAI-compatible API). The front end is static HTML (Tailwind CDN); the back end is FastAPI + MySQL.

## Team Members

- Bingzhuo Wang
- Ziheng Meng
- Yunuo Shao
- Zigeng Guo
- Wenqi Huang
- Junjie Chen

## Tech Stack

| Layer    | Details |
|----------|---------|
| Frontend | `vue-frontend/`: multi-page HTML (login, sign-up, student portal, etc.), calls the REST API via `fetch` |
| Backend  | `fastapi-backend/`: FastAPI, SQLAlchemy (synchronous Session + MySQL), bcrypt password hashing |
| Database | MySQL 8 (recommended: `utf8mb4`); schema defined in `backend/init_schema.sql` |
| AI       | OpenAI Chat Completions compatible (DeepSeek by default; switch to OpenAI etc. via `.env`) |

## Repository Structure

```
Workspace/
├── .env                    # Local environment variables (do NOT commit secrets; see below)
├── fastapi-backend/        # FastAPI application
│   ├── app/
│   │   ├── main.py         # Router registration: questions / courseworks / materials / auth / ai
│   │   ├── config.py       # DB_* and AI_* configuration
│   │   └── ...
│   └── requirements.txt
├── backend/                # Database scripts and seed data
│   ├── init_schema.sql     # Create database and tables (fresh environment)
│   ├── clear_all_data.sql  # Truncate all data while keeping table structure
│   ├── seed_data.py        # Import sample data from CSV files
│   ├── database_templates/ # materials.csv, questions.csv, links.csv, etc.
│   └── static/             # Material files (paths must match file_path in the DB)
└── vue-frontend/           # Static pages (serve via local HTTP server to avoid file:// CORS issues)
```

## Requirements

- Python 3.10+ (3.12 recommended)
- MySQL 8
- Optional: `python-dotenv` (`seed_data.py` reads `.env` from the project root)

## Configuration

Create or edit `.env` in the **repository root** (`fastapi-backend/app/config.py` reads `Workspace/.env` or `fastapi-backend/.env`).

**Database (choose one set; `DB_*` takes priority):**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pga_platform
```

Alternatively use `DATABASE_HOST`, `DATABASE_USER`, etc. (same semantics as FastAPI config).

**AI assistant (optional):**

```env
AI_API_KEY=your_key
AI_API_BASE=https://api.deepseek.com
AI_MODEL=deepseek-chat
```

Never commit real secrets to Git. If your password contains special characters, wrap it in double quotes; the backend URL-encodes credentials automatically.

## Database Initialisation

1. Run `backend/init_schema.sql` in MySQL (creates the `pga_platform` database; if the database already exists, run only the `CREATE TABLE` statements).
2. (Optional) Import sample data:

   ```bash
   cd "/path/to/Workspace"
   pip install pymysql cryptography python-dotenv
   python backend/seed_data.py
   ```

3. To **truncate all data while keeping table structure**:

   ```bash
   mysql -u USER -p DATABASE_NAME < backend/clear_all_data.sql
   ```

## Starting the Backend

```bash
cd fastapi-backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Default API root: `http://127.0.0.1:8000`; all business endpoints are under the `/api` prefix (e.g. `/api/auth/login`, `/api/questions`).

## Starting the Frontend

The front end uses `API_BASE = 'http://127.0.0.1:8000/api'`; open pages through a **local HTTP server** instead of `file://` to avoid CORS issues.

```bash
cd vue-frontend
python -m http.server 5173
```

Browser entry points:

- `http://127.0.0.1:5173/login.html` — Login
- `http://127.0.0.1:5173/signup.html` — Sign up
- `http://127.0.0.1:5173/student.html` — Student portal (requires login)

If the backend runs on a different host or port, update `API_BASE` in each HTML file accordingly.

## API Overview

| Prefix           | Description |
|------------------|-------------|
| `/api/auth`      | Register and login |
| `/api/questions` | Question list, favourite, complete, export PDF, etc. |
| `/api/courseworks` | Coursework entries |
| `/api/materials` | Material metadata and file download |
| `/api/ai`        | Session context and chat (requires `AI_API_KEY`) |

Interactive docs (Swagger UI): start the backend and open `http://127.0.0.1:8000/docs`.

## Troubleshooting

- **MySQL connection failure**: check `DB_*` in `.env`, ensure MySQL is running, and verify user permissions and the database name. MySQL 8 users should install `cryptography` to support `caching_sha2_password`.
- **Frontend CORS errors**: use `http.server` or serve from the same origin; avoid opening pages via `file://`.
- **Material file 404**: ensure files under `backend/static/` match the `Materials.file_path` values in the database, and set `STATIC_FILES_ROOT` in config if needed.

## Licence and Course Notice

This project is a group coursework submission (Project 15). Usage and citation requirements are governed by the course regulations.
